#!/usr/bin/env python3
"""将解析结果规范化为标准分镜表 CSV。"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


FIELDNAMES = [
    "shot_id",
    "duration_sec",
    "scene_id",
    "character_ids",
    "prop_ids",
    "shot_size",
    "camera_angle",
    "camera_movement",
    "subject",
    "action",
    "emotion",
    "visual_focus",
    "audio_hint",
    "continuity_notes",
    "seedance_prompt",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将结构化 JSON 转为标准分镜表 CSV。")
    parser.add_argument("--input", required=True, help="输入 JSON 路径")
    parser.add_argument("--output", required=True, help="输出 CSV 路径")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    characters = payload.get("characters", [])
    props = payload.get("props", [])
    beats = payload.get("beats", [])

    first_character = characters[0]["character_id"] if characters else ""
    first_prop = props[0]["prop_id"] if props else ""

    rows = []
    for index, beat in enumerate(beats, start=1):
        rows.append(
            {
                "shot_id": f"shot_{index:03d}",
                "duration_sec": "4",
                "scene_id": beat.get("scene_id", ""),
                "character_ids": first_character,
                "prop_ids": first_prop,
                "shot_size": "中景",
                "camera_angle": "平视",
                "camera_movement": "固定",
                "subject": beat.get("text", ""),
                "action": beat.get("text", ""),
                "emotion": "",
                "visual_focus": "",
                "audio_hint": "",
                "continuity_notes": "",
                "seedance_prompt": "",
            }
        )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] 已输出: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
