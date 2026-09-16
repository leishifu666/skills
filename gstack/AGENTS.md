# gstack 开发规则

本目录是包含技能、模板、浏览器工具和辅助脚本的源码库。技能能力目录见 README.md；按本次任务读取相关实现，不要求先加载全部技能。

## 修改与生成

- SKILL.md 由 SKILL.md.tmpl 和 scripts/resolvers 生成。修改指令时同步对应模板或共享生成源，保留已安装版本的用户定制与元数据。
- Codex 输出可用 `bun run gen:skill-docs --host codex` 生成；生成前检查会写入的路径，避免覆盖无关的已修改文件。
- 在原始目录工作，遵守全局的 worktree、授权和 Git 约束。浏览器、安全审查和发布技能不会自动扩大当前任务的权限。

## 可用检查

- `bun run test`：免费测试分片；仅在改动范围需要时运行。
- `bun run test:windows`：Windows 可用测试子集。
- `bun run build`：文档生成和二进制编译。
- `bun run skill:check`：技能结构与健康检查。

选择覆盖本次改动的检查，记录未验证项。付费模型评测需要适当授权，不作为普通指令精简的默认步骤。

## 必要运行约定

- Windows 的 setup 脚本需要 Git Bash/MSYS；确认实际运行时，不直接把 Bash 示例传给 PowerShell。
- 状态路径由 bin/gstack-paths 解析，支持 GSTACK_HOME、CLAUDE_PLUGIN_DATA 和 CLAUDE_PLANS_DIR；保留既有隐私、同步与授权设置。
- 浏览器工作流使用已构建的 browse 工具；实际工具调用前检查安装与接口。Claude CLI 路径及可选 WSL 参数由 browse/src/claude-bin.ts 处理。
