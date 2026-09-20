"""Windows-aware process, lock and output helpers. Standard library only."""
from __future__ import annotations

from collections import deque
from contextlib import contextmanager
import ctypes
import hashlib
import os
from pathlib import Path
import queue
import re
import signal
import subprocess
import sys
import threading
import time


def configure_stdio():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')


def redact(text):
    text = re.sub(r'https?://[^\s<>"\']+', '[URL omitted]', str(text))
    return re.sub(r'(?i)(cookie|authorization|decodekey|token|password)\s*[:=].*', r'\1=[redacted]', text)


def wechat_home():
    configured = os.environ.get('LSF_WX_VIDEO_HOME') or os.environ.get('QIAOMU_WX_VIDEO_HOME')
    if configured:
        return Path(configured).expanduser().resolve()
    if os.name == 'nt':
        return Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData/Local')) / 'lsf-yt-dlp/wechat'
    return Path.home() / '.local/share/lsf-yt-dlp/wechat'


class WindowsJob:
    """Own only this command's process tree; closing the job kills descendants."""
    def __init__(self):
        from ctypes import wintypes as w
        class Limits(ctypes.Structure):
            _fields_ = [('process_time', ctypes.c_int64), ('job_time', ctypes.c_int64),
                        ('flags', w.DWORD), ('min_working_set', ctypes.c_size_t),
                        ('max_working_set', ctypes.c_size_t), ('active_processes', w.DWORD),
                        ('affinity', ctypes.c_size_t), ('priority', w.DWORD), ('scheduling', w.DWORD)]
        class IO(ctypes.Structure):
            _fields_ = [(name, ctypes.c_uint64) for name in ('read_ops', 'write_ops', 'other_ops', 'read_bytes', 'write_bytes', 'other_bytes')]
        class Extended(ctypes.Structure):
            _fields_ = [('basic', Limits), ('io', IO), ('process_memory', ctypes.c_size_t),
                        ('job_memory', ctypes.c_size_t), ('peak_process', ctypes.c_size_t), ('peak_job', ctypes.c_size_t)]
        self.api = ctypes.WinDLL('kernel32', use_last_error=True)
        self.api.CreateJobObjectW.argtypes = [ctypes.c_void_p, w.LPCWSTR]
        self.api.CreateJobObjectW.restype = w.HANDLE
        self.api.SetInformationJobObject.argtypes = [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD]
        self.api.SetInformationJobObject.restype = w.BOOL
        self.api.AssignProcessToJobObject.argtypes = [w.HANDLE, w.HANDLE]
        self.api.AssignProcessToJobObject.restype = w.BOOL
        self.api.CloseHandle.argtypes = [w.HANDLE]
        self.api.CloseHandle.restype = w.BOOL
        self.handle = self.api.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = Extended()
        limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.api.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            error = ctypes.get_last_error()
            self.close()
            raise ctypes.WinError(error)

    def assign(self, process):
        if not self.api.AssignProcessToJobObject(self.handle, int(process._handle)):
            raise ctypes.WinError(ctypes.get_last_error())

    def close(self):
        if self.handle:
            self.api.CloseHandle(self.handle)
            self.handle = None


def run_process(args, timeout=120, *, on_line=None, on_stderr=None, env=None):
    """UTF-8 capture with bounded diagnostic tail for streaming commands."""
    child_env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    if env:
        child_env.update(env)
    job = WindowsJob() if os.name == 'nt' else None
    process = None
    readers = []
    try:
        process = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace',
                                   env=child_env, start_new_session=os.name == 'posix',
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        if job:
            job.assign(process)
        lines = queue.Queue(maxsize=256)
        stop = threading.Event()
        def read(pipe, channel):
            try:
                for line in pipe:
                    while not stop.is_set():
                        try:
                            lines.put((channel, line), timeout=0.1)
                            break
                        except queue.Full:
                            continue
                    if stop.is_set():
                        break
            finally:
                while not stop.is_set():
                    try:
                        lines.put((channel, None), timeout=0.1)
                        break
                    except queue.Full:
                        continue
        for channel, pipe in enumerate((process.stdout, process.stderr)):
            reader = threading.Thread(target=read, args=(pipe, channel), daemon=True)
            readers.append(reader)
            reader.start()
        output = [deque(maxlen=500) if on_line else [], deque(maxlen=500)]
        ended = 0
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise subprocess.TimeoutExpired('managed command', timeout)
            try:
                channel, line = lines.get(timeout=min(0.1, remaining))
            except queue.Empty:
                continue
            if line is None:
                ended += 1
                if ended == 2:
                    break
                continue
            output[channel].append(line)
            if on_line:
                on_line(line.rstrip())
            if channel == 1 and on_stderr:
                on_stderr(line.rstrip())
        code = process.wait(timeout=max(0.01, deadline - time.monotonic()))
        return subprocess.CompletedProcess(args, code, ''.join(output[0]), ''.join(output[1]))
    finally:
        if readers:
            stop.set()
        if job:
            job.close()
        elif process:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        if process:
            if process.poll() is None:
                process.kill()
            process.wait()
            for reader in readers:
                reader.join(timeout=2)
            if process.stdout:
                process.stdout.close()
            if process.stderr:
                process.stderr.close()


@contextmanager
def file_lock(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open('a+b')
    acquired = False
    try:
        if path.stat().st_size == 0:
            handle.write(b'0')
            handle.flush()
        handle.seek(0)
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        acquired = True
        yield handle
    finally:
        if acquired:
            handle.seek(0)
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


def media_lock_path(output, identity):
    normalized = os.path.normcase(str(output.resolve()))
    key = hashlib.sha256(f'{normalized}|{identity}'.encode()).hexdigest()
    # Fixed per-user location so callers with different cwd share the same lock.
    root = wechat_home().parent if os.name == 'nt' else Path.home() / '.cache/lsf-yt-dlp'
    return root / 'locks' / f'{key}.lock'


def publish_no_overwrite(temp, output, stem, suffix='.mp4'):
    for number in range(10000):
        dest = output / (stem + (f' ({number})' if number else '') + suffix)
        try:
            if os.name == 'nt':
                os.rename(temp, dest)  # Windows rename fails if destination exists, including exFAT.
            else:
                os.link(temp, dest)
                temp.unlink()
            return dest
        except FileExistsError:
            continue
    raise RuntimeError('too many existing filenames')
