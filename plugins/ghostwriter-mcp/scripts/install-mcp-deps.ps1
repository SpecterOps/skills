[CmdletBinding()]
param(
  [string]$Source = $env:GHOSTWRITER_MCP_SOURCE,
  [string]$Target = $env:GHOSTWRITER_MCP_DIR,
  [switch]$NoUvSync
)

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $PSCommandPath
$PluginDir = Resolve-Path (Join-Path $ScriptDir '..')
if (-not $Target) { $Target = Join-Path $PluginDir 'vendor\ghostwriter-mcp' }
$RunUvSync = -not $NoUvSync -and $env:GHOSTWRITER_MCP_UV_SYNC -ne '0'

if (-not $Source) {
  throw 'GHOSTWRITER_MCP_SOURCE or -Source is required; no canonical Ghostwriter MCP source is bundled in this repo.'
}

$Parent = Split-Path -Parent $Target
New-Item -ItemType Directory -Force -Path $Parent | Out-Null

if (Test-Path (Join-Path $Target '.git') -PathType Container) {
  Write-Host "Updating Ghostwriter MCP checkout at $Target"
  git -C $Target pull --ff-only
} elseif (Test-Path $Target) {
  throw "Target exists but is not a git checkout: $Target. Move it aside or set GHOSTWRITER_MCP_DIR to a different path."
} elseif ((Test-Path $Source -PathType Container) -and -not (Test-Path (Join-Path $Source '.git') -PathType Container)) {
  Write-Host "Copying Ghostwriter MCP source from $Source to $Target"
  New-Item -ItemType Directory -Force -Path $Target | Out-Null
  Copy-Item -Path (Join-Path $Source '*') -Destination $Target -Recurse -Force
} else {
  Write-Host "Installing Ghostwriter MCP from $Source to $Target"
  git clone $Source $Target
}

if ($RunUvSync) {
  if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw 'uv is required to sync Ghostwriter MCP dependencies. Install uv or rerun with -NoUvSync.'
  }
  Write-Host 'Syncing Ghostwriter MCP dependencies with uv'
  Push-Location $Target
  try { uv sync } finally { Pop-Location }
}

Write-Host @"
Ghostwriter MCP installed.

Server directory:
  $Target

Codex MCP runners:
  $ScriptDir\run-ghostwriter-mcp.ps1
  $ScriptDir\run-ghostwriter-mcp.sh

Runtime configuration:
  Provide GHOSTWRITER_URL, GHOSTWRITER_API_KEY, and optionally GHOSTWRITER_CA_BUNDLE
  through your Codex GUI config or environment before starting Codex.
"@
