---
name: web-artifacts-builder
title: 技能：WEB Artifacts Builder
description: 一套用于使用现代前端技术（React, Tailwind CSS, shadcn/ui）创建复杂的、多组件的 claude.ai HTML
  变体的工具。适用于需要状态管理、路由或 shadcn/ui 组件的复杂项目 - 不适用于简单的单文件 HTML/JSX 变体。
license: Complete terms in LICENSE.txt
---

# Web Artifacts 生成器

要构建强大的前端 claude.ai 变体，请遵循以下步骤：
1. 使用 `scripts/init-artifact.sh` 初始化前端仓库
2. 通过编辑生成的代码开发您的变体
3. 使用 `scripts/bundle-artifact.sh` 将所有代码打包成单个 HTML 文件
4. 向用户展示变体
5. (可选) 测试变体

**技术栈**: React 18 + TypeScript + Vite + Parcel (打包) + Tailwind CSS + shadcn/ui

## 设计与样式指南

非常重要：为了避免所谓的“AI 质感 (AI slop)”，请避免过度使用居中布局、紫色渐变、统一的圆角和 Inter 字体。

## 快速开始

### 第 1 步：初始化项目

运行初始化脚本创建新的 React 项目：
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

这将创建一个完整配置的项目，包含：
- ✅ React + TypeScript (通过 Vite)
- ✅ Tailwind CSS 3.4.1 配合 shadcn/ui 主题系统
- ✅ 路径别名 (`@/`) 已配置
- ✅ 40 多个预装的 shadcn/ui 组件
- ✅ 包含所有 Radix UI 依赖
- ✅ 已配置 Parcel 用于打包
- ✅ 获取最新 Node 兼容性

### 第 2 步：开发您的变体

编辑生成的文件来构建变体。

### 第 3 步：打包为单个 HTML 文件

将 React 应用打包为单个 HTML 变体：
```bash
bash scripts/bundle-artifact.sh
```

这将生成 `bundle.html` - 一个包含所有 JavaScript、CSS 和依赖项的自包含文件。此文件可以直接在对话中作为变体分享。

### 第 4 步：向用户分享

最后，在对话中向用户分享打包好的 HTML 文件。

### 第 5 步：测试/预览变体（可选）

注意：这是一个完全可选的步骤。仅在必要或应要求时执行。

## 参考资料

- **shadcn/ui 组件**: https://ui.shadcn.com/docs/components