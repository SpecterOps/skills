param(
    [string]$DatabasePath,
    [string]$OutputRoot
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path

if ([string]::IsNullOrWhiteSpace($DatabasePath)) {
    $DatabasePath = Join-Path $scriptDirectory '..\data\com-hijack-findings.jsonl'
}
if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $scriptDirectory '..\artifacts\COM-Proxy-Database'
}

function Convert-Row {
    param([psobject]$Row)

    $dllName = [System.IO.Path]::GetFileName([string]$Row.MachineInprocServer32)
    $rootProcessName = $null
    if ($Row.PSObject.Properties['RootProcessName']) {
        $rootProcessName = [string]$Row.RootProcessName
    } elseif ($Row.PSObject.Properties['ProcessName'] -and -not [string]::IsNullOrWhiteSpace([string]$Row.ProcessName)) {
        $rootProcessName = '{0}.exe' -f [string]$Row.ProcessName
    }

    $observedProcessName = $null
    if ($Row.PSObject.Properties['ObservedProcessName']) {
        $observedProcessName = [string]$Row.ObservedProcessName
    } elseif ($Row.PSObject.Properties['ProcessName']) {
        $observedProcessName = '{0}.exe' -f [string]$Row.ProcessName
    }

    $isChildProcess = $false
    if ($Row.PSObject.Properties['IsChildProcess']) {
        $isChildProcess = [bool]$Row.IsChildProcess
    }

    return [pscustomobject]@{
        timestamp = [string]$Row.Timestamp
        app = [string]$Row.AppName
        clsid = [string]$Row.Clsid
        dllName = [string]$dllName
        dllPath = [string]$Row.MachineInprocServer32
        rootProcessName = $rootProcessName
        observedProcessName = $observedProcessName
        isChildProcess = $isChildProcess
    }
}

function Get-ProcessDisplay {
    param([psobject]$Row)

    if ($Row.isChildProcess) {
        return '{0} (child of {1})' -f $Row.observedProcessName, $Row.rootProcessName
    }

    return [string]$Row.observedProcessName
}

function Write-JsonFile {
    param(
        [string]$Path,
        [object]$Value
    )

    $json = $Value | ConvertTo-Json -Depth 8
    Set-Content -LiteralPath $Path -Value $json
}

function New-MarkdownTableLine {
    param([string[]]$Columns)

    return '| {0} |' -f ($Columns -join ' | ')
}

$resolvedDatabasePath = [System.IO.Path]::GetFullPath($DatabasePath)
$resolvedOutputRoot = [System.IO.Path]::GetFullPath($OutputRoot)

foreach ($requiredPath in @($resolvedDatabasePath, $resolvedOutputRoot)) {
    if (-not (Test-Path -LiteralPath $requiredPath)) {
        throw "Required path not found: $requiredPath"
    }
}

$dataDirectory = Join-Path $resolvedOutputRoot 'data'
$reportsDirectory = Join-Path $resolvedOutputRoot 'reports'
$appReportsDirectory = Join-Path $reportsDirectory 'apps'
$clsidReportsDirectory = Join-Path $reportsDirectory 'clsids'
$dllReportsDirectory = Join-Path $reportsDirectory 'dlls'

$rawRows = @(Get-Content -LiteralPath $resolvedDatabasePath |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
    ForEach-Object { $_ | ConvertFrom-Json })
$results = @($rawRows | ForEach-Object { Convert-Row -Row $_ })

$clsidCanonical = @{}
$dllCanonical = @{}
foreach ($row in $results) {
    $clsidKey = $row.clsid.ToUpperInvariant()
    if (-not $clsidCanonical.ContainsKey($clsidKey)) {
        $clsidCanonical[$clsidKey] = $row.clsid
    }

    $dllKey = $row.dllName.ToLowerInvariant()
    if (-not $dllCanonical.ContainsKey($dllKey)) {
        $dllCanonical[$dllKey] = $row.dllName
    }
}

