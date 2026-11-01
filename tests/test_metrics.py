"""Automated tests for real calculations and measurement validation."""

import sys
import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from metrics import paired_statistics, analyze_pairs
from validate_data import validate_dataframe
from randomize import balanced_assignments


class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.sample = pd.read_csv(ROOT / 'data/sample/example_measurements.csv')

    def test_balanced_randomization_is_reproducible(self):
        a = balanced_assignments(8, 42)
        b = balanced_assignments(8, 42)
        self.assertEqual(a, b)
        self.assertEqual(len(a), 16)
        self.assertEqual(sum(x['condition'] == 'with_ai' for x in a), 8)
        self.assertEqual(sum(x['task_set'] == 'A' and x['condition'] == 'with_ai' for x in a), 4)

    def test_paired_time_difference(self):
        result = paired_statistics([20, 30], [15, 25])
        self.assertEqual(result['n_pairs'], 2)
        self.assertEqual(result['mean_paired_difference_with_minus_without'], -5)

    def test_real_analysis_from_csv(self):
        rows = validate_dataframe(self.sample)
        summary, person = analyze_pairs(rows)
        self.assertEqual(summary['participants_with_complete_pairs'], 4)
        self.assertEqual(summary['data_origin'], 'synthetic')
        self.assertEqual(len(person), 4)
        self.assertAlmostEqual(summary['time_minutes']['mean_paired_difference_with_minus_without'], -3.875)

    def test_missing_condition_is_rejected(self):
        bad = self.sample.iloc[:-1]
        with self.assertRaises(ValueError):
            validate_dataframe(bad)

    def test_invalid_quality_is_rejected(self):
        bad = self.sample.copy()
        bad.loc[0, 'quality_rater_1'] = 101
        with self.assertRaises(ValueError):
            validate_dataframe(bad)

    def test_incomplete_pair_is_excluded(self):
        rows = self.sample.copy()
        rows.loc[0, 'completed'] = 0
        for field in ['quality_rater_1', 'quality_rater_2', 'factual_correct', 'factual_total']:
            rows.loc[0, field] = float('nan')
        valid = validate_dataframe(rows)
        summary, people = analyze_pairs(valid)
        self.assertEqual(summary['participants_excluded_from_paired_analysis'], 1)
        self.assertEqual(len(people), 3)

    def test_no_completed_pairs_does_not_claim_effect(self):
        rows = self.sample.copy()
        rows['completed'] = 0
        for field in ['quality_rater_1', 'quality_rater_2', 'factual_correct', 'factual_total']:
            rows[field] = float('nan')
        valid = validate_dataframe(rows)
        summary, people = analyze_pairs(valid)
        self.assertNotIn('time_minutes', summary)
        self.assertTrue(people.empty)


if __name__ == '__main__':
    unittest.main()
