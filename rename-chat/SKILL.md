---
name: rename-chat
title: 技能：Rename CHAT
description: "处理显式 /rename-chat 请求，为当前对话生成符合宿主要求的标题。"
disable-model-invocation: true
environments:
- local
---
# Rename Chat

Slash-only. Text after `/rename-chat` is an optional naming hint, not a verbatim title.

Pick a 3-5 word topic title in sentence case: first letter uppercase, rest lowercase except acronyms and proper nouns. Hint steers wording only. Example: hint `billing retries` → `Billing retries`. Avoid "Chat", "Conversation", or "Rename chat". At most 200 characters.

Call `cursor-app-control.rename_chat` once with that title. Do not ask for confirmation. If the tool is missing or fails, say so plainly and do not claim the chat was renamed.
