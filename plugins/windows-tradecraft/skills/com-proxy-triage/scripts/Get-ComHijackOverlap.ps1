param(
    [string]$DatabasePath,
    [switch]$OnlySuccessful
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path

if ([string]::IsNullOrWhiteSpace($DatabasePath)) {
    $DatabasePath = Join-Path $scriptDirectory "..\data\com-hijack-findings.jsonl"
}

if (-not (Test-Path -LiteralPath $DatabasePath)) {
    throw "Database not found: $DatabasePath"
}

$rows = @(Get-Content -LiteralPath $DatabasePath | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | ForEach-Object {
    $_ | ConvertFrom-Json
})

if ($OnlySuccessful) {
    $rows = @($rows | Where-Object { $_.CalcLaunched })
}

$summary = $rows |
    Group-Object Clsid |
    ForEach-Object {
        $group = $_.Group
        [pscustomobject]@{
            Clsid = $_.Name
            AppCount = @($group | Group-Object AppName).Count
            Apps = @($group | Group-Object AppName | ForEach-Object { $_.Name })
            SuccessfulApps = @($group | Where-Object { $_.CalcLaunched } | Group-Object AppName | ForEach-Object { $_.Name })
            MachineInprocServer32 = ($group | Select-Object -First 1).MachineInprocServer32
        }
    } |
    Sort-Object -Property AppCount, Clsid -Descending

$summary
