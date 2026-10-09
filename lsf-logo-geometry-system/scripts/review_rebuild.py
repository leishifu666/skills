#!/usr/bin/env python3
"""Create registered logo comparison evidence; visual acceptance remains separate."""
import argparse
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from measure import compare, mask, topology


def source_mask(path, crop, mode, threshold):
    path = Path(path)
    with Image.open(path) as image:
        size = list(image.size)
    bounds = list(crop) if crop is not None else [0, 0, *size]
    left, top, right, bottom = bounds
    if not (0 <= left < right <= size[0] and 0 <= top < bottom <= size[1]):
        raise ValueError(f'Crop must lie inside {path.name}, whose size is {size}')
    a = mask(path, threshold, mode)[top:bottom, left:right]
    if not a.any():
        raise ValueError(f'No foreground in {path.name} with the selected crop and mask')
    yy, xx = np.where(a)
    bbox = [int(xx.min()), int(yy.min()), int(xx.max()+1), int(yy.max()+1)]
    return a, {
        'path': str(path.resolve()),
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'input_size': size,
        'crop': bounds,
        'mask': mode,
        'threshold': threshold,
        'foreground_bbox_in_input': [bbox[0]+left, bbox[1]+top, bbox[2]+left, bbox[3]+top],
        'foreground_dimensions': [bbox[2]-bbox[0], bbox[3]-bbox[1]],
        'source_topology': topology(a),
    }, bbox


def normalize(a, bbox, record, span, margin):
    left, top, right, bottom = bbox
    D = max(right-left, bottom-top)
    scale = span/D
    canvas = span+2*margin
    center = canvas/2
    cx, cy = (left+right)/2, (top+bottom)/2
    inverse = (1/scale, 0, cx-center/scale, 0, 1/scale, cy-center/scale)
    image = Image.fromarray(np.where(a, 0, 255).astype('uint8'))
    aligned = image.transform((canvas, canvas), Image.Transform.AFFINE, inverse,
                              resample=Image.Resampling.NEAREST, fillcolor=255)
    crop_left, crop_top = record['crop'][:2]
    record['registration'] = {
        'uniform_scale': scale,
        'translation_from_input': [center-scale*(cx+crop_left), center-scale*(cy+crop_top)],
        'rotation_degrees': 0,
        'source_D_pixels': D,
        'target_D_pixels': span,
        'resampling': 'nearest neighbor of the segmented mask',
    }
    return aligned


def comparison_sheet(out, result):
    panel, pad, gap, top = 440, 28, 26, 75
    width = panel*3+pad*2+gap*2
    image = Image.new('RGB', (width, 655), 'white')
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.load_default(size=21)
    except TypeError:
        font = ImageFont.load_default()
    draw.text((pad, 13), 'Logo review / uniform scale and bbox-center alignment', fill='#222222', font=font)
    for i, (name, label) in enumerate([
        ('registered-original.png', 'Reference mask'),
        ('registered-rebuilt.png', 'Rebuilt mask'),
        ('difference.png', 'Difference overlay'),
    ]):
        x = pad+i*(panel+gap)
        draw.text((x, 45), label, fill='#222222', font=font)
        with Image.open(out/name) as im:
            image.paste(im.convert('RGB').resize((panel, panel), Image.Resampling.LANCZOS), (x, top))
    draw.text((pad, 537), 'Dark: overlap   Red: reference only   Blue: rebuilt only', fill='#222222', font=font)
    draw.text((pad, 571),
              f'IoU {result["iou"]*100:.2f}%   Boundary mean {result["mean_pct_D"]:.2f}%D'
              f'   P95 {result["p95_pct_D"]:.2f}%D   Max {result["max_pct_D"]:.2f}%D',
              fill='#222222', font=font)
    a, b = result['original_topology'], result['rebuilt_topology']
    draw.text((pad, 604),
              f'Components {a["components"]} -> {b["components"]}   Holes {a["holes"]} -> {b["holes"]}'
              '   Visual review REQUIRED', fill='#222222', font=font)
    image.save(out/'comparison.png')


