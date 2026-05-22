[CmdletBinding()]
param(
  [string]$Source = $env:BLOODHOUND_MCP_SOURCE,
  [string]$Target = $env:BLOODHOUND_MCP_DIR,
  [switch]$NoUvSync
)

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $PSCommandPath
$PluginDir = Resolve-Path (Join-Path $ScriptDir '..')
if (-not $Source) { $Source = 'https://github.com/mwnickerson/bloodhound_mcp.git' }
if (-not $Target) { $Target = Join-Path $PluginDir 'vendor\bloodhound-mcp' }
$RunUvSync = -not $NoUvSync -and $env:BLOODHOUND_MCP_UV_SYNC -ne '0'

$Parent = Split-Path -Parent $Target
New-Item -ItemType Directory -Force -Path $Parent | Out-Null

if (Test-Path (Join-Path $Target '.git') -PathType Container) {
  Write-Host "Updating BloodHound MCP checkout at $Target"
  git -C $Target pull --ff-only
} elseif (Test-Path $Target) {
  throw "Target exists but is not a git checkout: $Target. Move it aside or set BLOODHOUND_MCP_DIR to a different path."
} else {
  Write-Host "Installing BloodHound MCP from $Source to $Target"
  git clone $Source $Target
}

if ($RunUvSync) {
  if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw 'uv is required to sync BloodHound MCP dependencies. Install uv or rerun with -NoUvSync.'
  }
  Write-Host 'Syncing BloodHound MCP dependencies with uv'
  Push-Location $Target
  try { uv sync } finally { Pop-Location }
}

Write-Host @"
BloodHound MCP installed.

Server directory:
  $Target

Codex MCP runners:
  $ScriptDir\run-bloodhound-mcp.ps1
  $ScriptDir\run-bloodhound-mcp.sh

Credential setup:
  Provide BLOODHOUND_* variables through your Codex GUI config or environment.
"@