$appSummaries = @(
    $results |
    Group-Object app |
    ForEach-Object {
        $childProcesses = @(
            $_.Group |
            Where-Object { $_.isChildProcess } |
            ForEach-Object { $_.observedProcessName } |
            Sort-Object -Unique
        )

        [pscustomobject]@{
            key = [string]$_.Name
            clsids = @($_.Group | ForEach-Object { $_.clsid.ToUpperInvariant() } | Sort-Object -Unique).Count
            dlls = @($_.Group | ForEach-Object { $_.dllName.ToLowerInvariant() } | Sort-Object -Unique).Count
            childProcessCount = $childProcesses.Count
            childProcesses = $childProcesses
        }
    } |
    Sort-Object @{ Expression = 'clsids'; Descending = $true }, @{ Expression = 'dlls'; Descending = $true }, @{ Expression = 'key'; Descending = $false }
)

$clsidSummaries = @(
    $results |
    Group-Object { $_.clsid.ToUpperInvariant() } |
    ForEach-Object {
        $apps = @($_.Group | ForEach-Object { $_.app } | Sort-Object -Unique)
        $canonicalKey = [string]$clsidCanonical[[string]$_.Name]
        [pscustomobject]@{
            key = $canonicalKey
            dll = [string]($_.Group | Select-Object -First 1).dllName
            apps = $apps
            appCount = $apps.Count
        }
    } |
    Sort-Object @{ Expression = 'appCount'; Descending = $true }, @{ Expression = 'key'; Descending = $false }
)

$dllSummaries = @(
    $results |
    Group-Object { $_.dllName.ToLowerInvariant() } |
    ForEach-Object {
        $apps = @($_.Group | ForEach-Object { $_.app } | Sort-Object -Unique)
        $canonicalKey = [string]$dllCanonical[[string]$_.Name]
        [pscustomobject]@{
            key = $canonicalKey
            apps = $apps
            appCount = $apps.Count
            clsidCount = @($_.Group | ForEach-Object { $_.clsid.ToUpperInvariant() } | Sort-Object -Unique).Count
        }
    } |
    Sort-Object @{ Expression = 'appCount'; Descending = $true }, @{ Expression = 'clsidCount'; Descending = $true }, @{ Expression = 'key'; Descending = $false }
)

$dashboardData = [pscustomobject]@{
    apps = $appSummaries
    clsids = $clsidSummaries
    dlls = $dllSummaries
    results = $results
}

Copy-Item -LiteralPath $resolvedDatabasePath -Destination (Join-Path $dataDirectory 'com-hijack-findings.jsonl') -Force
Write-JsonFile -Path (Join-Path $dataDirectory 'results.json') -Value $results
Write-JsonFile -Path (Join-Path $dataDirectory 'apps.json') -Value $appSummaries
Write-JsonFile -Path (Join-Path $dataDirectory 'clsids.json') -Value $clsidSummaries
Write-JsonFile -Path (Join-Path $dataDirectory 'dlls.json') -Value $dllSummaries
Set-Content -LiteralPath (Join-Path $dataDirectory 'dashboard-data.js') -Value ('window.COM_PROXY_DATA = {0};' -f ($dashboardData | ConvertTo-Json -Depth 8))

foreach ($directory in @($appReportsDirectory, $clsidReportsDirectory, $dllReportsDirectory)) {
    Get-ChildItem -LiteralPath $directory -File -Filter *.md -ErrorAction SilentlyContinue | Remove-Item -Force
}

$applicationsLines = @(
    '# Applications',
    '',
    '| Application | CLSIDs | DLLs | Child Processes |',
    '| --- | --- | --- | --- |'
)
foreach ($appSummary in $appSummaries) {
    $applicationsLines += New-MarkdownTableLine -Columns @(
        ('[{0}](./apps/{0}.md)' -f $appSummary.key),
        [string]$appSummary.clsids,
        [string]$appSummary.dlls,
        ($appSummary.childProcesses -join ', ')
    )

    $appRows = @($results | Where-Object { $_.app -eq $appSummary.key } | Sort-Object clsid, observedProcessName, dllPath)
    $appLines = @(
        ('# {0}' -f $appSummary.key),
        '',
        ('- CLSIDs: {0}' -f $appSummary.clsids),
        ('- DLLs: {0}' -f $appSummary.dlls),
        '',
        '| CLSID | Process | DLL Path |',
        '| --- | --- | --- |'
    )
    foreach ($row in $appRows) {
        $appLines += New-MarkdownTableLine -Columns @(
            [string]$row.clsid,
            (Get-ProcessDisplay -Row $row),
            [string]$row.dllPath
        )
    }

    Set-Content -LiteralPath (Join-Path $appReportsDirectory ('{0}.md' -f $appSummary.key)) -Value $appLines
}
Set-Content -LiteralPath (Join-Path $reportsDirectory 'applications.md') -Value $applicationsLines

