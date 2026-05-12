#!/usr/bin/env python3
"""
gpt-image-2 图片生成脚本
LeishiFu PPT Style Factory

用法:
  python generate_images.py --prompt "描述" --output "path/to/output.png"
  python generate_images.py --prompt "描述" --output "out.png" --size "1920x1080"
  python generate_images.py --prompt "描述" --output "out.png" --ratio "16:9" --resolution "2K"
  python generate_images.py --prompt "描述" --output "out.png" --style-suffix "editorial photography, high contrast"

参考: Penguin-Magic gptImage2Size.ts (1K/2K/4K 分档 + 比例映射)
"""

import argparse
import base64
import json
import os
import sys
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")

# gpt-image-2 尺寸约束 (来自 Penguin-Magic gptImage2Size.ts)
MAX_EDGE = 3840
MIN_PIXELS = 655_360
MAX_PIXELS = 8_294_400
DIVISOR = 16
MAX_RATIO = 3.0
MIN_SHORT_EDGE = 2048  # 最短边不低于此值，低于则等比放大

# 分辨率分档映射 (来自 Penguin-Magic gptImage2Size.ts SIZE_MAP)
SIZE_MAP = {
    "1K": {
        "1:1":  "1024x1024",
        "4:3":  "1152x864",
        "3:4":  "864x1152",
        "3:2":  "1536x1024",
        "2:3":  "1024x1536",
        "16:9": "1536x864",
        "9:16": "864x1536",
        "21:9": "1792x768",
        "4:5":  "896x1120",
        "5:4":  "1120x896",
    },
    "2K": {
        "1:1":  "2048x2048",
        "4:3":  "2048x1536",
        "3:4":  "1536x2048",
        "3:2":  "2304x1536",
        "2:3":  "1536x2304",
        "16:9": "2048x1152",
        "9:16": "1152x2048",
        "21:9": "2688x1152",
        "4:5":  "1536x1920",
        "5:4":  "1920x1536",
    },
    "4K": {
        "1:1":  "3840x3840",
        "4:3":  "2880x2160",
        "3:4":  "2160x2880",
        "3:2":  "3120x2080",
        "2:3":  "2080x3120",
        "16:9": "3840x2160",
        "9:16": "2160x3840",
        "21:9": "3840x1648",
        "4:5":  "2560x3200",
        "5:4":  "3200x2560",
    },
}

# 分档默认正方形 (Auto 比例时)
AUTO_SIZE_MAP = {"1K": "1024x1024", "2K": "2048x2048", "4K": "3840x3840"}


