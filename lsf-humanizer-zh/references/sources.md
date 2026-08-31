# 来源与改造说明

## 上游来源

- Humanizer-zh：https://github.com/op7418/Humanizer-zh
- 创建时提交：`91f3d394db8419c20d67ebe22a96cf8fee0a404b`
- 英文原版：https://github.com/blader/humanizer
- 规则参考：https://github.com/hardikpandya/stop-slop
- 背景资料：https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

## LSF 版本的主要调整

1. 从 Claude Code 的 `/humanizer-zh` 调用方式改为 Codex Skill：`$lsf-humanizer-zh`。
2. 将“去 AI 痕迹”改为“提高中文写作质量”，不承诺规避检测器。
3. 增加事实、作者、不确定性、证据、语域和意图六类锁定规则。
4. 删除将英文语法现象直接套到中文的规则，例如 `-ing` 结尾和英文标题大小写。
5. 禁止通过虚构数据、经历、来源、反馈和第一人称观点来制造“人味”。
6. 将 AI 高频词从禁词表改成上下文风险信号，避免机械替换。
7. 增加只审阅、保守润色和自由改写三种模式；默认保守润色。
8. 默认只交付改写正文，不机械附加评分、总结或客套话。

## 许可证

上游 Humanizer-zh 使用 MIT License。本目录保留其许可证文本和版权声明。
