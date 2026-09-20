"""同步上游 Skill 文件，并重新注入 LSF 元数据；不负责自动翻译新增正文。"""

from __future__ import annotations

import argparse
import shutil
import urllib.request
from pathlib import Path


def download_tree(source: str, ref: str, upstream_path: str, temp: Path) -> None:
    archive = temp.parent / "visual-skills.zip"
    archive.parent.mkdir(parents=True, exist_ok=True)
    extract_root = temp.parent / "extracted"
    if not archive.exists():
        archive_url = f"{source}/archive/{ref}.zip"
        urllib.request.urlretrieve(archive_url, archive)
    if not extract_root.exists():
        shutil.unpack_archive(str(archive), str(extract_root))
    candidates = list(extract_root.glob(f"*/{upstream_path}"))
    if len(candidates) != 1:
        raise RuntimeError(f"无法定位上游目录：{upstream_path}")
    shutil.copytree(candidates[0], temp, dirs_exist_ok=True)


def inject_metadata(skill_file: Path, name: str, upstream_path: str, commit: str) -> None:
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise RuntimeError(f"缺少 frontmatter：{skill_file}")
    end = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if end is None:
        raise RuntimeError(f"frontmatter 未闭合：{skill_file}")
    metadata = {
        "name": name,
        "title": "LSF AI 影像导演" if upstream_path == "video" else "LSF AI 图像导演",
        "github_url": "https://github.com/smixs/visual-skills",
        "github_hash": commit,
        "upstream_path": upstream_path,
        "version": "1.0.0-lsf.1",
        "localization": "zh-CN",
    }
    existing = []
    for line in lines[1:end]:
        key = line.split(":", 1)[0].strip()
        if key not in metadata:
            existing.append(line)
    frontmatter = ["---"] + [f"{key}: {value}" for key, value in metadata.items()] + existing + ["---"]
    skill_file.write_text("\n".join(frontmatter + lines[end + 1 :]) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--upstream-path", required=True)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--temp", type=Path, required=True)
    parser.add_argument("--hash", required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    download_tree(args.source, args.ref, args.upstream_path, args.temp)
    if args.target.exists():
        shutil.rmtree(args.target)
    shutil.copytree(args.temp, args.target)
    inject_metadata(args.target / "SKILL.md", args.name, args.upstream_path, args.hash)


if __name__ == "__main__":
    main()
