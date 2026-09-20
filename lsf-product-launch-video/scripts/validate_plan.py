"""Validate frame intervals and sound cues, not aesthetic quality."""
import argparse
import json
import math
from pathlib import Path


def validate(plan):
    errors = []
    def positive_int(value):
        return isinstance(value, int) and not isinstance(value, bool) and value > 0
    for field in ('fps', 'durationFrames', 'width', 'height'):
        if not positive_int(plan.get(field)):
            errors.append(f'{field}: positive integer required')
    if errors:
        return errors
    total = plan['durationFrames']
    if not plan.get('scenes'):
        errors.append('scenes: at least one scene required')
    end = 0
    ids = set()
    for scene in plan.get('scenes', []):
        sid = scene.get('id')
        if not sid or sid in ids:
            errors.append('scene id missing or duplicated')
        ids.add(sid)
        start, stop = scene.get('startFrame'), scene.get('endFrame')
        if not isinstance(start, int) or not isinstance(stop, int) or start != end or stop <= start or stop > total:
            errors.append(f'{sid}: scenes must be consecutive positive intervals within duration')
        if isinstance(stop, int):
            end = stop
        for field in ('message', 'focus', 'action', 'evidence'):
            if not scene.get(field):
                errors.append(f'{sid}: missing {field}')
    if end != total:
        errors.append('scene coverage does not equal durationFrames')
    if not plan.get('events'):
        errors.append('events: at least one synchronized sound effect required')
    ids = set()
    for cue in plan.get('events', []):
        cid = cue.get('id')
        if not cid or cid in ids:
            errors.append('event id missing or duplicated')
        ids.add(cid)
        frame, duration = cue.get('frame'), cue.get('durationFrames')
        if not isinstance(frame, int) or not positive_int(duration) or frame < 0 or frame + duration > total:
            errors.append(f'{cid}: cue falls outside timeline or has invalid duration')
        if cue.get('kind') not in ('click', 'swish', 'thump', 'chime', 'soft', 'air', 'tap', 'sweep', 'type', 'bloom', 'connect', 'drag', 'rise', 'resolve'):
            errors.append(f'{cid}: unsupported sound kind')
        for field, low, high in (('gain', 0, 1), ('pan', -1, 1)):
            val = cue.get(field)
            if not isinstance(val, (int, float)) or not math.isfinite(val) or not low <= val <= high:
                errors.append(f'{cid}: invalid {field}')
        if not cue.get('visual'):
            errors.append(f'{cid}: missing visual event description')
    music = plan.get('music', {})
    if music.get('enabled'):
        if not isinstance(music.get('bpm'), (int, float)) or not 30 <= music['bpm'] <= 240:
            errors.append('music.bpm must be between 30 and 240')
        if not isinstance(music.get('gain'), (int, float)) or not 0 <= music['gain'] <= 1:
            errors.append('music.gain must be between 0 and 1')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    result = validate(json.loads(args.plan.read_text(encoding='utf-8-sig')))
    print(json.dumps({'ok': not result, 'errors': result}, ensure_ascii=True, indent=2))
    raise SystemExit(1 if result else 0)
