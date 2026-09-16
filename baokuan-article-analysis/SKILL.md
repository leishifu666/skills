---
name: lsf-baokuan-article-analysis
description: LSF｜抓取并分析公众号爆款文章，支持按赛道或关键词查看阅读、点赞、分享、评论、标题模式和写作参考。
title: LSF 公众号爆款分析
metadata:
  github_url: https://github.com/SpaceZephyr/creator-buddy
  github_hash: edf46c567ff54b72ee2157d06f3a02dbd67aaa9c
  github_path: gzh-Skills/baokuan-article-analysis
  upstream_name: baokuan-article-analysis
  upstream_version: 1.0.0
  installed_at: '2026-09-09T15:20:30'
  localized: true
  owner: 雷嵘
---

> **LSF 汉化版**：上游模块名 `baokuan-article-analysis`，本机调用名 `lsf-baokuan-article-analysis`。

# 爆款文章分析

## Overview

Use this skill to fetch hot WeChat Official Account article data by sector and generate a daily analysis report. It is for sector-level or keyword-level analysis, not exact historical scraping for one specific account.

The bundled script queries the hot-article data source, merges keywords by sector, deduplicates articles, ranks them, and writes:

- `data.json`: raw structured data
- `report.html`: a minimal visual analysis report with KPI cards, bar charts, ranked article cards, writing style analysis, hot reasons, and writing references

Do not default to Markdown reports. The primary user-facing artifact is `report.html`.

## Quick Start

Run with the default sectors:

```bash
python3 ~/.codex/skills/baokuan-article-analysis/scripts/daily_sector_trends.py \
  --output-dir ./output/baokuan-article-analysis
```

Run custom sectors:

```bash
python3 ~/.codex/skills/baokuan-article-analysis/scripts/daily_sector_trends.py \
  --sector 'AI Agent=AI Agent,智能体,Agent框架' \
  --sector 'Skill=skill,Skills,AI Skill' \
  --sector 'Claude Code=Claude Code,Codex,AI编程' \
  --output-dir ./output/baokuan-article-analysis
```

Run with a JSON config:

```bash
python3 ~/.codex/skills/baokuan-article-analysis/scripts/daily_sector_trends.py \
  --sector-config ~/.codex/skills/baokuan-article-analysis/references/default-sectors.json \
  --days 7 \
  --output-dir ./output/baokuan-article-analysis
```

## Workflow

1. Identify sectors and keywords from the user request.
2. If the user only gives broad sectors, use or adapt `references/default-sectors.json`.
3. Run `scripts/daily_sector_trends.py`.
4. Open the generated `report.html`.
5. Summarize for the user:
   - highest-reading and highest-sharing articles
   - writing style patterns
   - hot article reasons
   - title and topic formulas
   - practical writing references
6. Return the HTML file path as the main artifact.

## Script Options

| Option | Purpose |
|---|---|
| `--sector '赛道=关键词1,关键词2'` | Add one sector. Can repeat. |
| `--sector-config path.json` | Load sectors from JSON object. |
| `--days N` | Lookback window. Default is 7 days. |
| `--start-date YYYY-MM-DD` | Explicit start date. Overrides `--days`. |
| `--max-items-per-sector N` | Limit ranked articles per sector. Default is 10. |
| `--output-dir DIR` | Parent output directory. A date folder is created inside. |
| `--report-date YYYY-MM-DD` | Report date. Default is today. |

## Data Boundaries

- This skill returns hot-list data, not a specific account’s complete recent history.
- `clicksCount` is a public data-source snapshot and may lag behind live WeChat backend reads.
- If a specific account name returns no data, switch to that account’s topic keywords and compare same-sector articles.
- If today’s data is sparse, use `--days 7` or `--days 30`.

## Output Interpretation

Use reading count for reach, share count for spread, comments for discussion, and low-fan high-reading entries for title/structure references. Repeated accounts indicate strong competitors or content sources worth following.
