---
name: penguin-magic-project
title: Penguin Magic 项目
description: 坤坤工坊 (Penguin Magic) 项目全局知识库。 包含项目架构、技术栈、文件结构、核心模块、API 服务、常见修改路径等关键信息。
  当需要修改、调试、扩展 Penguin-Magic 项目时，必须先阅读此文档以快速建立上下文。
---

# 坤坤工坊 Penguin Magic — 项目全局知识库

> **版本**: v1.4.1  
> **项目路径**: `d:\Penguin-Magic_7.0\Penguin_Magic_main`  
> **最后更新**: 2026-03-25 (v5)

---

## 一、项目概述

**坤坤工坊 (Penguin Magic)** 是一款 **AI 图像创意桌面管理工具**，集 AI 生图、桌面式文件管理、创意模板库、画布工作流于一体的 Electron 桌面应用。

### 核心功能
- 🖥️ **桌面式图片管理** — 拖拽、文件夹、叠放，Mac 风格的可视化管理
- 🎨 **AI 图像生成** — 支持 Gemini / nano-banana / Midjourney / RunningHub
- 📚 **创意库系统** — Smart / SmartPlus / BP 三种模板模式
- 🖼️ **画布工作流** — 节点式 AI 图像创作流程 (PebblingCanvas)
- 🎬 **视频生成** — 集成 Sora / Veo 3.1 视频生成服务
- 🔄 **自动更新** — electron-updater 自动版本更新

---

## 二、技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| **前端框架** | React + TypeScript | React 19, TS 5.8 |
| **构建工具** | Vite | 6.2 |
| **样式方案** | Vanilla CSS + 内联样式 | 主题变量 + 输入框微控件规范（无描边 filled） |
| **桌面壳** | Electron | 39.x |
| **后端服务** | Node.js + Express | — |
| **画布引擎** | @xyflow/react (ReactFlow) | 12.x |
| **3D 渲染** | Three.js | 0.182 |
| **AI SDK** | @google/genai | 1.16 |
| **图标库** | lucide-react | 0.562 |
| **打包发布** | electron-builder | 26.x |
| **自动更新** | electron-updater | 6.7 |

### 关键配置
- **Vite 开发端口**: `5176`
- **后端 API 端口**: `8765`
- **API 代理**: Vite 将 `/api`、`/files`、`/input`、`/output` 代理到后端
- **路径别名**: `@/` → 项目根目录

---

## 三、项目结构

