[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $PSCommandPath
$PluginDir = Resolve-Path (Join-Path $ScriptDir '..')
$DefaultServerDir = Join-Path $PluginDir 'vendor\ghostwriter-mcp'
$ServerDir = if ($env:GHOSTWRITER_MCP_DIR) { $env:GHOSTWRITER_MCP_DIR } else { $DefaultServerDir }

if (-not (Test-Path $ServerDir -PathType Container)) {
  if ($env:GHOSTWRITER_MCP_AUTO_INSTALL -ne '0') {
    [Console]::Error.WriteLine("Ghostwriter MCP is not installed at $ServerDir; installing plugin-local dependency...")
    & (Join-Path $ScriptDir 'install-mcp-deps.ps1') *>&1 | ForEach-Object { [Console]::Error.WriteLine([string]$_) }
    if (-not $?) { exit 1 }
  }
}

if (-not (Test-Path $ServerDir -PathType Container)) {
  [Console]::Error.WriteLine(@"
Ghostwriter MCP is not installed at:
  $ServerDir

Auto-install did not complete. Install it with:
  $ScriptDir\install-mcp-deps.ps1

Or set GHOSTWRITER_MCP_DIR to an existing Ghostwriter MCP server checkout.
Set GHOSTWRITER_MCP_AUTO_INSTALL=0 to disable first-run auto-install.
"@)
  exit 127
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  [Console]::Error.WriteLine('uv is required to run Ghostwriter MCP.')
  exit 127
}

& uv --directory $ServerDir run python -m ghostwritermcp.server
exit $LASTEXITCODE
