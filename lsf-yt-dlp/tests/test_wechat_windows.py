import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS / 'wechat'))
import download_online as online
import install_backend as installer
from runtime import run_process


class WeChatWindowsTests(unittest.TestCase):
    def test_online_cli_cannot_send_url_without_authorization(self):
        with patch.object(sys, 'argv', ['online', '--url', 'https://weixin.qq.com/sph/fixture']), \
             patch.object(online, 'attempt_worker') as worker, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as exit:
                online.main()
            self.assertEqual(exit.exception.code, 2)
            self.assertIn('consent_required', output.getvalue())
            worker.assert_not_called()

    def test_resolver_and_media_redirects_reject_before_following(self):
        with self.assertRaises(online.OnlineDownloadError):
            online.NoResolverRedirect().redirect_request(None, None, 307, '', {}, 'https://another.example')
        for url in ('http://qq.com/v', 'https://evil.example/v', 'https://u:p@qq.com/v'):
            with self.assertRaises(online.OnlineDownloadError):
                online.AllowedMediaRedirect().redirect_request(None, None, 302, '', {}, url)

    def test_online_partial_transfer_never_reaches_probe(self):
        class Response(io.BytesIO):
            status = 200
            headers = {'Content-Length': '12'}
            def geturl(self):
                return 'https://media.qq.com/v'
        class Opener:
            def open(self, *args, **kwargs):
                return Response(b'abc')
        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(online.urllib.request, 'build_opener', return_value=Opener()), \
             patch.object(online, 'probe_video') as probe:
            with self.assertRaises(online.OnlineDownloadError):
                online.download_to_stage('https://media.qq.com/v', Path(tmp), 3)
            probe.assert_not_called()
            self.assertFalse(list(Path(tmp).iterdir()))

    def test_online_result_uses_verified_codec_and_never_overwrites(self):
        payload = {'data': {'feedInfo': {'description': '示例', 'h264VideoInfo': {'videoUrl': 'https://media.qq.com/v'}}}}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '示例_hevc.mp4').write_bytes(b'old')
            staged = root / 'new.part'
            staged.write_bytes(b'new')
            with patch.object(online, 'post_profile', return_value=payload), \
                 patch.object(online, 'download_to_stage', return_value=(staged, {'codec': 'hevc', 'verification': 'full-decode'})):
                result = online.attempt_worker('fixture', 'https://example.invalid', 'https://weixin.qq.com/sph/f', root, 'best', 3, False)
            self.assertEqual((root / '示例_hevc.mp4').read_bytes(), b'old')
            self.assertEqual(Path(result['files'][0]['path']).read_bytes(), b'new')
            self.assertEqual(result['files'][0]['codec'], 'hevc')
            self.assertIn('hevc', result['files'][0]['path'])

    def test_windows_archive_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('../outside', '..\\outside', 'C:\\outside', '\\\\host\\share\\file', 'file:stream'):
                with self.assertRaises(ValueError, msg=name):
                    installer.safe_target(root, name)
            archive = root / 'fixture.zip'
            with zipfile.ZipFile(archive, 'w') as out:
                out.writestr('..\\escape.txt', 'data')
            with self.assertRaises(ValueError):
                installer.extract(archive, root / 'target')

    def test_windows_platform_alias(self):
        with patch.object(installer.platform, 'system', return_value='Windows'), \
             patch.object(installer.platform, 'machine', return_value='AMD64'):
            self.assertEqual(installer.platform_key(), 'windows-x86_64')

    def test_modified_installed_backend_is_not_accepted_as_cached(self):
        lock = json.loads((SCRIPTS / 'wechat/release-lock.json').read_text(encoding='utf-8'))
        key = 'windows-x86_64'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            destination = root / 'backend' / (lock['tag'] + '-' + key)
            destination.mkdir(parents=True)
            exe = destination / 'fixture.exe'
            exe.write_bytes(b'original')
            marker = {'archive_sha256': lock['assets'][key]['sha256'], 'platform': key,
                      'files': {'fixture.exe': installer.sha256(exe)}}
            (destination / '.qiaomu-install.json').write_text(json.dumps(marker), encoding='utf-8')
            exe.write_bytes(b'modified')
            argv = ['installer', '--accept-upstream-license', '--install-root', str(root), '--platform', key]
            with patch.object(sys, 'argv', argv), patch.object(installer.urllib.request, 'urlopen') as network:
                with self.assertRaises(SystemExit) as exit:
                    installer.main()
                self.assertIn('refusing to overwrite', str(exit.exception))
                network.assert_not_called()


if __name__ == '__main__':
    unittest.main()
