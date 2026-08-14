# 资产字段规范

## 总原则

- 资产 ID 必须稳定
- 资产字段必须服务于可复用和一致性控制
- `prompt_fragment` 只写稳定视觉信息，不写剧情动作和临时状态
- 参考图类资产允许在最终 Prompt 中通过 `@引用名` 被调用

## 协调系统交接要求

- 角色资产 agent 输出的 `visual_anchors` 与 `drift_bans` 必须能直接被 Prompt 整合 agent 复用
- 场景与道具资产必须能被 segment 级 Prompt 直接引用
- 所有资产字段都必须服务于“可复用 + 可审查”

## 角色库

字段：
- `character_id`
- `name`
- `role_type`
- `age_feel`
- `appearance`
- `hair_costume`
- `personality_keywords`
- `visual_anchors`
- `drift_bans`
- `prompt_fragment`

说明：
- `visual_anchors` 用于固定角色辨识特征，如年龄感、发型、服装、脸部结构、气质识别点
- `drift_bans` 用于记录不能变化的部分
- `prompt_fragment` 用于直接拼接进提示词，只保留稳定视觉设计信息

## 场景库

字段：
- `scene_id`
- `name`
- `space_type`
- `time_of_day`
- `lighting`
- `palette`
- `set_dressing`
- `mood`
- `visual_anchors`
- `prompt_fragment`

说明：
- `visual_anchors` 用于记录空间结构、核心陈设、灯光与色调稳定项
- `prompt_fragment` 用于场景稳定复用

## 道具库

字段：
- `prop_id`
- `name`
- `category`
- `material`
- `shape_features`
- `usage`
- `owner_character_id`
- `owner_scene_id`
- `visual_anchors`
- `prompt_fragment`

说明：
- 道具应重点记录材质、形态和视觉识别点
- 不要在 `prompt_fragment` 中写一次性剧情动作

## 参考图与引用建议

当用户已有参考素材时：
- 角色图建议绑定稳定别名，例如 `@Image1`
- 场景图建议绑定稳定别名，例如 `@AssetName`
- 动作参考视频建议绑定稳定别名，例如 `@Video1`
- 音频参考建议绑定稳定别名，例如 `@Audio1`

## 母库与子库关系

- 全局母库只放可复用的稳定资产
- 项目子库允许覆盖母库
- 同一项目中不要重复编号
