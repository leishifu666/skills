param(
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'
$repo = 'C:\Users\Administrator\.codex\skill-sources\guizang-ppt-skill'

if (-not (Test-Path -LiteralPath (Join-Path $repo '.git'))) {
    throw "Guizang source repository not found: $repo"
}

$dirty = @(git -C $repo status --porcelain)
if ($LASTEXITCODE -ne 0) {
    throw 'Unable to inspect Guizang repository.'
}
if ($dirty.Count -gt 0) {
    throw 'Guizang repository has local changes. Preserve or revert them before updating.'
}

git -C $repo fetch --quiet origin main
if ($LASTEXITCODE -ne 0) {
    throw 'Unable to fetch Guizang upstream.'
}

$current = (git -C $repo rev-parse HEAD).Trim()
$remote = (git -C $repo rev-parse origin/main).Trim()
$behind = [int](git -C $repo rev-list --count HEAD..origin/main)

if ($Apply -and $behind -gt 0) {
    git -C $repo merge --ff-only origin/main
    if ($LASTEXITCODE -ne 0) {
        throw 'Fast-forward update failed.'
    }
    $current = (git -C $repo rev-parse HEAD).Trim()
    $behind = 0
}

if ($Apply) {
    $sourcesPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\sources.json'))
    if (Test-Path -LiteralPath $sourcesPath) {
        $sources = Get-Content -LiteralPath $sourcesPath -Raw | ConvertFrom-Json
        $sources.guizang.locked_commit = $current
        $sources.guizang.checked_at = (Get-Date).ToString('yyyy-MM-dd')
        $json = $sources | ConvertTo-Json -Depth 8
        [IO.File]::WriteAllText($sourcesPath, $json, (New-Object System.Text.UTF8Encoding($false)))
    }
}

[pscustomobject]@{
    repository = $repo
    current = $current
    remote = $remote
    behind = $behind
    applied = [bool]$Apply
} | ConvertTo-Json