```
Penguin-Magic-main/
├── App.tsx                     # ⭐ 主应用组件 (4338行，核心状态管理中心)
├── index.tsx                   # 入口文件
├── index.html                  # HTML 模板
├── index.css                   # ⭐ 全局样式系统 (1053行，主题变量与组件基础样式)
├── types.ts                    # ⭐ 核心类型定义 (355行)
├── vite.config.ts              # Vite 配置
├── tsconfig.json               # TypeScript 配置
├── package.json                # 项目配置 (v1.4.1)
│
├── components/                 # 前端组件 ─────────────────────
│   ├── Desktop.tsx             # ⭐ 桌面管理器 (2549行，拖拽/文件夹/叠放)
│   ├── Desktop/
│   │   └── DesktopItem.tsx     # 桌面项目渲染组件
│   ├── SettingsModal.tsx       # 设置弹窗 (API配置/主题/存储/快捷键/API连接状态检测)
│   ├── NavSidebar.tsx          # 左侧图标导航栏 (56px, 含明暗切换)
│   ├── CreativeLibrary.tsx     # 创意库管理 (智能导入/导出)
│   ├── CreativeIdeasPanel.tsx  # 创意库面板 (右侧面板创意列表)
│   ├── AddCreativeIdeaModal.tsx # 创意模板编辑弹窗
│   ├── ImportCreativeModal.tsx # 创意库导入弹窗
│   ├── GenerateButton.tsx      # 生成按钮
│   ├── GeneratedImageDisplay.tsx # 图片结果展示
│   ├── ImagePreviewModal.tsx   # 图片预览弹窗 (含MJ U1-U4按钮)
│   ├── ImageUploader.tsx       # 图片上传器
│   ├── HistoryDock.tsx         # 历史记录面板 (Dock栏)
│   ├── HistoryStrip.tsx        # 历史记录条
│   ├── HistoryPanel.tsx        # 历史记录面板
│   ├── RunningHubGenerator.tsx # RunningHub 工作流生成
│   ├── RunningHubProgress.tsx  # RunningHub 进度展示
│   ├── WelcomeScreen.tsx       # 欢迎屏幕
│   ├── ApiKeyManager.tsx       # API Key 管理
│   ├── PromptPresets.tsx       # 提示词预设
│   ├── PromptPresetManager.tsx # 提示词预设管理器
│   ├── PromptManagerModal.tsx  # 提示词管理弹窗
│   ├── ErrorLogModal.tsx       # 错误日志弹窗
│   ├── EmptyState.tsx          # 空状态占位组件
│   ├── Accordion.tsx           # 手风琴折叠组件
│   ├── CollapsibleSection.tsx  # 可折叠区块组件
│   ├── Canvas/                 # ReactFlow 画布
│   │   ├── index.tsx           # 画布主组件 (1011行)
│   │   └── nodes/              # 自定义节点 (6种)
│   ├── PebblingCanvas/         # ⭐ 核心画布系统 (4193行)
│   │   ├── index.tsx           # 画布主组件 (含文生图/图生图/视频)
│   │   ├── CanvasNode.tsx      # 画布节点 (116412字节，最大单文件)
│   │   ├── Sidebar.tsx         # 画布侧边栏
│   │   ├── FloatingInput.tsx   # 浮动输入框
│   │   ├── ApiSettings.tsx     # 画布API设置
│   │   ├── MultiAngle3D.tsx    # 3D多角度预览
│   │   ├── Intro.tsx           # 画布介绍
│   │   ├── PresetCreationModal.tsx    # 预设创建
│   │   ├── PresetInstantiationModal.tsx # 预设实例化
│   │   ├── CanvasNameBadge.tsx # 画布名称徽章
│   │   ├── ContextMenu.tsx     # 画布右键菜单
│   │   └── Icons.tsx           # 画布自定义图标
│   └── Multiangle/             # 多角度组件
│
├── services/                   # 服务层 ──────────────────────
│   ├── geminiService.ts        # ⭐ 核心AI服务 (893行)
│   │                           #   文生图/图生图/BP Agent/SmartPlus/提示词优化
│   ├── mjService.ts            # Midjourney 服务 (292行)
│   ├── pebblingGeminiService.ts # 画布用API适配器 (465行)
│   ├── soraService.ts          # Sora 视频生成 (242行)
│   ├── veoService.ts           # Veo 3.1 视频生成 (359行)
│   ├── storyLibrary.ts         # 等待故事动画库 (1217行，纯数据)
│   ├── creativeExtractor.ts    # 创意库提取器
│   ├── promptManager.ts        # 提示词管理服务 (预设CRUD)
│   ├── api/                    # 后端API客户端
│   │   ├── index.ts            # API 基础请求封装 (get/post/put/del)
│   │   ├── ai.ts               # AI 相关API
│   │   ├── canvas.ts           # 画布数据API
│   │   ├── creativeIdeas.ts    # 创意库API
│   │   ├── desktop.ts          # 桌面数据API
│   │   ├── files.ts            # 文件操作API
│   │   ├── history.ts          # 历史记录API
│   │   ├── imageOps.ts         # 图片操作API (裁剪/合并)
│   │   └── runninghub.ts       # RunningHub API
│   ├── db/                     # IndexedDB 本地存储
│   │   ├── index.ts            # 数据库初始化
│   │   ├── creativeIdeasDb.ts  # 创意库存储
│   │   └── historyDb.ts        # 历史记录存储
│   └── export/                 # 导出服务 (ZIP下载等)
│
├── hooks/                      # 自定义 Hooks ─────────────────
│   ├── index.ts                # 导出入口
│   ├── useCreativeIdeas.ts     # 创意库管理
│   ├── useDesktopInteraction.ts # 桌面交互逻辑
│   ├── useDesktopLayout.ts     # 桌面布局计算
│   ├── useDesktopState.ts      # 桌面状态管理
│   └── useGenerationHistory.ts # 历史记录管理
│
├── contexts/                   # React Context ────────────────
│   ├── ThemeContext.tsx         # 主题系统 (dark/light 两种主题)
│   └── RunningHubTaskContext.tsx # RunningHub 任务上下文
│
├── types/                      # 类型定义 ─────────────────────
│   ├── desktopTypes.ts         # 桌面类型
│   └── pebblingTypes.ts        # 画布类型 (CanvasNode/GenerationConfig等)
│
├── constants/                  # 常量 ─────────────────────────
│   └── defaultRunningHubIdeas.ts # 默认 RunningHub 创意
│
├── utils/                      # 工具函数 ─────────────────────
│   └── image.ts                # 图片工具 (URL规范化/缩略图/错误解析)
│
├── backend-nodejs/             # Node.js 后端 ─────────────────
│   ├── package.json            # 后端依赖
│   ├── src/
│   │   ├── server.js           # Express 服务器入口
│   │   ├── config.js           # 配置 (端口/路径/限制)
│   │   ├── routes/             # API 路由
│   │   │   ├── creative.js     # /api/creative-ideas
│   │   │   ├── history.js      # /api/history
│   │   │   ├── files.js        # /api/files
│   │   │   ├── settings.js     # /api/settings
│   │   │   ├── desktop.js      # /api/desktop
│   │   │   ├── imageOps.js     # /api/image-ops
│   │   │   └── canvas.js       # /api/canvas
│   │   └── utils/
│   │       ├── jsonStorage.js  # JSON 文件存储
│   │       ├── fileHandler.js  # 文件操作 (含文件名冲突检测+写入重试)
│   │       ├── security.js     # API Token 验证/限速/Origin 校验
│   │       ├── thumbnail.js    # 缩略图生成
│   │       ├── pathHelper.js   # 路径助手
│   │       └── creativeExtractor.js # 创意提取
│   └── data/                   # 数据文件目录
│
├── electron/                   # Electron 主进程 ──────────────
│   ├── main.cjs                # ⭐ 主进程 (1540行)
│   │                           #   窗口管理/自动更新/启动画面/IPC通信
│   ├── preload.cjs             # 预加载脚本
│   └── create-icon.cjs         # 图标生成工具
│
├── scripts/                    # 构建脚本
├── resources/                  # 资源文件 (图标等)
├── public/                     # 静态资源
├── *.bat                       # Windows 启动脚本 (Install/Start/Stop/Restart/Release)
└── start-mac.command           # macOS 启动脚本
```

---

## 四、核心架构

### 4.1 应用启动流程

