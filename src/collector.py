"""Synthetic benchmark of the Task 2 CSV-analysis pipeline, with JSONL logging.

Course-lab demonstration only. This measures Python software execution latency
(milliseconds), NOT how long human employees take to complete writing tasks.
The input must be explicitly labeled synthetic; identifiable/raw study records
are intentionally refused.
"""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import random
import statistics
import sys
from time import perf_counter_ns
from typing import Callable

import numpy as np
import pandas as pd
import scipy
import yaml

from metrics import analyze_pairs
from validate_data import validate_dataframe


def utc_now() -> str:
    """ISO-8601 timestamp with microsecond formatting and UTC zone."""
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def physical_memory_bytes():
    """Use standard library only; return None when the OS cannot report RAM."""
    if os.name == "nt":
        try:
            import ctypes

            class MemoryStatus(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                           ("ullTotalPhys", ctypes.c_ulonglong),
                           ("ullAvailPhys", ctypes.c_ulonglong),
                           ("ullTotalPageFile", ctypes.c_ulonglong),
                           ("ullAvailPageFile", ctypes.c_ulonglong),
                           ("ullTotalVirtual", ctypes.c_ulonglong),
                           ("ullAvailVirtual", ctypes.c_ulonglong),
                           ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            status = MemoryStatus()
            status.dwLength = ctypes.sizeof(status)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return int(status.ullTotalPhys)
        except (OSError, AttributeError, ValueError):
            return None
    else:
        try:
            return int(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES"))
        except (OSError, ValueError, AttributeError):
            return None
    return None


def environment_metadata():
    return {
        "platform": platform.platform(),
        "os": platform.system(),
        "os_release": platform.release(),
        "cpu_model": platform.processor() or platform.uname().processor or "not_reported",
        "logical_cpu_count": os.cpu_count(),
        "total_ram_bytes": physical_memory_bytes(),
        "python_version": platform.python_version(),
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
    }


def load_settings(path: Path):
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("collector"), dict):
        raise ValueError("The YAML file must contain a collector mapping.")
    cfg = payload["collector"]
    required = {"source_csv", "output_jsonl", "summary_json", "random_seed",
                "warmup_runs", "measured_runs", "workload_profiles"}
    missing = required - set(cfg)
    if missing:
        raise ValueError(f"Missing collector settings: {sorted(missing)}")
    if (not isinstance(cfg["warmup_runs"], int) or cfg["warmup_runs"] < 0
            or not isinstance(cfg["measured_runs"], int) or cfg["measured_runs"] < 1):
        raise ValueError("warmup_runs must be >=0, and measured_runs must be >=1.")
    if not isinstance(cfg["random_seed"], int):
        raise ValueError("random_seed must be an integer.")
    profiles = cfg["workload_profiles"]
    if not isinstance(profiles, list) or not profiles:
        raise ValueError("workload_profiles must be a non-empty list.")
    for profile in profiles:
        if (not isinstance(profile, dict) or not isinstance(profile.get("name"), str)
                or not isinstance(profile.get("pair_multiplier"), int)
                or profile["pair_multiplier"] < 1
                or profile["pair_multiplier"] > 20
                or not isinstance(profile.get("weight"), (float, int))
                or profile["weight"] <= 0):
            raise ValueError("Invalid workload profile: name, pair_multiplier (1..20), weight >0 required.")
    if len({p["name"] for p in profiles}) != len(profiles):
        raise ValueError("Workload profile names must be unique.")
    return cfg


def synthetic_workload(base: pd.DataFrame, multiplier: int) -> pd.DataFrame:
    """Duplicate synthetic PAIRS with new pseudonyms, preserving crossover schema."""
    if multiplier < 1:
        raise ValueError("multiplier must be positive")
    if base.empty or set(base["data_origin"].unique()) != {"synthetic"}:
        raise ValueError("Collector accepts exclusively synthetic example data.")
    parts = []
    for block in range(multiplier):
        chunk = base.copy()
        chunk["participant_id"] = chunk["participant_id"].astype(str).map(
            lambda id_value: f"{id_value}_S{block:02d}"
        )
        parts.append(chunk)
    return pd.concat(parts, ignore_index=True)


def task2_analysis_pipeline(frame: pd.DataFrame):
    """Existing Task 2 validation + paired statistics, without disk I/O."""
    checked = validate_dataframe(frame)
    summary, _ = analyze_pairs(checked)
    if summary.get("participants_with_complete_pairs", 0) < 1:
        raise ValueError("Demo workload lacks complete pairs.")
    return summary


def linear_percentile(values, fraction: float):
    """Linear-interpolated percentile of successful software timings."""
    if not values:
        return None
    return float(np.percentile(values, fraction * 100))


def benchmark(settings: dict, base: pd.DataFrame, runner: Callable = task2_analysis_pipeline):
    """Prepare workloads outside timer; buffer log in memory; keep failures."""
    if set(base["data_origin"].unique()) != {"synthetic"}:
        raise ValueError("Real participant data must not enter this synthetic lab benchmark.")
    rng = random.Random(settings["random_seed"])
    profiles = settings["workload_profiles"]
    profile_names = [x["name"] for x in profiles]
    profile_weights = [x["weight"] for x in profiles]
    cache = {p["name"]: synthetic_workload(base, p["pair_multiplier"]) for p in profiles}
    events = []
    for phase, count in [("warmup", settings["warmup_runs"]),
                         ("benchmark", settings["measured_runs"])]:
        for index in range(1, count + 1):
            selected = rng.choices(profile_names, weights=profile_weights, k=1)[0]
            current = cache[selected]
            start = perf_counter_ns()
            error_type = None
            error_message = None
            try:
                runner(current)
                status = "ok"
            except Exception as exc:  # intentionally preserve failures for audit
                status = "error"
                error_type = type(exc).__name__
                error_message = str(exc).replace("\r", " ").replace("\n", " ")[:160]
            elapsed_ms = (perf_counter_ns() - start) / 1_000_000
            events.append({
                "event_type": "measurement",
                "timestamp_utc": utc_now(),
                "phase": phase,
                "run_index": index,
                "workload_profile": selected,
                "input_rows": int(len(current)),
                "duration_ms": round(elapsed_ms, 6),
                "status": status,
                "error_type": error_type,
                "error_message": error_message,
                "data_origin": "synthetic",
                "measurement_target": "task2_python_validation_and_analysis",
            })
    return events


def summarize(events, settings):
    active = [x for x in events if x["phase"] == "benchmark"]
    success = [x["duration_ms"] for x in active if x["status"] == "ok"]
    failures = len(active) - len(success)
    return {
        "status": "SYNTHETIC SOFTWARE BENCHMARK ONLY - NOT HUMAN PRODUCTIVITY EVIDENCE",
        "data_origin": "synthetic",
        "measurement_target": "task2_python_validation_and_analysis",
        "unit": "milliseconds",
        "warmup_runs": settings["warmup_runs"],
        "benchmark_runs": len(active),
        "successful_benchmark_runs": len(success),
        "failed_benchmark_runs": failures,
        "failure_rate_percent": 100 * failures / len(active) if active else None,
        "mean_ms_success_only": float(statistics.mean(success)) if success else None,
        "median_ms_success_only": float(statistics.median(success)) if success else None,
        "p95_ms_success_only": linear_percentile(success, .95),
        "p99_ms_success_only": linear_percentile(success, .99),
        "percentile_note": "Successful runs only; failures are separately counted, not silently deleted.",
        "random_seed": settings["random_seed"],
        "workload_profiles": settings["workload_profiles"],
    }


def write_outputs(events, summary, jsonl_path: Path, summary_path: Path):
    """Write buffered records after all timings; record I/O overhead separately."""
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    meta = {
        "event_type": "metadata",
        "timestamp_utc": utc_now(),
        "purpose": "synthetic data-analysis pipeline diagnostic, not human study",
        "environment": environment_metadata(),
        "seed": summary["random_seed"],
    }
    t0 = perf_counter_ns()
    with jsonl_path.open("w", encoding="utf-8", newline="\n") as target:
        target.write(json.dumps(meta, allow_nan=False) + "\n")
        for row in events:
            target.write(json.dumps(row, allow_nan=False) + "\n")
    logging_io_ms = (perf_counter_ns() - t0) / 1_000_000
    summary["logging_io_ms_separate_from_measurements"] = round(logging_io_ms, 6)
    summary["log_path"] = str(jsonl_path)
    summary["environment"] = meta["environment"]
    summary_path.write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Synthetic Task 2 pipeline benchmark with JSONL logging.")
    parser.add_argument("--config", type=Path, default=Path("configs/collector.yaml"))
    parser.add_argument("--output", type=Path, default=None, help="Override ignored JSONL log path.")
    parser.add_argument("--summary", type=Path, default=None, help="Override ignored summary path.")
    args = parser.parse_args()
    cfg = load_settings(args.config)
    base = pd.read_csv(cfg["source_csv"])
    # Fail fast on malformed sample, before generating any benchmark output.
    validate_dataframe(base)
    if set(base["data_origin"].unique()) != {"synthetic"}:
        raise SystemExit("Refusing real participant records in this synthetic benchmark.")
    events = benchmark(cfg, base)
    report = summarize(events, cfg)
    write_outputs(events, report, args.output or Path(cfg["output_jsonl"]),
                  args.summary or Path(cfg["summary_json"]))
    print("SYNTHETIC software-pipeline benchmark only; not human participant data.")
    print("Measured runs:", report["benchmark_runs"],
          "Warm-up runs:", report["warmup_runs"],
          "Failures:", report["failed_benchmark_runs"])
    print("p95 (ms):", report["p95_ms_success_only"],
          "p99 (ms):", report["p99_ms_success_only"])
    print("JSONL:", args.output or cfg["output_jsonl"])
    print("Summary:", args.summary or cfg["summary_json"])


if __name__ == "__main__":
    main()
