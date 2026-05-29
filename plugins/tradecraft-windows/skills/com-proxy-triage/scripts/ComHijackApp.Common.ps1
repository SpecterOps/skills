function Normalize-ComHijackExecutableName {
    param([AllowNull()][string]$Name)

    if ([string]::IsNullOrWhiteSpace($Name)) {
        return $null
    }

    $normalized = $Name.Trim()
    if (-not $normalized.EndsWith('.exe', [System.StringComparison]::OrdinalIgnoreCase)) {
        $normalized = '{0}.exe' -f $normalized
    }

    return $normalized.ToLowerInvariant()
}

function Normalize-ComHijackPackageId {
    param([AllowNull()][string]$Value)

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return $null
    }

    return ($Value.ToLowerInvariant() -replace '[^a-z0-9]+', '-').Trim('-')
}

function Get-ComHijackAppManifestEntries {
    param(
        [AllowNull()][string]$ConfigPath,
        [Parameter(Mandatory = $true)]
        [string]$ScriptDirectory
    )

    if ([string]::IsNullOrWhiteSpace($ConfigPath)) {
        $ConfigPath = Join-Path $ScriptDirectory '..\assets\apps.json'
    }

    if (-not (Test-Path -LiteralPath $ConfigPath)) {
        return @()
    }

    return @(Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json)
}

function Get-ComHijackManifestEntry {
    param(
        [object[]]$ManifestEntries,
        [AllowNull()][string]$AppName
    )

    if (-not $ManifestEntries -or [string]::IsNullOrWhiteSpace($AppName)) {
        return $null
    }

    $exact = @($ManifestEntries | Where-Object {
        $_.AppName -and $_.AppName.Equals($AppName, [System.StringComparison]::OrdinalIgnoreCase)
    } | Select-Object -First 1)
    if ($exact.Count -gt 0) {
        return $exact[0]
    }

    $contains = @($ManifestEntries | Where-Object {
        $_.AppName -and $_.AppName.IndexOf($AppName, [System.StringComparison]::OrdinalIgnoreCase) -ge 0
    } | Select-Object -First 1)
    if ($contains.Count -gt 0) {
        return $contains[0]
    }

    return $null
}

function Resolve-ComHijackDisplayIconPath {
    param([AllowNull()][string]$DisplayIcon)

    if ([string]::IsNullOrWhiteSpace($DisplayIcon)) {
        return $null
    }

    $candidate = $DisplayIcon.Trim().Trim('"')
    $commaIndex = $candidate.IndexOf(',')
    if ($commaIndex -gt 0) {
        $candidate = $candidate.Substring(0, $commaIndex)
    }

    if (Test-Path -LiteralPath $candidate) {
        return [System.IO.Path]::GetFullPath($candidate)
    }

    return $null
}

