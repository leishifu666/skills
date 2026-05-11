---
name: slack-gif-creator
description: 为 Slack 优化而设计的动态 GIF 创建知识和工具。提供限制、验证工具和动画概念。当用户请求为 Slack 创建动态 GIF 时使用，例如“为 Slack 制作一个 X 正在做 Y 的 GIF”。
license: Complete terms in LICENSE.txt
---

# Slack GIF 生成器

一个提供为 Slack 优化的动态 GIF 创建工具和知识的工具包。

## Slack 要求

**尺寸：**
- 表情包 GIF：128x128（推荐）
- 消息 GIF：480x480

**参数：**
- FPS：10-30（越低文件越小）
- 颜色：48-128（越少文件越小）
- 时长：对于表情包 GIF，保持在 3 秒以内

## 核心工作流

```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

# 1. 创建生成器
builder = GIFBuilder(width=128, height=128, fps=10)

# 2. 生成帧
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)

    # 使用 PIL 原语（圆、多边形、线等）绘制动画
    builder.add_frame(frame)

# 3. 优化保存
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## 绘制图形

### 使用用户上传的图像
如果用户上传了图像，请考虑他们是否想要：
- **直接使用**（例如“让这个动起来”、“将其拆分为帧”）
- **作为灵感**（例如“做一个类似这样的”）

使用 PIL 加载并处理图像：
```python
from PIL import Image
uploaded = Image.open('file.png')
```

### 从零绘制
从零绘制图形时，使用 PIL ImageDraw 原语：
- `draw.ellipse`: 圆/椭圆
- `draw.polygon`: 星形、三角形或任何多边形
- `draw.line`: 线条
- `draw.rectangle`: 矩形

**不要使用**：表情符号字体（在不同平台上不可靠）或假设此技能中存在预包装的图形。

### 让图形看起来更美观
图形应该看起来精致且富有创意，而不是基础。以下是方法：
- **使用粗线条**：始终为轮廓和线条设置 `width=2` 或更高。细线（width=1）看起来断断续续且业余。
- **增加视觉深度**：使用渐变背景 (`create_gradient_background`)，堆叠多个形状以增加复杂度。
- **让形状更有趣**：不要只画一个平淡的圆 - 添加高光、光圈或图案。

## 可用实用工具

### GIFBuilder (`core.gif_builder`)
组装帧并为 Slack 进行优化。

### Validators (`core.validators`)
检查 GIF 是否符合 Slack 要求。

### Easing Functions (`core.easing`)
用于平滑运动而非线性运动。

### Frame Helpers (`core.frame_composer`)
用于常用需求的便利函数（创建空白帧、渐变背景、绘制圆形、文本、星型）。

## 动画概念
- **抖动/震动 (Shake/Vibrate)**：使用 `math.sin()` 偏移位置。
- **脉动/心跳 (Pulse/Heartbeat)**：节奏性地缩放对象大小。
- **弹跳 (Bounce)**：利用 `easing='bounce_out'` 实现着陆效果。
- **旋转 (Spin/Rotate)**：绕中心旋转。
- **淡入/淡出 (Fade In/Out)**：调整 alpha 通道逐渐显示或消失。
- **滑动 (Slide)**：从屏幕外进入。
- **缩放 (Zoom)**：缩放并定位实现缩放效果。
- **爆炸/粒子喷发 (Explode/Particle Burst)**：创建向外辐射的粒子。

## 优化策略
仅在被要求缩小文件大小时执行：少帧、少色、小尺寸、删除重复帧、开启表情包模式。

## 核心理念
此技能提供：**知识**（Slack 要求和动画概念）、**工具**（GIFBuilder、验证器、缓动函数）、**灵活性**（使用 PIL 原语创建动画逻辑）。
它不提供：死板的动画模板或预设、表情符号字体渲染、预包装图形库。

发挥创意！结合多个概念并充分发挥 PIL 的能力。