```
Electron (main.cjs)
  ├─ 检查/释放端口 8765
  ├─ 启动 Node.js 后端 (server.js)
  ├─ 显示启动画面 (splash)
  ├─ 等待后端就绪
  ├─ 创建主窗口加载前端
  └─ 检查自动更新
```

**开发模式**: `npm run electron:dev`
- concurrently 同时启动后端、Vite dev server、Electron
- wait-on 等待 `http://localhost:5176` 和 `http://localhost:8765` 就绪

**纯前端开发**: `npm run dev`
- 仅启动 Vite，需手动启动后端 `cd backend-nodejs && node src/server.js`

### 4.2 状态管理架构

项目**没有使用**Redux/Zustand等状态管理库，所有状态集中在 `App.tsx` 中通过 `useState` 管理，通过 props 逐级传递。

```
App.tsx (状态中心, 4338行)
  ├── LeftPanel    — 左侧面板 (提示词/参数/模型选择)
  ├── Canvas       — 中间画布区域
  ├── RightPanel   — 右侧面板 (创意库列表)
  ├── Desktop      — 桌面管理器
  ├── HistoryDock  — 底部历史记录
  ├── SettingsModal — 设置弹窗
  └── PebblingCanvas — 画布工作流 (独立页面)
```

### 4.3 三层应用视图

应用有三个主视图，通过 `view` 状态切换：
1. **`editor`** — 编辑器模式（左面板 + 桌面 + 右面板）
2. **`local-library`** — 创意库管理模式
3. **`canvas`** — 画布工作流模式

### 4.4 数据持久化

| 数据 | 存储方式 | 存储位置 |
|------|----------|----------|
| 创意库 | Node.js 后端 JSON | `data/creative_ideas.json` |
| 历史记录 | Node.js 后端 JSON | `data/history.json` |
| 桌面项目 | Node.js 后端 JSON | `data/desktop_items.json` |
| 画布数据 | Node.js 后端 JSON | `data/canvas_list.json` |
| 设置 | Node.js 后端 JSON + localStorage | `data/settings.json` |
| API Key | localStorage | 浏览器本地 |
| 主题 | localStorage (`app_theme`) | 浏览器本地 |
| 图片文件 | 本地文件系统 | `output/`, `input/`, `creative_images/` |

> **注意**: Electron 打包后数据目录为 `%APPDATA%/penguin-magic`（通过 `config.js` 中 `USER_DATA_PATH` 环境变量控制）。支持用户自定义存储路径。

---

## 五、核心模块详解

### 5.1 AI 生图服务 (`geminiService.ts`)

这是最核心的服务文件，处理所有 AI 图像生成逻辑。

| 函数 | 功能 |
|------|------|
| `editImageWithThirdPartyApi()` | 🎯 贞贞API(nano-banana) 文生图/图生图 |
| `chatWithThirdPartyApi()` | 贞贞API 文字处理/图片分析 (Chat Completions) |
| `editImageWithGemini()` | 原生 Gemini API 图片编辑 |
| `processBPTemplate()` | BP 模式模板处理（含Agent依赖图解析、拓扑排序） |
| `generateCreativePromptFromImage()` | Smart/SmartPlus 模式提示词生成 |
| `optimizePrompt()` | 无模板时的提示词优化 |
| `autoClassifyCreative()` | AI 自动分类创意库 |
| `runBPAgentTask()` | BP Agent 单任务执行 |

**API 配置结构** (`ThirdPartyApiConfig`):
```typescript
{
  enabled: boolean;      // 是否启用
  baseUrl: string;       // API 基地址 (如 https://ai.t8star.cn)
  apiKey: string;        // API Key
  model: string;         // 图片模型 (默认 nano-banana-2)
  chatModel?: string;    // 分析模型 (如 gemini-2.5-pro)
  apiName?: string;      // 自定义API名称
}
```

### 5.2 桌面管理器 (`Desktop.tsx`)

Mac 风格的桌面图标管理系统。（2866行）

**核心类型**:
- `DesktopImageItem` — 图片项目（含 loading 状态、MJ 按钮、生图进度条等）
- `DesktopFolderItem` — 文件夹项目（含颜色、子项 ID 列表）
- `DesktopStackItem` — 叠放项目

**关键功能**:
- 网格吸附拖拽（`GRID_SIZE=100`, `ICON_SIZE=80`）
- 框选多选、Ctrl 多选
- 右键菜单（新建文件夹/叠放/删除/导出等）
- 拖入文件夹/叠放
- 键盘快捷键（Ctrl+C/V/X 复制粘贴、Delete 删除）
- 批量下载、ZIP 导出
- 从桌面拖拽图片到上传区
- **生图进度条**: 基于模型预估时间显示圆环进度+百分比 (MJ~45s, nano-banana~60s, Gemini~15s)
- **取消生成**: 支持生成过程中取消 (AbortController)

**拖拽系统架构** (v2, 2026-03-25 重构):
- **零重渲染拖拽**: 拖拽移动全程不触发 React state 更新，仅通过 ref + DOM transform 移动
- **轻量幽灵**: 通过 `ReactDOM.createPortal` 渲染到 `document.body`，`position: fixed` + `top:0; left:0` + `translate3d` 定位
- **幽灵缩略图**: 显示真实图片缩略图 + 选中数量角标，图片 src 在 mousedown 时从 `<img>.currentSrc` 缓存，避免移动中 src 失效
- **热点偏移**: mousedown 时记录点击位置相对图标左上角的偏移 (`dragGhostHotspotRef`)，拖拽时减去该偏移保证视觉跟手
- **拖拽阈值**: `DRAG_THRESHOLD=5`，mousedown 后鼠标移动超过 5px 才激活拖拽，避免破坏双击预览
- **命中检测延迟到 mouseup**: 拖拽移动中不做文件夹/资源区命中检测，全部移到 mouseup 处理，减少每帧计算
- **拖拽时禁用 hover**: 通过 `pointerEvents: 'none'` 禁用桌面项的 hover 效果，防止拖经其他图标时触发重绘
- **关键 ref**: `dragCurrentPosRef`, `draggingIdsRef`, `dragGhostRef`, `dragGhostHotspotRef`, `dragGhostImageUrlRef`

