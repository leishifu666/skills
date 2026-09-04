---
name: rename-chat
title: 技能：Rename CHAT
description: 用于处理“Rename CHAT”相关任务。仅在用户明确提出该需求，或任务与该技能的专业范围直接匹配时使用。
disable-model-invocation: true
environments:
- local
---
# Rename Chat

Slash-only. Text after `/rename-chat` is an optional naming hint, not a verbatim title.

Pick a 3-5 word topic title in sentence case: first letter uppercase, rest lowercase except acronyms and proper nouns. Hint steers wording only. Example: hint `billing retries` → `Billing retries`. Avoid "Chat", "Conversation", or "Rename chat". At most 200 characters.

Call `cursor-app-control.rename_chat` once with that title. Do not ask for confirmation. If the tool is missing or fails, say so plainly and do not claim the chat was renamed.
