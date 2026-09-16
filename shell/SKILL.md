---
name: shell
title: 技能：Shell
description: "仅处理显式 /shell 命令请求，按原文执行命令并遵守宿主权限。"
disable-model-invocation: true
---
# Run Shell Commands

Use this skill only when the user explicitly invokes `/shell`.

## Behavior

1. Treat all user text after the `/shell` invocation as the literal shell command to run.
2. Execute that command immediately with the terminal tool.
3. Do not rewrite, explain, or "improve" the command before running it.
4. Do not inspect the repository first unless the command itself requires repository context.
5. If the user invokes `/shell` without any following text, ask them which command to run.

## Response

- Run the command first.
- Then briefly report the exit status and any important stdout or stderr.
