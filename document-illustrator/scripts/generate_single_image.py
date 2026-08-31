#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
import httpx

def find_and_load_env():
    skill_root = Path(__file__).parent.parent
    env_path = skill_root / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=True)
    
    # 尝试 Antigravity Skill 标准位置
    antigravity_skill_env = Path.home() / ".gemini" / "antigravity" / "skills" / "document-illustrator" / ".env"
    if antigravity_skill_env.exists():
        load_dotenv(antigravity_skill_env, override=True)
        return

    load_dotenv(override=True)

find_and_load_env()

def generate_image(title, content, style_prompt, output_path, aspect_ratio="16:9", resolution="4K", is_cover=False):
    api_key = os.environ.get("GEMINI_API_KEY")
    api_base = os.environ.get("GEMINI_API_BASE", "https://api.bltcy.ai/v1").rstrip('/')
    url = f"{api_base}/images/generations"
    
    # 组合提示词
    full_prompt = f"{style_prompt}\n\n标题：{title}\n内容：{content}"
    
    payload = {
        "model": "nano-banana-pro",
        "prompt": full_prompt,
        "response_format": "url",
        "aspect_ratio": aspect_ratio,
        "image_size": resolution
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        print(f"正在调用 Nanobanana Pro 4K 接口...")
        response = httpx.post(url, json=payload, headers=headers, timeout=120.0)
        if response.status_code == 200:
            data = response.json()
            img_url = data.get("data", [{}])[0].get("url")
            if img_url:

                # Use output path directory or default to current directory
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                
                final_path = output_path
                print(f"下载中: {final_path}")
                img_res = httpx.get(img_url, timeout=30.0)
                with open(final_path, 'wb') as f:
                    f.write(img_res.content)
                return final_path
        else:
            print(f"错误: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"异常: {e}")
    return None

def main():
    parser = argparse.ArgumentParser(description='Document Illustrator - Nanobanana Pro 4K')
    parser.add_argument('--title', required=True)
    parser.add_argument('--content', required=True)
    parser.add_argument('--style-file', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--ratio', default='16:9', help='Image aspect ratio (e.g., 16:9, 3:4, etc.)')
    parser.add_argument('--resolution', default='4K')
    parser.add_argument('--cover', action='store_true')
    args = parser.parse_args()

    with open(args.style_file, 'r', encoding='utf-8') as f:
        style_prompt = f.read()

    result = generate_image(args.title, args.content, style_prompt, args.output, args.ratio, args.resolution, args.cover)
    if result:
        print(f"✓ 成功保存至: {result}")
    else:
        print("✗ 生成失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
