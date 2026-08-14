#!/usr/bin/env python3
"""将原始剧本解析为结构化 JSON。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CHARACTER_LINE = re.compile(r"^(角色|人物)[:：]\s*(.+)$")
SCENE_LINE = re.compile(r"^(场景|镜头|地点|环境)[:：]\s*(.+)$")
PROP_LINE = re.compile(r"^(道具)[:：]\s*(.+)$")
META_LINE = re.compile(r"^(角色|人物|场景|镜头|地点|环境|道具)[:：]\s*(.+)$")
PROP_HINT = re.compile(r"(拿着|手持|佩戴|桌上|椅子|手机|电脑|文件|箱子|卡片|屏幕)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="解析剧本文本，提取角色、场景、道具与剧情节拍。")
    parser.add_argument("--input", required=True, help="原始剧本文本路径")
    parser.add_argument("--output", required=True, help="输出 JSON 路径")
    return parser.parse_args()


def split_nonempty_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def extract_characters(lines: list[str]) -> list[dict[str, str]]:
    found: list[str] = []
    for line in lines:
        match = CHARACTER_LINE.match(line)
        if match:
            raw_value = match.group(2).strip()
            if not re.search(r"[、/；;]", raw_value) and re.search(r"[，,]", raw_value):
                raw_value = re.split(r"[，,]", raw_value, maxsplit=1)[0].strip()

            for part in re.split(r"[、/；;]+", raw_value):
                if part and part not in found:
                    found.append(part)

    return [
        {
            "character_id": f"char_{index:03d}",
            "name": name,
        }
        for index, name in enumerate(found, start=1)
    ]


def extract_scenes(lines: list[str]) -> list[dict[str, str]]:
    found: list[str] = []
    for line in lines:
        match = SCENE_LINE.match(line)
        if match:
            value = match.group(2).strip()
            if value and value not in found:
                found.append(value)

    if not found:
        found = ["默认场景"]

    return [
        {
            "scene_id": f"scene_{index:03d}",
            "name": name,
        }
        for index, name in enumerate(found, start=1)
    ]


def extract_props(lines: list[str]) -> list[dict[str, str]]:
    props: list[str] = []
    explicit_found = False
    for line in lines:
        prop_match = PROP_LINE.match(line)
        if prop_match:
            explicit_found = True
            for part in re.split(r"[，,、/；;]+", prop_match.group(2).strip()):
                if part and part not in props:
                    props.append(part)
            continue

        if META_LINE.match(line):
            continue

        if not explicit_found and PROP_HINT.search(line):
            cleaned = line[:60]
            if cleaned not in props:
                props.append(cleaned)

    return [
        {
            "prop_id": f"prop_{index:03d}",
            "name": name,
        }
        for index, name in enumerate(props, start=1)
    ]


def build_beats(lines: list[str], scenes: list[dict[str, str]]) -> list[dict[str, str]]:
    scene_id = scenes[0]["scene_id"]
    beats: list[dict[str, str]] = []
    for index, line in enumerate(lines, start=1):
        if SCENE_LINE.match(line):
            scene_name = SCENE_LINE.match(line).group(2).strip()
            for scene in scenes:
                if scene["name"] == scene_name:
                    scene_id = scene["scene_id"]
                    break
            continue

        if META_LINE.match(line):
            continue

        beats.append(
            {
                "beat_id": f"beat_{index:03d}",
                "scene_id": scene_id,
                "text": line,
            }
        )
    return beats


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    text = input_path.read_text(encoding="utf-8")
    lines = split_nonempty_lines(text)

    characters = extract_characters(lines)
    scenes = extract_scenes(lines)
    props = extract_props(lines)
    beats = build_beats(lines, scenes)

    payload = {
        "source_file": str(input_path),
        "characters": characters,
        "scenes": scenes,
        "props": props,
        "beats": beats,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] 已输出: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
