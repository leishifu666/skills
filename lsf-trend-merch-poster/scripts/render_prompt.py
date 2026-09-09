"""Filter the Chinese master prompt without rewriting its shared content."""
import argparse
from pathlib import Path
import re
import sys


def render(mode, background, template=None):
    if mode not in tuple("ABCDEFG") or background not in tuple("ABC"):
        raise ValueError("Expected mode A-G and background A-C")
    if template is None:
        template = (Path(__file__).resolve().parent.parent / "references" / "prompt-template.md").read_text(encoding="utf-8")
    head, rest = template.split("1. 实体造物模态库：", 1)
    modes, rest = rest.split("2. 背景与配色库：", 1)
    backgrounds, shared = rest.split("背景变量控制方案类别；", 1)

    def select(block, letter, expected):
        entries = re.findall(r"^- ([A-G])【[^\n]+", block, re.MULTILINE)
        if entries != list(expected):
            raise ValueError("Unexpected master choices; inspect template instead of guessing")
        return next(line for line in block.splitlines() if line.startswith(f"- {letter}【"))

    selected_mode = select(modes, mode, "ABCDEFG")
    selected_background = select(backgrounds, background, "ABC")
    head = re.sub(r"^【模态选择】：[^\n]*", f"【模态选择】：{mode}", head, count=1)
    head = re.sub(r"^【背景与配色】：[^\n]*", f"【背景与配色】：{background}", head, count=1, flags=re.MULTILINE)
    selection = "优先执行顶部变量指定的模态和背景；留空或填“随机”的项目分别独立抽取。"
    if selection not in head or "随机规则：" not in head or "库中举例仅作参考" not in head:
        raise ValueError("Unexpected routing instructions in master")
    head = head.replace(selection, "执行以下指定模态与背景。", 1)
    head = re.sub(r"随机规则：.*?(?=库中举例仅作参考)", "", head, count=1, flags=re.DOTALL)
    return (head + "1. 实体造物模态库：\n\n" + selected_mode
            + "\n\n2. 背景与配色库：\n\n" + selected_background
            + "\n\n背景变量控制方案类别；" + shared)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", required=True, choices=list("ABCDEFG"))
    parser.add_argument("--background", required=True, choices=list("ABC"))
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    print(render(args.mode, args.background), end="")
