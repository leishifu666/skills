"""Original deterministic UI soundtrack. Standard library only; no sampled media."""
import argparse
from array import array
import json
import math
from pathlib import Path
import random
import sys
import wave
from validate_plan import validate

RATE = 48000
TAU = 2 * math.pi


def render(plan, output):
    errors = validate(plan)
    if any(e.get('kind') not in ('click','swish','thump','chime') for e in plan.get('events', [])):
        errors.append('Use design_audio.py for refined sound kinds')
    if errors:
        raise ValueError('; '.join(errors))
    fps = plan['fps']
    count = round(plan['durationFrames'] / fps * RATE)
    channels = [array('f', [0]) * count, array('f', [0]) * count]
    rng = random.Random(20260919)
    for event in plan['events']:
        start = round(event['frame'] / fps * RATE)
        n = min(round(event['durationFrames'] / fps * RATE), count - start)
        seconds = n / RATE
        pan = (event['pan'] + 1) * math.pi / 4
        gains = (math.cos(pan) * event['gain'], math.sin(pan) * event['gain'])
        smooth_noise = 0.0
        for i in range(n):
            t, u = i / RATE, i / n
            edge = min(1.0, i / max(1, RATE * .003), (n - 1 - i) / max(1, RATE * .012))
            kind = event['kind']
            if kind == 'click':
                sample = (.7 * math.sin(TAU * 1550 * t) + .3 * rng.uniform(-1, 1)) * math.exp(-65 * t)
            elif kind == 'swish':
                smooth_noise = .87 * smooth_noise + .13 * rng.uniform(-1, 1)
                sample = 2.2 * smooth_noise * math.sin(math.pi * u) ** 2
            elif kind == 'thump':
                sample = math.sin(TAU * (88 * t - 19 * t * t)) * math.exp(-9 * t)
            else:
                sample = sum(math.sin(TAU * freq * t) for freq in (523.25, 659.25, 783.99)) / 3 * math.exp(-4 * t)
            for ch in range(2):
                channels[ch][start + i] += sample * edge * gains[ch]
    music = plan.get('music', {})
    if music.get('enabled'):
        beat = 60 / music['bpm']
        notes = (130.81, 164.81, 196, 164.81, 146.83, 174.61, 220, 196)
        for i in range(count):
            t = i / RATE
            within = t % beat
            note = notes[int(t / beat) % len(notes)]
            attack = min(1, within / .012)
            fade = min(1, t / .4, (count / RATE - t) / 1.2)
            pulse = (math.sin(TAU * note * within) + .25 * math.sin(TAU * note * 2 * within)) * math.exp(-5 * within)
            sample = pulse * attack * fade * music['gain']
            channels[0][i] += sample * .7
            channels[1][i] += sample * .7
    peak = max(max(abs(v) for v in channel) for channel in channels)
    scale = min(1, 10 ** (-3 / 20) / max(peak, 1e-12))
    pcm = array('h')
    for i in range(count):
        pcm.extend(round(max(-1, min(1, channels[ch][i] * scale)) * 32767) for ch in range(2))
    if sys.byteorder != 'little':
        pcm.byteswap()
    output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output), 'wb') as wav:
        wav.setparams((2, 2, RATE, count, 'NONE', 'not compressed'))
        wav.writeframes(pcm.tobytes())
    report = {'sampleRate': RATE, 'channels': 2, 'samples': count, 'duration': count / RATE,
              'samplePeakDbfs': 20 * math.log10(max(peak * scale, 1e-12)), 'attenuation': scale,
              'eventCount': len(plan['events']), 'source': 'original procedural synthesis',
              'listeningReview': 'not performed by this script'}
    output.with_suffix('.audio-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('plan', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    render(json.loads(args.plan.read_text(encoding='utf-8-sig')), args.output)
