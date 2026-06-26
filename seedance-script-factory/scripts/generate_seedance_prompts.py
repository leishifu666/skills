#!/usr/bin/env python3
"""根据分镜表生成适配 Seedance 2.0 的资产提示词和视频提示词。"""

from __future__ import annotations

import argparse
import csv
import math
import re
from dataclasses import dataclass
from pathlib import Path


MIN_SEGMENT_DURATION = 5
MAX_SEGMENT_DURATION = 15
TARGET_SEGMENT_DURATION = 10
VIDEO_NEGATIVE_RULE = "画面不要出现字幕，不要出现屏幕文字、字卡、水印。"

CHARACTER_PROMPT_OVERRIDES = {
    "小央": "角色设定图，@小央，红黑配色的服务机器人，黑色镜面面罩，细长机械四肢，央视网家族感，工业设计感干净利落，科技感高级，不夸张不卡通，不带道具，不做剧情动作，纯净背景。",
    "小慧": "角色设定图，@小慧，基于小央家族的女性化机器人变体，红黑配色，黑色面罩结构，线条更纤细，体态更轻盈，年轻感与机灵感并存，设计利落高级，不带道具，不做剧情动作，纯净背景。",
    "老王": "超写实人像角色设定图，@老王，半身特写，上胸到头部构图，镜头聚焦面部，电影级写实摄影质感，RAW质感，8K，高一致性同一人物，中年中国男性，真实自然的东方五官，脸部轮廓干净，额头到下颌线结构清晰，眉眼鼻唇比例自然，皮肤纹理真实细腻，轻微生活化肤质，短发清爽利落，发丝走向清晰，简洁合身的职场便装，面料质感自然，中性冷灰纯净背景，专业棚拍人像布光，整体克制真实，画面高级耐看，适合做统一角色资产参考。",
    "领导": "超写实人像角色设定图，@领导，半身特写，上胸到头部构图，镜头聚焦面部，电影级写实摄影质感，RAW质感，8K，高一致性同一人物，中年中国男性领导形象，成熟稳重的东方五官，面部结构清晰，眉骨鼻梁与下颌线利落，眉眼鼻唇比例自然，皮肤纹理真实细腻，发型整洁克制，发丝层次清楚，简洁克制的商务着装或半正装，材质干净挺括，中性冷灰纯净背景，专业棚拍人像布光，整体成熟专业可信，画面高级耐看，适合做统一角色资产参考。",
}

HUMAN_ROLE_KEYWORDS = (
    "真人",
    "人像",
    "人类",
    "男",
    "女",
    "男性",
    "女性",
    "同事",
    "领导",
    "老师",
    "员工",
    "主持",
    "记者",
    "医生",
    "警察",
    "顾客",
    "上班族",
    "青年",
    "中年",
)

SCENE_PROMPT_OVERRIDES = {
    "展厅服务台": "场景设定图，@展厅服务台，现代媒体展厅服务台空间，白天室内商业照明，白灰基底，红黑点缀，整体整洁明亮，科技感高级，真实职场环境，无人物，广角环境全景。",
    "茶水间微波炉区": "场景设定图，@茶水间微波炉区，办公茶水间微波炉区域，午间顶灯照明，空间略局促，米白墙面与银灰电器，生活化职场细节清晰，真实办公后场环境，无人物，广角环境全景。",
    "柱子旁办公区": "场景设定图，@柱子旁办公区，办公室过道与柱边空间，午间办公照明，中性色调，真实职场走廊环境，适合反转出场，空间关系清楚，无人物，广角环境全景。",
}

PROP_PROMPT_OVERRIDES = {
    "手表": "道具设定图，@手表，小巧金属电子手表，屏幕清晰显示11:00，产品质感清楚，主体居中，背景干净。",
    "检修工具": "道具设定图，@检修工具，小型维修工具，金属与塑料结构清晰，造型简洁专业，主体居中，背景干净。",
    "微波炉": "道具设定图，@微波炉，办公茶水间旧式微波炉，金属机壳与塑料面板，结构完整清楚，真实生活电器质感，主体居中，背景干净。",
    "白馒头与黑馒头": "道具设定图，@白馒头与黑馒头，一白一黑两只馒头形成强反差，材质真实，主体清楚，背景干净。",
    "饭盒": "道具设定图，@饭盒，普通职场午餐饭盒，日常生活感明确，结构简单真实，主体居中，背景干净。",
    "电话": "道具设定图，@电话，办公电话或手机通话道具，造型清晰简洁，真实办公用品质感，主体居中，背景干净。",
}


