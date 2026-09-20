"""Audit a native divider-drag trace; geometry checks are not aesthetic approval."""
import argparse
import json
import math
from pathlib import Path


def audit(data, max_speed, max_contact_error):
    rows = data.get('rows', [])
    fps = data.get('fps', 0)
    if len(rows) < 3 or fps <= 0:
        raise ValueError('Need >=3 samples and positive fps')
    failures = []
    if data.get('errors'):
        failures.append('runtime_errors')
    if not all(r['frame'] == i and abs(r['time'] - i / fps) < 1e-6 for i, r in enumerate(rows)):
        failures.append('non_contiguous_samples')
    if not all(all(math.isfinite(r[k]) for k in ('x', 'y', 'dividerX', 'position')) for r in rows):
        raise ValueError('Non-finite coordinates')
    speeds = [math.hypot(b['x']-a['x'], b['y']-a['y'])*fps for a, b in zip(rows, rows[1:])]
    down = [r for r in rows if r.get('event') == 'down']
    up = [r for r in rows if r.get('event') == 'up']
    if len(down) != 1 or len(up) != 1 or down[0]['frame'] >= up[0]['frame']:
        raise ValueError('Expected one ordered down/up pair')
    d, u = down[0], up[0]
    rect = d['rect']
    if not d['hover'] or not (rect['left'] <= d['x'] <= rect['left']+rect['width'] and rect['top'] <= d['y'] <= rect['top']+rect['height']):
        failures.append('missed_native_target')
    if not all(r['images'] for r in rows):
        failures.append('unloaded_image')
    held = [r for r in rows if r['buttons'] == 1]
    if len(held) != u['frame'] - d['frame']:
        failures.append('broken_hold')
    error = max(abs(r['dividerX']-r['x']) for r in held)
    if error > max_contact_error:
        failures.append('drag_contact_error')
    if max(speeds) > max_speed:
        failures.append('cursor_speed_budget')
    if any(r['position'] != rows[0]['position'] for r in rows[:d['frame']]):
        failures.append('state_changed_before_press')
    if any(r['position'] != u['position'] for r in rows[u['frame']:]):
        failures.append('state_changed_after_release')
    if max(r['position'] for r in held)-min(r['position'] for r in held) < 20:
        failures.append('no_meaningful_drag')
    return {'passed': not failures, 'failures': failures, 'frames': len(rows), 'fps': fps,
            'peakSpeedPxPerSec': round(max(speeds), 3), 'maxContactErrorPx': round(error, 4),
            'holdSeconds': (u['frame']-d['frame'])/fps, 'finalPosition': u['position'],
            'limits': {'maxSpeedPxPerSec': max_speed, 'maxContactErrorPx': max_contact_error},
            'aestheticApproval': False, 'earAudited': False}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('trace', type=Path)
    p.add_argument('--max-speed', type=float, required=True)
    p.add_argument('--max-contact-error', type=float, required=True)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    result = audit(json.loads(args.trace.read_text(encoding='utf-8')), args.max_speed, args.max_contact_error)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    print(text)
    raise SystemExit(0 if result['passed'] else 1)
