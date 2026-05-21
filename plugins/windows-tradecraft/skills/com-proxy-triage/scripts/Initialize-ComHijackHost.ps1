param(
    [switch]$InstallBuildTools,
    [switch]$InitSubmodules,
    [switch]$ValidateOnly,
    [string]$MsBuildPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDirectory 'ComHijackHost.Common.ps1')
$repoRoot = Get-ComHijackRepoRoot -ScriptDirectory $scriptDirectory
$repoKoppelingRoot = Join-Path $repoRoot 'Koppeling'

if ($ValidateOnly -and ($InstallBuildTools -or $InitSubmodules)) {
    throw 'ValidateOnly cannot be combined with InstallBuildTools or InitSubmodules.'
}

function New-ValidationRow {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Check,
        [Parameter(Mandatory = $true)]
        [bool]$Passed,
        [Parameter(Mandatory = $true)]
        [string]$Details
    )

    [pscustomobject]@{
        Check   = $Check
        Status  = if ($Passed) { 'PASS' } else { 'FAIL' }
        Details = $Details
    }
}

function Invoke-SubmoduleInitialization {
    if (-not (Test-Path -LiteralPath (Join-Path $repoRoot '.gitmodules')) -or -not (Test-Path -LiteralPath (Join-Path $repoRoot '.git'))) {
        Initialize-ComHijackKoppelingCache -ScriptDirectory $scriptDirectory | Out-Null
        return
    }

    & git -C $repoRoot submodule update --init --recursive Koppeling
    if ($LASTEXITCODE -ne 0) {
        throw 'git submodule update failed while initializing Koppeling.'
    }
}

function Install-VisualStudioBuildTools {
    if (-not (Test-ComHijackAdministrator)) {
        throw 'InstallBuildTools must run from an elevated PowerShell session.'
    }

    $override = '--wait --norestart --passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended'
    $wingetPath = Get-Command winget.exe -ErrorAction SilentlyContinue
    if ($wingetPath) {
        & $wingetPath.Source install --id Microsoft.VisualStudio.2022.BuildTools --exact --accept-package-agreements --accept-source-agreements --override $override
        if ($LASTEXITCODE -eq 0) {
            return
        }
    }

    $bootstrapperPath = Join-Path $env:TEMP 'vs_BuildTools.exe'
    try {
        Invoke-WebRequest -UseBasicParsing -Uri 'https://aka.ms/vs/17/release/vs_BuildTools.exe' -OutFile $bootstrapperPath
    } catch {
        throw "Unable to download vs_BuildTools.exe after winget failed. $($_.Exception.Message)"
    }

    $bootstrapperArguments = @(
        '--wait',
        '--norestart',
        '--passive',
        '--add', 'Microsoft.VisualStudio.Workload.VCTools',
        '--includeRecommended'
    )
    $bootstrapperProcess = Start-Process -FilePath $bootstrapperPath -ArgumentList $bootstrapperArguments -Wait -PassThru
    if ($bootstrapperProcess.ExitCode -ne 0) {
        throw "Visual Studio 2022 Build Tools installer failed with exit code $($bootstrapperProcess.ExitCode). Check the newest dd_bootstrapper*, dd_setup*, and dd_client* logs under $env:TEMP."
    }
}

function Build-KoppelingNetClone {
    param(
        [Parameter(Mandatory = $true)]
        [string]$KoppelingRoot,
        [AllowNull()][string]$PreferredMsBuildPath
    )

    $msbuildPath = Resolve-ComHijackMsBuildPath -PreferredMsBuildPath $PreferredMsBuildPath
    $netCloneProjectPath = Join-Path $KoppelingRoot 'NetClone\NetClone.csproj'
    $netCloneOutputPath = Join-Path $KoppelingRoot 'Bin\NetClone.exe'
    $solutionDir = [System.IO.Path]::GetFullPath((Join-Path $KoppelingRoot '.'))
    if (-not $solutionDir.EndsWith('\')) {
        $solutionDir = '{0}\' -f $solutionDir
    }

    & $msbuildPath $netCloneProjectPath /restore /t:Build /p:RestorePackagesConfig=true /p:SolutionDir=$solutionDir /p:Configuration=Debug /p:Platform=AnyCPU | Out-Host
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $netCloneOutputPath)) {
        throw 'MSBuild failed while building NetClone.exe.'
    }
}

