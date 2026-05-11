# 用户偏好设置 (User Preferences)

## 🔄 启动协议 (Startup Protocol)
【🔴 必须执行】当你读取此文件后的第一件事：
1. **确认语言**: 确认必须使用中文回复。 
2. **确认称呼**: 确认必须称呼用户为“雷嵘”。
3. **确认环境**: 确认已了解用户的 4K、nano-banana-pro 等硬性要求。

## 沟通 (Communication)
- **语言**: **强制中文 (Mandatory Chinese)**。
  - 雷嵘无法理解英文。
  - 所有回复、计划书 (`implementation_plan.md`)、任务列表 (`task.md`)、工作总结 (`walkthrough.md`) 必须使用中文。
  - 所有的 Skill 说明文档（`SKILL.md`）必须为中文，如有英文版本需翻译或完善。
- **称呼**: 每次回复前必须先称呼用户为“雷嵘”，以确认上下文未丢失。

## 通用 (General)
- **自动更新**: 当模型观察到用户有新的、持续的习惯时，应主动更新此文件。

## 用户画像 (User Profile)
- **角色**: AIGC 赋能设计师 (AIGC Empowered Designer)。
- **设计偏好**: 所有生成的插图、图像必须强制使用 **4K** 分辨率，不接受 2K 或更低画质。
- **存储偏好**: 所有生成的图片资源必须强制保存至路径：`D:\AI素材\Antigravity自动生图`。
- **Git 偏好**: 
  - 邮箱: `2934546967@qq.com`
  - 用户名: `LeiRong`
  - 提交规范: 建议使用 `feat:`, `fix:`, `docs:` 等前缀进行记录。

- **模型偏好**: 绘图模型仅限使用 **nano-banana** (Pro)，严禁使用 HD 或其他变体。
- **交互偏好**: 在执行生图任务前，必须先确认**风格**和**比例**。比例确认必须参考 `document-illustrator` 技能文档中整理的 **完整 4K 比例列表**，禁止仅提供部分选项。 (Must confirm style/full scale ratio before generating).
- **工具偏好**: 默认情况下，凡是涉及“生图”、“插图”、“生成图片”的指令，**必须**调用 `document-illustrator` skill 中的脚本 (`scripts/generate_illustrations.py`) 进行处理，**严禁**直接使用原生的 `generate_image` 工具，除非用户有特殊说明。
- **环境信息**: 用户操作系统为 **Windows** (Windows_NT)。

