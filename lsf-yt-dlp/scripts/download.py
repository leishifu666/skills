#!/usr/bin/env python3
"""Guarded universal video downloader with an embedded WeChat adapter."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import ipaddress
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, BinaryIO, Iterator
import urllib.error
import urllib.parse
import urllib.request
from urllib.parse import urlsplit, urlunsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runtime import configure_stdio, file_lock, media_lock_path, redact, run_process

VERSION = "1.2.0-lsf-windows.1"
YT_DLP_RELEASE_API = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"
YT_DLP_RELEASE_LATEST = "https://github.com/yt-dlp/yt-dlp/releases/latest"
BROWSER_APPLICATIONS = {
    "chrome": ("/Applications/Google Chrome.app", "~/Applications/Google Chrome.app"),
    "edge": ("/Applications/Microsoft Edge.app", "~/Applications/Microsoft Edge.app"),
    "firefox": ("/Applications/Firefox.app", "~/Applications/Firefox.app"),
    "safari": ("/Applications/Safari.app",),
}
QUALITY_FORMATS = {
    "best": "bv*+ba/b",
    "1080p": "bv*[height<=1080]+ba/b[height<=1080]",
    "720p": "bv*[height<=720]+ba/b[height<=720]",
    "480p": "bv*[height<=480]+ba/b[height<=480]",
}
KNOWN_PLATFORMS = {
    "youtube.com": "YouTube", "youtu.be": "YouTube", "bilibili.com": "Bilibili",
    "b23.tv": "Bilibili", "x.com": "X", "twitter.com": "X", "vimeo.com": "Vimeo",
    "tiktok.com": "TikTok", "instagram.com": "Instagram", "facebook.com": "Facebook",
    "twitch.tv": "Twitch", "reddit.com": "Reddit",
}
WECHAT_ADAPTER = Path(__file__).with_name("wechat_adapter.py")


class SkillError(RuntimeError):
    def __init__(self, stage: str, message: str):
        super().__init__(message)
        self.stage = stage


def require_tool(name: str) -> str:
    key = name.upper().replace('-', '_')
    override = os.environ.get(f"LSF_{key}_BIN") or os.environ.get(f"QIAOMU_{key}_BIN")
    path = override or shutil.which(name)
    if not path or not Path(path).expanduser().is_file():
        raise SkillError("dependency", f"{name} not found; run doctor for installation guidance")
    return str(Path(path).expanduser())


def error_summary(completed: subprocess.CompletedProcess[str]) -> str:
    text = "\n".join(part for part in (completed.stderr, completed.stdout) if part).strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return redact(" | ".join(lines[-8:])[:1600]) or f"command exited with {completed.returncode}"


def run_command(args: list[str], stage: str, timeout: int, *, stream: bool = False) -> subprocess.CompletedProcess[str]:
    try:
        callback = (lambda line: print(redact(line), file=sys.stderr, flush=True)) if stream else None
        completed = run_process(args, timeout, on_line=callback)
    except subprocess.TimeoutExpired as exc:
        raise SkillError(stage, f"command timed out after {timeout}s; owned process tree stopped") from exc
    if completed.returncode:
        raise SkillError(stage, error_summary(completed))
    return completed


def normalize_url(raw: str) -> str:
    value = raw.strip().strip("<>[](){}\"'")
    parsed = urlsplit(value)
    if parsed.scheme.lower() != "https":
        raise SkillError("validate", "video URL must use HTTPS")
    try:
        custom_port = parsed.port
    except ValueError as exc:
        raise SkillError("validate", "video URL contains an invalid port") from exc
    if parsed.username or parsed.password or custom_port:
        raise SkillError("validate", "video URL must not contain credentials or a custom port")
    host = (parsed.hostname or "").rstrip(".").lower()
    if not host or host == "localhost" or host.endswith(".localhost"):
        raise SkillError("validate", "video URL must use a public host")
    try:
        address = ipaddress.ip_address(host.strip("[]"))
        if not address.is_global:
            raise SkillError("validate", "private, loopback, and link-local addresses are not allowed")
    except ValueError:
        pass
    if host == "weixin.qq.com" and parsed.path.startswith("/sph/") and len(parsed.path) <= len("/sph/"):
        raise SkillError("validate", "WeChat Channels URL is missing its share token")
    return urlunsplit(("https", host, parsed.path or "/", parsed.query, ""))


def platform_name(url: str) -> str:
    host = (urlsplit(url).hostname or "").lower()
    if host == "weixin.qq.com" and urlsplit(url).path.startswith("/sph/"):
        return "WeChat Channels"
    for suffix, name in KNOWN_PLATFORMS.items():
        if host == suffix or host.endswith("." + suffix):
            return name
    return "yt-dlp generic extractor"


def is_wechat_channels_url(url: str) -> bool:
    parsed = urlsplit(url)
    return (parsed.hostname or "").rstrip(".").lower() == "weixin.qq.com" and parsed.path.startswith("/sph/")


def run_wechat_adapter(url: str, output_dir: Path, timeout: int, online: str,
                       wait_page: int, single: bool) -> dict[str, Any]:
    if not WECHAT_ADAPTER.is_file():
        raise SkillError("dependency", "embedded WeChat Channels adapter is missing")
    command = [sys.executable, str(WECHAT_ADAPTER), "download", url, "--dir", str(output_dir),
               "--timeout", str(timeout), "--online", online, "--wait-page", str(max(0, wait_page))]
    if single:
        command.append("--single")
    try:
        completed = run_process(command, timeout + 30,
                                on_stderr=lambda line: print(redact(line), file=sys.stderr, flush=True))
    except subprocess.TimeoutExpired as exc:
        raise SkillError("wechat_download", f"embedded WeChat adapter timed out after {timeout}s") from exc
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise SkillError("wechat_download", "embedded WeChat adapter returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise SkillError("wechat_download", "embedded WeChat adapter returned a non-object result")
    return payload


def wechat_doctor(url: str | None = None) -> dict[str, Any]:
    if not WECHAT_ADAPTER.is_file():
        return {"ok": False, "adapter": "embedded-wechat", "error": "adapter missing"}
    command = [sys.executable, str(WECHAT_ADAPTER), "doctor"]
    if url:
        command += ["--url", url]
    completed = run_process(command, 30)
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "adapter": "embedded-wechat", "error": "doctor returned invalid JSON"}


def detect_cookie_browser(mode: str) -> str | None:
    if mode == "none":
        return None
    if mode != "auto":
        if mode.split(":", 1)[0] not in BROWSER_APPLICATIONS:
            raise SkillError("cookies", "expected none, auto, edge, chrome, firefox, safari or browser:profile")
        return mode
    if os.name == "nt":
        local = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
        roaming = Path(os.environ.get("APPDATA", Path.home() / "AppData/Roaming"))
        paths = {"edge": local / "Microsoft/Edge/User Data", "chrome": local / "Google/Chrome/User Data",
                 "firefox": roaming / "Mozilla/Firefox/Profiles"}
        return next((name for name, path in paths.items() if path.is_dir()), None)
    for browser in ("chrome", "edge", "firefox", "safari"):
        if any(Path(path).expanduser().exists() for path in BROWSER_APPLICATIONS[browser]):
            return browser
    return None


def cookie_args(browser: str | None) -> list[str]:
    return ["--cookies-from-browser", browser] if browser else []


def ffmpeg_args() -> list[str]:
    override = os.environ.get("LSF_FFMPEG_BIN") or os.environ.get("QIAOMU_FFMPEG_BIN")
    return ["--ffmpeg-location", str(Path(override).expanduser())] if override else []


def executable_version(executable: str) -> str:
    result = run_command([executable, "--version"], "dependency", 30)
    return next((line.strip() for line in result.stdout.splitlines() if line.strip()), "unknown")


def version_key(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", value)) or (0,)


def latest_ytdlp_version(timeout: int) -> str:
    request = urllib.request.Request(YT_DLP_RELEASE_API, headers={
        "Accept": "application/vnd.github+json", "User-Agent": f"qiaomu-download/{VERSION}"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            latest = str(json.loads(response.read().decode("utf-8")).get("tag_name") or "").lstrip("v")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        redirect = urllib.request.Request(YT_DLP_RELEASE_LATEST,
                                          headers={"User-Agent": f"qiaomu-download/{VERSION}"})
        try:
            with urllib.request.urlopen(redirect, timeout=timeout) as response:
                latest = urllib.parse.unquote(response.geturl().rstrip("/").rsplit("/", 1)[-1]).lstrip("v")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            raise SkillError("update-check", f"cannot read the official yt-dlp release: {exc}") from exc
    if not re.fullmatch(r"\d{4}\.\d{1,2}\.\d{1,2}(?:\.\d+)?", latest):
        raise SkillError("update-check", "official yt-dlp release returned an unexpected version")
    return latest


def optional_tool_version(name: str) -> str | None:
    try:
        executable = require_tool(name)
        result = run_command([executable, "-version"], "dependency", 30)
        return next(iter(result.stdout.splitlines()), None)
    except SkillError:
        return None


def doctor(check_updates: bool, timeout: int) -> dict[str, Any]:
    yt_dlp = require_tool("yt-dlp")
    installed = executable_version(yt_dlp)
    result = {"ok": True, "command": "doctor", "yt_dlp": {
        "executable": str(Path(yt_dlp).resolve()), "installed_version": installed,
        "update_checked": check_updates, "upgraded": False},
        "ffmpeg_version": optional_tool_version("ffmpeg"), "ffprobe_version": optional_tool_version("ffprobe"),
        "wechat_channels": wechat_doctor()}
    if check_updates:
        try:
            latest = latest_ytdlp_version(min(timeout, 30))
            result["yt_dlp"].update(latest_stable_version=latest, outdated=version_key(installed) < version_key(latest))
        except SkillError as exc:
            result["yt_dlp"]["update_error"] = redact(str(exc))
    return result


def base_args():
    args = [require_tool("yt-dlp"), "--ignore-config", "--no-playlist", "--encoding", "utf-8",
            "--retries", "3", "--fragment-retries", "3", "--socket-timeout", "20"]
    if os.name == "nt":
        args.append("--windows-filenames")
    node = shutil.which("node")
    if node and not shutil.which("deno"):
        try:
            result = run_process([node, "--version"], 10)
            if result.returncode == 0 and version_key(result.stdout)[0] >= 22:
                args += ["--js-runtimes", "node"]
        except (OSError, subprocess.TimeoutExpired):
            pass
    return args


def load_metadata_once(url: str, browser: str | None, timeout: int) -> dict[str, Any]:
    command = [*base_args(), "--dump-single-json", "--flat-playlist", "--playlist-end", "1",
               "--no-warnings", *cookie_args(browser), "--", url]
    result = run_command(command, "metadata", timeout)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SkillError("metadata", "yt-dlp returned invalid JSON") from exc
    if not isinstance(payload, dict) or payload.get("_type") in ("playlist", "multi_video") or "entries" in payload:
        raise SkillError("scope", "playlist or multi-video URL requires an explicit range; use the advanced CLI recipe")
    if payload.get("is_live") or payload.get("live_status") in ("is_live", "is_upcoming"):
        raise SkillError("scope", "live recording requires an explicit end condition; use the live CLI recipe")
    if not payload.get("id"):
        raise SkillError("metadata", "yt-dlp metadata is missing a media ID")
    return payload


def load_metadata(url: str, cookie_mode: str, timeout: int = 90) -> tuple[dict[str, Any], str | None, list[str]]:
    warnings: list[str] = []
    if cookie_mode != "auto":
        browser = detect_cookie_browser(cookie_mode)
        return load_metadata_once(url, browser, timeout), browser, warnings
    try:
        return load_metadata_once(url, None, timeout), None, warnings
    except SkillError as public_error:
        if public_error.stage != "metadata":
            raise
        browser = detect_cookie_browser("auto")
        if not browser:
            raise
        warnings.append(f"public extraction failed; retried with local {browser} cookies: {public_error}")
        return load_metadata_once(url, browser, timeout), browser, warnings


def metadata_summary(payload: dict[str, Any], source_url: str) -> dict[str, Any]:
    return {"id": payload.get("id"), "title": payload.get("title"),
            "channel": payload.get("channel") or payload.get("uploader"), "duration_seconds": payload.get("duration"),
            "width": payload.get("width"), "height": payload.get("height"),
            "extractor": payload.get("extractor_key") or payload.get("extractor"),
            "platform": platform_name(source_url), "webpage_url": payload.get("webpage_url") or source_url}


def prepare_output_dir(value: str | None) -> Path:
    output = Path(value or os.environ.get("LSF_DOWNLOAD_OUTPUT") or os.environ.get("QIAOMU_DOWNLOAD_OUTPUT") or Path.cwd() / "outputs").expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    return output


def lock_path(output_dir: Path, media_id: str, operation: str) -> Path:
    return media_lock_path(output_dir, f"{media_id}|{operation}")


@contextmanager
def download_lock(output_dir: Path, media_id: str, operation: str) -> Iterator[BinaryIO]:
    context = file_lock(lock_path(output_dir, media_id, operation))
    try:
        handle = context.__enter__()
    except OSError as exc:
        raise SkillError("lock", "this media is already downloading or the lock directory is inaccessible") from exc
    try:
        yield handle
    finally:
        context.__exit__(None, None, None)


def probe_media(path: Path, expect: str) -> dict[str, Any]:
    command = [require_tool("ffprobe"), "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height",
               "-show_entries", "format=format_name,duration,size", "-of", "json", str(path)]
    result = run_command(command, "verify", 60)
    payload = json.loads(result.stdout)
    streams = payload.get("streams") or []
    expected = "audio" if expect == "audio" else "video"
    if not any(stream.get("codec_type") == expected for stream in streams):
        raise SkillError("verify", f"{path.name} has no {expected} stream")
    duration = float((payload.get("format") or {}).get("duration") or 0)
    if duration <= 0 or path.stat().st_size <= 0:
        raise SkillError("verify", f"{path.name} has invalid duration or size")
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), {})
    return {"path": str(path.resolve()), "bytes": path.stat().st_size,
            "container": (payload.get("format") or {}).get("format_name"), "video_codec": video.get("codec_name"),
            "audio_codec": audio.get("codec_name"), "width": video.get("width"), "height": video.get("height"),
            "duration_seconds": round(duration, 3)}


def download_media(url: str, output_dir: Path, quality: str, cookie_mode: str,
                   audio_only: bool, timeout: int) -> dict[str, Any]:
    require_tool("ffmpeg"); require_tool("ffprobe")
    metadata, browser, warnings = load_metadata(url, cookie_mode, min(timeout, 120))
    media_id = str(metadata["id"])
    operation = "audio" if audio_only else "video"
    # Quality is part of the filename to keep lower-quality old files from satisfying a new request.
    template = "%(title).120B [%(id)s]" + ("-audio" if audio_only else "-" + quality) + ".%(ext)s"
    with download_lock(output_dir, media_id, operation):
        before = {p.resolve() for p in output_dir.iterdir() if p.is_file()}
        work = Path.cwd() / "work/yt-dlp"
        work.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="task-", dir=work) as temp:
            manifest = Path(temp) / "files.jsonl"
            command = [*base_args(), "--no-overwrites", "--newline", "--progress", "--progress-delta", "1",
                       *ffmpeg_args(), *cookie_args(browser), "-P", str(output_dir), "-P", f"temp:{temp}",
                       "--print-to-file", "after_move:%(filepath)j", str(manifest), "--no-simulate", "-o", template]
            command += (["-f", "ba/b", "-x", "--audio-format", "mp3", "--audio-quality", "0"] if audio_only else
                        ["-f", QUALITY_FORMATS[quality], "--merge-output-format", "mp4"])
            run_command([*command, "--", url], "download", timeout, stream=True)
            if not manifest.is_file():
                raise SkillError("download", "yt-dlp returned no final output path")
            files = list(dict.fromkeys(Path(json.loads(line)).resolve() for line in manifest.read_text(encoding="utf-8").splitlines() if line.strip()))
        if not files:
            raise SkillError("download", "no final media file was produced")
        verified = []
        expects_audio = metadata.get("acodec") not in (None, "none") or any(f.get("acodec") not in (None, "none") for f in metadata.get("formats", []))
        for path in files:
            if path.parent != output_dir.resolve() or not path.is_file():
                raise SkillError("verify", "output path is missing or outside the requested directory")
            item = probe_media(path, operation)
            if not audio_only and expects_audio and not item["audio_codec"]:
                raise SkillError("verify", "downloaded video is missing the expected audio stream")
            if not audio_only and quality != "best" and (not item["height"] or item["height"] > int(quality[:-1])):
                raise SkillError("verify", "downloaded video exceeds the requested height cap")
            item["created"] = path not in before
            verified.append(item)
    return {"ok": True, "command": operation, **metadata_summary(metadata, url), "quality": quality,
            "status": "downloaded" if any(f["created"] for f in verified) else "existing",
            "files": verified, "cookies_from_browser": browser, "warnings": warnings}


def download_subtitles(url: str, output_dir: Path, langs: str, cookie_mode: str, timeout: int) -> dict[str, Any]:
    require_tool("ffmpeg")
    metadata, browser, warnings = load_metadata(url, cookie_mode, min(timeout, 120))
    media_id = str(metadata["id"])
    work = Path.cwd() / "work/yt-dlp"
    work.mkdir(parents=True, exist_ok=True)
    files = []
    with download_lock(output_dir, media_id, "subtitles"), tempfile.TemporaryDirectory(prefix="subs-", dir=work) as temp:
        command = [*base_args(), "--no-overwrites", *ffmpeg_args(), "--write-subs", "--write-auto-subs",
                   "--sub-langs", langs, "--convert-subs", "srt", "--skip-download", *cookie_args(browser),
                   "-o", str(Path(temp) / "%(title).120B [%(id)s].%(ext)s"), "--", url]
        run_command(command, "download", timeout, stream=True)
        for path in Path(temp).glob("*.srt"):
            content = path.read_text(encoding="utf-8-sig")
            if not content.strip() or "-->" not in content:
                raise SkillError("verify", "subtitle is empty or has no timestamps")
            destination = output_dir / path.name
            created = False
            try:
                with destination.open("xb") as out:
                    out.write(path.read_bytes())
                created = True
            except FileExistsError:
                if destination.read_bytes() != path.read_bytes():
                    raise SkillError("existing", "a different subtitle already exists; choose another directory")
            files.append({"path": str(destination.resolve()), "bytes": destination.stat().st_size, "created": created})
    if not files:
        raise SkillError("download", "no requested subtitles were available")
    return {"ok": True, "command": "subtitles", **metadata_summary(metadata, url), "files": files,
            "status": "downloaded" if any(f["created"] for f in files) else "existing",
            "cookies_from_browser": browser, "warnings": warnings}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download and verify public or user-authorized online video with yt-dlp.")
    parser.add_argument("--version", action="version", version=VERSION)
    commands = parser.add_subparsers(dest="command", required=True)
    dependency = commands.add_parser("doctor")
    dependency.add_argument("--check-updates", action="store_true", help="optional read-only release check; never upgrades")
    dependency.add_argument("--timeout", type=int, default=300)
    def add_url_args(item: argparse.ArgumentParser, include_dir: bool = False) -> None:
        item.add_argument("url")
        if include_dir:
            item.add_argument("--dir", dest="output_dir")
        item.add_argument("--cookies-from-browser", default="none", help="none (default), or authorized browser[:profile]; auto permits one fallback")
        item.add_argument("--timeout", type=int, default=1200)
    info = commands.add_parser("info"); add_url_args(info)
    download = commands.add_parser("download"); add_url_args(download, True)
    download.add_argument("--quality", choices=tuple(QUALITY_FORMATS), default="best")
    download.add_argument("--wechat-online", choices=("never", "allowed"), default="never",
                          help="allow sending only the public WeChat share URL to fixed resolvers")
    download.add_argument("--wait-page", type=int, default=0,
                          help="seconds to wait for a user-operated WeChat page connection")
    download.add_argument("--single-version", action="store_true",
                          help="for WeChat Channels, save one verified codec version")
    audio = commands.add_parser("audio"); add_url_args(audio, True)
    subtitles = commands.add_parser("subtitles"); add_url_args(subtitles, True)
    subtitles.add_argument("--langs", default="en,zh-Hans,zh-Hant")
    return parser


def main() -> None:
    configure_stdio()
    args = build_parser().parse_args()
    try:
        if args.command == "doctor":
            result = doctor(args.check_updates, args.timeout)
        else:
            url = normalize_url(args.url)
            if is_wechat_channels_url(url):
                if args.command == "download":
                    if args.quality != "best":
                        raise SkillError("unsupported", "WeChat quality caps are not implemented; omit --quality and inspect actual dimensions")
                    result = run_wechat_adapter(url, prepare_output_dir(args.output_dir), args.timeout,
                                                args.wechat_online, args.wait_page, args.single_version)
                elif args.command == "info":
                    result = {"ok": True, "command": "info", "platform": "WeChat Channels",
                              "url": url, "wechat_channels": wechat_doctor(url), "ui_automation_used": False}
                else:
                    raise SkillError("unsupported", f"{args.command} is not supported for WeChat Channels links")
            elif args.command == "info":
                metadata, browser, warnings = load_metadata(url, args.cookies_from_browser, args.timeout)
                result = {"ok": True, "command": "info", **metadata_summary(metadata, url),
                          "cookies_from_browser": browser, "warnings": warnings}
            elif args.command == "download":
                result = download_media(url, prepare_output_dir(args.output_dir), args.quality,
                                        args.cookies_from_browser, False, args.timeout)
            elif args.command == "audio":
                result = download_media(url, prepare_output_dir(args.output_dir), "best",
                                        args.cookies_from_browser, True, args.timeout)
            else:
                result = download_subtitles(url, prepare_output_dir(args.output_dir), args.langs,
                                            args.cookies_from_browser, args.timeout)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if not result.get("ok", False):
            raise SystemExit(4)
    except SkillError as exc:
        print(json.dumps({"ok": False, "stage": exc.stage, "error": redact(str(exc))}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"ok": False, "stage": "runtime", "error": redact(str(exc))}, ensure_ascii=False))
        raise SystemExit(2)
    except KeyboardInterrupt:
        print(json.dumps({"ok": False, "stage": "interrupted", "error": "operation interrupted"}, ensure_ascii=False, indent=2))
        raise SystemExit(130)


if __name__ == "__main__":
    main()
