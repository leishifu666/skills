---
name: lsf-remotion-create
description: LSF Remotion 视频创建：为新项目或现有项目搭建视频合成；用户要求制作 Remotion 视频时启用。
version: 4.0.534
github_url: https://github.com/remotion-dev/skills
github_hash: 32b241b97f4e0e4ab61fe9a41b05e6e64503f8c5
---

# LSF Remotion 视频创建

本技能说明如何创建 Remotion 项目和视频合成。若当前任务不是创建视频或合成，请改用 `lsf-remotion-best-practices`。

## 搭建项目

如果项目已经存在，跳过项目初始化。
确认 Node.js 和 Git 已安装，并确认当前目录适合创建新项目。

选择项目位置前，检查当前目录，包括隐藏文件。

### 空目录

如果目录为空，或只包含可丢弃的操作系统元数据（例如 `.DS_Store`），可直接在当前目录创建项目。

先只删除这些可丢弃的元数据文件，因为 `create-video` 不接受非空目录。不要把所有隐藏文件都当成可丢弃内容；例如 `.env` 和 `.git` 有实际用途。

在当前目录搭建：

```bash
npx create-video@latest --yes --blank --no-tailwind .
npm i
```

### 非空目录

如果当前目录已有有效内容，但还不是 Remotion 项目，就在新的子目录中搭建。
将 `my-video` 替换成合适的项目名称。

```bash
npx create-video@latest --yes --blank --no-tailwind my-video
cd my-video
npm i
```

## 先打开预览

项目可以运行后，在修改合成前启动 Studio，打开命令实际返回的地址并验证预览，制作时保持预览可见。注册 Composition 或 Still 前核对 compositions.md；每个需要独立编辑的媒体片段使用独立 JSX 节点，带同步字幕的片段把时间属性放在共享分组上。

## 设计视频

保留项目脚手架并添加 React 标记。按照 Remotion React 标记最佳实践编写；视频优先的布局和字号规则见[视频版式规则](video-layout.md)。

## 多场景视频

如果视频由多个连续场景组成，请参考“多场景视频”的指导。

## 交互最佳实践

按 Remotion 交互最佳实践组织 React 标记，让用户可以在 Studio 中编辑内容，并把编辑结果写回代码。

## Tailwind CSS

如果用户要求使用 Tailwind，请阅读 [tailwind.md](tailwind.md)，了解在 Remotion 项目中使用 Tailwind CSS 的方法。

## 打开预览

完成合成后启动预览服务器：

```bash
npx remotion studio --no-open
```

命令会启动一个持续运行的进程，并输出预览服务器 URL。
如果服务器已经启动，命令会输出现有 URL。
如果有可用的内置浏览器，在浏览器中打开该 URL。
可以通过访问 `/[composition-id]` 直接打开某个合成，例如 `http://localhost:3000/MapAnimation`。

## 渲染视频

用户要求导出、MP4 或完整制作流程包含成片交付时执行渲染。只要求预览时先交付 Studio。

```
npx remotion render
```

更多选项见“渲染”技能。

## 后续操作

视频创建流程到此完成。
处理后续请求时，使用 `lsf-remotion-best-practices`。

## 当前版本接口

实现前按本次问题读取 [4.0.534 官方接口与示例](references/upstream-current.md)。其中的媒体时间、可编辑节点和合成注册约定更新了旧版实现说明；本地用户改动、授权和交付要求继续适用。
