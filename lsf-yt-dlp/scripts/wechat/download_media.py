#!/usr/bin/env python3
"""Capture via an already connected local API; download/verify without operating WeChat.

Never starts a server, changes proxy settings, installs certificates, or operates UI.
JSONL output contains progress/results, never signed URLs, cookies or decode keys.
"""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime import configure_stdio, publish_no_overwrite, run_process, wechat_home
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

from preflight import normalize_url


def emit(event, **fields):
    print(json.dumps({'event': event, **fields}, ensure_ascii=False), flush=True)


def validate_api(api):
    p = urllib.parse.urlsplit(api)
    if p.scheme != 'http' or p.hostname not in ('127.0.0.1', 'localhost', '::1') or p.username or p.password or p.query or p.fragment:
        raise ValueError('API must be a local HTTP endpoint')
    return api.rstrip('/')


def profile_from_response(response):
    if response.get('code') != 0:
        raise RuntimeError('local API unavailable')
    payload = response.get('data') or {}
    if payload.get('errCode') != 0:
        raise RuntimeError('feed response error: ' + str(payload.get('errCode')))
    obj = (payload.get('data') or {}).get('object') or {}
    desc = obj.get('objectDesc') or {}
    media = desc.get('media') or []
    if not media or not media[0].get('url'):
        raise RuntimeError('feed contains no downloadable media')
    # Store only download fields, never account/login/full response data.
    fields = ('url', 'urlToken', 'decodeKey', 'spec', 'videoPlayLen', 'width', 'height')
    return {'title': desc.get('description', ''),
            'media': [{k: m[k] for k in fields if k in m} for m in media]}


def capture(url, api, timeout):
    endpoint = api + '/api/channels/feed/profile?' + urllib.parse.urlencode({'url': normalize_url(url)})
    deadline = time.monotonic() + timeout
    announced = False
    while True:
        # No OS/system proxy for loopback requests.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        try:
            with opener.open(endpoint, timeout=15) as r:
                response = json.load(r)
        except (urllib.error.URLError, TimeoutError):
            raise RuntimeError('local API not reachable; check backend before asking user to refresh') from None
        if response.get('code') == 0:
            return profile_from_response(response)
        if 'socket' not in str(response.get('msg', '')).lower():
            raise RuntimeError('local API rejected request: code ' + str(response.get('code')))
        if not announced:
            emit('manual_action_needed', action='请手动刷新一个视频号页面并播放一次，无需点击下载按钮')
            announced = True
        if time.monotonic() >= deadline:
            raise RuntimeError('page connection timeout; restore proxy and stop owned backend')
        time.sleep(min(3, max(0, deadline - time.monotonic())))


def media_url(media, spec):
    # Preserve EVERY signed parameter, including sign, basedata and svrnonce.
    url = media['url'] + media.get('urlToken', '')
    p = urllib.parse.urlsplit(url)
    if p.scheme != 'https' or not p.hostname or p.username or p.password:
        raise ValueError('media must be an HTTPS URL without credentials')
    if not spec:
        return url
    # Do not parse/re-encode signatures; only replace the quality parameter.
    query = '&'.join(part for part in p.query.split('&')
                     if urllib.parse.unquote_plus(part.split('=', 1)[0]) != 'X-snsvideoflag')
    query += ('&' if query else '') + 'X-snsvideoflag=' + urllib.parse.quote(spec, safe='')
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path, query, p.fragment))