function Get-ValidationSummary {
    param([AllowNull()][string]$PreferredMsBuildPath)

    $rows = [System.Collections.Generic.List[object]]::new()

    try {
        $visualStudio = Get-ComHijackVisualStudioInstall -PreferredMsBuildPath $PreferredMsBuildPath
        $rows.Add((New-ValidationRow -Check 'MSBuild' -Passed $true -Details $visualStudio.MSBuildPath))
    } catch {
        $visualStudio = $null
        $rows.Add((New-ValidationRow -Check 'MSBuild' -Passed $false -Details $_.Exception.Message))
    }

    if ($null -ne $visualStudio -and -not [string]::IsNullOrWhiteSpace($visualStudio.CompilerPath)) {
        $rows.Add((New-ValidationRow -Check 'VC x64 toolchain' -Passed $true -Details $visualStudio.CompilerPath))
    } else {
        $rows.Add((New-ValidationRow -Check 'VC x64 toolchain' -Passed $false -Details 'Missing x64 C++ compiler. Install Visual Studio 2022 Build Tools with the Desktop development with C++ workload.'))
    }

    $windowsSdkLibraryPath = Get-ComHijackWindowsSdkLibraryPath
    if ([string]::IsNullOrWhiteSpace($windowsSdkLibraryPath)) {
        $rows.Add((New-ValidationRow -Check 'Windows SDK' -Passed $false -Details 'Missing Windows SDK x64 libraries. Re-run the Build Tools install with the Desktop development with C++ workload.'))
    } else {
        $rows.Add((New-ValidationRow -Check 'Windows SDK' -Passed $true -Details $windowsSdkLibraryPath))
    }

    try {
        $resolvedKoppelingRoot = Resolve-ComHijackKoppelingRoot -ScriptDirectory $scriptDirectory -RequiredRelativePath 'Theif\Theif.vcxproj' -HydrateIfMissing
        $rows.Add((New-ValidationRow -Check 'Koppeling root' -Passed $true -Details $resolvedKoppelingRoot))
    } catch {
        $resolvedKoppelingRoot = $null
        $rows.Add((New-ValidationRow -Check 'Koppeling root' -Passed $false -Details $_.Exception.Message))
    }

    if ($null -ne $resolvedKoppelingRoot) {
        $netClonePath = Join-Path $resolvedKoppelingRoot 'Bin\NetClone.exe'
        $projectPath = Join-Path $resolvedKoppelingRoot 'Theif\Theif.vcxproj'
        $rows.Add((New-ValidationRow -Check 'NetClone.exe' -Passed (Test-Path -LiteralPath $netClonePath) -Details $netClonePath))
        $rows.Add((New-ValidationRow -Check 'Theif.vcxproj' -Passed (Test-Path -LiteralPath $projectPath) -Details $projectPath))
    } else {
        $rows.Add((New-ValidationRow -Check 'NetClone.exe' -Passed $false -Details 'Koppeling is not available yet. Run .\scripts\Initialize-ComHijackHost.ps1 -InitSubmodules.'))
        $rows.Add((New-ValidationRow -Check 'Theif.vcxproj' -Passed $false -Details 'Koppeling is not available yet. Run .\scripts\Initialize-ComHijackHost.ps1 -InitSubmodules.'))
    }

    $watcherPath = Join-Path $scriptDirectory 'Watch-InProcServer32Misses.ps1'
    $rows.Add((New-ValidationRow -Check 'Watcher script' -Passed (Test-Path -LiteralPath $watcherPath) -Details $watcherPath))

    return @($rows)
}

if (-not $PSBoundParameters.ContainsKey('InitSubmodules') -and -not (Test-Path -LiteralPath $repoKoppelingRoot)) {
    $InitSubmodules = $true
}

if ($InitSubmodules) {
    Invoke-SubmoduleInitialization
}

if ($InstallBuildTools) {
    Install-VisualStudioBuildTools
}

if (-not $ValidateOnly) {
    try {
        $resolvedKoppelingRoot = Resolve-ComHijackKoppelingRoot -ScriptDirectory $scriptDirectory -RequiredRelativePath 'Theif\Theif.vcxproj' -HydrateIfMissing
        $netClonePath = Join-Path $resolvedKoppelingRoot 'Bin\NetClone.exe'
        if (-not (Test-Path -LiteralPath $netClonePath)) {
            $seededFromAssets = Install-ComHijackPackagedNetCloneRuntime -KoppelingRoot $resolvedKoppelingRoot -ScriptDirectory $scriptDirectory
            if (-not $seededFromAssets) {
                Build-KoppelingNetClone -KoppelingRoot $resolvedKoppelingRoot -PreferredMsBuildPath $MsBuildPath
            }
        }
    } catch {
    }
}

$summary = @(Get-ValidationSummary -PreferredMsBuildPath $MsBuildPath)
$summary

 $failedRows = @($summary | Where-Object { $_.Status -eq 'FAIL' })
if ($failedRows.Count -gt 0) {
    $failedText = @($failedRows | ForEach-Object {
        '{0}: {1}' -f $_.Check, $_.Details
    }) -join [Environment]::NewLine

    throw ("Host validation failed.{0}{1}{0}Rerun .\scripts\Initialize-ComHijackHost.ps1 -ValidateOnly after fixing the failed checks." -f [Environment]::NewLine, $failedText)
}