function Get-ComHijackUninstallEntries {
    $registryPaths = @(
        'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
        'Registry::HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall',
        'Registry::HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    )

    $results = [System.Collections.Generic.List[object]]::new()
    foreach ($registryPath in $registryPaths) {
        if (-not (Test-Path -LiteralPath $registryPath)) {
            continue
        }

        foreach ($child in @(Get-ChildItem -LiteralPath $registryPath -ErrorAction SilentlyContinue)) {
            try {
                $item = Get-ItemProperty -LiteralPath $child.PSPath -ErrorAction Stop
                if ([string]::IsNullOrWhiteSpace($item.DisplayName)) {
                    continue
                }

                $results.Add([pscustomobject]@{
                    DisplayName     = [string]$item.DisplayName
                    DisplayVersion  = [string]$item.DisplayVersion
                    DisplayIcon     = [string]$item.DisplayIcon
                    InstallLocation = [string]$item.InstallLocation
                    Publisher       = [string]$item.Publisher
                    RegistryPath    = [string]$child.PSPath
                })
            } catch {
            }
        }
    }

    return @($results)
}

function Get-ComHijackAppTokens {
    param([string[]]$Values)

    return @($Values |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        ForEach-Object {
            $raw = $_.Trim()
            @(
                $raw,
                [System.IO.Path]::GetFileNameWithoutExtension($raw)
            ) + ($raw -split '[^A-Za-z0-9]+')
        } |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        ForEach-Object { $_.ToLowerInvariant() } |
        Sort-Object -Unique)
}

function Find-ComHijackExecutableInDirectory {
    param(
        [AllowNull()][string]$DirectoryPath,
        [string[]]$Hints
    )

    if ([string]::IsNullOrWhiteSpace($DirectoryPath) -or -not (Test-Path -LiteralPath $DirectoryPath)) {
        return $null
    }

    $tokens = Get-ComHijackAppTokens -Values $Hints
    $candidates = @(Get-ChildItem -LiteralPath $DirectoryPath -Filter *.exe -File -Recurse -ErrorAction SilentlyContinue)
    if ($candidates.Count -eq 0) {
        return $null
    }

    $best = $candidates |
        ForEach-Object {
            $name = $_.Name.ToLowerInvariant()
            $baseName = $_.BaseName.ToLowerInvariant()
            $fullName = $_.FullName.ToLowerInvariant()
            $score = 100
            foreach ($token in $tokens) {
                if ($baseName -eq $token) {
                    $score = [Math]::Min($score, 0)
                } elseif ($name -eq ('{0}.exe' -f $token)) {
                    $score = [Math]::Min($score, 1)
                } elseif ($baseName.Contains($token)) {
                    $score = [Math]::Min($score, 2)
                } elseif ($fullName.Contains($token)) {
                    $score = [Math]::Min($score, 3)
                }
            }

            [pscustomobject]@{
                FullName = $_.FullName
                Score    = $score
                Length   = $_.Length
            }
        } |
        Sort-Object Score, Length |
        Select-Object -First 1

    if ($null -eq $best -or $best.Score -ge 100) {
        return $null
    }

    return $best.FullName
}

function Find-ComHijackExecutableInCommonRoots {
    param(
        [string]$AppName,
        [string[]]$Hints
    )

    $roots = @(
        $env:ProgramFiles,
        ${env:ProgramFiles(x86)},
        (Join-Path $env:LOCALAPPDATA 'Programs'),
        $env:LOCALAPPDATA,
        $env:APPDATA
    ) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) -and (Test-Path -LiteralPath $_) }

    $tokens = Get-ComHijackAppTokens -Values @($AppName) + $Hints
    foreach ($root in $roots | Select-Object -Unique) {
        $matchingDirectories = @(Get-ChildItem -LiteralPath $root -Directory -ErrorAction SilentlyContinue | Where-Object {
            $directoryName = $_.Name.ToLowerInvariant()
            @($tokens | Where-Object { $directoryName.Contains($_) }).Count -gt 0
        })

        foreach ($directory in $matchingDirectories) {
            $match = Find-ComHijackExecutableInDirectory -DirectoryPath $directory.FullName -Hints (@($AppName) + $Hints)
            if (-not [string]::IsNullOrWhiteSpace($match)) {
                return $match
            }
        }
    }

    return $null
}

