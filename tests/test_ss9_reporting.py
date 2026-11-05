"""SS9 source-to-report consistency; never pretend synthetic records are real humans."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from generate_ss9_report import REPORT, TABLES, markdown_report, latex_tables, stats


class TestSS9Reporting(unittest.TestCase):
    def test_synthetic_pair_and_human_metrics(self):
        s = stats()
        self.assertEqual(s['n'], 4)
        self.assertAlmostEqual(s['saved'], 3.875)
        self.assertAlmostEqual(s['speedup'], 23.375/19.5)
        self.assertAlmostEqual(s['reduction'], 100*(23.375-19.5)/23.375)

    def test_software_source_uses_milliseconds_and_100_runs(self):
        s = stats()
        self.assertEqual(int(s['overall']['benchmark_runs']), 100)
        self.assertEqual(s['overall']['measurement_unit'], 'milliseconds')
        self.assertEqual(int(s['overall']['iqr_outlier_flags']), 11)

    def test_provenance_and_complete_figure_captions(self):
        report = markdown_report(stats())
        self.assertIn('NO RECRUITED PARTICIPANTS', report)
        self.assertIn('**3.875 min**', report)
        self.assertIn('**[0.00, 6.25] min**', report)
        self.assertIn('Figure 4. Technical runtime distributions', report)
        self.assertIn('**minutes**', report)
        self.assertIn('**milliseconds**', report)
        self.assertNotIn('100 real participants', report)

    def test_saved_report_and_booktabs_are_deterministic(self):
        report = markdown_report(stats())
        tables = latex_tables(stats())
        self.assertEqual(REPORT.read_text(encoding='utf-8'), report)
        self.assertEqual(TABLES.read_text(encoding='utf-8'), tables)
        self.assertIn('\\toprule', tables)
        self.assertIn('\\bottomrule', tables)
        self.assertIn('81.63', tables)  # Conventional half-up display of 81.625.


if __name__ == '__main__':
    unittest.main()
