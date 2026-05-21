param(
    [int]$DurationSeconds = 0,
    [string]$Suffix = "InProcServer32",
    [uint32]$Status = 3221225524,
    [string]$TracePath = "C:\Users\zach\Documents\Codex\2026-05-13\how-to-i-use-the-windbg\inprocserver32-regtrace.etl",
    [int]$PollMilliseconds = 1000,
    [int]$RootProcessId = 0,
    [switch]$IncludeDescendants,
    [string]$ProcessName,
    [switch]$ResolveProcessName,
    [switch]$KeepTrace
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$script:MachineInprocCache = @{}

function Test-IsAdministrator {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Join-RegistryPath {
    param(
        [AllowNull()][string]$BaseName,
        [AllowNull()][string]$RelativeName
    )

    $base = if ($null -eq $BaseName) { "" } else { $BaseName.Trim() }
    $relative = if ($null -eq $RelativeName) { "" } else { $RelativeName.Trim() }

    if ([string]::IsNullOrWhiteSpace($base)) {
        return $relative
    }

    if ([string]::IsNullOrWhiteSpace($relative)) {
        return $base
    }

    if ($base.EndsWith("\")) {
        return $base + $relative
    }

    return "$base\$relative"
}

function Convert-StatusValue {
    param([AllowNull()][string]$Value)

    if ([string]::IsNullOrWhiteSpace($Value)) {
        throw "Missing Status value."
    }

    $trimmed = $Value.Trim()
    if ($trimmed.StartsWith("0x", [System.StringComparison]::OrdinalIgnoreCase)) {
        return [uint32]::Parse($trimmed.Substring(2), [System.Globalization.NumberStyles]::AllowHexSpecifier)
    }

    return [uint32]$trimmed
}

function Get-ProcessNameSafe {
    param([int]$ProcessId)

    try {
        return (Get-Process -Id $ProcessId -ErrorAction Stop).ProcessName
    } catch {
        return $null
    }
}

function Get-TrackedProcessMap {
    param(
        [int]$RootPid,
        [switch]$IncludeDescendants
    )

    if ($RootPid -le 0) {
        return @{}
    }

    $processes = @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Select-Object ProcessId, ParentProcessId, Name)
    $tracked = @{}
    $queue = [System.Collections.Generic.Queue[int]]::new()
    $queue.Enqueue($RootPid)

    while ($queue.Count -gt 0) {
        $currentPid = $queue.Dequeue()
        if ($tracked.ContainsKey($currentPid)) {
            continue
        }

        $current = @($processes | Where-Object { $_.ProcessId -eq $currentPid } | Select-Object -First 1)
        if ($current.Count -gt 0) {
            $tracked[$currentPid] = [string]$current[0].Name
        } else {
            $tracked[$currentPid] = $null
        }

        if (-not $IncludeDescendants) {
            continue
        }

        foreach ($child in @($processes | Where-Object { $_.ParentProcessId -eq $currentPid })) {
            if (-not $tracked.ContainsKey([int]$child.ProcessId)) {
                $queue.Enqueue([int]$child.ProcessId)
            }
        }
    }

    return $tracked
}

function Get-ClsidFromPath {
    param([AllowNull()][string]$Path)

    if ([string]::IsNullOrWhiteSpace($Path)) {
        return $null
    }

    $match = [regex]::Match($Path, '\{[0-9A-Fa-f-]+\}')
    if ($match.Success) {
        return $match.Value
    }

    return $null
}

function Get-MachineInprocServer32 {
    param([AllowNull()][string]$Clsid)

    if ([string]::IsNullOrWhiteSpace($Clsid)) {
        return $null
    }

    if ($script:MachineInprocCache.ContainsKey($Clsid)) {
        return $script:MachineInprocCache[$Clsid]
    }

    $registryPath = "Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\$Clsid\InprocServer32"

    try {
        $value = (Get-ItemProperty -LiteralPath $registryPath -ErrorAction Stop).'(default)'
    } catch {
        $value = $null
    }

    $script:MachineInprocCache[$Clsid] = $value
    return $value
}

if (-not (Test-IsAdministrator)) {
    throw "This script must run from an elevated PowerShell session because ETW trace sessions for Microsoft-Windows-Kernel-Registry require administrator rights."
}

$resolvedTracePath = [System.IO.Path]::GetFullPath($TracePath)
$traceDirectory = [System.IO.Path]::GetDirectoryName($resolvedTracePath)
if ([string]::IsNullOrWhiteSpace($traceDirectory)) {
    throw "Unable to determine the trace output directory for '$TracePath'."
}

if (-not (Test-Path -LiteralPath $traceDirectory)) {
    New-Item -ItemType Directory -Path $traceDirectory | Out-Null
}

if (Test-Path -LiteralPath $resolvedTracePath) {
    Remove-Item -LiteralPath $resolvedTracePath -Force
}

$sessionName = "CodexRegTrace_{0}" -f ([Guid]::NewGuid().ToString("N"))
$providerName = "Microsoft-Windows-Kernel-Registry"
$keywordMask = "0x2000"
$level = "0x4"

try {
    & logman start $sessionName -p $providerName $keywordMask $level -o $resolvedTracePath -ets | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to start the ETW trace session '$sessionName'."
    }

    $startedAt = [DateTimeOffset]::UtcNow
    $lastRecordId = 0L

    while ($true) {
        $trackedProcessMap = Get-TrackedProcessMap -RootPid $RootProcessId -IncludeDescendants:$IncludeDescendants
        $xPath = "*[System[(EventID=2 and EventRecordID > $lastRecordId)]]"
        $events = @(Get-WinEvent -Path $resolvedTracePath -Oldest -FilterXPath $xPath -ErrorAction SilentlyContinue)

        foreach ($event in $events) {
            if ($event.RecordId -gt $lastRecordId) {
                $lastRecordId = $event.RecordId
            }

            $xml = [xml]$event.ToXml()
            $data = @{}

            foreach ($node in $xml.Event.EventData.Data) {
                $data[$node.Name] = [string]$node.InnerText
            }

            $statusValue = $data["Status"]
            if ([string]::IsNullOrWhiteSpace($statusValue)) {
                continue
            }

            $eventStatus = Convert-StatusValue -Value $statusValue
            if ($eventStatus -ne $Status) {
                continue
            }

            $path = Join-RegistryPath -BaseName $data["BaseName"] -RelativeName $data["RelativeName"]
            if (-not $path.EndsWith($Suffix, [System.StringComparison]::OrdinalIgnoreCase)) {
                continue
            }

            $clsid = Get-ClsidFromPath -Path $path
            $machineInprocServer32 = Get-MachineInprocServer32 -Clsid $clsid

            if ($RootProcessId -gt 0 -and -not $trackedProcessMap.ContainsKey([int]$event.ProcessId)) {
                continue
            }

            $resolvedProcessName = $null
            $needProcessName = $ResolveProcessName -or -not [string]::IsNullOrWhiteSpace($ProcessName)
            if ($needProcessName) {
                if ($trackedProcessMap.ContainsKey([int]$event.ProcessId) -and -not [string]::IsNullOrWhiteSpace($trackedProcessMap[[int]$event.ProcessId])) {
                    $resolvedProcessName = $trackedProcessMap[[int]$event.ProcessId]
                } else {
                    $resolvedProcessName = Get-ProcessNameSafe -ProcessId $event.ProcessId
                }
            }

            if (-not [string]::IsNullOrWhiteSpace($ProcessName)) {
                if ([string]::IsNullOrWhiteSpace($resolvedProcessName)) {
                    continue
                }

                if (-not $resolvedProcessName.Equals($ProcessName, [System.StringComparison]::OrdinalIgnoreCase)) {
                    continue
                }
            }

            [pscustomobject]@{
                Timestamp = $event.TimeCreated.ToString("o")
                ProcessId = $event.ProcessId
                ProcessName = $resolvedProcessName
                ThreadId = $event.ThreadId
                Operation = "OpenKey"
                Status = ("0x{0:X8}" -f $eventStatus)
                Clsid = $clsid
                BaseName = [string]$data["BaseName"]
                RelativeName = [string]$data["RelativeName"]
                Path = $path
                MachineInprocServer32 = $machineInprocServer32
            } | ConvertTo-Json -Compress
        }

        if ($DurationSeconds -gt 0) {
            $elapsed = [DateTimeOffset]::UtcNow - $startedAt
            if ($elapsed.TotalSeconds -ge $DurationSeconds) {
                break
            }
        }

        Start-Sleep -Milliseconds $PollMilliseconds
    }
} finally {
    & logman stop $sessionName -ets | Out-Null

    if (-not $KeepTrace -and (Test-Path -LiteralPath $resolvedTracePath)) {
        Remove-Item -LiteralPath $resolvedTracePath -Force
    }
}