### 5.3 画布工作流 (`PebblingCanvas/`)

节点图谱式 AI 创作工作台，是项目最大的功能模块。

**节点类型** (`NodeType`):
- `text` — 文本节点
- `image` — 图片节点
- `idea` — 创意节点
- `edit` — 编辑节点
- `video` — 视频节点
- `llm` — LLM 文本处理节点
- `resize` — 缩放节点
- `relay` — 中继节点
- `remove-bg` — 去背景节点
- `upscale` — 超分辨率节点

**画布服务** (`pebblingGeminiService.ts`):
- 独立的 API 配置 (`getApiConfig()` / `saveApiConfig()`)
- 支持文本生成、图片生成、图片编辑、LLM 高级处理
- 余额查询

### 5.4 创意库系统

三种模板模式：

| 模式 | 标识 | 特点 |
|------|------|------|
| **Smart** | `isSmart=true` | 基础智能模式，分析图片+模板生成提示词 |
| **SmartPlus** | `isSmartPlus=true` | 高级模式，支持 Product/Person/Scene 组件配置 |
| **BP** (Blueprint) | `isBP=true` | 蓝图模式，支持自定义输入字段和 Agent 依赖链 |
| **RunningHub** | `isRunningHub=true` | 外部工作流对接模式 |
| **Workflow** | `isWorkflow=true` | 画布工作流模式 |

### 5.5 主题系统 (`ThemeContext.tsx`)

仅支持两种主题：
- **`dark`** — 暗色主题
- **`light`** — 亮色主题

通过 CSS 变量 + `theme-{name}` class 实现，变量包括:
`--color-primary`, `--color-bg-primary`, `--color-text-primary`, `--color-border` 等。

**样式原则（当前）**:
- 输入框外层容器允许 1px 细边框；输入框内部小组件（工具按钮/参数选择器/主按钮）默认无描边
- 参数触发器采用低干扰 filled 风格，避免 outlined 表单化视觉
- 交互反馈优先使用背景层次、透明度、阴影与图标动效，而非额外边框

### 5.6 设置弹窗 (`SettingsModal.tsx`)

**API 模式**:
- `local-third-party` — 贞贞API (本地直连)
- `gemini-direct` — 原生 Gemini API

**配置项**:
- 贞贞 API 配置 (BaseURL/Key/模型) + 连接状态检测
- Gemini API Key
- Sora 视频配置
- Veo 视频配置
- 自动保存开关
- 数据存储路径
- 主题切换
- 快捷键参考(生图操作/界面导航/画布操作)
- **存储管理**: 查看 output/input/thumbnails/creative_images 四个目录的文件数和占用空间，支持单目录清理和一键清理

**亮色主题适配**:
- `SettingsModal.tsx` 使用 `getStyles(isDark)` 函数动态计算样式常量
- 内联 `<style>` 中也使用 `${isDark ? ... : ...}` 动态适配
- 修改设置弹窗样式时必须同时提供明/暗两套色值

**API 连接状态检测**:
- 通过 `fetch(baseUrl + '/v1/models')` 检测 API 连通性
- 状态: `idle` / `testing` / `connected` / `failed`
- 左侧导航显示小圆点状态灯，API 卡片内显示状态徽章

---

## 六、样式系统

### 6.1 CSS 设计体系 (`index.css`)

当前样式基线以 **主题变量 + 输入框微控件规范** 为主，不再把“Liquid Glass / ice-blue”作为硬性设计约束。

**当前优先规则**:
- 主题通过 `theme-dark` / `theme-light` + CSS 变量驱动
- 输入框内小组件遵循无描边、低打扰、filled trigger 规范
- 交互反馈优先通过背景层次、透明度、阴影与图标动效表达
- 设置弹窗与创意库以信息清晰和可读性优先，不绑定固定蓝紫主色

**兼容说明**:
- `index.css` 中保留的 `.liquid-*`、`.modern-*` 等类名视为历史兼容样式，可复用但不作为新页面默认设计基准

**设计变量**:
- 颜色由主题变量控制（dark / light），按页面语义使用
- 字体: Inter
- 缓动: `--ease-out-expo`, `--ease-spring`, `--ease-smooth`

### 6.2 日间模式适配

在 `index.css` 中通过大量 `.theme-light` 选择器覆盖暗色变量，实现浅色主题。

**注意**: 部分内联样式未通过主题变量控制，修改主题时需同时检查 CSS 和 JSX 内联样式。

### 6.3 【强制】输入框小组件样式与交互规范

此规则适用于项目内所有“输入框内部小组件”，尤其包括：
- 输入框左下角工具图标按钮
- 输入框底部模型 / 比例 / 分辨率等参数选择器
- 输入框右下角主操作按钮
- 输入框中的图片缩略图与缩略图操作按钮
- 输入框相关的 hover / active / open / drag / loading / disabled 状态