def resolve_size_from_tier(ratio, resolution):
    """
    根据比例 + 分辨率档位解析为具体像素尺寸
    如: ratio="16:9", resolution="2K" → "2048x1152"
    """
    tier = resolution if resolution in SIZE_MAP else "1K"
    tier_map = SIZE_MAP[tier]

    if not ratio or ratio.lower() == "auto":
        return AUTO_SIZE_MAP[tier]

    size = tier_map.get(ratio)
    if size:
        return size

    # 未命中映射表, 尝试用比例自己计算
    print(f"WARNING: 比例 '{ratio}' 不在 {tier} 映射表中, 将手动计算", file=sys.stderr)
    try:
        rw, rh = map(int, ratio.split(":"))
        longest = {"1K": 1024, "2K": 2048, "4K": 3840}[tier]
        if rw >= rh:
            w = longest
            h = int(longest * rh / rw)
        else:
            h = longest
            w = int(longest * rw / rh)
        w = (w // DIVISOR) * DIVISOR
        h = (h // DIVISOR) * DIVISOR
        return f"{w}x{h}"
    except Exception:
        return AUTO_SIZE_MAP[tier]


def load_config():
    """读取 config.json 中的 image_api 配置"""
    if not os.path.exists(CONFIG_PATH):
        print(f"ERROR: 配置文件不存在: {CONFIG_PATH}", file=sys.stderr)
        print("请创建 config.json 并填入 api_key", file=sys.stderr)
        sys.exit(1)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    api_cfg = config.get("image_api", {})
    if not api_cfg.get("api_key"):
        print("ERROR: config.json 中 image_api.api_key 为空", file=sys.stderr)
        print("请填入你的 API key (如 sk-...)", file=sys.stderr)
        sys.exit(1)

    if not api_cfg.get("enabled", True):
        print("INFO: image_api.enabled = false, 图片生成已禁用", file=sys.stderr)
        sys.exit(0)

    return api_cfg


def validate_size(size_str):
    """
    验证并规范化尺寸字符串
    规则 (来自 Penguin-Magic):
    - 两边必须是 16 的倍数
    - 最大边 3840px
    - 宽高比 ≤ 3:1
    - 总像素 ∈ [655,360 – 8,294,400]
    """
    try:
        w, h = map(int, size_str.lower().split("x"))
    except ValueError:
        print(f"ERROR: 无效尺寸格式 '{size_str}', 应为 'WxH' (如 1920x1080)", file=sys.stderr)
        sys.exit(1)

    # 对齐到 16 的倍数
    w = (w // DIVISOR) * DIVISOR
    h = (h // DIVISOR) * DIVISOR

    if w <= 0 or h <= 0:
        print("ERROR: 尺寸必须大于 0", file=sys.stderr)
        sys.exit(1)

    if max(w, h) > MAX_EDGE:
        scale = MAX_EDGE / max(w, h)
        w = (int(w * scale) // DIVISOR) * DIVISOR
        h = (int(h * scale) // DIVISOR) * DIVISOR

    ratio = max(w, h) / min(w, h)
    if ratio > MAX_RATIO:
        print(f"WARNING: 宽高比 {ratio:.1f}:1 超过 {MAX_RATIO}:1 限制, 将裁剪", file=sys.stderr)
        if w > h:
            w = (int(h * MAX_RATIO) // DIVISOR) * DIVISOR
        else:
            h = (int(w * MAX_RATIO) // DIVISOR) * DIVISOR

    # 最短边保底: 低于 MIN_SHORT_EDGE 时等比放大（保持宽高比）
    short_edge = min(w, h)
    if short_edge < MIN_SHORT_EDGE:
        scale = MIN_SHORT_EDGE / short_edge
        w_new = (int(w * scale) // DIVISOR) * DIVISOR
        h_new = (int(h * scale) // DIVISOR) * DIVISOR
        # 放大后仍需检查最大边不超限
        if max(w_new, h_new) > MAX_EDGE:
            clamp_scale = MAX_EDGE / max(w_new, h_new)
            w_new = (int(w_new * clamp_scale) // DIVISOR) * DIVISOR
            h_new = (int(h_new * clamp_scale) // DIVISOR) * DIVISOR
        print(f"INFO: 最短边 {short_edge}px < {MIN_SHORT_EDGE}px, 等比放大 {w}x{h} → {w_new}x{h_new}", file=sys.stderr)
        w, h = w_new, h_new

    total = w * h
    if total < MIN_PIXELS:
        print(f"WARNING: 总像素 {total} 低于最小值 {MIN_PIXELS}, 将放大", file=sys.stderr)
        scale = (MIN_PIXELS / total) ** 0.5
        w = (int(w * scale) // DIVISOR) * DIVISOR
        h = (int(h * scale) // DIVISOR) * DIVISOR
    elif total > MAX_PIXELS:
        print(f"WARNING: 总像素 {total} 超过最大值 {MAX_PIXELS}, 将缩小", file=sys.stderr)
        scale = (MAX_PIXELS / total) ** 0.5
        w = (int(w * scale) // DIVISOR) * DIVISOR
        h = (int(h * scale) // DIVISOR) * DIVISOR

    return f"{w}x{h}"


def generate_image(api_cfg, prompt, output_path, size, style_suffix=None):
    """
    调用 gpt-image-2 API 生成图片

    参考 Penguin-Magic gptImage2Api.ts:
    - POST {base_url}/v1/images/generations
    - Authorization: Bearer {api_key}
    - model: "gpt-image-2"
    - response_format: "b64_json"
    """
    base_url = api_cfg.get("base_url", "https://ai.t8star.cn").rstrip("/")
    api_key = api_cfg["api_key"]
    model = api_cfg.get("model", "gpt-image-2")

    # 拼接 prompt + 风格后缀
    full_prompt = prompt
    if style_suffix:
        full_prompt = f"{prompt}\n\n{style_suffix}"

    # 验证尺寸
    validated_size = validate_size(size)

    url = f"{base_url}/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "prompt": full_prompt,
        "size": validated_size,
        "response_format": "b64_json",
    }

    print(f"正在生成图片...", file=sys.stderr)
    print(f"  模型: {model}", file=sys.stderr)
    print(f"  尺寸: {validated_size}", file=sys.stderr)
    print(f"  端点: {url}", file=sys.stderr)
    print(f"  Prompt: {full_prompt[:80]}{'...' if len(full_prompt) > 80 else ''}", file=sys.stderr)

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        print("ERROR: API 请求超时 (120s)", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: API 返回错误 {resp.status_code}", file=sys.stderr)
        try:
            err_body = resp.json()
            print(f"  详情: {json.dumps(err_body, ensure_ascii=False, indent=2)}", file=sys.stderr)
        except Exception:
            print(f"  响应: {resp.text[:500]}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"ERROR: 网络错误: {e}", file=sys.stderr)
        sys.exit(1)

    # 解析响应
    result = resp.json()
    data_list = result.get("data", [])
    if not data_list:
        print("ERROR: API 返回空 data", file=sys.stderr)
        print(f"  响应: {json.dumps(result, ensure_ascii=False)[:500]}", file=sys.stderr)
        sys.exit(1)

    b64_data = data_list[0].get("b64_json")
    if not b64_data:
        # 尝试 url 格式
        img_url = data_list[0].get("url")
        if img_url:
            print("INFO: API 返回 URL 格式, 正在下载...", file=sys.stderr)
            img_resp = requests.get(img_url, timeout=60)
            img_resp.raise_for_status()
            img_bytes = img_resp.content
        else:
            print("ERROR: API 响应中无 b64_json 也无 url", file=sys.stderr)
            sys.exit(1)
    else:
        # 某些 API 会返回 data URI 前缀 (data:image/png;base64,...), 需要剥离
        if b64_data.startswith("data:"):
            b64_data = b64_data.split(",", 1)[1]
        # 修复缺少 padding 的 base64（某些 API 会省略尾部 =）
        missing_padding = len(b64_data) % 4
        if missing_padding:
            b64_data += "=" * (4 - missing_padding)
        img_bytes = base64.b64decode(b64_data)

    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 保存文件
    with open(output_path, "wb") as f:
        f.write(img_bytes)

    file_size_kb = len(img_bytes) / 1024
    print(f"✅ 图片已保存: {output_path} ({file_size_kb:.0f} KB)", file=sys.stderr)
    # stdout 输出路径供 Claude Bash 调用捕获
    print(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="gpt-image-2 图片生成 — LeishiFu PPT Style Factory"
    )
    parser.add_argument(
        "--prompt", required=True,
        help="图片描述 prompt"
    )
    parser.add_argument(
        "--output", required=True,
        help="输出文件路径 (如 images/slug/cover.png)"
    )
    parser.add_argument(
        "--size", default=None,
        help="图片尺寸 WxH (如 1920x1080), 与 --ratio/--resolution 互斥"
    )
    parser.add_argument(
        "--ratio", default=None,
        help="宽高比 (如 16:9, 4:3, 1:1), 配合 --resolution 使用"
    )
    parser.add_argument(
        "--resolution", default=None, choices=["1K", "2K", "4K"],
        help="分辨率档位: 1K (~1024), 2K (~2048), 4K (~3840)"
    )
    parser.add_argument(
        "--style-suffix", default=None,
        help="风格后缀, 追加到 prompt 末尾"
    )
    parser.add_argument(
        "--config", default=None,
        help="配置文件路径, 默认 skill 目录下的 config.json"
    )

    args = parser.parse_args()

    # 支持自定义 config 路径
    global CONFIG_PATH
    if args.config:
        CONFIG_PATH = args.config

    api_cfg = load_config()

    # 尺寸优先级: --size > --ratio+--resolution > config默认
    if args.size:
        size = args.size
    elif args.ratio or args.resolution:
        ratio = args.ratio or "16:9"
        resolution = args.resolution or api_cfg.get("default_resolution", "1K")
        size = resolve_size_from_tier(ratio, resolution)
        print(f"  分档解析: {ratio} @ {resolution} → {size}", file=sys.stderr)
    else:
        size = api_cfg.get("default_size", "1920x1080")

    generate_image(
        api_cfg=api_cfg,
        prompt=args.prompt,
        output_path=args.output,
        size=size,
        style_suffix=args.style_suffix,
    )


if __name__ == "__main__":
    main()
