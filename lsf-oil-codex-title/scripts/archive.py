"""定位完整插件中的归档程序；未安装插件时给出说明。"""
from pathlib import Path
import runpy
import sys

plugin_root = Path(__file__).resolve().parents[3]
runner = plugin_root / "scripts" / "archive_policy.py"
if not runner.is_file():
    print("未找到完整的 oil-codex-title 插件归档程序。请通过 Codex 官方插件入口安装完整插件后再运行。", file=sys.stderr)
    raise SystemExit(2)

sys.path.insert(0, str(runner.parent))
runpy.run_path(str(runner), run_name="__main__")