**核心定位**:
- 这套输入框不是传统表单，而是“悬浮式创作工作台”
- 风格关键词：轻、稳、干净、克制、无描边、filled 微控件
- 目标是内容优先、参数附着、主按钮明确、工具弱化

**相关核心文件（修改前优先参考）**:
- `components/shared/inputComposerStyles.ts`
- `components/shared/ChatComposer.tsx`
- `components/BottomInputBar.tsx`
- `components/shared/ChatFileUploader.tsx`
- 第二批统一输入框页面：`components/ImageRendererPage.tsx`、`components/PptGeneratorPage.tsx`、`components/PptPromptPage.tsx`、`components/TemplateConcretePromptPage.tsx`、`components/TemplateCreatorPage.tsx`、`components/WeChatCoverGeneratorPage.tsx`

#### 6.3.1 最高优先级规则

- **外层输入框容器可以有细边框**：输入框整体外壳允许 1px 细边框、柔和阴影、毛玻璃和大圆角。
- **输入框内部小组件默认禁止额外描边**：工具按钮、参数选择器、主按钮、步进器等默认不要独立 border / outline。
- **交互反馈不得依赖描边表达**：状态变化优先通过背景、透明度、阴影、图标、箭头方向和轻动效表达，不要靠“多加一圈边框”。
- **参数按钮不能长得像表单框**：模型 / 比例 / 分辨率触发器必须是 filled trigger，不是 outlined select，不是后台筛选框视觉。
- **比例选择器以桌面版为唯一标杆**：凡是图片生成相关页面的比例选择器，默认遵循 `components/BottomInputBar.tsx` 的桌面版比例选择器语言与交互；包括触发器尺寸、轻底色 filled 形态、左侧比例图标（RatioIcon）、右侧箭头、弹层信息密度、选中态与 hover 节奏。除非用户明确要求，不要私自发明另一套比例选择器样式。
- **模型选择器也以桌面版为唯一标杆**：凡是图片生成相关页面的模型选择器，默认遵循 `components/BottomInputBar.tsx` 的桌面版模型选择器语言与交互；包括触发器尺寸、轻底色 filled 形态、左侧模型图标（`getModelIconPath`）、模型名截断方式、右侧箭头、弹层信息密度、选中态与 hover 节奏。除非用户明确要求，不要私自发明另一套模型选择器样式。
- **分辨率选择器也以桌面版为唯一标杆**：凡是图片生成相关页面的分辨率选择器，默认遵循 `components/BottomInputBar.tsx` 的桌面版分辨率选择器语言与交互；包括触发器尺寸、轻底色 filled 形态、文本密度、右侧箭头、弹层信息密度、选中态与 hover 节奏。除非用户明确要求，不要私自发明另一套分辨率选择器样式。
- **所有图片生成输入框默认带桌面三组件**：除非用户明确要求移除、隐藏或改成别的交互，所有图片生成相关输入框默认应在底部参数区带上这三项：`模型选择器 + 比例选择器 + 分辨率选择器`。不要因为页面变体、插件页或对话场景不同就擅自省略其中任意一项；若某模型客观不支持某项能力，才允许按能力约束禁用、替换或条件隐藏。
- **所有 AI 输出必须可缓存与可恢复**：不论是大语言模型文本输出还是生图结果，都必须支持持久化缓存；页面切换、视图切换、刷新后不得丢失已生成内容、关键上下文与可追溯状态。除非用户明确要求“临时会话不保存”，否则默认保留。
- **所有生图入口必须支持取消生成（中断）**：生成进行中必须提供可见且可点击的“取消/停止”入口，允许用户随时中断当前任务；禁止只能等待超时或结束。
- **所有生图入口必须支持批量生成**：默认提供批量参数与批量执行能力（如 batchCount）；页面变体不得删除此能力，除非用户明确要求或模型能力客观不支持。
- **所有 LLM 输出必须支持 Markdown 渲染**：所有大语言模型文本回复默认按 Markdown 渲染，至少保证代码块、标题、列表、引用、链接等基础结构可读，不允许长期停留为纯文本拼接。
- **所有图片缩略图必须支持点击直接预览**：缩略图作为一等交互入口，默认支持单击直接预览（大图/弹窗/查看器）；页面变体不得移除此能力。
- **前端 UI/UX 统一基准**：新增页面、改样式、做重构时，输入区与参数区设计语言必须以桌面生图输入框（`components/BottomInputBar.tsx`）为基准，保持同一套视觉层级、交互节奏和组件语义；未获用户明确授权，不得新造一套独立设计语言。
- **参数触发器零描边强化**：模型 / 比例 / 分辨率等参数触发器及其常态按钮默认不得出现可见 border / outline / 分割线（含 1px 描边、内描边、伪元素描边）；状态反馈仅通过底色、透明度、阴影、图标与轻动效表达。
- **AI 对话区视觉基调统一**：所有 AI 对话页面默认采用图片渲染器式的一体化、少线框、弱分隔风格；禁止多层卡片套卡片、密集边框、强分割条导致“后台表单感”。
- **文案极简高级化**：界面文案默认短句直给、可操作、少解释；禁止解释性废话、重复提示、教学式长段落；非必要说明移入 tooltip 或帮助入口，不占主界面视觉重心。

#### 6.3.2 输入框容器与文本区规范

- 外层容器统一使用大圆角、半透明背景、柔和大范围阴影，可带 `backdrop-filter: blur(...)`。
- 文本输入区本质上是“写作区”，不是参数填写区：
  - textarea 保持透明背景、无可见边框、无可见外轮廓线
  - 正文字号优先，适合长提示词输入
  - placeholder 降低存在感
  - 滚动条尽量弱化或隐藏
