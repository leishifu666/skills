---
name: lsf-skill-updater
description: LSF｜更新本机已汉化的 LSF 内容创作技能组。当用户说「更新 LSF skills」「更新我的 LSF 内容技能」「同步上游并重装 LSF」时触发。
title: LSF 技能更新器
metadata:
  github_url: local://codex/skill-repos
  github_hash: local
  upstream_name: lsf-skill-updater
  upstream_version: 1.0.0
  installed_at: 2026-09-09T15:20:00
  localized: true
  owner: 雷嵘
---

# LSF 技能更新器

## 用途

更新以下三组已汉化并重命名的 LSF 技能：

- `lsf-wewrite`
- `lsf-creator-buddy`
- `lsf-qu-ai-wei`

## 执行步骤

1. 依次进入上游仓库：
   - `C:/Users/Administrator/.codex/skill-repos/wewrite`
   - `C:/Users/Administrator/.codex/skill-repos/creator-buddy`
   - `C:/Users/Administrator/.codex/skill-repos/qu-ai-wei`
2. 在每个仓库执行 `git pull origin main`。
3. 运行安装脚本：
   ```powershell
   python C:/Users/Administrator/.codex/skill-repos/install_lsf_skills.py
   ```
4. 汇报更新后的技能数量、上游提交号和是否有失败。

## 注意

- 该脚本会重新生成 `~/.codex/skills/lsf-wewrite`、`lsf-creator-buddy`、`lsf-qu-ai-wei`。
- 如果你在这些目录里手改过内容，重装前先备份或把改动同步回上游仓库。
