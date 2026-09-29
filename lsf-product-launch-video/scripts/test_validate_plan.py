"""Regression cases for editorial freedom, continuity and honest review reporting."""
import copy
import json
import unittest
from pathlib import Path

from validate_plan import assess, validate


ASSETS = Path(__file__).resolve().parents[1] / 'assets'


class DirectorPlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ASSETS / 'director-plan.example.json').read_text(encoding='utf-8-sig'))

    def test_result_first_teaser_and_semantic_hard_cut_are_valid(self):
        self.assertEqual(self.plan['scenes'][0]['presentation'], 'artwork')
        seam = self.plan['transitions'][0]
        self.assertEqual(seam['startFrame'], seam['endFrame'])
        self.assertNotIn('assetId', seam['continuity'])
        self.assertEqual(validate(self.plan), [])

    def test_legacy_plans_keep_error_list_api_without_quality_claim(self):
        for filename in ('example-plan.json', 'segment-plan.example.json'):
            with self.subTest(filename=filename):
                plan = json.loads((ASSETS / filename).read_text(encoding='utf-8-sig'))
                self.assertEqual(validate(plan), [])
                report = assess(plan)
                self.assertTrue(report['warnings'])
                self.assertEqual(report['qualityVerdict'], 'not_assessed_by_validator')

    def test_empty_viewer_takeaway_is_incomplete_directing(self):
        self.plan['scenes'][0]['viewerTakeaway'] = ' '
        self.assertTrue(validate(self.plan))

    def test_read_hold_cannot_extend_into_another_scene(self):
        scene = self.plan['scenes'][2]
        scene['readability']['endFrame'] = scene['endFrame'] + 1
        self.assertTrue(validate(self.plan))

    def test_missing_reference_or_asset_is_rejected(self):
        for field in ('referenceIds', 'assetIds'):
            with self.subTest(field=field):
                plan = copy.deepcopy(self.plan)
                plan['scenes'][0][field] = ['does-not-exist']
                self.assertTrue(validate(plan))

    def test_same_object_handoff_cannot_silently_change_image(self):
        seam = self.plan['transitions'][4]
        self.assertEqual(seam['continuity']['kind'], 'object')
        self.plan['scenes'][5]['assetIds'].remove('tea-poster')
        self.assertTrue(validate(self.plan))

    def test_transition_must_join_actual_adjacent_scenes(self):
        self.plan['transitions'][0]['to'] = 'agent'
        self.assertTrue(validate(self.plan))

    def test_alignment_uses_audible_point_not_file_start(self):
        cue = self.plan['events'][0]
        self.assertEqual(cue['frame'], 66)
        cue['peakOffsetFrames'] = 12  # Visual reveal is frame 78.
        self.assertEqual(validate(self.plan), [])
        cue['peakOffsetFrames'] = 0
        self.assertTrue(validate(self.plan))

    def test_unknown_sync_target_fails(self):
        self.plan['events'][0]['syncTargetId'] = 'unregistered-reveal'
        self.assertTrue(validate(self.plan))

    def test_unknown_bpm_allowed_but_algorithm_is_not_audition(self):
        self.assertEqual(validate(self.plan), [])
        self.plan['music']['anchors'] = [{'frame': 78, 'evidenceLevel': 'beat-estimated', 'evidence': 'Algorithm candidate, no listening'}]
        self.assertEqual(validate(self.plan), [])
        self.plan['music']['anchors'][0]['evidenceLevel'] = 'audition-confirmed'
        self.assertTrue(validate(self.plan))

    def test_passed_review_needs_attributed_evidence(self):
        self.plan['reviews']['creative']['status'] = 'passed'
        self.assertTrue(validate(self.plan))

    def test_structural_success_never_becomes_aesthetic_approval(self):
        report = assess(self.plan)
        self.assertTrue(report['ok'])
        self.assertEqual(set(report['reviewDeclarations'].values()), {'pending'})
        for record in self.plan['reviews'].values():
            record.update(status='passed', reviewer='test-only reviewer', evidence='Test-only record, no media inspected')
        report = assess(self.plan)
        self.assertTrue(report['ok'])
        self.assertEqual(report['qualityVerdict'], 'not_assessed_by_validator')

    def test_malformed_input_reports_errors_instead_of_crashing(self):
        variants = [None, [], {'schemaVersion': 999}]
        for key, value in (('scenes', None), ('music', []), ('schemaVersion', True)):
            bad = copy.deepcopy(self.plan)
            bad[key] = value
            variants.append(bad)
        bad = copy.deepcopy(self.plan)
        bad['scenes'][0]['startFrame'] = False
        variants.append(bad)
        for plan in variants:
            with self.subTest(plan_type=type(plan).__name__):
                self.assertFalse(assess(plan)['ok'])


if __name__ == '__main__':
    unittest.main()