- 容器层允许边框，不代表内部按钮也应该继续套第二层边框语言。

#### 6.3.3 按钮体系分级规范

- **主按钮（Primary CTA）**:
  - 输入框内只能有一个高强调主按钮，固定在右下角主操作位
  - 使用高对比 filled 风格，默认不加描边
  - hover 只做轻微亮度 / 阴影增强，disabled 仅降低透明度
- **工具图标按钮（Tool Icon Buttons）**:
  - 默认透明背景、无描边、低存在感
  - hover 只出现极轻背景浮层或亮度变化
  - loading / active 通过图标切换、轻底色或 spinner 表达
- **参数选择器按钮（Selector Triggers）**:
  - 统一为低对比 filled trigger
  - 默认无描边，可带图标、文本、箭头
  - open 状态通过背景层次变化 + 箭头翻转 + 面板弹出表达
- **步进器按钮（Stepper Buttons）**:
  - 属于低权重微调控件，不允许视觉上抢过主按钮
  - hover 只用轻背景表达，disabled 明显降透明度
- **缩略图操作按钮（Thumbnail Micro Actions）**:
  - 平时隐藏，hover 时出现
  - 可使用小体积危险色，但不能长期污染界面

#### 6.3.4 交互规范

- **Hover**:
  - 工具按钮：极轻背景浮层，不描边，不重阴影，不大幅缩放
  - 参数按钮：只轻微提亮，不跳动，不描边，不突然增强边界感
  - 缩略图：允许轻微放大、轻微旋转、柔和光晕、中央查看提示层和删除按钮浮现
- **Active / Selected**:
  - 主按钮：通过填充色和轻压感表达，不额外加描边
  - 参数按钮：通过内容值、背景微差、展开态表达，不通过外框加粗表达选中
  - 缩略图：允许 ring / 阴影表达当前激活素材；这是素材选中态，不是按钮描边语言
- **Open / Close**:
  - 模型 / 比例 / 分辨率等下拉触发器，靠背景层次变化、箭头旋转和弹层出现表达打开态
  - 禁止通过加一圈 border 来提示 open
- **Drag / Drop**:
  - 拖入输入框时出现清晰但克制的覆盖提示
  - 缩略图拖拽排序时，拖拽源和目标态必须明显区分
  - 拖拽目标可以用 outline / ring，但仅限拖拽态，不得外溢到日常按钮样式
- **Loading / Disabled**:
  - loading 优先通过 spinner、图标切换、轻底色表达
  - disabled 统一用透明度和 cursor 表达，不要额外加灰边框
- **键盘与快捷行为**:
  - 输入框相关组件应支持 Enter 触发主操作、Shift+Enter 换行、Esc 关闭放大层 / 弹层
  - 粘贴图片、拖拽图片进入素材队列属于标准工作流，不应丢失

#### 6.3.5 缩略图规范

- 缩略图属于“素材卡片”，允许比参数按钮更灵动。
- 默认状态保持安静；hover 时可出现轻微放大、旋转、柔和蓝色阴影、中央预览提示和删除按钮。
- active 状态允许使用 ring / 阴影强调当前素材。
- drag 状态允许：
  - 拖拽源透明度降低
  - 放置目标显示高亮提示
  - 放手后完成重排
- 这套交互可参考 `components/BottomInputBar.tsx` 中的 `InlineThumbnail` 实现。

#### 6.3.6 明确禁忌

以下做法在本项目输入框小组件中默认禁止：
- 给工具按钮、参数按钮、主按钮统一套 1px 外描边
- 把模型 / 比例 / 分辨率触发器做成 outlined select 或后台筛选框视觉
- hover 时突然出现边框、重阴影或大幅缩放
- 让工具按钮、参数按钮与主按钮处于同级高亮
- 在同一输入框内混用多套圆角、阴影、按钮尺寸或描边语言

#### 6.3.7 一句话总纲

**输入框内部所有小组件统一采用无描边、低打扰、filled 悬浮控件风格；交互反馈通过背景、透明度、阴影、图标和轻动效表达，而不是通过额外 border 表达。**

### 6.4 【强制】展开编辑弹窗统一规范（以图片渲染器为唯一标杆）

> 适用范围：所有输入框的“展开编辑”页面/弹窗。

- **唯一基准**：统一对齐“图片渲染器”的 `编辑输入内容` 弹窗样式与结构；未获用户明确授权，不得新造一套展开弹窗视觉语言。
- **弹窗层级与遮罩**：`fixed inset-0` 全屏遮罩，居中展示，遮罩使用中等强度黑色半透明（约 `rgba(0,0,0,0.5)`）。
- **容器规格**：中等宽度弹窗（基准宽约 `640px`，`max-h` 约 `80vh`），`rounded-2xl`，1px 细边框，纵向 `flex` 布局。
- **头部结构**：顶部 `border-bottom`，左侧标题固定为 **“编辑输入内容”**，右侧为低干扰关闭图标按钮（X）。
- **正文编辑区**：主体为大面积 textarea，透明背景、无额外内描边，支持滚动；文字可读性优先（中小字号，舒适行高）。
- **底部操作区**：底部 `border-top`，按钮右对齐，固定为“双按钮结构”：
  - 次按钮：`关闭`（低干扰风格）
  - 主按钮：`发送`（高对比 filled 主按钮）
