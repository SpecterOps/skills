function Get-ComHijackRepoRoot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ScriptDirectory
    )

    return [System.IO.Path]::GetFullPath((Join-Path $ScriptDirectory '..'))
}

function Get-ComHijackCacheRoot {
    if ([string]::IsNullOrWhiteSpace($env:USERPROFILE)) {
        return $null
    }

    return Join-Path $env:USERPROFILE '.codex\cache\com-proxy-triage'
}

function Get-ComHijackKoppelingCacheRoot {
    $cacheRoot = Get-ComHijackCacheRoot
    if ([string]::IsNullOrWhiteSpace($cacheRoot)) {
        return $null
    }

    return Join-Path $cacheRoot 'Koppeling'
}

function Get-ComHijackKoppelingCloneUrl {
    return 'https://github.com/monoxgas/Koppeling.git'
}

function Test-ComHijackAdministrator {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Get-ComHijackVsWherePath {
    $candidates = @()
    if ($env:ProgramFiles -and ${env:ProgramFiles(x86)}) {
        $candidates += (Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe')
    }
    if ($env:ProgramFiles) {
        $candidates += (Join-Path $env:ProgramFiles 'Microsoft Visual Studio\Installer\vswhere.exe')
    }

    foreach ($candidate in $candidates | Select-Object -Unique) {
        if (-not [string]::IsNullOrWhiteSpace($candidate) -and (Test-Path -LiteralPath $candidate)) {
            return $candidate
        }
    }

    return $null
}

function Get-ComHijackVisualStudioInstall {
    param([AllowNull()][string]$PreferredMsBuildPath)

    if (-not [string]::IsNullOrWhiteSpace($PreferredMsBuildPath)) {
        $resolvedMsBuildPath = [System.IO.Path]::GetFullPath($PreferredMsBuildPath)
        if (-not (Test-Path -LiteralPath $resolvedMsBuildPath)) {
            throw "Requested MSBuild path not found: $PreferredMsBuildPath"
        }

        return [pscustomobject]@{
            Source              = 'Explicit'
            InstallationName    = 'Explicit MSBuild path'
            InstallationPath    = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $resolvedMsBuildPath))
            InstallationVersion = $null
            ProductId           = $null
            ChannelId           = $null
            MSBuildPath         = $resolvedMsBuildPath
            CompilerPath        = $null
        }
    }

    $vswherePath = Get-ComHijackVsWherePath
    if (-not $vswherePath) {
        throw 'Unable to locate vswhere.exe. Install Visual Studio 2022 Build Tools with the Desktop development with C++ workload, or pass -MsBuildPath.'
    }

    $msbuildMatches = @(& $vswherePath -latest -products * -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe')
    if ($LASTEXITCODE -ne 0 -or $msbuildMatches.Count -eq 0 -or [string]::IsNullOrWhiteSpace($msbuildMatches[0])) {
        throw 'Unable to locate an MSBuild-capable Visual Studio installation. Install Visual Studio 2022 Build Tools with the Desktop development with C++ workload, or pass -MsBuildPath.'
    }

    $installJson = @(& $vswherePath -latest -products * -requires Microsoft.Component.MSBuild -format json)
    if ($LASTEXITCODE -ne 0 -or $installJson.Count -eq 0) {
        throw 'vswhere located MSBuild, but could not describe the owning Visual Studio installation.'
    }

    $installation = @($installJson -join [Environment]::NewLine | ConvertFrom-Json) | Select-Object -First 1
    if ($null -eq $installation) {
        throw 'vswhere located MSBuild, but returned an empty Visual Studio installation set.'
    }

    $compilerPath = $null
    $msvcRoot = Join-Path $installation.installationPath 'VC\Tools\MSVC'
    if (Test-Path -LiteralPath $msvcRoot) {
        $compilerPath = Get-ChildItem -Path $msvcRoot -Recurse -Filter cl.exe -ErrorAction SilentlyContinue |
            Where-Object { $_.FullName -like '*\bin\Hostx64\x64\cl.exe' } |
            Select-Object -ExpandProperty FullName -First 1
    }

    return [pscustomobject]@{
        Source              = 'vswhere'
        InstallationName    = $installation.displayName
        InstallationPath    = $installation.installationPath
        InstallationVersion = $installation.installationVersion
        ProductId           = $installation.productId
        ChannelId           = $installation.channelId
        MSBuildPath         = [System.IO.Path]::GetFullPath($msbuildMatches[0])
        CompilerPath        = $compilerPath
    }
}

function Resolve-ComHijackMsBuildPath {
    param([AllowNull()][string]$PreferredMsBuildPath)

    return (Get-ComHijackVisualStudioInstall -PreferredMsBuildPath $PreferredMsBuildPath).MSBuildPath
}

function Get-ComHijackWindowsSdkLibraryPath {
    $roots = @()
    if (${env:ProgramFiles(x86)}) {
        $roots += (Join-Path ${env:ProgramFiles(x86)} 'Windows Kits\10\Lib')
    }
    if ($env:ProgramFiles) {
        $roots += (Join-Path $env:ProgramFiles 'Windows Kits\10\Lib')
    }

    foreach ($root in $roots | Select-Object -Unique) {
        if (-not (Test-Path -LiteralPath $root)) {
            continue
        }

        $versions = @(Get-ChildItem -Path $root -Directory -ErrorAction SilentlyContinue | Sort-Object Name -Descending)
        foreach ($version in $versions) {
            $candidate = Join-Path $version.FullName 'um\x64\kernel32.lib'
            if (Test-Path -LiteralPath $candidate) {
                return $candidate
            }
        }
    }

    return $null
}

function Install-ComHijackPackagedNetCloneRuntime {
    param(
        [Parameter(Mandatory = $true)]
        [string]$KoppelingRoot,
        [Parameter(Mandatory = $true)]
        [string]$ScriptDirectory
    )

    $repoRoot = Get-ComHijackRepoRoot -ScriptDirectory $ScriptDirectory
    $packagedRuntimeRoot = Join-Path $repoRoot 'assets\koppeling-netclone'
    if (-not (Test-Path -LiteralPath $packagedRuntimeRoot)) {
        return $false
    }

    $destinationRoot = Join-Path $KoppelingRoot 'Bin'
    New-Item -ItemType Directory -Force -Path $destinationRoot | Out-Null

    Get-ChildItem -Path $packagedRuntimeRoot -File | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $destinationRoot $_.Name) -Force
    }

    return (Test-Path -LiteralPath (Join-Path $destinationRoot 'NetClone.exe'))
}