class HTTPSOnly(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        p = urllib.parse.urlsplit(newurl)
        if p.scheme != 'https' or p.username or p.password:
            raise ValueError('refusing unsafe media redirect')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_bytes(url, path, spec):
    opener = urllib.request.build_opener(HTTPSOnly())
    with opener.open(url, timeout=30) as response, path.open('wb') as out:
        if response.status != 200:
            raise RuntimeError('unexpected media HTTP status')
        total = int(response.headers.get('Content-Length') or 0)
        downloaded = 0
        last = 0
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            out.write(block)
            downloaded += len(block)
            if time.monotonic() - last >= 2:
                emit('progress', spec=spec, bytes=downloaded, total=total or None)
                last = time.monotonic()
        if downloaded == 0 or (total and downloaded != total):
            raise RuntimeError('incomplete media transfer')


def verify(path, ffmpeg):
    ffprobe = shutil.which('ffprobe')
    if not ffprobe:
        sibling = Path(ffmpeg).with_name('ffprobe.exe' if os.name == 'nt' else 'ffprobe')
        ffprobe = str(sibling) if sibling.is_file() else None
    if not ffprobe:
        raise RuntimeError('ffprobe is required for verification')
    metadata = run_process([ffprobe, '-v', 'error', '-show_entries',
                            'stream=codec_type,codec_name,width,height:format=duration', '-of', 'json', str(path)], 60)
    if metadata.returncode:
        raise RuntimeError('ffprobe failed')
    payload = json.loads(metadata.stdout)
    video = next((v for v in payload.get('streams', []) if v.get('codec_type') == 'video'), {})
    duration = float(payload.get('format', {}).get('duration') or 0)
    if not video.get('width') or not video.get('height') or duration <= 0 or path.stat().st_size <= 0:
        raise RuntimeError('no valid video stream or duration')
    decoded = run_process([ffmpeg, '-hide_banner', '-v', 'error', '-nostdin', '-xerror', '-i', str(path),
                           '-map', '0:v:0', '-map', '0:a?', '-f', 'null', '-'], 600)
    if decoded.returncode:
        raise RuntimeError('full media decode validation failed')
    return dict(codec=video['codec_name'], width=video['width'], height=video['height'],
                duration_seconds=duration, bytes=path.stat().st_size)


def safe_name(title):
    s = re.sub(r'[\x00-\x1f/\\:*?"<>|#]', ' ', title)
    s = re.sub(r'\s+', ' ', s).strip(' .')
    return s[:48].rstrip(' .') or '视频号视频'


def publish(temp, output, stem):
    return publish_no_overwrite(temp, output, stem)


def candidate(media, spec, args):
    fd, name = tempfile.mkstemp(prefix='.wx-download-', suffix='.partial', dir=args.output)
    os.close(fd)
    path = Path(name)
    try:
        fetch_bytes(media_url(media, spec), path, spec)
        key = int(media.get('decodeKey') or 0)
        if key:
            command = [str(args.backend), '--config', str(args.config), 'decrypt',
                       '--filepath', str(path), '--key', str(key)]
            r = run_process(command, 120)
            if r.returncode or '解密完成' not in r.stdout:
                raise RuntimeError('local decrypt failed')
        return path, verify(path, args.ffmpeg)
    except BaseException:
        path.unlink(missing_ok=True)
        raise


def choose_specs(media, single):
    values = list(dict.fromkeys(s['fileFormat'] for s in media.get('spec', []) if s.get('fileFormat')))
    if not values:
        return ['']
    first = 'xWT111' if 'xWT111' in values else values[0]
    if single:
        return [first]
    # These two HEVC candidates were observed, not guaranteed codec mappings.
    extra = [s for s in ('xWT126', 'xWT156') if s in values]
    extra += [s for s in values if s != first and s not in extra]
    return [first] + extra[:3]


def download(profile, args):
    if len(profile['media']) != 1:
        raise RuntimeError('multi-media feed needs explicit handling')
    media = profile['media'][0]
    specs = choose_specs(media, args.single)
    seen, outputs = set(), []
    # At most two concurrent transfers. Try additional candidates only if a codec is missing.
    for offset in range(0, len(specs), 2):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            jobs = [(s, pool.submit(candidate, media, s, args)) for s in specs[offset:offset + 2]]
            for spec, job in jobs:
                try:
                    temp, info = job.result()
                except Exception as exc:
                    # Exception strings may contain signed media URLs: do not log them.
                    emit('candidate_failed', spec=spec, reason=type(exc).__name__)
                    continue
                try:
                    if info['codec'] in seen:
                        continue
                    label = {'h264': '高清兼容版_H264', 'hevc': '省空间版_H265'}.get(info['codec'], info['codec'])
                    dest = publish(temp, args.output, safe_name(args.name or profile['title']) + '_' + label)
                    seen.add(info['codec'])
                    info.update(path=str(dest), spec=spec)
                    outputs.append(info)
                    emit('saved', **info)
                finally:
                    temp.unlink(missing_ok=True)
        if args.single or {'h264', 'hevc'} <= seen:
            break
    if not outputs:
        raise RuntimeError('no candidate downloaded and verified')
    return outputs


def main():
    configure_stdio()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--url', required=True, help='One explicitly requested share URL')
    p.add_argument('--api', default='http://127.0.0.1:2022')
    p.add_argument('--wait-page', type=int, default=0)
    p.add_argument('--backend', type=Path, required=True)
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('--ffmpeg', default=shutil.which('ffmpeg'))
    p.add_argument('--output', type=Path, default=Path.cwd() / 'outputs')
    p.add_argument('--name')
    p.add_argument('--single', action='store_true')
    args = p.parse_args()
    try:
        args.api = validate_api(args.api)
        if not all(value and Path(value).is_file() for value in (args.backend, args.config, args.ffmpeg)):
            raise ValueError('backend, config and ffmpeg must be existing files')
        args.output = args.output.expanduser().resolve()
        profile = capture(args.url, args.api, max(0, args.wait_page))
        args.output.mkdir(parents=True, exist_ok=True)
        download(profile, args)
        return 0
    except KeyboardInterrupt:
        emit('interrupted', action='owned download stopped; existing backend and proxy untouched')
        return 130
    except Exception as exc:
        emit('failed', reason=type(exc).__name__, action='check local backend and configuration')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