- **交互规范**：必须支持 `Esc` 关闭、右上角 X 关闭；发送动作完成后关闭弹窗；禁用态统一使用 `opacity + cursor`，避免额外灰色描边。

### 6.5 输入框按钮完整性检查（新增基线）

- **基础标配**：所有输入框默认应具备 **上传/附件按钮** 与 **展开按钮**。
- **提示词编辑场景**：默认应具备 **翻译按钮** 与 **优化按钮**（用于快速语言处理与提示词优化）。
- **非提示词编辑场景**：若页面是纯执行型输入（例如只上传并直接执行），可按页面定位不展示翻译/优化，但需经用户明确确认。

---

## 七、常见修改路径速查

### 7.1 修改/新增 AI 模型

1. **前端下拉选项**: `App.tsx` → 搜索模型名称或 `model` 相关变量
2. **API 调用逻辑**: `services/geminiService.ts` → `editImageWithThirdPartyApi()`
3. **宽高比映射**: `services/geminiService.ts` → `convertAspectRatio()`
4. **类型定义**: `types.ts` → `AspectRatioType`, `NanoBananaRequest`

### 7.2 修改设置弹窗

- **文件**: `components/SettingsModal.tsx`
- **样式常量**: 文件顶部 `getStyles(isDark)` 函数 (返回明/暗两套变量)
- **API 模式**: `ApiMode` 类型定义
- **Tab 导航**: `api` / `preferences` / `shortcuts` / `about`
- **API 连接检测**: `testApiConnection()` 函数, `apiConnStatus` 状态

### 7.2.1 修改侧边图标导航栏

- **文件**: `components/NavSidebar.tsx`
- **宽度**: 固定 56px
- **含明暗模式切换按钮**
- ❗ 影响 App.tsx 中拖拽手柄的 `left` 定位计算 (+ 56px 偏移)

### 7.3 修改桌面功能

- **主组件**: `components/Desktop.tsx`
- **桌面项渲染**: `components/Desktop/DesktopItem.tsx`
- **交互逻辑 Hook**: `hooks/useDesktopInteraction.ts`
- **布局计算 Hook**: `hooks/useDesktopLayout.ts`
- **状态管理 Hook**: `hooks/useDesktopState.ts`
- **类型定义**: `types.ts` → `DesktopItem` 相关接口

### 7.4 修改画布功能

- **画布主组件**: `components/PebblingCanvas/index.tsx`
- **画布节点**: `components/PebblingCanvas/CanvasNode.tsx` ⚠️ 超大文件
- **画布侧边栏**: `components/PebblingCanvas/Sidebar.tsx`
- **画布 API 服务**: `services/pebblingGeminiService.ts`
- **画布类型**: `types/pebblingTypes.ts`
- **后端画布路由**: `backend-nodejs/src/routes/canvas.js`

### 7.5 修改创意库

- **创意库组件**: `components/CreativeLibrary.tsx`
- **创意编辑弹窗**: `components/AddCreativeIdeaModal.tsx`
- **创意库类型**: `types.ts` → `CreativeIdea`
- **前端API**: `services/api/creativeIdeas.ts`
- **后端路由**: `backend-nodejs/src/routes/creative.js`

### 7.6 修改历史记录

- **Dock 面板**: `components/HistoryDock.tsx`
- **历史条**: `components/HistoryStrip.tsx`
- **历史记录类型**: `types.ts` → `GenerationHistory`
- **App 中历史操作**: `App.tsx` → `handleHistorySelect`, `saveToHistory`

### 7.7 修改 Electron 行为

- **主进程**: `electron/main.cjs`
- **IPC 通信**: `electron/preload.cjs` + `main.cjs` 中的 `ipcMain`
- **自动更新**: `main.cjs` → `autoUpdater` 相关代码
- **版本更新弹窗**: `main.cjs` → `RELEASE_NOTES` 对象

### 7.8 修改后端 API

- **路由文件**: `backend-nodejs/src/routes/`
- **服务器配置**: `backend-nodejs/src/config.js`
- **存储工具**: `backend-nodejs/src/utils/jsonStorage.js`
- **文件操作**: `backend-nodejs/src/utils/fileHandler.js`

---

## 八、关键注意事项

### 🔴 8.0 【强制】修改前端代码后必须重新构建

> **这是最重要的一条规则！** 用户使用的是通过 `Start.bat` 启动的**生产构建版本**（`dist/` 目录），而不是 Vite 开发模式。
> 
> 如果不执行构建，用户看到的仍然是旧代码，会误以为修改没有完成。

**📋 构建固定指令（每次修改前端源码后必须执行）：**

```bash
# 步骤 1: 在项目根目录执行构建
cd /d d:\Penguin-Magic_7.0\Penguin_Magic_main
npm run build

# 步骤 2: 提醒用户重启应用
# 告知雷嵘：关闭当前应用窗口，重新双击 Start.bat 启动
```

**触发条件** — 修改了以下任意类型的文件后必须执行构建：
- `.tsx` 文件（React 组件）
- `.ts` 文件（TypeScript 模块/服务/类型/工具）
- `.css` 文件（样式）
- `index.html`（HTML 模板）
- `vite.config.ts`（构建配置）

**不需要构建的修改**：
- `backend-nodejs/` 下的后端代码 — 只需重启后端即可
- `electron/` 下的主进程代码 — 需重启 Electron
- `data/` 下的数据文件 — 无需任何操作
- `*.bat` / `*.command` 脚本 — 无需任何操作

### 8.0.1 【强制】代码编写规范

