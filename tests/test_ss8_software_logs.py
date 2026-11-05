"""SS8: audit of warmup handling, failures, IQR flags, CI and synthetic lab separation."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from process_ss7_logs import read_jsonl, mark_outliers, summarize, bootstrap_ci, run_analysis

SS7_SOURCE=ROOT/'data/sample/ss7_software_benchmark_demo.jsonl'


class TestSS8Logs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example, cls.meta=read_jsonl(SS7_SOURCE)

    def test_original_schema_and_phase_counts(self):
        self.assertEqual(len(self.example),105)
        self.assertEqual((self.example.phase=='warmup').sum(),5)
        self.assertEqual((self.example.phase=='benchmark').sum(),100)
        self.assertEqual(self.meta['event_type'],'metadata')

    def test_summary_does_not_count_warmup(self):
        summary=summarize(mark_outliers(self.example),resamples=100)
        row=summary.loc[summary.group=='overall'].iloc[0]
        self.assertEqual(row.benchmark_runs,100)
        self.assertEqual(row.successful_runs+row.failed_runs,100)
        self.assertAlmostEqual(row.failure_rate_percent,0.)

    def test_failure_retained_and_rate_changes(self):
        altered=self.example.copy()
        row=altered.index[altered.phase=='benchmark'][0]
        altered.loc[row,'status']='error'
        altered.loc[row,'error_type']='TimeoutError'
        marked=mark_outliers(altered)
        summary=summarize(marked,resamples=100)
        total=summary[summary.group=='overall'].iloc[0]
        self.assertEqual(total.failed_runs,1)
        self.assertAlmostEqual(total.failure_rate_percent,1.)
        self.assertEqual(int((marked.phase=='benchmark').sum()),100)

    def test_outlier_mark_only_not_deleted(self):
        altered=self.example.copy()
        row=altered.index[altered.phase=='benchmark'][0]
        altered.loc[row,'duration_ms']=10000.0
        mark=mark_outliers(altered)
        self.assertTrue(bool(mark.loc[row,'iqr_outlier']))
        self.assertEqual(len(mark),len(altered))

    def test_deterministic_bootstrap(self):
        a=bootstrap_ci([1,2,3,4],42,300)
        b=bootstrap_ci([1,2,3,4],42,300)
        self.assertEqual(a,b)
        self.assertLessEqual(a[0],2.5)
        self.assertGreaterEqual(a[1],2.5)

    def test_empty_success_group_report(self):
        altered=self.example.copy()
        altered.loc[altered.phase=='benchmark','status']='error'
        row=summarize(mark_outliers(altered),resamples=100).iloc[0]
        self.assertEqual(row.failed_runs,100)
        self.assertTrue(pd.isna(row.p95_ms))
        self.assertTrue(pd.isna(row.bootstrap_mean_ci95_lower_ms))

    def test_reject_real_data_origin(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'invalid.jsonl'
            content=SS7_SOURCE.read_text(encoding='utf-8').splitlines()
            rec=json.loads(content[1]);rec['data_origin']='real';content[1]=json.dumps(rec)
            p.write_text('\n'.join(content)+'\n',encoding='utf-8')
            with self.assertRaises(ValueError):read_jsonl(p)

    def test_invalid_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'invalid.jsonl'
            p.write_text('{\"event_type\":\"metadata\"}\nno json\n',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Invalid JSON'):read_jsonl(p)

    def test_integrated_output_and_audit(self):
        with tempfile.TemporaryDirectory() as d:
            q=Path(d)
            summary,detail,audit=run_analysis(SS7_SOURCE,q/'metrics.csv',q/'clean.csv',q/'audit.json',resamples=100)
            self.assertEqual(len(detail),100)
            self.assertEqual(audit['warmup_excluded'],5)
            self.assertEqual(audit['benchmark_kept'],100)
            self.assertTrue((q/'metrics.csv').exists())
            self.assertTrue((q/'audit.json').exists())
            self.assertEqual(summary.iloc[0]['measurement_unit'],'milliseconds')


if __name__ == '__main__':
    unittest.main()
