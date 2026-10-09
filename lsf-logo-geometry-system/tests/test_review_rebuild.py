"""Review regression: registration cannot replace structural or visual acceptance."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import review_rebuild as review_tool


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def save(self, name, a):
        p = self.dir/name
        Image.fromarray(np.where(a,0,255).astype('uint8')).save(p)
        return p

    def review(self, a, b, **kwargs):
        return review_tool.review(a,b,self.dir/'review',span=160,max_points=10000,**kwargs)

    def test_uniform_scale_and_translation_preserve_shape(self):
        a = np.zeros((50,80),bool)
        a[12:32,13:53] = True
        a[17:27,28:38] = False
        b = np.pad(np.repeat(np.repeat(a[12:32,13:53],2,axis=0),2,axis=1),((9,21),(33,7)))
        r = self.review(self.save('a.png',a),self.save('b.png',b))
        self.assertEqual(r['iou'],1)
        self.assertEqual(r['max_px'],0)
        self.assertTrue(r['numeric_checks_passed'])
        self.assertTrue(r['visual_review_required'])
        self.assertEqual(r['design_acceptance'],'not_evaluated')
        self.assertEqual(r['sources']['original']['foreground_dimensions'],[40,20])
        self.assertAlmostEqual(r['sources']['original']['registration']['uniform_scale'],4)
        self.assertEqual(r['sources']['original']['registration']['rotation_degrees'],0)
        for f in ('comparison.png','difference.png','registered-original.png','registered-rebuilt.png','review.json'):
            self.assertTrue((self.dir/'review'/f).exists())

    def test_aspect_ratio_change_is_not_stretched_away(self):
        a = np.ones((20,40),bool)
        b = np.ones((40,40),bool)
        r = self.review(self.save('a.png',a),self.save('b.png',b),min_iou=.9)
        self.assertAlmostEqual(r['iou'],.5)
        self.assertGreater(r['max_pct_D'],20)
        self.assertFalse(r['numeric_checks_passed'])

    def test_same_topology_different_shape_still_needs_review(self):
        a = np.zeros((60,60),bool)
        a[8:52,8:20] = True
        a[40:52,8:52] = True
        b = np.zeros_like(a)
        b[8:52,40:52] = True
        b[8:20,8:52] = True
        r = self.review(self.save('a.png',a),self.save('b.png',b),max_p95_pct=1)
        self.assertTrue(r['topology_equal'])
        self.assertLess(r['iou'],.5)
        self.assertFalse(r['numeric_checks_passed'])
        self.assertTrue(r['visual_review_required'])
        self.assertEqual(r['design_acceptance'],'not_evaluated')

    def test_hole_and_component_loss_are_reported_from_reference(self):
        a = np.zeros((60,60),bool)
        a[5:40,5:40] = True
        a[15:30,15:30] = False
        a[46:55,46:55] = True
        b = a.copy()
        b[15:30,15:30] = True
        b[46:55,46:55] = False
        r = self.review(self.save('a.png',a),self.save('b.png',b))
        self.assertEqual(r['sources']['original']['source_topology'],{'components':2,'holes':1})
        self.assertEqual(r['sources']['rebuilt']['source_topology'],{'components':1,'holes':0})
        self.assertIn('source_topology_equal',r['numeric_attention'])

    def test_crop_excludes_wordmark_and_records_input_coordinates(self):
        a = np.zeros((70,60),bool)
        a[10:30,10:50] = True
        a[50:60,5:15] = True
        p = self.save('a.png',a)
        q = self.save('b.png',a[10:30,10:50])
        original_bytes = p.read_bytes()
        r = self.review(p,q,original_crop=[0,0,60,40])
        self.assertEqual(r['iou'],1)
        self.assertEqual(r['sources']['original']['foreground_bbox_in_input'],[10,10,50,30])
        self.assertEqual(r['sources']['original']['sha256'],hashlib.sha256(original_bytes).hexdigest())
        self.assertEqual(p.read_bytes(),original_bytes)

    def test_white_transparent_mark_can_use_alpha_for_one_input(self):
        a = np.zeros((40,40),bool)
        a[5:35,10:30] = True
        rgba = np.full((40,40,4),255,dtype='uint8')
        rgba[:,:,3] = np.where(a,255,0)
        p = self.dir/'white.png'
        Image.fromarray(rgba).save(p)
        r = self.review(p,self.save('black.png',a),original_mask='alpha')
        self.assertEqual(r['iou'],1)
        self.assertEqual(r['sources']['original']['mask'],'alpha')

    def test_invalid_crop_or_blank_image_is_rejected(self):
        p = self.save('empty.png',np.zeros((20,20),bool))
        q = self.save('solid.png',np.ones((20,20),bool))
        with self.assertRaisesRegex(ValueError,'No foreground'):
            self.review(p,q)
        with self.assertRaisesRegex(ValueError,'Crop must lie inside'):
            self.review(q,q,original_crop=[0,0,21,20])
        self.assertFalse((self.dir/'review').exists())

    def test_existing_review_is_not_overwritten(self):
        p = self.save('a.png',np.ones((20,20),bool))
        self.review(p,p)
        target = self.dir/'review/review.json'
        before = target.read_bytes()
        with self.assertRaisesRegex(ValueError,'new or empty'):
            self.review(p,p)
        self.assertEqual(target.read_bytes(),before)

    def test_cli_returns_two_for_topology_loss_with_evidence_saved(self):
        a = np.ones((40,40),bool)
        a[10:30,10:30] = False
        p = self.save('a.png',a)
        q = self.save('b.png',np.ones((40,40),bool))
        result = subprocess.run([sys.executable,str(ROOT/'scripts/review_rebuild.py'),str(p),str(q),
                                 '--span','160','--out',str(self.dir/'review')],capture_output=True,text=True)
        self.assertEqual(result.returncode,2,result.stderr)
        report = json.loads((self.dir/'review/review.json').read_text(encoding='utf-8'))
        self.assertFalse(report['numeric_checks_passed'])
        self.assertTrue(report['visual_review_required'])


if __name__ == '__main__':
    unittest.main()