- **禁止制造屎山代码**: 代码必须整洁、可读、可维护。
- **禁止随意修改逻辑**: 未经用户确认不得更改现有业务逻辑。
- **长代码拆分**: 新建组件应控制在 500 行以内，复杂逻辑抽取到 Hook/工具函数，常量抽离到文件顶部���独立文件。
- **不能影响正常使用**: 任何重构必须保证功能完全正常，禁止引入回归 bug。
- **注释中文**: 代码注释必须使用中文，关键操作必须记录日志。

### 8.1 ⚠️ 巨型文件警告

以下文件体积极大，修改时应精准定位，避免加载全文：

| 文件 | 行数 | 说明 |
|------|------|------|
| `App.tsx` | 4338 | 主应用，所有状态在此 |
| `PebblingCanvas/index.tsx` | 4193 | 画布主组件 |
| `PebblingCanvas/CanvasNode.tsx` | ~3000+ | 画布节点，最大单文件 |
| `Desktop.tsx` | 2866 | 桌面管理器（含拖拽系统v2重构） |
| `storyLibrary.ts` | 1217 | 纯故事数据 |
| `index.css` | 1053 | 全局样式 |
| `electron/main.cjs` | 1540 | Electron 主进程 |

### 8.2 ⚠️ API 服务分离

项目有**两套独立的 API 配置**：
1. **主应用 API** (geminiService.ts) — 通过 `App.tsx` 的 `thirdPartyConfig` state 管理
2. **画布 API** (pebblingGeminiService.ts) — 通过 localStorage (`pebbling_api_config`) 独立管理

修改 API 相关逻辑时需注意是哪套配置。

### 8.3 ⚠️ 端口占用

- 前端 Vite: `5176`
- 后端 Express: `8765`
- Electron main.cjs 会在启动时自动检查并释放 `8765` 端口
- **server.js 端口冲突自动处理**: 启动时检测到 EADDRINUSE 会自动杀掉占用端口的旧进程并重试（最多2次）

### 8.4 ⚠️ 样式混用

项目同时使用了：
- 自定义 CSS 类 (`index.css` 中的 `.liquid-*`, `.modern-*`)
- Tailwind-like 内联类名（如 `bg-white/5`, `text-gray-300`）
- React 内联 `style` 对象

修改样式时需注意三者的优先级和覆盖关系。

### 8.5 ⚠️ 数据存储双轨制

开发模式 vs 打包模式的数据存储路径不同：
- **开发**: 项目根目录下的 `data/`, `output/`, `input/` 等
- **打包**: `%APPDATA%/penguin-magic/` 或用户自定义路径

### 8.7 Midjourney 集成要点

MJ 使用贞贞 API 的中转接口：
- 生成后返回 `mjTaskId` 和 `mjButtons` (U1-U4 放大按钮)
- 这些数据需要在保存到桌面、历史记录时一并保存
- 预览图片时需要传递这些数据以显示操作按钮

---

## 九、开发命令

```bash
# 纯前端开发
npm run dev

# Electron 联调开发 (推荐)
npm run electron:dev

# 构建前端
npm run build

# 打包 Windows 安装包
npm run package

# 打包并上传
npm run release
```

---

## 十、版本日志关键位置

- **前端版本号**: `package.json` → `version` 字段
- **Electron 更新日志**: `electron/main.cjs` → `RELEASE_NOTES` 对象
- **CHANGELOG**: `CHANGELOG.md`

---

## 十一、常见错误与避坑指南

> 此部分持续更新，记录开发中遇到的典型错误及解决方案。

### 11.1 构建相关

| 错误 | 原因 | 解决 |
|------|------|------|
| 修改代码后页面无变化 | 未执行 `npm run build` | 前端源码修改后必须 `npm run build` 再重启 |
| Vite 构建报 TS 类型错误 | 新增 props/类型未同步 | 检查 `types.ts` 和组件 props 接口定义 |
| `__APP_VERSION__` 未定义 | Vite define 配置缺失 | 检查 `vite.config.ts` 中 `define` 字段 |

### 11.2 运行时常见问题

| 错误 | 原因 | 解决 |
|------|------|------|
| 端口 8765 被占用 | 上次未正常关闭 | server.js 已自动处理，直接重新启动即可，或执行 `Stop.bat` |
| API 请求 404 | 后端未启动或代理未配置 | 检查后端是否启动，检查 Vite proxy |
| localStorage 数据丢失 | Electron 切换了 userData 路径 | 检查 `electron/main.cjs` 中 userData 配置 |
| 图片加载失败显示空白 | 路径包含中文或特殊字符 | 使用 `encodeURIComponent` 处理路径 |

### 11.3 样式相关

| 错误 | 原因 | 解决 |
|------|------|------|
| 暗色主题下文字不可见 | 内联样式硬编码了颜色 | 使用 CSS 变量 `var(--color-text-*)` |
| 亮色主题样式异常 | `.theme-light` 覆盖不完整 | 同时检查 `index.css` 和组件内联样式 |
| 毛玻璃效果不生效 | `backdrop-filter` 浏览器兼容性 | 添加 `-webkit-backdrop-filter` 前缀 |

### 11.4 Electron 打包

| 错误 | 原因 | 解决 |
|------|------|------|
| 打包后后端不工作 | `node_modules` 未正确打包 | 检查 `extraResources` 配置 |
| 自动更新失败 | `publish.url` 配置错误 | 检查 `package.json` 中 build.publish |
| 图标不显示 | `resources/icon.ico` 缺失或格式错误 | 重新生成 ico 文件 |

