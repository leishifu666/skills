"""Real yt-dlp/FFmpeg pipeline using generated media served only on loopback."""
import contextlib
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import io
import os
from pathlib import Path
import shutil
import sys
import tempfile
import threading
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import download
from runtime import run_process
sys.path.insert(0, str(SCRIPTS / 'wechat'))
import download_media
import download_online


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@unittest.skipUnless(all(shutil.which(x) for x in ('yt-dlp', 'ffmpeg', 'ffprobe')), 'requires actual media tools')
class MediaPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        work = Path.cwd() / 'work'
        work.mkdir(exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(prefix='媒体验证-', dir=work)
        cls.root = Path(cls.temp.name).resolve()
        cls.media = cls.root / 'sample.mp4'
        result = run_process([shutil.which('ffmpeg'), '-hide_banner', '-loglevel', 'error', '-nostdin',
                              '-f', 'lavfi', '-i', 'color=c=blue:s=1280x720:r=10',
                              '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=44100',
                              '-t', '1', '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
                              '-c:a', 'aac', '-movflags', '+faststart', str(cls.media)], 30)
        if result.returncode:
            raise RuntimeError(result.stderr)
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(cls.root)))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}/sample.mp4'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.temp.cleanup()

    def test_real_download_chinese_path_and_existing_file(self):
        output = self.root / '中文 输出'
        output.mkdir()
        with contextlib.redirect_stderr(io.StringIO()):
            first = download.download_media(self.url, output, 'best', 'none', False, 60)
            second = download.download_media(self.url, output, 'best', 'none', False, 60)
        self.assertTrue(first['ok'])
        self.assertEqual(first['status'], 'downloaded')
        self.assertEqual(first['files'][0]['height'], 720)
        self.assertEqual(first['files'][0]['audio_codec'], 'aac')
        self.assertEqual(second['status'], 'existing')
        self.assertFalse(second['files'][0]['created'])
        self.assertEqual(first['files'][0]['path'], second['files'][0]['path'])

    def test_real_quality_cap_rejects_720p_when_480p_requested(self):
        output = self.root / '上限'
        output.mkdir()
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(download.SkillError):
            download.download_media(self.url, output, '480p', 'none', False, 60)
        self.assertFalse(list(output.glob('*.mp4')))

    def test_real_mp3_extraction(self):
        output = self.root / '音频'
        output.mkdir()
        with contextlib.redirect_stderr(io.StringIO()):
            result = download.download_media(self.url, output, 'best', 'none', True, 60)
        self.assertEqual(result['files'][0]['audio_codec'], 'mp3')
        self.assertGreater(result['files'][0]['duration_seconds'], 0)

    def test_wechat_full_decode_checks_real_media(self):
        result = download_media.verify(self.media, shutil.which('ffmpeg'))
        self.assertEqual(result['codec'], 'h264')
        self.assertEqual(result['height'], 720)
        online = download_online.probe_video(self.media)
        self.assertEqual(online['verification'], 'full-decode')
        broken = self.root / 'broken.mp4'
        broken.write_bytes(b'fake ftyp')
        with self.assertRaises(RuntimeError):
            download_media.verify(broken, shutil.which('ffmpeg'))


if __name__ == '__main__':
    unittest.main()
