> **说明：** 本仓库包含 Anthropic 为 Claude 提供的 Skills 实现。关于 Agent Skills 标准，可查看 [agentskills.io](http://agentskills.io)。

# Skills
`Skills` 是一组目录，内含指令、脚本和资源，Claude 可动态加载它们以提升特定场景下的任务表现。无论是按企业品牌规范生成文档、按你的业务流程做数据分析，还是自动化日常个人事务，Skills 都能以可复用的方式稳定产出结果。

For more information, check out:
- [什么是 Skills？](https://support.claude.com/en/articles/12512176-what-are-skills)
- [如何在 Claude 中使用 Skills](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [如何创建自定义 Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [如何通过 Agent Skills 让 Agent 更贴近真实场景](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

# 关于本仓库

本仓库收录了一组 Skill 示例，演示了 Claude Skills 系统可实现的能力。示例覆盖从创意方向（如艺术、音乐、设计）到技术方向（如网页应用测试、MCP 服务生成），再到企业工作流（如沟通、品牌传播等）等多种场景。

每个 Skill 都是独立目录，并含有 `SKILL.md`，其中存放 Claude 读取的说明与元数据。你可以浏览这些示例，借鉴实现思路，或理解不同的模式与实现路径。

本仓库中的不少 Skill 采用 Apache 2.0 开源许可；同时我们也在 [`skills/docx`](./skills/docx)、[`skills/pdf`](./skills/pdf)、[`skills/pptx`](./skills/pptx)、[`skills/xlsx`](./skills/xlsx) 目录里提供了支撑 [Claude 文档能力](https://www.anthropic.com/news/create-files)的相关实现。它们为源码可见（source-available）而非完整开源，目的是给开发者提供更复杂 Skill 的参考。

## 免责声明

## 仅供个人使用

本仓库仅供我个人学习、研究与自用。

- 未经书面授权，不得复制、再分发、公开镜像或转载本仓库内容。
- 禁止任何形式的商业用途，包括但不限于：面向第三方收取费用的产品、SaaS 服务、咨询服务或转售。
- 未经书面授权，不得将仓库公开分发，或以公开仓库形式创建 public fork。
- 禁止任何用于公共传播或商业目的的修改再发布（包括派生作品）。

如非仓库所有者，访问与使用本仓库请确保已获得我的书面许可。默认建议保持仓库为 `Private` 可见性。

**本仓库中的示例仅用于演示与学习。** Claude 某些能力可能已在官方产品中可用，但你在本仓库中的实际实现与 Claude 实际表现可能存在差异。示例主要用于展示模式与思路，仅可用于实验与学习，关键场景请先在你的环境充分测试。

# Skill Sets
- [./skills](./skills): Skill examples for Creative & Design, Development & Technical, Enterprise & Communication, and Document Skills
- [./spec](./spec): The Agent Skills specification
- [./template](./template): Skill template

# Try in Claude Code, Claude.ai, and the API

## Claude Code
You can register this repository as a Claude Code Plugin marketplace by running the following command in Claude Code:
```
/plugin marketplace add anthropics/skills
```

Then, to install a specific set of skills:
1. Select `Browse and install plugins`
2. Select `anthropic-agent-skills`
3. Select `document-skills` or `example-skills`
4. Select `Install now`

Alternatively, directly install either Plugin via:
```
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

After installing the plugin, you can use the skill by just mentioning it. For instance, if you install the `document-skills` plugin from the marketplace, you can ask Claude Code to do something like: "Use the PDF skill to extract the form fields from `path/to/some-file.pdf`"

## Claude.ai

These example skills are all already available to paid plans in Claude.ai. 

To use any skill from this repository or upload custom skills, follow the instructions in [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude#h_a4222fa77b).

## Claude API

You can use Anthropic's pre-built skills, and upload custom skills, via the Claude API. See the [Skills API Quickstart](https://docs.claude.com/en/api/skills-guide#creating-a-skill) for more.

# Creating a Basic Skill

Skills are simple to create - just a folder with a `SKILL.md` file containing YAML frontmatter and instructions. You can use the **template-skill** in this repository as a starting point:

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Add your instructions here that Claude will follow when this skill is active]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

The frontmatter requires only two fields:
- `name` - A unique identifier for your skill (lowercase, hyphens for spaces)
- `description` - A complete description of what the skill does and when to use it

The markdown content below contains the instructions, examples, and guidelines that Claude will follow. For more details, see [How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills).

# Partner Skills

Skills are a great way to teach Claude how to get better at using specific pieces of software. As we see awesome example skills from partners, we may highlight some of them here:

- **Notion** - [Notion Skills for Claude](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0)
