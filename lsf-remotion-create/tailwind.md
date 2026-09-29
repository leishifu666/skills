---
name: lsf-remotion-tailwind
description: "LSF Remotion Tailwind CSS 用法：在 Remotion 项目中使用 Tailwind CSS 编写样式。"
metadata:
---

# LSF Remotion Tailwind CSS

如果项目已安装 Tailwind CSS，可以在 Remotion 项目中使用它。

不要使用 transition-* 或 animate-* 类制作动画；始终通过 useCurrentFrame() hook 驱动动画。

先在 Remotion 项目中安装并启用 Tailwind。具体步骤见：https://www.remotion.dev/docs/tailwind
