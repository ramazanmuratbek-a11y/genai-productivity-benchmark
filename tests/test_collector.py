"""Tests for the *synthetic* Task 2 pipeline logging exercise."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collector import (benchmark, load_settings, synthetic_workload, summarize,
                       write_outputs)
from validate_data import validate_dataframe


class TestSyntheticCollector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = pd.read_csv(ROOT / "data/sample/example_measurements.csv")
        cls.settings = load_settings(ROOT / "configs/collector.yaml")

    def test_workload_preserves_valid_crossover_pairs(self):
        sample = synthetic_workload(self.base, 3)
        validated = validate_dataframe(sample)
        self.assertEqual(len(validated), len(self.base) * 3)
        self.assertEqual(validated.participant_id.nunique(), 12)
        self.assertEqual(set(validated.data_origin), {"synthetic"})

    def test_reject_real_data(self):
        rows = self.base.copy()
        rows["data_origin"] = "real"
        with self.assertRaises(ValueError):
            synthetic_workload(rows, 1)
        with self.assertRaises(ValueError):
            benchmark(self.settings, rows)

    def test_default_schedule_has_100_measurements_and_warmup(self):
        cfg = dict(self.settings, measured_runs=2, warmup_runs=1)
        records = benchmark(cfg, self.base)
        self.assertEqual(len(records), 3)
        self.assertEqual([x["phase"] for x in records],
                         ["warmup", "benchmark", "benchmark"])
        self.assertTrue(all(x["data_origin"] == "synthetic" for x in records))
        self.assertEqual(self.settings["measured_runs"], 100)

    def test_deterministic_workload_profile_schedule(self):
        cfg = dict(self.settings, measured_runs=8, warmup_runs=2)
        a = [x["workload_profile"] for x in benchmark(cfg, self.base)]
        b = [x["workload_profile"] for x in benchmark(cfg, self.base)]
        self.assertEqual(a, b)  # durations themselves are NOT deterministic

    def test_failures_are_logged_and_counted(self):
        cfg = dict(self.settings, measured_runs=3, warmup_runs=1)
        calls = {"n": 0}
        def broken_once(_):
            calls["n"] += 1
            if calls["n"] == 3:
                raise RuntimeError("simulated pipeline error")
        events = benchmark(cfg, self.base, runner=broken_once)
        report = summarize(events, cfg)
        self.assertEqual(report["benchmark_runs"], 3)
        self.assertEqual(report["failed_benchmark_runs"], 1)
        self.assertAlmostEqual(report["failure_rate_percent"], 100 / 3)
        self.assertTrue(any(x["error_type"] == "RuntimeError" for x in events))

    def test_microsecond_timestamps_and_io_outside_timer(self):
        cfg = dict(self.settings, measured_runs=2, warmup_runs=1)
        events = benchmark(cfg, self.base)
        summary = summarize(events, cfg)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "data/raw/test_run.jsonl"
            s = Path(tmp) / "outputs/ss6/summary.json"
            write_outputs(events, summary, p, s)
            lines = [json.loads(x) for x in p.read_text().splitlines()]
            self.assertEqual(len(lines), 4) # 1 metadata + 3 timed events
            self.assertEqual(lines[0]["event_type"], "metadata")
            self.assertIn("python_version", lines[0]["environment"])
            self.assertEqual(len(lines[1]["timestamp_utc"].split(".")[1].split("+")[0]), 6)
            self.assertIn("logging_io_ms_separate_from_measurements", json.loads(s.read_text()))

    def test_zero_success_runs_produce_null_percentiles(self):
        cfg = dict(self.settings, measured_runs=2, warmup_runs=0)
        def always_fail(_):
            raise ValueError("synthetic error")
        report = summarize(benchmark(cfg, self.base, runner=always_fail), cfg)
        self.assertEqual(report["failed_benchmark_runs"], 2)
        self.assertIsNone(report["p95_ms_success_only"])
        self.assertIsNone(report["median_ms_success_only"])


if __name__ == "__main__":
    unittest.main()
