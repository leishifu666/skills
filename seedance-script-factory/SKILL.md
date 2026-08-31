---
name: seedance-script-factory
title: 技能：Seedance Script Factory
description: Use when 用户需要把剧本、storyboard、shot list、已有视频 Prompt 或混合素材整理成适配 Seedance
  2.0 的分镜、资产库、segment 单段总提示词，或需要处理角色漂移、参考图绑定、跨镜头一致性与 prompt-package 交付问题。
---

# Seedance Script Factory

## 概述

这个 Skill 不是单纯的 Prompt 模板库，而是一个面向 `Seedance 2.0` 的多 agent 协调系统。

它的职责是：
- 识别输入类型
- 拆分分镜 / 角色 / 场景 / 道具 / Prompt 子任务
- 统一约束各模块输出
- 在交付前执行质量 gate

默认输出语言固定为中文，目标平台固定为 `Seedance 2.0`。

## 什么时候使用

当用户的目标属于以下任一类型时，应优先调用本 Skill：
- 把原始剧本、梗概、脚本大纲拆成可执行分镜
- 把 storyboard、shot list、粗分镜整理成标准字段
- 把已有 Prompt、镜头描述或半成品生产包压成 `5-15s` 的 segment 级最终单段连贯总提示词
- 处理角色漂移、跨镜头一致性、参考图绑定、`@引用素材` 规划
- 需要交付 `storyboard.csv`、资产库和 `prompt-package.md`
- 需要把镜头级 Prompt、结构化草稿（内部整理态）和最终单段连贯总提示词分层管理

## 不适用场景

以下情况不应调用本 Skill：
- 只要一句简单视频 Prompt，不需要分镜、资产库或 segment 规划
- 只是润色现成视频文案，不涉及 Seedance 生产链路
- 纯单图生图任务，不涉及 `Seedance 2.0`
- 非 Seedance 平台的普通文案任务或通用创意脑暴
- 不涉及角色一致性、参考素材绑定、交付模板或质量 gate 的轻量任务

## 核心入口条件

优先把以下关键词视为调用信号：
- 剧本拆分
- storyboard 标准化
- shot list 整理
- segment 级最终单段连贯总提示词
- 角色一致性 / 角色漂移
- 图生视频参考图绑定
- `@Image1` / `@AssetName` / `@Video1` / `@Audio1`
- prompt-package 交付

## 适用输入

### 1. 原始剧本 / 梗概 / 脚本
- 先拆剧本
- 再规范化镜头
- 再建立资产库

### 2. 现成分镜表 / storyboard / shot list
- 先规范字段
- 再补资产引用与一致性约束
- 再生成 segment 级最终单段连贯总提示词

### 3. 已有视频 Prompt / 半成品生产包
- 先识别它是镜头级、结构化草稿（内部整理态）还是最终交付态
- 再补齐缺失的分镜、资产或一致性约束
- 再压缩成可交付的单段连贯总提示词

### 4. 角色 / 场景 / 道具 / 参考素材混合输入
- 先由总控层识别缺失信息
- 再补分镜骨架
- 再组织资产库与最终 Prompt

## 最小执行顺序

1. 识别输入类型
2. 判断项目视觉定位（真人 / CG / 二次元 / 混合）
3. 由总控层拆分子任务
4. 规范化分镜
5. 建立角色库 / 场景库 / 道具库
6. 规划参考素材与 `@引用素材`
7. 生成镜头级 Prompt
8. 合成为 `5-15s` 的 segment 级最终单段连贯总提示词
9. 执行质量检查
10. 不通过则回退到对应子任务修改
11. 通过后才可视为完成交付

## 多 agent 角色分工

- 总控层：识别输入、拆分任务、汇总结果、触发质量审核
- 分镜 agent：负责分镜拆解、时长分配、节奏与反转位置
- 角色资产 agent：负责角色外观锚点、漂移禁令、参考图绑定
- 场景资产 agent：负责场景稳定结构、灯光、陈设和氛围
- 道具资产 agent：负责道具识别特征、材质和连续性
- Prompt 整合 agent：负责镜头级 Prompt 与 segment 级最终单段连贯总提示词
- 质量 gate：负责审查结构一致性、生成稳定性、开场吸引力、节奏、脚本改编质量和成片感

## 硬性交付物

- `storyboard.csv`
- `characters.csv`
- `scenes.csv`
- `props.csv`
- `prompt-package.md`

## 必读导航

- 流程规则：读 `references/workflow.md`
- Prompt 规范：读 `references/prompt-patterns.md`
- 资产字段：读 `references/asset-schema.md`
- 分镜字段：读 `references/storyboard-schema.md`
- 总控层提示词工程：读 `references/orchestrator-agent.md`
- 分镜 agent 提示词工程：读 `references/storyboard-agent.md`
- 角色资产 agent 提示词工程：读 `references/character-agent.md`
- 场景资产 agent 提示词工程：读 `references/scene-agent.md`
- 道具资产 agent 提示词工程：读 `references/prop-agent.md`
- Prompt 整合 agent 提示词工程：读 `references/prompt-agent.md`
- 质量 gate 提示词工程：读 `references/quality-gate.md`

## 硬规则摘要

- 永远使用中文输出
- 目标平台固定为 `Seedance 2.0`
- 这是多 agent 协调系统，不是单一 Prompt 写作模板
- 单条视频时长按 `5-15s` 口径处理
- 最终视频提示词默认输出为 `segment` 级结果
- 最终视频 Prompt 的最终交付形态必须是**单段连贯总提示词**，而不是拆块说明书
- 最终视频 Prompt 只保留生视频真正需要的信息
- 最终视频 Prompt 强制加入“不要出现字幕，不要出现屏幕文字、字卡、水印”
- 图负责外观，Prompt 负责动作和镜头
- 角色一致性优先于复杂动作和复杂运镜
- 支持 `@引用素材` 机制，如 `@AssetName`、`@Image1`、`@Video1`、`@Audio1`
- 素材输入上限采用谨慎口径：`9图 / 3视频 / 3音频`
- 不把“9图”写死成“总共最多 9 个素材”
- 如果用户给了明确样板，优先对齐用户样板
- 不得擅自发明新剧情
- 未完成质量检查，不得视为交付完成

## 资源说明

### scripts/
- `bootstrap_project.py`：初始化项目目录与模板
- `parse_script.py`：把原始剧本拆成结构化草案
- `normalize_storyboard.py`：把分镜表规范化为统一字段
- `build_asset_libraries.py`：生成角色/场景/道具资产库
- `generate_seedance_prompts.py`：输出 `prompt-package.md`

### references/
- `workflow.md`：流程规则
- `asset-schema.md`：资产字段定义
- `storyboard-schema.md`：分镜字段定义
- `prompt-patterns.md`：Prompt 工程规范

### assets/
- `assets/templates/*.csv`：标准 CSV 模板
- `assets/templates/prompt-package.md`：提示词包模板
