---
name: lsf-lemo-opuscar
description: "LSF Lemo-Opuscar 短片制作：按 39 种代码生成影片风格创作短片、动画或宣传片；用户指定风格或询问可用风格时启用。"
---

# LSF Lemo-Opuscar

风格库、导演与制作指南以及工具都在 Lemo-Opuscar 本地资料库中。此技能会定位该资料库，并引导你按其中的流程制作。

## 1. 准备风格库

从此技能目录运行初始化脚本：

```sh
sh "<skill base directory>/scripts/setup.sh"
```

首次运行时会把指南、core 工具和全部 STYLE.md（约 60 MB）下载到指定目录。之后会尝试更新。若当前工作目录已经位于该仓库克隆版中，就直接使用该克隆版；LEMO_OPUSCAR_HOME 环境变量可以指定位置。脚本最后一行会输出 LIB=<path>。

在真正制作视频且确实需要渲染时，再运行依赖初始化命令：

运行技能目录下的 scripts/setup.sh deps。

该步骤会安装 Node.js 和 Python 包以及渲染器使用的无头浏览器，首次运行需要几分钟。若缺少系统工具（Node 20+、ffmpeg、Python 3.11+），在首次需求确认时告诉用户；不要自行安装系统软件。

## 2. 遵循资料库说明

阅读 $LIB/AGENTS.md 并按其中要求操作。它包含完整流程：

- 在 styles/README.md 中选择风格。
- 阅读 DIRECTOR.md、TECHNIQUE.md 和所选风格的 STYLE.md。
- 开始制作前集中询问一次必要信息。
- 按用户要求提供可选分镜。

## 使用此技能时的项目位置

- 在用户当前项目目录下创建 <name>/，名称使用小写字母、数字和连字符（例如 orange-cat）；路径中的 # 或 % 会导致 ffmpeg 出错。如果名称已被其他内容占用，换一个名称。代码、音频、静帧、build.sh、最终 MP4、SRT 和海报都放在该目录。资料库文档中提到 films/<name>/ 时，在此技能模式下指这个目录。
- 从 $LIB 运行工具，并传入项目绝对路径。例如，使用 Node.js 运行 core/render/still.mjs 生成静帧，或用 $LIB/.venv/bin/python 运行 core/tts/tts.py 并传入项目的 lines.json 与 voices 路径。

  渲染服务器会从 /@film/ 提供项目文件，从 / 提供资料库文件。
- 访问资料库文件时：
  - 在页面中使用绝对 URL，例如 /core/lib.js、/node_modules/three/...、/styles/<slug>/demo/...。
  - 在 Python、Node.js 脚本和 build.sh 中使用 $LIB/... 路径。不要使用 ../..，因为项目目录不在资料库内部。
  - 在 build.sh 开头设置 LIB=<path>。
- 示例源代码默认不会下载。当 STYLE.md 第 9 节指向你需要查看或引用的文件时，运行技能目录下的 scripts/setup.sh，并传入 demo 和风格 slug 参数。示例是用于参考的实现：学习并复用技术方法，不要重做示例或照搬示例故事。
- 交付时告诉用户项目目录和成片路径。

## 当前 Codex 工作区约定

setup.sh 默认路径不能用于本环境。先检查当前工作区的 work/lemo-opuscar 是否已包含该仓库；若有，就把 LEMO_OPUSCAR_HOME 指向它。否则把该变量设为当前工作区内的目录，例如 work/lemo-opuscar-library。不要将资料库写入用户主目录。

技能安装阶段不要运行 setup.sh deps。只有用户任务确实需要渲染成片时才安装项目依赖；不要通过此脚本安装系统软件。
