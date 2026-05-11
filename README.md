> **注意：** 本仓库包含 Anthropic 为 Claude 实现的技能（Skills）。有关 Agent Skills 标准的信息，请参阅 [agentskills.io](http://agentskills.io)。

# 技能（Skills）
技能是由指令、脚本和资源组成的文件夹，Claude 会动态加载这些内容以提升在特定任务上的表现。技能教会 Claude 如何以可重复的方式完成特定任务，无论是按照公司品牌指南创建文档、使用组织特定工作流分析数据，还是自动化个人任务。

了解更多信息：
- [什么是技能？](https://support.claude.com/en/articles/12512176-what-are-skills)
- [在 Claude 中使用技能](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [如何创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [用 Agent Skills 为真实世界的 Agent 赋能](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

# 关于本仓库

本仓库包含展示 Claude 技能系统能力的各种技能。这些技能涵盖创意应用（艺术、音乐、设计）、技术任务（Web 应用测试、MCP 服务器生成）以及企业工作流（沟通、品牌等）。

每个技能都独立存放在自己的文件夹中，包含一个 `SKILL.md` 文件，其中有 Claude 使用的指令和元数据。浏览这些技能可以为你创建自己的技能提供灵感，或帮助你理解不同的模式和方法。

本仓库中的许多技能是开源的（Apache 2.0）。我们还包含了支撑 [Claude 文档功能](https://www.anthropic.com/news/create-files) 的文档创建和编辑技能，位于 [`skills/docx`](./skills/docx)、[`skills/pdf`](./skills/pdf)、[`skills/pptx`](./skills/pptx) 和 [`skills/xlsx`](./skills/xlsx) 子文件夹中。这些是源代码可见（source-available）而非开源的，但我们希望将它们分享给开发者，作为在生产 AI 应用中实际使用的复杂技能的参考。

## 免责声明

**这些技能仅供演示和教育目的。** 虽然其中一些功能可能在 Claude 中可用，但你从 Claude 获得的实现和行为可能与这些技能中展示的有所不同。这些技能旨在说明模式和可能性。在依赖它们完成关键任务之前，请始终在你自己的环境中彻底测试。

# 技能集
- [./skills](./skills)：创意与设计、开发与技术、企业与沟通、文档技能的示例
- [./spec](./spec)：Agent Skills 规范
- [./template](./template)：技能模板

# 在 Claude Code、Claude.ai 和 API 中使用

## Claude Code
你可以通过在 Claude Code 中运行以下命令，将本仓库注册为 Claude Code 插件市场：
```
/plugin marketplace add anthropics/skills
```

然后，安装特定的技能集：
1. 选择 `Browse and install plugins`（浏览并安装插件）
2. 选择 `anthropic-agent-skills`
3. 选择 `document-skills` 或 `example-skills`
4. 选择 `Install now`（立即安装）

或者，直接通过以下命令安装插件：
```
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

安装插件后，只需提及即可使用该技能。例如，如果你从市场安装了 `document-skills` 插件，可以让 Claude Code 执行类似这样的操作："使用 PDF 技能从 `path/to/some-file.pdf` 提取表单字段"

## Claude.ai

这些示例技能已在 Claude.ai 的付费计划中全部可用。

要使用本仓库中的任何技能或上传自定义技能，请按照 [在 Claude 中使用技能](https://support.claude.com/en/articles/12512180-using-skills-in-claude#h_a4222fa77b) 中的说明操作。

## Claude API

你可以通过 Claude API 使用 Anthropic 预构建的技能，也可以上传自定义技能。详情请参阅 [Skills API 快速入门](https://docs.claude.com/en/api/skills-guide#creating-a-skill)。

# 创建基础技能

创建技能很简单——只需一个包含 `SKILL.md` 文件的文件夹，文件中包含 YAML 前言（frontmatter）和指令。你可以使用本仓库中的 **template-skill** 作为起点：

```markdown
---
name: my-skill-name
description: 清晰描述此技能的功能以及何时使用
---

# 我的技能名称

[在此添加 Claude 在此技能激活时将遵循的指令]

## 示例
- 示例用法 1
- 示例用法 2

## 指南
- 指南 1
- 指南 2
```

前言（frontmatter）只需要两个字段：
- `name` - 技能的唯一标识符（小写，用连字符代替空格）
- `description` - 技能功能及使用场景的完整描述

下方的 Markdown 内容包含 Claude 将遵循的指令、示例和指南。更多详情请参阅 [如何创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills)。

# 合作伙伴技能

技能是教 Claude 更好地使用特定软件的好方法。随着我们看到合作伙伴提供的优秀示例技能，我们可能会在这里重点展示：

- **Notion** - [Notion Skills for Claude](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0)
