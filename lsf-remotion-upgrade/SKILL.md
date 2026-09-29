---
name: lsf-remotion-upgrade
description: "LSF Remotion 升级：检查并统一升级 Remotion、相关依赖和本地技能。"
version: 4.0.529
---

# LSF Remotion 升级

1. 检查项目清单文件和锁文件，确认包管理器及工作区结构。保留无关改动。
2. 确认项目是否本地安装了 @remotion/cli。如果已安装，运行：

```bash
   npx remotion upgrade
   ```

此命令也会更新项目内的 Remotion skills。运行后跳过下面的手动升级步骤。

3. 如果项目没有安装 @remotion/cli，请手动升级：
   - 使用 npm view remotion version 获取最新稳定版。
   - 检查项目中所有已安装的 remotion 和 @remotion/* 依赖，并将它们全部升级到同一版本。保留原有依赖分区，以及项目的工作区或 catalog 约定。
   - 使用 npm view @remotion/studio@<version> dependencies --json 查询目标 Remotion 版本的 @remotion/studio 依赖。将 zod、mediabunny 和 @huggingface/transformers 等辅助包对齐到其列出的版本。项目如安装了 @mediabunny/*，使用该版本对应的 mediabunny 版本。
   - 使用项目的包管理器更新锁文件。
4. 如果项目没有安装 @remotion/cli，再更新已安装的 Remotion skills：

```bash
   npx skills update lsf-remotion-best-practices remotion-captions lsf-remotion-create lsf-remotion-docs lsf-remotion-interactivity lsf-remotion-maps lsf-remotion-markup remotion-multimedia lsf-remotion-render lsf-remotion-saas remotion-studio lsf-remotion-upgrade --yes
   ```

5. 检查项目清单和锁文件的差异。确认所有 Remotion 包使用同一版本，辅助包也使用推荐版本。如果项目安装了 CLI，再运行 npx remotion versions 进行额外检查。

[Remotion 发布记录](https://github.com/remotion-dev/remotion/releases)包含变更日志，可用于总结升级内容。