def review(original, rebuilt, out, *, original_crop=None, rebuilt_crop=None,
           original_mask='luminance', rebuilt_mask='luminance', threshold=128,
           span=1000, margin=80, max_points=6000,
           min_iou=None, max_mean_pct=None, max_p95_pct=None):
    original, rebuilt, out = Path(original), Path(rebuilt), Path(out)
    if not 1 <= threshold <= 254:
        raise ValueError('threshold must be 1..254')
    if span < 32 or margin < 1 or max_points < 4:
        raise ValueError('span must be >=32, margin >=1, max_points >=4')
    if min_iou is not None and not 0 <= min_iou <= 1:
        raise ValueError('min_iou must be between 0 and 1')
    if any(v is not None and v < 0 for v in (max_mean_pct, max_p95_pct)):
        raise ValueError('Distance limits must be nonnegative')
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError('Use a new or empty output directory; previous review evidence is not overwritten')
    a, original_record, abox = source_mask(original, original_crop, original_mask, threshold)
    b, rebuilt_record, bbox = source_mask(rebuilt, rebuilt_crop, rebuilt_mask, threshold)
    aligned_a = normalize(a, abox, original_record, span, margin)
    aligned_b = normalize(b, bbox, rebuilt_record, span, margin)
    out.mkdir(parents=True, exist_ok=True)
    aligned_a.save(out/'registered-original.png')
    aligned_b.save(out/'registered-rebuilt.png')
    result = compare(SimpleNamespace(
        original=out/'registered-original.png', rebuilt=out/'registered-rebuilt.png',
        mask='luminance', threshold=128, max_points=max_points,
        max_mean_pct=max_mean_pct, max_p95_pct=max_p95_pct, diff=out/'difference.png',
    ))
    result['method'] = 'segmented masks; uniform bbox-center registration; bidirectional boundary-pixel distance'
    result['source_threshold'] = threshold
    result['sources'] = {'original':original_record, 'rebuilt':rebuilt_record}
    result['registration'] = {'rotation_degrees':0, 'local_warp':False,
                              'nominal_D_pixels':span, 'margin_pixels':margin}
    checks = result['checks']
    checks['source_topology_equal'] = original_record['source_topology'] == rebuilt_record['source_topology']
    checks['original_topology_survived_normalization'] = original_record['source_topology'] == result['original_topology']
    checks['rebuilt_topology_survived_normalization'] = rebuilt_record['source_topology'] == result['rebuilt_topology']
    if min_iou is not None:
        checks['iou_within_limit'] = result['iou'] >= min_iou
    result.pop('passed_requested_checks')
    result['numeric_checks_passed'] = all(checks.values())
    result['numeric_attention'] = [name for name, passed in checks.items() if not passed]
    result['configured_limits'] = {'min_iou':min_iou, 'max_mean_pct':max_mean_pct, 'max_p95_pct':max_p95_pct}
    result['visual_review_required'] = True
    result['design_acceptance'] = 'not_evaluated'
    aa, bb = np.asarray(aligned_a)<128, np.asarray(aligned_b)<128
    intersection, union = int((aa&bb).sum()), int((aa|bb).sum())
    result['area'] = {
        'original':int(aa.sum()), 'rebuilt':int(bb.sum()),
        'intersection':intersection, 'union':union,
        'original_only':int((aa&~bb).sum()), 'rebuilt_only':int((bb&~aa).sum()),
        'original_area_removed_fraction':float((aa&~bb).sum()/aa.sum()),
        'rebuilt_area_added_fraction':float((bb&~aa).sum()/bb.sum()),
    }
    for metric in ('mean','p95','max'):
        result[metric+'_original_pixel_equivalent'] = result[metric+'_px']/original_record['registration']['uniform_scale']
    comparison_sheet(out, result)
    (out/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('original',type=Path)
    p.add_argument('rebuilt',type=Path)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--original-crop',nargs=4,type=int,metavar=('LEFT','TOP','RIGHT','BOTTOM'))
    p.add_argument('--rebuilt-crop',nargs=4,type=int,metavar=('LEFT','TOP','RIGHT','BOTTOM'))
    p.add_argument('--original-mask',choices=['luminance','alpha'],default='luminance')
    p.add_argument('--rebuilt-mask',choices=['luminance','alpha'],default='luminance')
    p.add_argument('--threshold',type=int,default=128)
    p.add_argument('--span',type=int,default=1000)
    p.add_argument('--margin',type=int,default=80)
    p.add_argument('--max-points',type=int,default=6000)
    p.add_argument('--min-iou',type=float)
    p.add_argument('--max-mean-pct',type=float)
    p.add_argument('--max-p95-pct',type=float)
    args = p.parse_args()
    try:
        result = review(**vars(args))
    except ValueError as e:
        p.error(str(e))
    print(json.dumps({
        'out':str(args.out.resolve()), 'iou':result['iou'],
        'mean_pct_D':result['mean_pct_D'], 'p95_pct_D':result['p95_pct_D'],
        'max_pct_D':result['max_pct_D'], 'sampled':result['sampled'],
        'original_topology':result['original_topology'], 'rebuilt_topology':result['rebuilt_topology'],
        'numeric_attention':result['numeric_attention'],
        'visual_review_required':True, 'design_acceptance':'not_evaluated',
    },ensure_ascii=False,indent=2))
    if not result['numeric_checks_passed']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
