[CmdletBinding()]
param(
    [ValidateSet('check', 'update')]
    [string]$Action = 'check',
    [string]$Ref = 'main'
)

$ErrorActionPreference = 'Stop'
$SkillsRoot = $PSScriptRoot
$ManifestPath = Join-Path $SkillsRoot 'lsf-visual-upstream.json'
$Source = 'https://github.com/smixs/visual-skills'
$Manifest = Get-Content -Raw -LiteralPath $ManifestPath | ConvertFrom-Json

function Get-RemoteHash {
    $result = & gh api "repos/smixs/visual-skills/commits/$Ref" --jq '.sha'
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($result)) {
        throw "无法读取上游提交：$Source ($Ref)"
    }
    return $result.Trim()
}

$remoteHash = Get-RemoteHash
$localHash = $Manifest.installed_hash
Write-Output "上游：$Source"
Write-Output "本地记录：$localHash"
Write-Output "远程 $Ref：$remoteHash"

if ($remoteHash -eq $localHash) {
    Write-Output '状态：当前已是最新版本。'
    if ($Action -eq 'check') { exit 0 }
    Write-Output '没有需要同步的上游文件。'
    exit 0
}

Write-Output '状态：上游有更新。'
if ($Action -eq 'check') {
    Write-Output '检查模式不会修改本地文件。'
    exit 10
}

# 更新模式只暂存上游原文，绝不覆盖已经汉化的 LSF Skill。
$stageRoot = Join-Path $SkillsRoot ("_upstream\visual-skills-" + $remoteHash.Substring(0, 7))
if (Test-Path -LiteralPath $stageRoot) {
    Write-Output "该上游版本已暂存：$stageRoot"
    exit 0
}

$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("lsf-visual-update-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $stageRoot, $tempRoot | Out-Null
try {
    foreach ($skill in $Manifest.skills) {
        $target = Join-Path $SkillsRoot $skill.name
        $upstream = Join-Path $tempRoot $skill.upstream_path
        if (-not (Test-Path -LiteralPath $target)) { throw "本地 Skill 不存在：$target" }

        & python (Join-Path $PSScriptRoot 'update-lsf-visual-content.py') `
            --source $Source --ref $Ref --upstream-path $skill.upstream_path `
            --target (Join-Path $stageRoot $skill.name) --temp $upstream --hash $remoteHash --name $skill.name
        if ($LASTEXITCODE -ne 0) { throw "暂存失败：$($skill.name)" }
    }
    Write-Output "上游版本已暂存：$stageRoot"
    Write-Output '现有 LSF Skill 未修改。请先比较暂存内容，完成汉化复核后再人工替换。'
}
catch {
    Write-Error $_
    if (Test-Path -LiteralPath $stageRoot) { Remove-Item -LiteralPath $stageRoot -Recurse -Force }
    exit 1
}
finally {
    if (Test-Path -LiteralPath $tempRoot) { Remove-Item -LiteralPath $tempRoot -Recurse -Force }
}
