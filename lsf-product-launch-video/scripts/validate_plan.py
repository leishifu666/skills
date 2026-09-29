"""Check plan structure and review declarations, never aesthetic approval."""
import argparse
import json
import math
from pathlib import Path


def _validate_timeline(plan):
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
        if not integer(start) or not integer(stop) or start != end or stop <= start or stop > total:
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
        if not integer(frame) or not positive_int(duration) or frame < 0 or frame + duration > total:
            errors.append(f'{cid}: cue falls outside timeline or has invalid duration')
        if cue.get('kind') not in ('click', 'swish', 'thump', 'chime', 'soft', 'air', 'tap', 'sweep', 'type', 'bloom', 'connect', 'drag', 'rise', 'resolve'):
            errors.append(f'{cid}: unsupported sound kind')
        for field, low, high in (('gain', 0, 1), ('pan', -1, 1)):
            val = cue.get(field)
            if not number(val, low, high):
                errors.append(f'{cid}: invalid {field}')
        if not cue.get('visual'):
            errors.append(f'{cid}: missing visual event description')
    music = plan.get('music', {})
    if music.get('enabled'):
        if (plan.get('schemaVersion', 1) == 1 or music.get('bpm') is not None) and not number(music.get('bpm'), 30, 240):
            errors.append('music.bpm must be between 30 and 240 (v2 may omit unknown BPM)')
        if not number(music.get('gain'), 0, 1):
            errors.append('music.gain must be between 0 and 1')
    return errors


REVIEW_NAMES = ('nativeInteraction', 'visualContinuity', 'creative', 'audio')
REVIEW_STATES = ('pending', 'passed', 'needs-revision', 'not-applicable')


def integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def number(value, low, high):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and low <= value <= high)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def rows(value, label, errors):
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        errors.append(f'{label}: array of objects required')
        return []
    return value


def registry(items, label, errors):
    result = {}
    for item in items:
        ident = item.get('id')
        if not text(ident) or ident in result:
            errors.append(f'{label}: id missing or duplicated')
        else:
            result[ident] = item
    return result


def has_id(value, table):
    return isinstance(value, str) and value in table


def validate(plan):
    """Return errors only, preserving the API used by legacy audio scripts."""
    errors = []
    if not isinstance(plan, dict):
        return ['plan: object required']
    version = plan.get('schemaVersion', 1)
    if not integer(version) or version not in (1, 2):
        errors.append('schemaVersion: supported versions are 1 and 2')
    scenes = rows(plan.get('scenes'), 'scenes', errors)
    events = rows(plan.get('events'), 'events', errors)
    registry(scenes, 'scenes', errors)
    registry(events, 'events', errors)
    if not isinstance(plan.get('music', {}), dict):
        errors.append('music: object required')
    if errors:
        return errors
    errors.extend(_validate_timeline(plan))
    if version == 2 and not errors:
        _validate_director(plan, errors)
    return errors


