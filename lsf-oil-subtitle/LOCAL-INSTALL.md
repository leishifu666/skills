# 本机安装记录

来源：https://github.com/oil-oil/oil-subtitle
仓库路径：.
调用名：$lsf-oil-subtitle

仅调整本机技能名称、展示名及相关技能转交名称，保留上游配置目录与凭据引用。

本机 Windows。已安装 .venv/Scripts/python.exe 及 flask、jieba、dashscope、keyring，已安装 credential-ui 依赖。Python 导入和两个业务入口 --help 通过，Windows 系统凭据库假凭据测试通过。百炼 Key 尚未配置；未调用云端 ASR。上游 setup.sh 仅支持 macOS；完整字幕烧录仍需 Windows 验证/适配（/tmp 进度文件、字体等），自动人脸检测和美颜依赖 macOS Vision。勿宣称完整链路可用。
