#!/usr/bin/env python3
"""Resolve and download one WeChat Channels share URL through fixed Workers."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime import configure_stdio, publish_no_overwrite, run_process, wechat_home
from typing import Any

from preflight import normalize_url
from download_media import verify


VERSION = "0.2.1"
WORKERS = (
    ("upstream", "https://sph.litao.workers.dev/api/fetch_video_profile"),
    ("qiaomu", "https://wx-dl.qiaomu.ai/api/fetch_video_profile"),
)
MEDIA_HOST_SUFFIXES = ("qq.com", "weixin.qq.com", "gtimg.com", "qpic.cn")


class OnlineDownloadError(RuntimeError):
    pass


def post_profile(endpoint: str, share_url: str, timeout: float) -> dict[str, Any]:
    body = json.dumps({"url": share_url}).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": f"qiaomu-wx-video/{VERSION}"},
        method="POST",
    )
    try:
        with urllib.request.build_opener(NoResolverRedirect()).open(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = ""
        try:
            data = json.loads(exc.read(4096).decode("utf-8", errors="replace"))
            detail = str(data.get("error") or data.get("errMsg") or "")
        except Exception:
            pass
        raise OnlineDownloadError(f"HTTP {exc.code}{': ' + detail if detail else ''}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise OnlineDownloadError(str(exc)) from exc

    if not isinstance(payload, dict):
        raise OnlineDownloadError("response is not a JSON object")
    if payload.get("error"):
        raise OnlineDownloadError(str(payload["error"]))
    feed = ((payload.get("data") or {}).get("feedInfo") or {})
    if not isinstance(feed, dict) or not feed:
        raise OnlineDownloadError(str(payload.get("errMsg") or "missing data.feedInfo"))
    return payload


def validated_media_url(value: Any) -> str:
    if not isinstance(value, str) or not value:
        return ""
    parsed = urllib.parse.urlsplit(value)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not host or parsed.username or parsed.password or parsed.port:
        return ""
    if not any(host == suffix or host.endswith(f".{suffix}") for suffix in MEDIA_HOST_SUFFIXES):
        return ""
    return value


def media_candidates(payload: dict[str, Any], one_version: str | None) -> list[tuple[str, str]]:
    feed = payload["data"]["feedInfo"]
    raw = [
        ("h264", validated_media_url((feed.get("h264VideoInfo") or {}).get("videoUrl"))),
        ("h265", validated_media_url((feed.get("h265VideoInfo") or {}).get("videoUrl"))),
        ("video", validated_media_url(feed.get("videoUrl"))),
    ]
    available = [(kind, url) for kind, url in raw if url]
    if one_version:
        preferred = "h264" if one_version == "best" else one_version
        selected = next(((kind, url) for kind, url in available if kind == preferred), None)
        if selected is None and one_version == "best":
            selected = next(iter(available), None)
        available = [selected] if selected else []
    unique: list[tuple[str, str]] = []
    seen: set[str] = set()
    for kind, url in available:
        if url in seen:
            continue
        seen.add(url)
        unique.append((kind, url))
    if not unique:
        raise OnlineDownloadError("no allowed HTTPS media URL in response")
    return unique


def safe_stem(value: Any) -> str:
    title = str(value or "视频号视频").strip()
    title = re.sub(r"[\\/:*?\"<>|\x00-\x1f]", "_", title)
    title = re.sub(r"\s+", " ", title).strip(" ._")
    return title[:48] or "视频号视频"


def output_path(output_dir: Path, stem: str, kind: str) -> Path:
    suffix = {
        "h264": "_H264_高清兼容版.mp4",
        "h265": "_H265_省空间版.mp4",
        "video": "_视频.mp4",
    }[kind]
    candidate = output_dir / f"{stem}{suffix}"
    counter = 2
    while candidate.exists():
        candidate = output_dir / f"{stem}{suffix[:-4]}_{counter}.mp4"
        counter += 1
    return candidate


def probe_video(path: Path) -> dict[str, Any]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise OnlineDownloadError("ffmpeg and ffprobe are required")
    return {"verification": "full-decode", **verify(path, ffmpeg)}


class AllowedMediaRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not validated_media_url(newurl):
            raise OnlineDownloadError("media redirect left the allowed HTTPS hosts")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class NoResolverRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise OnlineDownloadError("fixed resolver redirects are not allowed")


def download_to_stage(url: str, output_dir: Path, timeout: float) -> tuple[Path, dict[str, Any]]:
    descriptor, temp_name = tempfile.mkstemp(prefix=".qiaomu-wx-video-", suffix=".part", dir=output_dir)
    os.close(descriptor)
    temp_path = Path(temp_name)
    try:
        request = urllib.request.Request(url, headers={"User-Agent": f"qiaomu-wx-video/{VERSION}"})
        with urllib.request.build_opener(AllowedMediaRedirect()).open(request, timeout=timeout) as response, temp_path.open("wb") as output:
            final_url = response.geturl()
            if not validated_media_url(final_url):
                raise OnlineDownloadError("media redirect left the allowed HTTPS hosts")
            if response.status != 200:
                raise OnlineDownloadError("unexpected media status")
            expected = int(response.headers.get("Content-Length") or 0)
            count = 0
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                output.write(chunk)
                count += len(chunk)
            if count == 0 or (expected and expected != count):
                raise OnlineDownloadError("incomplete media transfer")
        return temp_path, probe_video(temp_path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def attempt_worker(
    worker_name: str,
    endpoint: str,
    share_url: str,
    output_dir: Path,
    one_version: str | None,
    timeout: float,
    resolve_only: bool,
) -> dict[str, Any]:
    payload = post_profile(endpoint, share_url, timeout)
    feed = payload["data"]["feedInfo"]
    candidates = media_candidates(payload, one_version)
    result: dict[str, Any] = {
        "ok": True,
        "worker": worker_name,
        "worker_endpoint": endpoint,
        "title": str(feed.get("description") or ""),
        "candidate_codecs": [kind for kind, _ in candidates],
        "files": [],
    }
    if resolve_only:
        return result

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = safe_stem(feed.get("description"))
    staged: list[tuple[Path, Path, str, dict[str, Any]]] = []
    try:
        for kind, media_url in candidates:
            final_path = output_path(output_dir, stem, kind)
            temp_path, probe = download_to_stage(media_url, output_dir, timeout)
            staged.append((temp_path, final_path, kind, probe))
        for temp_path, final_path, kind, probe in staged:
            codec = re.sub(r"[^a-zA-Z0-9_-]", "", str(probe.get("codec") or "video"))
            final_path = publish_no_overwrite(temp_path, output_dir, stem + "_" + codec)
            result["files"].append({
                "path": str(final_path.resolve()),
                "kind": kind,
                "bytes": final_path.stat().st_size,
                **probe,
            })
        return result
    except Exception:
        for temp_path, _, _, _ in staged:
            temp_path.unlink(missing_ok=True)
        raise


def main() -> None:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Download a WeChat Channels video through fixed online Workers.")
    parser.add_argument("--allow-share-url", action="store_true", help="explicit authorization to send the share URL to the two fixed resolvers")
    parser.add_argument("--url", required=True, help="https://weixin.qq.com/sph/... share URL")
    parser.add_argument("--output-dir", help="Destination directory; defaults to QIAOMU_WX_VIDEO_OUTPUT or cwd")
    parser.add_argument("--one-version", choices=("h264", "h265", "best"), help="Download only one version")
    parser.add_argument("--resolve-only", action="store_true", help="Resolve metadata without downloading media")
    parser.add_argument("--timeout", type=float, default=60, help="Per-request timeout in seconds")
    args = parser.parse_args()
    if not args.allow_share_url:
        print(json.dumps({"ok": False, "stage": "consent_required", "error": "sending share URLs to third parties requires explicit authorization"}))
        raise SystemExit(2)

    try:
        share_url = normalize_url(args.url)
    except ValueError as exc:
        print(json.dumps({"ok": False, "stage": "validate", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
    output_dir = Path(args.output_dir or os.environ.get("LSF_WX_VIDEO_OUTPUT", Path.cwd() / "outputs")).expanduser().resolve()
    failures: list[dict[str, str]] = []
    for worker_name, endpoint in WORKERS:
        try:
            result = attempt_worker(
                worker_name, endpoint, share_url, output_dir, args.one_version, args.timeout, args.resolve_only
            )
            result["fallbacks"] = failures
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return
        except Exception as exc:
            failures.append({"worker": worker_name, "error": type(exc).__name__})
    print(json.dumps({
        "ok": False,
        "stage": "online_workers",
        "fallbacks": failures,
        "local_backend_required": True,
    }, ensure_ascii=False, indent=2))
    raise SystemExit(3)


if __name__ == "__main__":
    main()