function Initialize-ComHijackKoppelingCache {
    param([Parameter(Mandatory = $true)][string]$ScriptDirectory)

    $cacheRoot = Get-ComHijackKoppelingCacheRoot
    if ([string]::IsNullOrWhiteSpace($cacheRoot)) {
        throw 'Unable to determine the Codex cache directory for Koppeling.'
    }

    if (Test-Path -LiteralPath (Join-Path $cacheRoot 'Theif\Theif.vcxproj')) {
        return $cacheRoot
    }

    $cacheParent = Split-Path -Parent $cacheRoot
    if (-not (Test-Path -LiteralPath $cacheParent)) {
        New-Item -ItemType Directory -Force -Path $cacheParent | Out-Null
    }

    $repoRoot = Get-ComHijackRepoRoot -ScriptDirectory $ScriptDirectory
    $repoLocalKoppeling = Join-Path $repoRoot 'Koppeling'
    if (Test-Path -LiteralPath (Join-Path $repoLocalKoppeling 'Theif\Theif.vcxproj')) {
        if (Test-Path -LiteralPath $cacheRoot) {
            Remove-Item -LiteralPath $cacheRoot -Recurse -Force
        }
        Copy-Item -LiteralPath $repoLocalKoppeling -Destination $cacheRoot -Recurse -Force
        return $cacheRoot
    }

    if (-not (Get-Command git.exe -ErrorAction SilentlyContinue) -and -not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw 'git is unavailable, so Koppeling cannot be hydrated automatically. Install git or provide -KoppelingRoot.'
    }

    if (Test-Path -LiteralPath $cacheRoot) {
        Remove-Item -LiteralPath $cacheRoot -Recurse -Force
    }

    & git clone --depth 1 (Get-ComHijackKoppelingCloneUrl) $cacheRoot
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath (Join-Path $cacheRoot 'Theif\Theif.vcxproj'))) {
        throw 'Failed to hydrate the Koppeling cache checkout.'
    }

    return $cacheRoot
}

function Resolve-ComHijackKoppelingRoot {
    param(
        [AllowNull()][string]$PreferredRoot,
        [Parameter(Mandatory = $true)]
        [string]$ScriptDirectory,
        [Parameter(Mandatory = $true)]
        [string]$RequiredRelativePath,
        [switch]$HydrateIfMissing
    )

    $repoRoot = Get-ComHijackRepoRoot -ScriptDirectory $ScriptDirectory
    $cacheRoot = Get-ComHijackKoppelingCacheRoot
    $candidates = @()
    if (-not [string]::IsNullOrWhiteSpace($PreferredRoot)) {
        $candidates += $PreferredRoot
    }

    $candidates += @(
        (Join-Path $repoRoot 'Koppeling'),
        $cacheRoot,
        (Join-Path $repoRoot '..\Koppeling')
    )

    foreach ($candidate in $candidates) {
        $resolvedCandidate = [System.IO.Path]::GetFullPath($candidate)
        if (Test-Path -LiteralPath (Join-Path $resolvedCandidate $RequiredRelativePath)) {
            return $resolvedCandidate
        }
    }

    if ($HydrateIfMissing) {
        $hydratedRoot = Initialize-ComHijackKoppelingCache -ScriptDirectory $ScriptDirectory
        if (-not [string]::IsNullOrWhiteSpace($hydratedRoot) -and (Test-Path -LiteralPath (Join-Path $hydratedRoot $RequiredRelativePath))) {
            return $hydratedRoot
        }
    }

    $documentsRoot = Split-Path -Parent $repoRoot
    $codexRoot = Join-Path $documentsRoot 'Codex'
    if (Test-Path -LiteralPath $codexRoot) {
        $match = Get-ChildItem -Path $codexRoot -Directory -Recurse -Filter Koppeling -ErrorAction SilentlyContinue |
            Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName $RequiredRelativePath) } |
            Select-Object -First 1
        if ($match) {
            return $match.FullName
        }
    }

    throw "Unable to locate a Koppeling checkout with $RequiredRelativePath. Run .\scripts\Initialize-ComHijackHost.ps1 from the skill directory, or pass -KoppelingRoot."
}
