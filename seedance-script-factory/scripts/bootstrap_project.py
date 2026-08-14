#!/usr/bin/env python3
"""初始化 Seedance 项目目录。"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="初始化 Seedance 项目目录与模板文件。")
    parser.add_argument("--project-name", required=True, help="项目名称")
    parser.add_argument("--output-dir", required=True, help="项目输出目录")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    template_dir = skill_root / "assets" / "templates"

    project_root = Path(args.output_dir).resolve() / args.project_name
    (project_root / "assets" / "global").mkdir(parents=True, exist_ok=True)
    (project_root / "assets" / "project").mkdir(parents=True, exist_ok=True)
    (project_root / "storyboard").mkdir(parents=True, exist_ok=True)
    (project_root / "prompts").mkdir(parents=True, exist_ok=True)

    for template_name in [
        "storyboard.csv",
        "characters.csv",
        "scenes.csv",
        "props.csv",
        "prompt-package.md",
    ]:
        source = template_dir / template_name
        if template_name.endswith(".csv"):
            target = project_root / "assets" / "project" / template_name
        else:
            target = project_root / "prompts" / template_name
        shutil.copyfile(source, target)

    print(f"[OK] 项目已初始化: {project_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
