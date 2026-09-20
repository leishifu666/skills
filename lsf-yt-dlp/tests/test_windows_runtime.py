import ctypes
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import runtime
import download
import wechat_adapter


class RuntimeTests(unittest.TestCase):
    def test_utf8_output_and_stderr_are_separate(self):
        result = runtime.run_process([sys.executable, '-c', "import sys; print('中文路径'); print('进度', file=sys.stderr)"], 10)
        self.assertEqual(result.returncode, 0)
        self.assertIn('中文路径', result.stdout)
        self.assertNotIn('进度', result.stdout)
        self.assertIn('进度', result.stderr)

    def test_progress_arrives_before_process_finishes(self):
        seen = []
        started = time.monotonic()
        result = runtime.run_process([sys.executable, '-c', "import time; print('first', flush=True); time.sleep(1); print('last')"], 5,
                                     on_line=lambda line: seen.append((line, time.monotonic() - started)))
        self.assertEqual(result.returncode, 0)
        self.assertEqual([x[0] for x in seen], ['first', 'last'])
        self.assertGreater(seen[1][1] - seen[0][1], 0.7)

    def test_lock_blocks_second_process_and_releases(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / '锁.lock'
            child = "import sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); from runtime import file_lock\nwith file_lock(Path(sys.argv[2])): print('acquired')"
            with runtime.file_lock(path):
                result = runtime.run_process([sys.executable, '-c', child, str(SCRIPTS), str(path)], 10)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('acquired', result.stdout)
            result = runtime.run_process([sys.executable, '-c', child, str(SCRIPTS), str(path)], 10)
            self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(os.name == 'nt', 'Windows Job Object test')
    def test_timeout_kills_grandchild(self):
        lines = []
        code = "import subprocess, sys, time; p=subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)']); print(p.pid, flush=True); time.sleep(60)"
        with self.assertRaises(subprocess.TimeoutExpired):
            runtime.run_process([sys.executable, '-c', code], 1, on_line=lines.append)
        self.assertTrue(lines)
        pid = int(lines[0])
        from ctypes import wintypes as w
        api = ctypes.WinDLL('kernel32', use_last_error=True)
        api.OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]
        api.OpenProcess.restype = w.HANDLE
        api.WaitForSingleObject.argtypes = [w.HANDLE, w.DWORD]
        api.WaitForSingleObject.restype = w.DWORD
        api.CloseHandle.argtypes = [w.HANDLE]
        handle = api.OpenProcess(0x00100000, False, pid)
        if handle:
            try:
                self.assertEqual(api.WaitForSingleObject(handle, 3000), 0)
            finally:
                api.CloseHandle(handle)

    def test_atomic_publish_preserves_previous_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '视频.mp4').write_bytes(b'old')
            staged = root / 'new.partial'
            staged.write_bytes(b'new')
            result = runtime.publish_no_overwrite(staged, root, '视频')
            self.assertNotEqual(result.name, '视频.mp4')
            self.assertEqual(result.read_bytes(), b'new')
            self.assertEqual((root / '视频.mp4').read_bytes(), b'old')

    def test_logs_redact_signed_urls_and_tokens(self):
        value = runtime.redact('failed https://cdn.example/video?sign=secret\nCookie: private\ndecodeKey=123')
        for secret in ('secret', 'private', '123'):
            self.assertNotIn(secret, value)

    @unittest.skipUnless(os.name == 'nt', 'Windows profile paths')
    def test_windows_browser_discovery(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'LOCALAPPDATA': tmp, 'APPDATA': tmp}):
            (Path(tmp) / 'Microsoft/Edge/User Data').mkdir(parents=True)
            self.assertEqual(download.detect_cookie_browser('auto'), 'edge')
            self.assertIsNone(download.detect_cookie_browser('none'))

    def test_cookie_and_update_defaults_are_off(self):
        args = download.build_parser().parse_args(['download', 'https://example.com/v'])
        self.assertEqual(args.cookies_from_browser, 'none')
        with patch.object(download, 'require_tool', return_value=sys.executable), \
             patch.object(download, 'executable_version', return_value='2026.07.04'), \
             patch.object(download, 'optional_tool_version', return_value='available'), \
             patch.object(download, 'latest_ytdlp_version') as latest:
            result = download.doctor(False, 5)
            latest.assert_not_called()
            self.assertFalse(result['yt_dlp']['update_checked'])

    def test_scope_errors_never_retry_with_cookies(self):
        payload = {'id': 'playlist', '_type': 'playlist', 'entries': [{'id': 'one'}]}
        result = subprocess.CompletedProcess([], 0, json.dumps(payload), '')
        with patch.object(download, 'base_args', return_value=['yt-dlp']), \
             patch.object(download, 'run_command', return_value=result) as run, \
             patch.object(download, 'detect_cookie_browser') as cookie:
            with self.assertRaises(download.SkillError) as error:
                download.load_metadata('https://example.com/playlist', 'auto')
            self.assertEqual(error.exception.stage, 'scope')
            self.assertEqual(run.call_count, 1)
            cookie.assert_not_called()

    def test_configure_records_paths_without_running_backend(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            files = [root / name for name in ('后端.exe', '配置.yaml', 'ffmpeg.exe')]
            for file in files:
                file.write_text('fixture', encoding='utf-8')
            with patch.dict(os.environ, {'LSF_WX_VIDEO_HOME': str(root / 'settings')}), \
                 patch.object(wechat_adapter, 'run_component') as run:
                result = wechat_adapter.configure(*files)
                self.assertTrue(result['ok'])
                self.assertEqual(wechat_adapter.local_settings()['backend'], str(files[0].resolve()))
                self.assertFalse(result['started_backend'])
                run.assert_not_called()
                with self.assertRaises(ValueError):
                    wechat_adapter.configure(files[2], files[1], files[0])


if __name__ == '__main__':
    unittest.main()