function Resolve-ComHijackAppTarget {
    param(
        [Parameter(Mandatory = $true)]
        [string]$AppName,
        [AllowNull()][string]$ConfigPath,
        [AllowNull()][string]$LaunchExecutable,
        [AllowNull()][string[]]$LaunchArgumentList,
        [AllowNull()][string[]]$TargetProcesses,
        [AllowNull()][string]$ProcessName,
        [AllowNull()][string]$PackageId,
        [Parameter(Mandatory = $true)]
        [string]$ScriptDirectory
    )

    $manifestEntries = Get-ComHijackAppManifestEntries -ConfigPath $ConfigPath -ScriptDirectory $ScriptDirectory
    $manifestEntry = Get-ComHijackManifestEntry -ManifestEntries $manifestEntries -AppName $AppName
    $resolvedExecutable = $null
    $resolutionSource = $null
    $matchingInstallEntry = $null

    if (-not [string]::IsNullOrWhiteSpace($LaunchExecutable)) {
        $resolvedExecutable = [System.IO.Path]::GetFullPath($LaunchExecutable)
        if (-not (Test-Path -LiteralPath $resolvedExecutable)) {
            throw "Requested launch executable not found: $LaunchExecutable"
        }
        $resolutionSource = 'ExplicitExecutable'
    }

    if ([string]::IsNullOrWhiteSpace($resolvedExecutable) -and $null -ne $manifestEntry -and -not [string]::IsNullOrWhiteSpace($manifestEntry.LaunchExecutable)) {
        $candidate = [System.IO.Path]::GetFullPath([string]$manifestEntry.LaunchExecutable)
        if (Test-Path -LiteralPath $candidate) {
            $resolvedExecutable = $candidate
            $resolutionSource = 'Manifest'
        }
    }

    $searchHints = @(
        $AppName,
        $ProcessName,
        $PackageId
    )
    if ($null -ne $manifestEntry) {
        $searchHints += @(
            [string]$manifestEntry.AppName,
            [string]$manifestEntry.ProcessName,
            [string]$manifestEntry.PackageId,
            [System.IO.Path]::GetFileNameWithoutExtension([string]$manifestEntry.LaunchExecutable)
        )
    }

    if ([string]::IsNullOrWhiteSpace($resolvedExecutable)) {
        $installEntries = Get-ComHijackUninstallEntries
        $matchingInstallEntry = @($installEntries |
            Where-Object {
                $_.DisplayName -and (
                    $_.DisplayName.Equals($AppName, [System.StringComparison]::OrdinalIgnoreCase) -or
                    $_.DisplayName.IndexOf($AppName, [System.StringComparison]::OrdinalIgnoreCase) -ge 0
                )
            } |
            Sort-Object {
                if ($_.DisplayName.Equals($AppName, [System.StringComparison]::OrdinalIgnoreCase)) { 0 } else { 1 }
            } |
            Select-Object -First 1)

        if ($matchingInstallEntry.Count -gt 0) {
            $matchingInstallEntry = $matchingInstallEntry[0]
            $resolvedExecutable = Resolve-ComHijackDisplayIconPath -DisplayIcon $matchingInstallEntry.DisplayIcon
            if ([string]::IsNullOrWhiteSpace($resolvedExecutable)) {
                $resolvedExecutable = Find-ComHijackExecutableInDirectory -DirectoryPath $matchingInstallEntry.InstallLocation -Hints $searchHints
            }

            if (-not [string]::IsNullOrWhiteSpace($resolvedExecutable)) {
                $resolutionSource = 'UninstallRegistry'
            }
        }
    }

    if ([string]::IsNullOrWhiteSpace($resolvedExecutable)) {
        $resolvedExecutable = Find-ComHijackExecutableInCommonRoots -AppName $AppName -Hints $searchHints
        if (-not [string]::IsNullOrWhiteSpace($resolvedExecutable)) {
            $resolutionSource = 'CommonInstallRoots'
        }
    }

    if ([string]::IsNullOrWhiteSpace($resolvedExecutable)) {
        throw "Unable to locate an installed executable for app '$AppName'. Provide -LaunchExecutable or add an override entry in assets\\apps.json."
    }

    $resolvedLeafName = [System.IO.Path]::GetFileName($resolvedExecutable)
    if ([string]::IsNullOrWhiteSpace($ProcessName)) {
        if ($null -ne $manifestEntry -and -not [string]::IsNullOrWhiteSpace($manifestEntry.ProcessName)) {
            $ProcessName = [string]$manifestEntry.ProcessName
        } else {
            $ProcessName = [System.IO.Path]::GetFileNameWithoutExtension($resolvedExecutable)
        }
    }

    if (-not $LaunchArgumentList -or $LaunchArgumentList.Count -eq 0) {
        if ($null -ne $manifestEntry -and $manifestEntry.LaunchArgumentList) {
            $LaunchArgumentList = @($manifestEntry.LaunchArgumentList)
        } else {
            $LaunchArgumentList = @()
        }
    }

    if (-not $TargetProcesses -or $TargetProcesses.Count -eq 0) {
        if ($null -ne $manifestEntry -and $manifestEntry.TargetProcesses) {
            $TargetProcesses = @($manifestEntry.TargetProcesses)
        } else {
            $TargetProcesses = @($resolvedLeafName)
        }
    }

    if ([string]::IsNullOrWhiteSpace($PackageId)) {
        if ($null -ne $manifestEntry -and -not [string]::IsNullOrWhiteSpace($manifestEntry.PackageId)) {
            $PackageId = [string]$manifestEntry.PackageId
        } else {
            $PackageId = Normalize-ComHijackPackageId -Value $AppName
        }
    }

    $resolvedAppName = $AppName
    if ($null -ne $manifestEntry -and -not [string]::IsNullOrWhiteSpace($manifestEntry.AppName)) {
        $resolvedAppName = [string]$manifestEntry.AppName
    } elseif ($matchingInstallEntry -and -not [string]::IsNullOrWhiteSpace($matchingInstallEntry.DisplayName)) {
        $resolvedAppName = [string]$matchingInstallEntry.DisplayName
    }

    return [pscustomobject]@{
        AppName          = $resolvedAppName
        PackageId        = $PackageId
        ProcessName      = $ProcessName
        LaunchExecutable = $resolvedExecutable
        LaunchArgumentList = @($LaunchArgumentList)
        TargetProcesses  = @($TargetProcesses | ForEach-Object { Normalize-ComHijackExecutableName -Name $_ } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Sort-Object -Unique)
        ResolutionSource = $resolutionSource
    }
}
