[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $PSCommandPath
$PluginDir = Resolve-Path (Join-Path $ScriptDir '..')
$DefaultServerDir = Join-Path $PluginDir 'vendor\bloodhound-mcp'
$ServerDir = if ($env:BLOODHOUND_MCP_DIR) { $env:BLOODHOUND_MCP_DIR } else { $DefaultServerDir }

if (-not (Test-Path (Join-Path $ServerDir 'main.py') -PathType Leaf)) {
  [Console]::Error.WriteLine(@"
BloodHound MCP is not installed at:
  $ServerDir

Install it alongside the plugin with:
  $ScriptDir\install-mcp-deps.ps1

Or set BLOODHOUND_MCP_DIR to an existing bloodhound_mcp checkout.
"@)
  exit 127
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  [Console]::Error.WriteLine('uv is required to run BloodHound MCP.')
  exit 127
}

& uv --directory $ServerDir run main.py
exit $LASTEXITCODE