def _validate_director(plan, errors):
    assets = registry(rows(plan.get('assets'), 'assets', errors), 'assets', errors)
    refs = registry(rows(plan.get('referenceLibrary'), 'referenceLibrary', errors), 'referenceLibrary', errors)
    markers = {}
    scenes = plan['scenes']
    for scene in scenes:
        sid, start, end = scene['id'], scene['startFrame'], scene['endFrame']
        if scene.get('role') not in ('attention', 'claim', 'proof', 'payoff', 'context', 'brand'):
            errors.append(f'{sid}: invalid role')
        if scene.get('presentation') not in ('native-ui', 'artwork', 'typography', 'concept'):
            errors.append(f'{sid}: invalid presentation')
        if not text(scene.get('viewerTakeaway')):
            errors.append(f'{sid}: viewerTakeaway required')
        for field, table in (('assetIds', assets), ('referenceIds', refs)):
            values = scene.get(field)
            if (not isinstance(values, list) or (field == 'referenceIds' and not values)
                    or any(not has_id(value, table) for value in values)):
                errors.append(f'{sid}: {field} must reference registered IDs')
        hold = scene.get('readability')
        if not isinstance(hold, dict):
            errors.append(f'{sid}: readability object required')
        else:
            a, b = hold.get('startFrame'), hold.get('endFrame')
            if not integer(a) or not integer(b) or not start <= a < b <= end:
                errors.append(f'{sid}: readability interval must be within scene')
            if hold.get('mode') not in ('read', 'recognize') or not text(hold.get('reason')):
                errors.append(f'{sid}: readability mode and reason required')
        local = rows(scene.get('syncTargets'), f'{sid}.syncTargets', errors)
        if not local:
            errors.append(f'{sid}: at least one visual sync target required (sound optional)')
        for marker in local:
            mid, frame = marker.get('id'), marker.get('frame')
            if not text(mid) or mid in markers:
                errors.append(f'{sid}: sync target id missing or duplicated')
            else:
                markers[mid] = marker
            if (not integer(frame) or not start <= frame < end
                    or marker.get('kind') not in ('cut', 'land', 'reveal', 'contact', 'settle')):
                errors.append(f'{sid}: invalid sync target frame or kind')
    transitions = rows(plan.get('transitions'), 'transitions', errors)
    if len(transitions) != max(0, len(scenes) - 1):
        errors.append('transitions: one entry per adjacent scene pair required')
    for prev, nxt, transition in zip(scenes, scenes[1:], transitions):
        if transition.get('from') != prev['id'] or transition.get('to') != nxt['id']:
            errors.append('transitions: entries must follow adjacent scene pairs in order')
        start, cut, end = (transition.get(key) for key in ('startFrame', 'cutFrame', 'endFrame'))
        if (not all(integer(v) for v in (start, cut, end))
                or not 0 <= start <= cut <= end <= plan['durationFrames'] or cut != nxt['startFrame']):
            errors.append('transition: invalid interval or cutFrame differs from scene boundary')
        continuity = transition.get('continuity')
        if not isinstance(continuity, dict):
            errors.append('transition: continuity object required')
        elif (continuity.get('kind') not in ('semantic', 'object', 'action', 'composition', 'direction')
              or not text(continuity.get('basis'))):
            errors.append('transition: continuity kind and basis required')
        elif continuity['kind'] == 'object':
            carried = continuity.get('assetId')
            if (not has_id(carried, assets)
                    or any(not isinstance(s.get('assetIds'), list) or carried not in s['assetIds'] for s in (prev, nxt))):
                errors.append('transition: carried object must be a registered asset in both scenes')
        if not text(transition.get('reason')) or not text(transition.get('technique')):
            errors.append('transition: reason and technique required')
    for cue in plan['events']:
        target = cue.get('syncTargetId')
        if not has_id(target, markers):
            errors.append(f'{cue["id"]}: unknown syncTargetId')
            continue
        if 'peakOffsetFrames' not in cue:
            errors.append(f'{cue["id"]}: peakOffsetFrames required (null when unknown)')
        offset = cue.get('peakOffsetFrames')
        if offset is not None and (not integer(offset) or not 0 <= offset < cue['durationFrames']
                                   or cue['frame'] + offset != markers[target].get('frame')):
            errors.append(f'{cue["id"]}: audible alignment point does not match sync target')
    music = plan.get('music', {})
    audition = music.get('audition', {})
    for anchor in rows(music.get('anchors', []), 'music.anchors', errors):
        if (not integer(anchor.get('frame')) or not 0 <= anchor['frame'] < plan['durationFrames']
                or anchor.get('evidenceLevel') not in ('audio-measured', 'beat-estimated', 'audition-confirmed')
                or not text(anchor.get('evidence'))):
            errors.append('music anchor: frame, evidenceLevel and evidence required')
        if anchor.get('evidenceLevel') == 'audition-confirmed':
            if (not isinstance(audition, dict) or audition.get('status') != 'reviewed'
                    or not text(audition.get('reviewer')) or not text(audition.get('evidence'))):
                errors.append('music anchor: audition-confirmed requires an actual listening record')
    reviews = plan.get('reviews')
    if not isinstance(reviews, dict):
        errors.append('reviews: review records required')
        reviews = {}
    for name in REVIEW_NAMES:
        record = reviews.get(name)
        if not isinstance(record, dict) or record.get('status') not in REVIEW_STATES:
            errors.append(f'reviews.{name}: valid review status required')
        elif record['status'] != 'pending':
            if not text(record.get('evidence')):
                errors.append(f'reviews.{name}: evidence or non-applicability reason required')
            if record['status'] in ('passed', 'needs-revision') and not text(record.get('reviewer')):
                errors.append(f'reviews.{name}: reviewer required')


def assess(plan):
    errors = validate(plan)
    warnings = []
    declarations = {name: 'unrecorded' for name in REVIEW_NAMES}
    if isinstance(plan, dict) and plan.get('schemaVersion') == 2:
        reviews = plan.get('reviews', {})
        if isinstance(reviews, dict):
            for name in REVIEW_NAMES:
                record = reviews.get(name)
                if isinstance(record, dict):
                    declarations[name] = record.get('status', 'unrecorded')
        events = plan.get('events')
        if isinstance(events, list) and any(isinstance(e, dict) and e.get('peakOffsetFrames') is None for e in events):
            warnings.append('Sound alignment points remain unknown; sample selection and audition are pending')
    else:
        warnings.append('Legacy plan: only basic timeline and sound fields are checked')
    unresolved = [name for name, status in declarations.items() if status not in ('passed', 'not-applicable')]
    if unresolved:
        warnings.append('Unresolved reviews: ' + ', '.join(unresolved))
    return {'ok': not errors, 'scope': 'plan_structure_and_declarations', 'errors': errors,
            'warnings': warnings, 'reviewDeclarations': declarations,
            'qualityVerdict': 'not_assessed_by_validator'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    try:
        report = assess(json.loads(args.plan.read_text(encoding='utf-8-sig')))
    except (OSError, ValueError) as exc:
        report = {'ok': False, 'errors': [str(exc)], 'qualityVerdict': 'not_assessed_by_validator'}
    print(json.dumps(report, ensure_ascii=True, indent=2))
    raise SystemExit(0 if report['ok'] else 1)
