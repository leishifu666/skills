---
name: lsf-remotion-best-practices
description: LSF Remotion 总路由：根据视频创作、合成、渲染、文档、地图、交互和升级任务选择对应技能。
version: 4.0.534
github_url: https://github.com/remotion-dev/skills
github_hash: 32b241b97f4e0e4ab61fe9a41b05e6e64503f8c5
---

# LSF Remotion 最佳实践

Remotion 任务类型尚不明确，或任务横跨多个领域时，从这里开始，再加载最相关的专用技能。

- 创建 Remotion 项目、视频或合成：加载 `lsf-remotion-create`。
- 编写合成结构、时间轴、动画、媒体、布局或排版：加载 `lsf-remotion-markup`。
- 渲染已有合成：加载 `lsf-remotion-render`。
- 查找当前 API 和官方文档：加载 `lsf-remotion-docs`。
- 制作地图和地理动画：加载 `lsf-remotion-maps`。
- 调整 Studio 交互：加载 `lsf-remotion-interactivity`。
- 构建基于 Remotion 的 SaaS 应用或部署架构：加载 `lsf-remotion-saas`。
- 升级 Remotion 包和已安装的 Remotion skills：加载 `lsf-remotion-upgrade`。

这些 Agent Skills 提供操作指导，不会替具体项目安装 Remotion 运行库。只有在某个项目确实需要时，才把 Remotion 包添加到该项目中。

## 当前版本接口

实现前按本次问题读取 [4.0.534 官方接口与示例](references/upstream-current.md)。其中的媒体时间、可编辑节点和合成注册约定更新了旧版实现说明；本地用户改动、授权和交付要求继续适用。