$clsidLines = @(
    '# CLSIDs',
    '',
    '| CLSID | DLL | Apps |',
    '| --- | --- | --- |'
)
foreach ($clsidSummary in $clsidSummaries) {
    $clsidLines += New-MarkdownTableLine -Columns @(
        ('[{0}](./clsids/{0}.md)' -f $clsidSummary.key),
        [string]$clsidSummary.dll,
        ($clsidSummary.apps -join ', ')
    )

    $clsidRows = @(
        $results |
        Where-Object { $_.clsid.ToUpperInvariant() -eq $clsidSummary.key.ToUpperInvariant() } |
        Sort-Object app, observedProcessName, dllPath
    )
    $clsidDetailLines = @(
        ('# {0}' -f $clsidSummary.key),
        '',
        ('- DLL: {0}' -f $clsidSummary.dll),
        ('- Apps: {0}' -f $clsidSummary.appCount),
        '',
        '| Application | Process | DLL Path |',
        '| --- | --- | --- |'
    )
    foreach ($row in $clsidRows) {
        $clsidDetailLines += New-MarkdownTableLine -Columns @(
            [string]$row.app,
            (Get-ProcessDisplay -Row $row),
            [string]$row.dllPath
        )
    }

    Set-Content -LiteralPath (Join-Path $clsidReportsDirectory ('{0}.md' -f $clsidSummary.key)) -Value $clsidDetailLines
}
Set-Content -LiteralPath (Join-Path $reportsDirectory 'clsids.md') -Value $clsidLines

$dllLines = @(
    '# DLLs',
    '',
    '| DLL | Apps | CLSIDs |',
    '| --- | --- | --- |'
)
foreach ($dllSummary in $dllSummaries) {
    $dllLines += New-MarkdownTableLine -Columns @(
        ('[{0}](./dlls/{0}.md)' -f $dllSummary.key),
        ($dllSummary.apps -join ', '),
        [string]$dllSummary.clsidCount
    )

    $dllRows = @(
        $results |
        Where-Object { $_.dllName.ToLowerInvariant() -eq $dllSummary.key.ToLowerInvariant() } |
        Sort-Object app, clsid, observedProcessName
    )
    $dllDetailLines = @(
        ('# {0}' -f $dllSummary.key),
        '',
        ('- Apps: {0}' -f $dllSummary.appCount),
        ('- CLSIDs: {0}' -f $dllSummary.clsidCount),
        '',
        '| Application | CLSID | Process | DLL Path |',
        '| --- | --- | --- | --- |'
    )
    foreach ($row in $dllRows) {
        $dllDetailLines += New-MarkdownTableLine -Columns @(
            [string]$row.app,
            [string]$row.clsid,
            (Get-ProcessDisplay -Row $row),
            [string]$row.dllPath
        )
    }

    Set-Content -LiteralPath (Join-Path $dllReportsDirectory ('{0}.md' -f $dllSummary.key)) -Value $dllDetailLines
}
Set-Content -LiteralPath (Join-Path $reportsDirectory 'dlls.md') -Value $dllLines

$sharedDlls = @($dllSummaries | Where-Object { $_.appCount -gt 1 }).Count
$sharedClsids = @($clsidSummaries | Where-Object { $_.appCount -gt 1 }).Count

$readmeLines = @(
    '# COM Proxy Database',
    '',
    'This repository contains generated COM proxy findings data.',
    '',
    '- Open index.html for the interactive dashboard.',
    '- Browse reports/ for GitHub-friendly summaries.',
    '- Inspect data/ for raw and derived files.',
    '',
    '## Current Snapshot',
    '',
    ('- Active Apps: {0}' -f $appSummaries.Count),
    ('- Unique CLSIDs: {0}' -f $clsidSummaries.Count),
    ('- Unique DLLs: {0}' -f $dllSummaries.Count),
    ('- Shared DLLs: {0}' -f $sharedDlls),
    ('- Shared CLSIDs: {0}' -f $sharedClsids)
)
Set-Content -LiteralPath (Join-Path $resolvedOutputRoot 'README.md') -Value $readmeLines
