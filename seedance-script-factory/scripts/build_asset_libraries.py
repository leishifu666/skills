#!/usr/bin/env python3
"""根据解析结果建立角色、场景、道具资产库。"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="输出角色、场景、道具资产库 CSV。")
    parser.add_argument("--input", required=True, help="输入 JSON 路径")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    return parser.parse_args()


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    output_dir = Path(args.output_dir)

    character_rows = []
    for character in payload.get("characters", []):
        character_rows.append(
            {
                "character_id": character["character_id"],
                "name": character["name"],
                "role_type": "",
                "age_feel": "",
                "appearance": "",
                "hair_costume": "",
                "personality_keywords": "",
                "visual_anchors": character["name"],
                "drift_bans": "",
                "prompt_fragment": f"角色{character['name']}，保持核心外形稳定",
            }
        )

    scene_rows = []
    for scene in payload.get("scenes", []):
        scene_rows.append(
            {
                "scene_id": scene["scene_id"],
                "name": scene["name"],
                "space_type": "",
                "time_of_day": "",
                "lighting": "",
                "palette": "",
                "set_dressing": "",
                "mood": "",
                "visual_anchors": scene["name"],
                "prompt_fragment": f"场景{scene['name']}，保持空间结构和主色调一致",
            }
        )

    prop_rows = []
    for prop in payload.get("props", []):
        prop_rows.append(
            {
                "prop_id": prop["prop_id"],
                "name": prop["name"],
                "category": "",
                "material": "",
                "shape_features": "",
                "usage": "",
                "owner_character_id": "",
                "owner_scene_id": "",
                "visual_anchors": prop["name"],
                "prompt_fragment": f"道具{prop['name']}，保持材质与形态稳定",
            }
        )

    write_csv(
        output_dir / "characters.csv",
        [
            "character_id",
            "name",
            "role_type",
            "age_feel",
            "appearance",
            "hair_costume",
            "personality_keywords",
            "visual_anchors",
            "drift_bans",
            "prompt_fragment",
        ],
        character_rows,
    )
    write_csv(
        output_dir / "scenes.csv",
        [
            "scene_id",
            "name",
            "space_type",
            "time_of_day",
            "lighting",
            "palette",
            "set_dressing",
            "mood",
            "visual_anchors",
            "prompt_fragment",
        ],
        scene_rows,
    )
    write_csv(
        output_dir / "props.csv",
        [
            "prop_id",
            "name",
            "category",
            "material",
            "shape_features",
            "usage",
            "owner_character_id",
            "owner_scene_id",
            "visual_anchors",
            "prompt_fragment",
        ],
        prop_rows,
    )

    print(f"[OK] 已输出资产库: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
