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

以下流程只覆盖上面三组，不代表“全部已安装技能”。全量更新先盘点各安装根目录、嵌套 Git 仓库及包管理来源，并按同一来源去重。

更新前先检查原目录的 Git 状态、锁定上游提交、阅读变更说明和相关源文件，再逐文件比较旧基线、本地定制和上游新版本。保留中文名称、描述、用户规则与既有隐私设置。备份放在技能扫描目录之外。

**存在本地定制或来源不明时，不直接执行下面的 pull / 重装步骤。** 先做可审查的三方适配；没有共同版本沿革时保留原技能并标明来源，不用同名或改版后的无关项目覆盖。仅无冲突且确认安装器不会覆盖定制时，使用以下快捷步骤：

1. 依次进入上游仓库：
   - `C:/Users/Administrator/.codex/skill-repos/wewrite`
   - `C:/Users/Administrator/.codex/skill-repos/creator-buddy`
   - `C:/Users/Administrator/.codex/skill-repos/qu-ai-wei`
2. 确认分支与工作区无冲突后，在每个仓库执行 `git pull --ff-only origin main`。
3. 运行安装脚本：
   ```powershell
   python C:/Users/Administrator/.codex/skill-repos/install_lsf_skills.py
   ```
4. 验证入口、引用文件和受影响脚本；分别汇报静态检查、运行测试和未验证限制。上游哈希不同仅表示有差异，不代表已适配完成。
5. 只有用户要求上传时才检查公开范围、密钥与机器配置，审查 diff 后提交到明确的目标；不自动 commit、push、PR，也不创建或切换 worktree。公开仓库不上传私有记忆、认证文件、机器路径登记或备份。

## 注意

- 该脚本会重新生成 `~/.codex/skills/lsf-wewrite`、`lsf-creator-buddy`、`lsf-qu-ai-wei`。
- 如果你在这些目录里手改过内容，重装前先备份或把改动同步回上游仓库。
