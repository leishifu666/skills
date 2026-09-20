#!/usr/bin/env python3
"""Unit tests for qiaomu-download."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_INTERFACE = "internal-module"

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "download.py"
SPEC = importlib.util.spec_from_file_location("qiaomu_download", MODULE_PATH)
assert SPEC and SPEC.loader
download = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(download)


class DownloadSkillTests(unittest.TestCase):
    def test_accepts_supported_public_https_urls(self) -> None:
        for url in ("https://x.com/a/status/1", "https://www.bilibili.com/video/BV1x", "https://youtu.be/abcdefghijk"):
            self.assertEqual(download.normalize_url(url), url)

    def test_rejects_non_https_and_private_targets(self) -> None:
        for url in ("http://x.com/a/status/1", "https://localhost/a", "https://127.0.0.1/video", "https://user:pass@x.com/a"):
            with self.assertRaises(download.SkillError):
                download.normalize_url(url)

    def test_accepts_wechat_for_embedded_adapter(self) -> None:
        url = "https://weixin.qq.com/sph/abc"
        self.assertEqual(download.normalize_url(url), url)
        self.assertTrue(download.is_wechat_channels_url(url))
        self.assertEqual(download.platform_name(url), "WeChat Channels")

    def test_rejects_wechat_without_share_token(self) -> None:
        with self.assertRaises(download.SkillError) as caught:
            download.normalize_url("https://weixin.qq.com/sph/")
        self.assertEqual(caught.exception.stage, "validate")

    def test_platform_detection(self) -> None:
        self.assertEqual(download.platform_name("https://m.youtube.com/watch?v=x"), "YouTube")
        self.assertEqual(download.platform_name("https://www.bilibili.com/video/x"), "Bilibili")
        self.assertEqual(download.platform_name("https://x.com/a/status/1"), "X")
        self.assertEqual(download.platform_name("https://example.com/video"), "yt-dlp generic extractor")

    def test_quality_presets_do_not_fall_back_without_cap(self) -> None:
        for quality in ("1080p", "720p", "480p"):
            self.assertNotIn("/bv*+ba/b", download.QUALITY_FORMATS[quality])

    def test_auto_cookie_is_public_first(self) -> None:
        with patch.object(download, "load_metadata_once", return_value={"id": "x"}) as loader:
            payload, browser, warnings = download.load_metadata("https://x.com/a/status/1", "auto")
        self.assertEqual(payload["id"], "x")
        self.assertIsNone(browser)
        self.assertEqual(warnings, [])
        loader.assert_called_once_with("https://x.com/a/status/1", None, 90)

    def test_auto_cookie_falls_back_after_public_failure(self) -> None:
        with patch.object(download, "detect_cookie_browser", return_value="chrome"), patch.object(
            download, "load_metadata_once", side_effect=[download.SkillError("metadata", "blocked"), {"id": "x"}]
        ) as loader:
            payload, browser, warnings = download.load_metadata("https://x.com/a/status/1", "auto")
        self.assertEqual(payload["id"], "x")
        self.assertEqual(browser, "chrome")
        self.assertEqual(len(warnings), 1)
        self.assertEqual(loader.call_count, 2)

    def test_old_subtitles_cannot_turn_missing_subtitles_into_success(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old = root / "Title [id].en.srt"
            old.write_text('old subtitle', encoding='utf-8')
            with patch.object(download, 'require_tool', return_value='ffmpeg'), \
                 patch.object(download, 'base_args', return_value=['yt-dlp']), \
                 patch.object(download, 'load_metadata', return_value=({'id': 'id'}, None, [])), \
                 patch.object(download, 'run_command'):
                with self.assertRaises(download.SkillError):
                    download.download_subtitles('https://example.com/v', root, 'zh-Hans', 'none', 5)
            self.assertEqual(old.read_text(encoding='utf-8'), 'old subtitle')

    def test_new_subtitles_never_overwrite_different_existing_subtitles(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old = root / 'Title [id].en.srt'
            old.write_bytes(b'old')
            def produce(args, *pos, **kw):
                output = Path(args[args.index('-o') + 1]).parent / old.name
                output.write_text('1\n00:00:00,000 --> 00:00:01,000\nnew\n', encoding='utf-8')
            with patch.object(download, 'require_tool', return_value='ffmpeg'), \
                 patch.object(download, 'base_args', return_value=['yt-dlp']), \
                 patch.object(download, 'load_metadata', return_value=({'id': 'id'}, None, [])), \
                 patch.object(download, 'run_command', side_effect=produce):
                with self.assertRaises(download.SkillError) as error:
                    download.download_subtitles('https://example.com/v', root, 'en', 'none', 5)
                self.assertEqual(error.exception.stage, 'existing')
            self.assertEqual(old.read_bytes(), b'old')

    @patch.object(download, "optional_tool_version", return_value="available")
    @patch.object(download, "latest_ytdlp_version", return_value="2026.09.18")
    @patch.object(download, "executable_version", return_value="2026.09.18")
    @patch.object(download, "require_tool", return_value="/tmp/yt-dlp")
    def test_doctor_reports_current_version(self, *_mocks) -> None:
        result = download.doctor(False, 30)
        self.assertFalse(result["yt_dlp"]["update_checked"])
        self.assertFalse(result["yt_dlp"]["upgraded"])

    def test_cli_help_has_required_commands(self) -> None:
        parser = download.build_parser()
        help_text = parser.format_help()
        for command in ("doctor", "info", "download", "audio", "subtitles"):
            self.assertIn(command, help_text)

    def test_wechat_adapter_result_is_forwarded(self) -> None:
        payload = {"ok": True, "platform": "WeChat Channels", "files": [{"path": "/tmp/video.mp4"}]}
        completed = download.subprocess.CompletedProcess([], 0, json.dumps(payload), "")
        with patch.object(download, "run_process", return_value=completed):
            result = download.run_wechat_adapter(
                "https://weixin.qq.com/sph/abc", Path("/tmp"), 30, "never", 0, False
            )
        self.assertEqual(result, payload)


if __name__ == "__main__":
    unittest.main(verbosity=2)
