# LSF oil-cover

**先选风格，再用真实视频或截图制作封面。** 一套 Skill，两种方向：AI 教程与设计分享；默认输出 **3:4、4:3、16:9** 三张。

> **这是二次开发项目。** 基于 [@oil-oil（oil 欧呦）](https://github.com/oil-oil) 的 [oil-cover](https://github.com/oil-oil/oil-cover)，感谢原作者提供视频选帧、真实界面证据、标题锁定和多画幅生成流程。二次开发与设计分享风格：[LSF 设计日常 / @leishifu666](https://github.com/leishifu666)。本项目保留原作者署名与 MIT 许可，不代表原作者背书。

## 两种风格，制作前由你选择

| | AI 教程 · 原版风格 | 设计分享 · LSF 扩展 |
| --- | --- | --- |
| 适合 | 工具教学、操作演示、AI 工作流 | 作品集、网页设计、视觉作品与创作分享 |
| 视觉 | 清爽产品视觉、真实界面、网格与轻透视 | 标题主次对比、单色渐变、正面作品展示 |
| 个人标识 | 无人物，或原版可选右下角头像 | 左上角圆形头像、作者名、底部账号和年份 |
| Logo | 产品识别与界面证据 | 截图右上角的 Logo 贴纸 |
| 执行方式 | Agent 自主模式 / 原版 API 脚本 | Agent 自主模式，需支持参考图的内置图像工具 |

每组新封面先询问风格；你已经说了“做设计分享封面”，就不会重复问。同一组封面的修改沿用已选风格。

### AI 教程风格效果

以下示例来自上游 [oil-cover](https://github.com/oil-oil/oil-cover)，作者 [@oil-oil](https://github.com/oil-oil)。

<p align="center"><img src="docs/showcase/gallery.png" alt="原作者 oil-oil 的 AI 教程封面示例" width="880"></p>
<p align="center"><img src="docs/showcase/gallery-4x3.png" alt="原版 AI 教程 4:3 横版示例" width="700"></p>

### 设计分享风格效果

以下是同一条个人网站视频生成的三种构图，展示标题里的字体、字重和颜色对比，以及圆形头像、Logo 贴纸、主题注释和账号署名。

<p align="center"><img src="docs/showcase/design-share-3x4.png" alt="设计分享 3:4 竖版：我用 Codex 从零做了个个人网站" width="390"></p>
<p align="center"><img src="docs/showcase/design-share-4x3.png" alt="设计分享 4:3 横版" width="760"></p>
<p align="center"><img src="docs/showcase/design-share-16x9.png" alt="设计分享近似 16:9 宽版" width="880"></p>

示例为内置图像工具的实际输出：1086×1448、1448×1086、1672×941（最后一张接近 16:9，未本地裁切）。效果图中的账号、头像与网站属于案例作者，安装后不会成为你的默认资料。

## 安装与调用

```bash
npx skills add leishifu666/lsf-oil-cover
```

或把本仓库放入宿主支持的 Skills 目录，确保能读取根目录的 `SKILL.md`。在支持 `$skill-name` 的宿主中调用：

```text
用 $lsf-oil-cover 给这个视频做封面。
```

也可以直接指定：

```text
用 $lsf-oil-cover 做设计分享风格，发小红书。
标题：我用 Codex 从零做了个个人网站。
生成 3:4、4:3、16:9 三版。
```

## 第一次使用设计分享：保存你的资料

Agent 会先问发布平台，再收集该平台的**账号名称和头像图片**。你可以分别提供小红书、公众号、抖音、B 站等平台资料，也可以明确让几个平台共用一套。

- 同个平台已保存完整资料时，直接复用，不再反复问名字或头像。
- 头像原图复制到本机资料目录，聊天临时图片清理后仍可使用。
- 平台之间独立保存，更换公众号头像不会影响小红书。
- 默认底部署名为 `@账号名称`；公众号等可以设置不带 @ 的自定义署名。
- 资料只存本机，不登录社交平台，不发布内容，不写进开源仓库。

默认位置：`~/.lsf-oil-cover/profiles.json` 与 `~/.lsf-oil-cover/avatars/`。可通过 `LSF_OIL_COVER_HOME` 指定其他本机目录；不要放进 Skill 或 Git 仓库。

需要手动管理时，在仓库根目录运行：

```bash
python -m pip install -r requirements.txt
python scripts/creator_profiles.py set --platform xiaohongshu --name "你的账号名称" --avatar "头像.png"
python scripts/creator_profiles.py set --platform wechat --name "你的公众号" --avatar "公众号头像.png" --signature "你的公众号"
python scripts/creator_profiles.py set --platform douyin --name "你的抖音名称" --avatar "抖音头像.png"
python scripts/creator_profiles.py list
python scripts/creator_profiles.py show --platform xiaohongshu
```

名字与头像会被读取并用于本次生成。详细更新方法、中文平台别名与数据格式见 [作者资料说明](references/creator-profiles.md)。

## 设计分享风格的设计规则

- **标题有重点**：先区分结果、工具、说明词；用字体、粗细、字号或颜色建立主次，不把每个词都做成同样的超粗黑字。
- **单色渐变**：一个纯色逐渐过渡到白色；深色截图可过渡到黑色。中间不混入第二种彩色，也不加网格或光斑。
- **作者与作品分开**：左上角圆形头像＋作者名，截图右上角为作品或产品 Logo 贴纸。
- **装饰与主题相关**：标题下的说明小字、右侧括号注释、页脚上方的装饰条码与分类标签按内容和位置组织。
- **署名可复用**：底部左侧是平台账号，右侧为当年的年份。

完整规则见 [设计分享预设](references/lsf-editorial-cover.md)。

## 执行方式与依赖

**Agent 自主模式**：使用宿主视觉与支持参考图的内置图像生成工具；在 Codex 中使用 `image_gen`，不需要另外填写 API Key。视频抽帧需要可用的 ffmpeg；头像归档与图片验证需要 Python 3.10+ 和 Pillow。没有图像工具时，Skill 本身不能独立生图。

**原版脚本模式（AI 教程）**：保留上游的 Python 生成脚本与凭据页面，默认通过 ZenMux 调用视觉和图像服务。需要相应服务的 Key，可能产生服务费用。详见 [脚本用法](references/script-mode.md) 与 [API Key 配置](references/api-key-setup.md)。现有脚本尚不支持设计分享的圆形头像、多平台署名版式；不会把保存账号误称为已接通 API 生成。

执行模式偏好沿用 `~/.oil-cover/config.json`，与新的作者资料分开保存。设计分享不会静默改写已有脚本模式偏好。

默认三画幅是通用交付组合，不代表每个平台的所有发布位置规格。公众号头条等有特定比例时，直接告诉 Agent 所需尺寸；内置工具输出近似比例时应如实说明。

## 本地验证

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -p "test_*.py"
```

测试不调用生图服务，覆盖原版标题与 Logo 规则，以及多平台资料隔离、更新保留、临时头像归档、损坏配置保护和路径边界。上游凭据组件保留独立测试与 CI。

## 致谢与许可

原始项目：[oil-oil/oil-cover](https://github.com/oil-oil/oil-cover)，原作者 **[@oil-oil](https://github.com/oil-oil)**。

上游基线：[f6bffe7](https://github.com/oil-oil/oil-cover/commit/f6bffe73dbe17b03c10c1b24b4aab3540bac7345)。二次开发增加风格选择、设计分享规范与离线多平台作者资料；原版核心脚本保持兼容。

代码采用 [MIT](LICENSE)，保留原作者版权声明。产品 Logo 属于各自权利人；示例中的头像、商标和网站作品不作为独立素材重新授权。来源和范围见 [NOTICE](NOTICE)。
