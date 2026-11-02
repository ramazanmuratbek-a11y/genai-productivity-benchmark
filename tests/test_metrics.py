"""Automated tests for paired measures, reviewer data, and claim scores."""

import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from metrics import paired_statistics, analyze_pairs, factual_claim_scores
from validate_data import validate_dataframe

# Reuse the existing randomized assignment implementation, not a stub.
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

    def test_analysis_from_synthetic_csv(self):
        rows = validate_dataframe(self.sample)
        summary, people = analyze_pairs(rows)
        self.assertEqual(summary['participants_with_complete_pairs'], 4)
        self.assertEqual(summary['data_origin'], 'synthetic')
        self.assertEqual(len(people), 4)
        self.assertAlmostEqual(summary['time_minutes']['mean_paired_difference_with_minus_without'], -3.875)
        self.assertEqual(summary['factual_precision_percent']['n_pairs'], 4)
        self.assertEqual(summary['factual_f1_percent']['n_pairs'], 4)
        self.assertEqual(summary['factual_recall_percent'], summary['factual_accuracy_percent'])
        self.assertTrue((people['factual_f1_with_ai_percent'] >= 0).all())

    def test_missing_condition_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_dataframe(self.sample.iloc[:-1])

    def test_invalid_quality_is_rejected(self):
        bad = self.sample.copy()
        bad.loc[0, 'quality_rater_1'] = 101
        with self.assertRaises(ValueError):
            validate_dataframe(bad)

    def test_incomplete_pair_is_excluded(self):
        bad = self.sample.copy()
        bad.loc[0, 'completed'] = 0
        for col in ['quality_rater_1', 'quality_rater_2', 'factual_correct', 'factual_total',
                    'supported_claims', 'unsupported_claims']:
            bad.loc[0, col] = float('nan')
        summary, people = analyze_pairs(validate_dataframe(bad))
        self.assertEqual(summary['participants_excluded_from_paired_analysis'], 1)
        self.assertEqual(len(people), 3)
        self.assertEqual(summary['claim_metric_pairs_with_valid_precision'], 3)

    def test_no_completed_pairs_does_not_claim_effect(self):
        rows = self.sample.copy()
        rows['completed'] = 0
        for field in ['quality_rater_1', 'quality_rater_2', 'factual_correct', 'factual_total',
                      'supported_claims', 'unsupported_claims']:
            rows[field] = float('nan')
        summary, people = analyze_pairs(validate_dataframe(rows))
        self.assertNotIn('time_minutes', summary)
        self.assertTrue(people.empty)

    def test_precision_recall_f1_example(self):
        p, r, f1 = factual_claim_scores(4, 5, 4, 1)
        self.assertAlmostEqual(p, .8)
        self.assertAlmostEqual(r, .8)
        self.assertAlmostEqual(f1, .8)

    def test_precision_differs_from_recall(self):
        p, r, f1 = factual_claim_scores(4, 5, 4, 0)
        self.assertEqual(p, 1)
        self.assertAlmostEqual(r, .8)
        self.assertAlmostEqual(f1, 2 * 1 * .8 / 1.8)

    def test_no_claims_precision_and_f1_undefined(self):
        p, r, f1 = factual_claim_scores(0, 5, 0, 0)
        self.assertIsNone(p)
        self.assertEqual(r, 0)
        self.assertIsNone(f1)

    def test_zero_precision_zero_recall_f1_zero(self):
        p, r, f1 = factual_claim_scores(0, 5, 0, 3)
        self.assertEqual((p, r, f1), (0, 0, 0))

    def test_old_csv_without_claim_fields_still_valid(self):
        old = self.sample.drop(columns=['supported_claims', 'unsupported_claims'])
        summary, person = analyze_pairs(validate_dataframe(old))
        self.assertIsNone(summary['factual_precision_percent'])
        self.assertIsNone(summary['factual_f1_percent'])
        self.assertEqual(summary['claim_metric_pairs_with_valid_precision'], 0)
        self.assertEqual(summary['factual_recall_percent']['n_pairs'], 4)
        self.assertTrue(person['factual_precision_with_ai_percent'].isna().all())

    def test_both_claim_fields_required_together(self):
        bad = self.sample.drop(columns=['unsupported_claims'])
        with self.assertRaises(ValueError):
            validate_dataframe(bad)

    def test_negative_claim_count_rejected(self):
        bad = self.sample.copy()
        bad.loc[0, 'unsupported_claims'] = -1
        with self.assertRaises(ValueError):
            validate_dataframe(bad)

    def test_fractional_and_non_numeric_claim_counts_rejected(self):
        for invalid in [1.5, 'not-count']:
            with self.subTest(invalid=invalid):
                bad = self.sample.copy()
                bad['supported_claims'] = bad['supported_claims'].astype(object)
                bad.loc[0, 'supported_claims'] = invalid
                with self.assertRaises(ValueError):
                    validate_dataframe(bad)

    def test_missing_only_one_claim_count_rejected(self):
        bad = self.sample.copy()
        bad.loc[0, 'supported_claims'] = float('nan')
        with self.assertRaises(ValueError):
            validate_dataframe(bad)

    def test_supported_claims_below_anchor_facts_rejected(self):
        bad = self.sample.copy()
        bad.loc[0, 'supported_claims'] = 3  # correct anchor facts = 4
        with self.assertRaises(ValueError):
            validate_dataframe(bad)

    def test_incomplete_task_must_have_blank_claim_counts(self):
        bad = self.sample.copy()
        bad.loc[0, 'completed'] = 0
        for col in ['quality_rater_1', 'quality_rater_2', 'factual_correct', 'factual_total']:
            bad.loc[0, col] = float('nan')
        with self.assertRaises(ValueError):
            validate_dataframe(bad)

    def test_partially_unannotated_pair_does_not_drop_time_measurement(self):
        mixed = self.sample.copy()
        mixed.loc[0, ['supported_claims', 'unsupported_claims']] = float('nan')
        summary, person = analyze_pairs(validate_dataframe(mixed))
        self.assertEqual(summary['time_minutes']['n_pairs'], 4)
        self.assertEqual(summary['factual_precision_percent']['n_pairs'], 3)
        self.assertEqual(summary['factual_f1_percent']['n_pairs'], 3)
        self.assertTrue(pd.isna(person.loc[person.participant_id == 'DEMO_001',
                                       'factual_precision_without_ai_percent'].iloc[0]))

    def test_all_zero_claims_precision_unavailable_without_mislabeling(self):
        rows = self.sample.copy()
        rows['factual_correct'] = 0
        rows['supported_claims'] = 0
        rows['unsupported_claims'] = 0
        summary, _ = analyze_pairs(validate_dataframe(rows))
        self.assertIsNone(summary['factual_precision_percent'])
        self.assertIsNone(summary['factual_f1_percent'])
        self.assertEqual(summary['factual_recall_percent']['mean_without_ai'], 0)


if __name__ == '__main__':
    unittest.main()