@dataclass
class Shot:
    row: dict[str, str]
    duration: int
    start: int
    end: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 Seedance 2.0 提示词包")
    parser.add_argument("--storyboard", required=True, help="分镜 CSV 路径")
    parser.add_argument("--characters", required=True, help="角色库 CSV 路径")
    parser.add_argument("--scenes", required=True, help="场景库 CSV 路径")
    parser.add_argument("--props", required=True, help="道具库 CSV 路径")
    parser.add_argument("--output", required=True, help="输出 Markdown 路径")
    parser.add_argument("--project-name", default="", help="项目名")
    parser.add_argument("--style", default="", help="风格关键词")
    parser.add_argument("--core-relationship", default="", help="核心角色关系")
    return parser.parse_args()


def safe_get(row: dict[str, str], key: str, default: str = "") -> str:
    return (row.get(key) or default).strip()


def split_ids(ids_text: str) -> list[str]:
    return [item.strip() for item in (ids_text or "").split(",") if item.strip()]


def load_csv(path: Path, key_field: str) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return {row[key_field]: row for row in reader if row.get(key_field)}


def read_storyboard(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def join_nonempty(parts: list[str], sep: str = "，") -> str:
    return sep.join([part.strip() for part in parts if part and part.strip()])


def find_spoken_boundary(text: str) -> int:
    indices = [text.find(mark) for mark in "。！？?!"]
    indices = [index for index in indices if index >= 0]
    if not indices:
        return len(text)
    return min(indices) + 1


def quote_dialogue_text(text: str) -> str:
    if not text:
        return ""
    if text.startswith("无对白"):
        return text

    pattern = re.compile(
        r"(?P<label>[A-Za-z0-9_\u4e00-\u9fff]{1,20})：(?P<body>.*?)(?=(?:[A-Za-z0-9_\u4e00-\u9fff]{1,20}：)|$)"
    )
    if not pattern.search(text):
        return text

    parts: list[str] = []
    last_end = 0
    for match in pattern.finditer(text):
        parts.append(text[last_end:match.start()])
        label = match.group("label").strip()
        body = match.group("body").strip()
        if not body:
            parts.append(f"{label}：")
            last_end = match.end()
            continue

        boundary = find_spoken_boundary(body)
        spoken = body[:boundary].strip()
        tail = body[boundary:].strip()
        if spoken and not spoken.startswith('"'):
            spoken = f'"{spoken}"'

        rebuilt = f"{label}：{spoken}"
        if tail:
            rebuilt = f"{rebuilt} {tail}"
        parts.append(rebuilt)
        last_end = match.end()

    parts.append(text[last_end:])
    return "".join(parts).strip()


def normalize_durations(rows: list[dict[str, str]]) -> list[int]:
    raw_durations = [float(safe_get(row, "duration_sec", "0") or 0) for row in rows]
    base = [int(math.floor(value)) for value in raw_durations]
    target_total = int(round(sum(raw_durations)))
    delta = target_total - sum(base)

    ranking = sorted(
        range(len(raw_durations)),
        key=lambda index: (raw_durations[index] - math.floor(raw_durations[index]), -index),
        reverse=True,
    )

    if delta > 0:
        for index in ranking[:delta]:
            base[index] += 1
    elif delta < 0:
        for index in reversed(ranking[: abs(delta)]):
            if base[index] > 1:
                base[index] -= 1

    return [max(1, value) for value in base]


def build_shots(rows: list[dict[str, str]]) -> list[Shot]:
    durations = normalize_durations(rows)
    shots: list[Shot] = []
    current = 0
    for row, duration in zip(rows, durations):
        shots.append(Shot(row=row, duration=duration, start=current, end=current + duration))
        current += duration
    return shots


def get_names(ids_text: str, mapping: dict[str, dict[str, str]]) -> list[str]:
    names: list[str] = []
    for item in split_ids(ids_text):
        row = mapping.get(item)
        if row:
            name = safe_get(row, "name")
            if name:
                names.append(name)
    return names


def get_alias_name(asset_id: str, mapping: dict[str, dict[str, str]], fallback: str = "") -> str:
    row = mapping.get(asset_id)
    if row:
        name = safe_get(row, "name")
        if name:
            return f"@{name}"
    if fallback:
        return f"@{fallback}"
    return f"@{asset_id}" if asset_id else ""


def get_scene_text(scene_id: str, scenes: dict[str, dict[str, str]]) -> str:
    row = scenes.get(scene_id)
    if not row:
        return scene_id or "-"
    return join_nonempty(
        [
            safe_get(row, "name"),
            safe_get(row, "time_of_day"),
            safe_get(row, "lighting"),
        ]
    )


def get_camera_text(row: dict[str, str]) -> str:
    return join_nonempty(
        [
            safe_get(row, "shot_size"),
            safe_get(row, "camera_angle"),
            safe_get(row, "camera_movement"),
            safe_get(row, "visual_focus"),
        ],
        sep="；",
    )


def ordered_ids(rows: list[dict[str, str]], field: str) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for row in rows:
        values = [safe_get(row, field)] if field == "scene_id" else split_ids(safe_get(row, field))
        for value in values:
            if value and value not in seen:
                ordered.append(value)
                seen.add(value)
    return ordered


def looks_like_human_character(row: dict[str, str]) -> bool:
    haystack = " ".join(
        [
            safe_get(row, "role_type"),
            safe_get(row, "appearance"),
            safe_get(row, "hair_costume"),
        ]
    )
    if any(keyword in haystack for keyword in ("机器人", "机体", "机械", "面罩", "仿生")):
        return False
    return any(keyword in haystack for keyword in HUMAN_ROLE_KEYWORDS)


def build_human_character_prompt(row: dict[str, str]) -> str:
    name = safe_get(row, "name")
    identity = safe_get(row, "role_type") or f"{name}的人像角色"
    appearance = safe_get(row, "appearance")
    styling = safe_get(row, "hair_costume")
    fragments = [
        "超写实人像角色设定图",
        f"@{name}",
        "半身特写",
        "上胸到头部构图",
        "镜头聚焦面部",
        "电影级写实摄影质感",
        "RAW质感",
        "8K",
        "高一致性同一人物",
        identity,
    ]
    if appearance:
        fragments.append(appearance)
        fragments.extend(
        [
            "五官自然真实",
            "面部结构清晰干净",
            "皮肤纹理细腻不过度磨皮",
        ]
    )
    if styling:
        fragments.append(styling)
    fragments.extend(
        [
            "中性冷灰纯净背景",
            "专业棚拍人像布光",
            "整体高级自然",
            "适合做统一角色资产参考",
        ]
    )
    return "，".join(fragment for fragment in fragments if fragment)


def build_storyboard_cards(
    shots: list[Shot],
    characters: dict[str, dict[str, str]],
    scenes: dict[str, dict[str, str]],
    props: dict[str, dict[str, str]],
) -> list[str]:
    lines: list[str] = []
    for shot in shots:
        row = shot.row
        lines.extend(
            [
                f"### {safe_get(row, 'shot_id')}",
                "",
                f"- 时间段：{shot.start}-{shot.end}秒",
                f"- 时长：{shot.duration}秒",
                f"- 场景：{get_scene_text(safe_get(row, 'scene_id'), scenes)}",
                f"- 角色：{'、'.join(get_names(safe_get(row, 'character_ids'), characters)) or '-'}",
                f"- 道具：{'、'.join(get_names(safe_get(row, 'prop_ids'), props)) or '-'}",
                f"- 动作：{safe_get(row, 'action').replace('|', '/').replace(chr(10), ' ') or '-'}",
                f"- 对白：{quote_dialogue_text(safe_get(row, 'dialogue')).replace('|', '/').replace(chr(10), ' ') or '-'}",
                f"- 镜头语言：{get_camera_text(row).replace(chr(10), ' ') or '-'}",
                "",
            ]
        )
    return lines


def segment_scene_changes(shots: list[Shot], start: int, end: int) -> int:
    count = 0
    for index in range(start, end - 1):
        if safe_get(shots[index].row, "scene_id") != safe_get(shots[index + 1].row, "scene_id"):
            count += 1
    return count


def plan_segments(shots: list[Shot]) -> list[tuple[int, int]]:
    count = len(shots)
    best: list[tuple[int, int, int] | None] = [None] * (count + 1)
    nxt = [-1] * (count + 1)
    best[count] = (0, 0, 0)

    for start in range(count - 1, -1, -1):
        duration = 0
        for end in range(start, count):
            duration += shots[end].duration
            if duration > MAX_SEGMENT_DURATION:
                break
            if duration < MIN_SEGMENT_DURATION:
                continue
            if best[end + 1] is None:
                continue

            rest = best[end + 1]
            candidate = (
                1 + rest[0],
                segment_scene_changes(shots, start, end + 1) + rest[1],
                abs(duration - TARGET_SEGMENT_DURATION) + rest[2],
            )
            if best[start] is None or candidate < best[start]:
                best[start] = candidate
                nxt[start] = end + 1

    if nxt[0] == -1:
        return [(0, count)]

    segments: list[tuple[int, int]] = []
    index = 0
    while index < count and nxt[index] != -1:
        segments.append((index, nxt[index]))
        index = nxt[index]

    if index < count:
        segments.append((index, count))
    return segments


def build_character_asset_prompt(row: dict[str, str]) -> str:
    name = safe_get(row, "name")
    if name in CHARACTER_PROMPT_OVERRIDES:
        return CHARACTER_PROMPT_OVERRIDES[name]
    if looks_like_human_character(row):
        return build_human_character_prompt(row)

    body = join_nonempty(
        [
            safe_get(row, "role_type"),
            f"外观：{safe_get(row, 'appearance')}" if safe_get(row, "appearance") else "",
            f"结构/服装：{safe_get(row, 'hair_costume')}" if safe_get(row, "hair_costume") else "",
        ]
    )
    return f"角色设定图，@{name}，{name}，{body}，不带道具，不做剧情动作，纯净背景。"


def build_scene_asset_prompt(row: dict[str, str]) -> str:
    name = safe_get(row, "name")
    if name in SCENE_PROMPT_OVERRIDES:
        return SCENE_PROMPT_OVERRIDES[name]

    body = join_nonempty(
        [
            f"空间类型：{safe_get(row, 'space_type')}" if safe_get(row, "space_type") else "",
            f"时间：{safe_get(row, 'time_of_day')}" if safe_get(row, "time_of_day") else "",
            f"光线：{safe_get(row, 'lighting')}" if safe_get(row, "lighting") else "",
            f"色彩：{safe_get(row, 'palette')}" if safe_get(row, "palette") else "",
            f"陈设：{safe_get(row, 'set_dressing')}" if safe_get(row, "set_dressing") else "",
        ]
    )
    return f"场景设定图，@{name}，{name}，{body}，无人物，广角环境全景。"


def build_prop_asset_prompt(row: dict[str, str]) -> str:
    name = safe_get(row, "name")
    if name in PROP_PROMPT_OVERRIDES:
        return PROP_PROMPT_OVERRIDES[name]

    body = join_nonempty(
        [
            f"材质：{safe_get(row, 'material')}" if safe_get(row, "material") else "",
            f"形态：{safe_get(row, 'shape_features')}" if safe_get(row, "shape_features") else "",
        ]
    )
    return f"道具设定图，@{name}，{name}，{body}，主体居中，背景干净。"


def build_asset_prompt_sections(
    rows: list[dict[str, str]],
    characters: dict[str, dict[str, str]],
    scenes: dict[str, dict[str, str]],
    props: dict[str, dict[str, str]],
) -> list[str]:
    used_characters = ordered_ids(rows, "character_ids")
    used_scenes = ordered_ids(rows, "scene_id")
    used_props = ordered_ids(rows, "prop_ids")

    lines = ["## 资产生成提示词", ""]

    lines.extend(["### 角色资产提示词", ""])
    for character_id in used_characters:
        row = characters.get(character_id)
        if not row:
            continue
        lines.extend(
            [
                f"#### {safe_get(row, 'name')}",
                "",
                "```text",
                build_character_asset_prompt(row),
                "```",
                "",
            ]
        )

    lines.extend(["### 场景资产提示词", ""])
    for scene_id in used_scenes:
        row = scenes.get(scene_id)
        if not row:
            continue
        lines.extend(
            [
                f"#### {safe_get(row, 'name')}",
                "",
                "```text",
                build_scene_asset_prompt(row),
                "```",
                "",
            ]
        )

    lines.extend(["### 道具资产提示词", ""])
    for prop_id in used_props:
        row = props.get(prop_id)
        if not row:
            continue
        lines.extend(
            [
                f"#### {safe_get(row, 'name')}",
                "",
                "```text",
                build_prop_asset_prompt(row),
                "```",
                "",
            ]
        )

    return lines


def build_segment_prompt(
    segment_index: int,
    segment_shots: list[Shot],
    characters: dict[str, dict[str, str]],
    scenes: dict[str, dict[str, str]],
    props: dict[str, dict[str, str]],
    style_text: str,
) -> tuple[str, str]:
    segment_start = segment_shots[0].start
    segment_end = segment_shots[-1].end
    segment_duration = segment_end - segment_start

    alias_order: list[str] = []
    seen_alias: set[str] = set()
    for shot in segment_shots:
        for item in split_ids(safe_get(shot.row, "character_ids")):
            alias = get_alias_name(item, characters)
            if alias not in seen_alias:
                alias_order.append(alias)
                seen_alias.add(alias)
        scene_id = safe_get(shot.row, "scene_id")
        if scene_id:
            alias = get_alias_name(scene_id, scenes)
            if alias not in seen_alias:
                alias_order.append(alias)
                seen_alias.add(alias)
        for item in split_ids(safe_get(shot.row, "prop_ids")):
            alias = get_alias_name(item, props)
            if alias not in seen_alias:
                alias_order.append(alias)
                seen_alias.add(alias)

    beat_texts: list[str] = []
    for shot in segment_shots:
        row = shot.row
        local_start = shot.start - segment_start
        local_end = shot.end - segment_start
        beat_lines = [
            join_nonempty(
                [
                    f"{local_start}-{local_end}秒",
                    safe_get(row, "subject"),
                    safe_get(row, "action"),
                    quote_dialogue_text(safe_get(row, "dialogue")),
                ]
            )
        ]
        scene_text = get_scene_text(safe_get(row, "scene_id"), scenes)
        camera_text = get_camera_text(row)
        audio_text = safe_get(row, "audio_hint")
        if scene_text:
            beat_lines.append(f"场景：{scene_text}")
        if camera_text:
            beat_lines.append(f"镜头：{camera_text}")
        if audio_text:
            beat_lines.append(f"音频：{audio_text}")
        beat_texts.append("\n\n".join(line for line in beat_lines if line))

    label = (
        f"segment_{segment_index:03d}"
        f"（{safe_get(segment_shots[0].row, 'shot_id')}-{safe_get(segment_shots[-1].row, 'shot_id')}）"
    )
    prompt_lines = [
        f"{segment_duration}秒视频段（{segment_start}-{segment_end}秒），{' '.join(alias_order)}。",
    ]
    if style_text:
        prompt_lines.extend(["", f"风格：{style_text}。"])
    for beat_text in beat_texts:
        prompt_lines.extend(["", beat_text])
    prompt_lines.extend(
        [
            "",
            "统一要求：保持角色、场景、道具前后一致，避免角色漂移、道具变形、场景跳变、风格失真。",
            f"限制：{VIDEO_NEGATIVE_RULE}",
        ]
    )
    prompt = "\n".join(prompt_lines)
    return label, prompt


def main() -> int:
    args = parse_args()

    rows = read_storyboard(Path(args.storyboard))
    characters = load_csv(Path(args.characters), "character_id")
    scenes = load_csv(Path(args.scenes), "scene_id")
    props = load_csv(Path(args.props), "prop_id")
    shots = build_shots(rows)
    segments = plan_segments(shots)

    total_duration = shots[-1].end if shots else 0
    output_lines = [
        "# Prompt Package",
        "",
        "## 项目信息",
        "",
        f"- 项目名：{args.project_name or '未命名项目'}",
        "- 平台：Seedance 2.0",
        "- 类型：剧情短片 / 分镜视频生成",
        f"- 总时长：{total_duration}秒",
        f"- 风格关键词：{args.style or '待补充'}",
        f"- 核心角色关系：{args.core_relationship or '待补充'}",
        f"- 视频分段数：{len(segments)}",
        "",
        "## 分镜表格（Notion友好版）",
        "",
        *build_storyboard_cards(shots, characters, scenes, props),
        "",
        *build_asset_prompt_sections(rows, characters, scenes, props),
        "## 最终视频提示词",
        "",
    ]

    for segment_index, (start, end) in enumerate(segments, start=1):
        label, prompt = build_segment_prompt(
            segment_index=segment_index,
            segment_shots=shots[start:end],
            characters=characters,
            scenes=scenes,
            props=props,
            style_text=args.style,
        )
        output_lines.extend([f"### {label}", "", "```text", prompt, "```", ""])

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(output_lines), encoding="utf-8")
    print(f"[OK] 已输出 {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
