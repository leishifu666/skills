# LSF：2.0 兼容与恢复

2026-09-16 已适配 base `6e60b5e22419464b4853e01ddb6c0e6f6659a733`，保留中文入口。

## 外置依赖

- img2 harness 0.2.3：`img2threejs/img2`，提交 `7aa41b37ee24dde844390bb05eca76b709e91599`。
- CS2 0.1.2：`img2threejs/plugin-cs2`，提交 `e5e29ba53290a18809907d0b90992aba6e8ce975`。
- Character 0.2.0：`img2threejs/plugin-character`，提交 `d8750638f9fc092714e7fcb4941053514455295d`。

新机器需按官方 harness 安装说明注册上述插件，再运行 `img2 doctor --json`。单独复制本技能或插件文件不等于完成注册；`plugins.json`、`receipts.json` 和 `_img2_local.py` 都是机器专属文件，不随公开技能仓库上传。安装器可能设置其他客户端的技能链接或目录权限，执行前检查并遵守用户授权。

## 已有任务

- 新任务显式选择 `generic`、`character`、`cs2` 或 `animated-character`；不从名字猜领域。
- 新规范使用 `objectClass.domain`。旧 `objectClass.cs2` 需明确迁移后验证，不静默丢弃。
- 已有任务的持久化步骤不会自动迁移；先检查原任务状态和引用命令，保留已有产物。不能为了用新版而擅自重新初始化。
- 旧 CS2 内置脚本已迁到官方插件，不能继续拼接已移除的 `forge/stage1_intake/cs2_*.py` 路径。无法恢复原命令时说明兼容问题，由用户确认任务迁移。

本次验证涵盖注册表、插件静态检查及工作流单元测试，不表示已经完成真实图片到 3D 的端到端生成。
