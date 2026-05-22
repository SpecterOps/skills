[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $PSCommandPath
$PluginDir = Resolve-Path (Join-Path $ScriptDir '..')
$DefaultServerDir = Join-Path $PluginDir 'vendor\bloodhound-mcp'
$ServerDir = if ($env:BLOODHOUND_MCP_DIR) { $env:BLOODHOUND_MCP_DIR } else { $DefaultServerDir }

if (-not (Test-Path (Join-Path $ServerDir 'main.py') -PathType Leaf)) {
  if ($env:BLOODHOUND_MCP_AUTO_INSTALL -ne '0') {
    [Console]::Error.WriteLine("BloodHound MCP is not installed at $ServerDir; installing plugin-local dependency...")
    & (Join-Path $ScriptDir 'install-mcp-deps.ps1') *>&1 | ForEach-Object { [Console]::Error.WriteLine([string]$_) }
    if (-not $?) { exit 1 }
  }
}

if (-not (Test-Path (Join-Path $ServerDir 'main.py') -PathType Leaf)) {
  [Console]::Error.WriteLine(@"
BloodHound MCP is not installed at:
  $ServerDir

Auto-install did not complete. Install it with:
  $ScriptDir\install-mcp-deps.ps1

Or set BLOODHOUND_MCP_DIR to an existing bloodhound_mcp checkout.
Set BLOODHOUND_MCP_AUTO_INSTALL=0 to disable first-run auto-install.
"@)
  exit 127
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  [Console]::Error.WriteLine('uv is required to run BloodHound MCP.')
  exit 127
}

& uv --directory $ServerDir run main.py
exit $LASTEXITCODE
