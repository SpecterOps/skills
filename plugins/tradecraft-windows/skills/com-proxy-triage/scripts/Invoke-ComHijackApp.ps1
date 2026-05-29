param(
    [Parameter(Mandatory = $true)]
    [string]$AppName,

    [string]$ConfigPath,
    [string]$LaunchExecutable,
    [string[]]$LaunchArgumentList,
    [string[]]$TargetProcesses,
    [string]$ProcessName,
    [string]$PackageId,
    [string]$PayloadCommand = 'C:\Windows\System32\calc.exe',
    [int]$CaptureSeconds = 20,
    [int]$TestWaitSeconds = 0,
    [int]$MaxCandidates = 0,
    [switch]$KillExisting
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDirectory 'ComHijackApp.Common.ps1')

$app = Resolve-ComHijackAppTarget `
    -AppName $AppName `
    -ConfigPath $ConfigPath `
    -LaunchExecutable $LaunchExecutable `
    -LaunchArgumentList $LaunchArgumentList `
    -TargetProcesses $TargetProcesses `
    -ProcessName $ProcessName `
    -PackageId $PackageId `
    -ScriptDirectory $scriptDirectory

& (Join-Path $scriptDirectory 'Invoke-ComHijackProbe.ps1') `
    -AppName $app.AppName `
    -PackageId $app.PackageId `
    -ProcessName $app.ProcessName `
    -LaunchExecutable $app.LaunchExecutable `
    -LaunchArgumentList $app.LaunchArgumentList `
    -TargetProcesses $app.TargetProcesses `
    -PayloadCommand $PayloadCommand `
    -CaptureSeconds $CaptureSeconds `
    -TestWaitSeconds $TestWaitSeconds `
    -MaxCandidates $MaxCandidates `
    -KillExisting:$KillExisting
