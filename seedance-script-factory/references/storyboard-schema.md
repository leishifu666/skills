# 分镜表字段规范

## 标准字段

- `shot_id`
- `duration_sec`
- `scene_id`
- `character_ids`
- `prop_ids`
- `shot_size`
- `camera_angle`
- `camera_movement`
- `subject`
- `action`
- `dialogue`
- `emotion`
- `visual_focus`
- `audio_hint`
- `continuity_notes`
- `seedance_prompt`

## 多 agent 交接要求

- 分镜 agent 输出的字段必须足够支撑角色资产、场景资产、道具资产与 Prompt 整合模块继续工作
- `continuity_notes` 必须允许记录跨镜头稳定性要求、回退修订提示和复检关注点
- `seedance_prompt` 属于镜头级工作层字段，不是最终交付层字段

## 字段说明

### `duration_sec`
- 记录单镜头时长
- 最终 segment 合成时，要能按 `5-15s` 的口径重新规划

### `shot_size`
可选值示例：
- 特写
- 近景
- 中景
- 全景
- 远景

### `camera_angle`
可选值示例：
- 平视
- 俯拍
- 仰拍
- 侧拍
- 微俯
- 微仰

### `camera_movement`
可选值示例：
- 固定
- 推进
- 拉远
- 平移
- 跟拍
- 环绕
- 手持

### `dialogue`
用于记录该镜头中的对白、口播、旁白、拟声吟唱或明确口型内容。

建议写法：
- `小慧："你说，你什么办法，可以让我早一点放假？" 语气机灵试探，口型同步`
- `小央："这个……不好吧。" 语气迟疑克制，轻微停顿，口型同步`
- `无对白，以环境音和配乐推进`

### `continuity_notes`
用于记录与前后镜头共享的一致性约束，比如：
- 角色服装不变
- 道具位置延续
- 灯光保持冷色调
- 继续使用 @Image1 锁定角色外观
- 当前镜头若不过审，应优先回退给哪个模块
- 下轮复检要重点检查什么

### `seedance_prompt`
- 用于记录单镜头层的可用 Prompt
- 服务于镜头级工作层，不是最终 segment 交付层
- 不可直接串接多个 `seedance_prompt` 冒充最终单段总 Prompt
- 最终交付层仍需进一步合成为 `segment`

## 字段最小完整性要求

以下条件不满足时，不应进入 Prompt 整合或最终交付：
- 缺少 `subject` 或 `action`
- 缺少 `scene_id`
- 缺少 `continuity_notes`
- 有对白但 `dialogue` 未写清说话者、语气或口型同步要求
- 镜头级 `seedance_prompt` 与字段内容明显不一致

## 使用要求

- 一个镜头一行
- `character_ids` 和 `prop_ids` 用英文逗号分隔
- `dialogue` 建议写清说话者、原句、语气、是否需要口型同步
- `continuity_notes` 建议同步记录跨镜头一致性与复检关注点
- `seedance_prompt` 只用于镜头级整理，最终交付层必须进一步合成为 segment 单段总 Prompt
