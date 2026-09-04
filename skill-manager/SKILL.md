---
name: skill-manager
title: 技能管理器
description: 管理本机技能生命周期：列出库存、检查 GitHub 更新、识别重复安装并辅助升级或归档技能。
license: MIT
---

# Skill Lifecycle Manager

This skill helps you maintain your library of GitHub-wrapped skills by automating the detection of updates and assisting in the refactoring process.

## Core Capabilities

1.  **Audit**: Scans your local skills folder for skills with `github_url` metadata.
2.  **Check**: Queries GitHub (via `git ls-remote`) to compare local commit hashes against the latest remote HEAD.
3.  **Report**: Generates a status report identifying which skills are "Stale" or "Current".
4.  **Update Workflow**: Provides a structured process for the Agent to upgrade a skill.
5.  **Inventory Management**: Lists all local skills and provides deletion capabilities.

## Usage

**Trigger**: `/skill-manager check` or "Scan my skills for updates"
**Trigger**: `/skill-manager list` or "List my skills"
**Trigger**: `/skill-manager delete <skill_name>` or "Delete skill <skill_name>"

### Workflow 1: Check for Updates

1.  **Run Scanner**: The agent runs `scripts/scan_and_check.py` to analyze all skills.
2.  **Review Report**: The script outputs a JSON summary. The Agent presents this to the user.
    *   Example: "Found 3 outdated skills: `yt-dlp` (behind 50 commits), `ffmpeg-tool` (behind 2 commits)..."

### Workflow 2: Update a Skill

**Trigger**: "Update [Skill Name]" (after a check)

1.  **Fetch New Context**: The agent fetches the *new* README from the remote repo.
2.  **Diff Analysis**:
    *   The agent compares the new README with the old `SKILL.md`.
    *   Identifies new features, deprecated flags, or usage changes.
3.  **Refactor**:
    *   The agent rewrites `SKILL.md` to reflect the new capabilities.
    *   The agent updates the `github_hash` in the frontmatter.
    *   The agent (optionally) attempts to update the `wrapper.py` if CLI args have changed.
4.  **Verify**: Runs a quick validation (if available).

## Scripts

- `scripts/scan_and_check.py`: The workhorse. Scans directories, parses Frontmatter, fetches remote tags, returns status.
- `scripts/update_helper.py`: (Optional) Helper to backup files before update.
- `scripts/list_skills.py`: Lists all installed skills with type and version.
- `scripts/delete_skill.py`: Permanently removes a skill folder.

## Metadata Requirements

This manager relies on the `github-to-skills` metadata standard:
- `github_url`: Source of truth.
- `github_hash`: State of truth.

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 当用户明确“以本地为准”时，本机当前可识别的 Skills 集合是发布唯一准本；上游差异只记录，不自动合并。
- 发布个人 Skills 仓库时，应同时核对默认 main 分支与既有同步分支，确保仓库首页展示最终镜像。

### Known Fixes & Workarounds
- Windows 上运行 Python Skill 校验器时先启用 UTF-8 模式；若全部报 UnicodeDecodeError，应判定为环境编码问题而非批量修改 Skill。
- 标准更新扫描器只覆盖带 github_url/github_hash 元数据的 Skill；完整盘点还应检查嵌套 Git 仓库并用 git ls-remote 对比远端 HEAD。
- 本地镜像发布必须排除 .system、嵌套 .git、.env、缓存、日志、node_modules、本机构建程序和超大文件，并逐路径暂存，禁止 git add -A。
- 同步嵌套仓库后检查 Git tree mode 160000；需要完整镜像时将子仓库指针转换为普通文件目录，并复核本地与提交后的 Skill 数量。
- 推送命令超时后先查询远端引用；只有远端未更新时才重试，避免重复操作。

### Custom Instruction Injection

执行 Skills 镜像发布时遵循 SCAN→PLAN→CONFIRM→EXECUTE→VERIFY。先确认用户说的“删除远端 Skills”是清空旧内容还是删除整个仓库；镜像完成后必须比较本地可识别 Skill 根目录与提交树，确保 missing=0、extra=0。
