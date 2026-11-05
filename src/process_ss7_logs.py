"""SS8: read SS7 synthetic software-benchmark JSONL without mixing it with human time.

Outputs have the unit MILLISECONDS and are explicitly NOT employee productivity.
Warm-up records are excluded from summaries, but failures remain in denominators.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

REQUIRED_FIELDS = {'event_type','phase','run_index','workload_profile','input_rows',
                   'duration_ms','status','data_origin','measurement_target','timestamp_utc'}
ALLOWED_STATUSES = {'ok', 'error'}
ALLOWED_PHASES = {'warmup', 'benchmark'}
TARGET = 'task2_python_validation_and_analysis'


def read_jsonl(path: Path) -> tuple[pd.DataFrame, dict]:
    """Validate SS7 JSONL schema strictly; return records and metadata."""
    if not path.is_file():
        raise FileNotFoundError(f'SS7 raw JSONL not found: {path}')
    records = []
    metadata = None
    with path.open(encoding='utf-8') as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f'Invalid JSON on line {line_number}: {exc.msg}') from exc
            if not isinstance(event, dict):
                raise ValueError(f'Line {line_number}: JSON object expected.')
            kind = event.get('event_type')
            if kind == 'metadata':
                if metadata is not None or records:
                    raise ValueError('Exactly one metadata record must appear first.')
                metadata = event
                continue
            if kind != 'measurement':
                raise ValueError(f'Line {line_number}: unexpected event_type={kind!r}.')
            missing = REQUIRED_FIELDS - event.keys()
            if missing:
                raise ValueError(f'Line {line_number}: missing fields: {sorted(missing)}')
            if event['phase'] not in ALLOWED_PHASES:
                raise ValueError(f'Line {line_number}: invalid phase.')
            if event['status'] not in ALLOWED_STATUSES:
                raise ValueError(f'Line {line_number}: invalid status.')
            if event['data_origin'] != 'synthetic' or event['measurement_target'] != TARGET:
                raise ValueError('SS8 software-log mode accepts only synthetic SS7 analysis-pipeline logs.')
            if not isinstance(event['run_index'], int) or event['run_index'] < 1:
                raise ValueError(f'Line {line_number}: run_index must be a positive integer.')
            if not isinstance(event['input_rows'], int) or event['input_rows'] < 1:
                raise ValueError(f'Line {line_number}: input_rows must be a positive integer.')
            if not isinstance(event['workload_profile'], str) or not event['workload_profile']:
                raise ValueError(f'Line {line_number}: workload_profile must be nonempty.')
            d = event['duration_ms']
            if d is not None and (not isinstance(d, (int, float)) or not math.isfinite(d) or d < 0):
                raise ValueError(f'Line {line_number}: duration_ms must be finite and nonnegative.')
            if event['status'] == 'ok' and (d is None or d <= 0):
                raise ValueError(f'Line {line_number}: success needs a positive duration_ms.')
            try:
                pd.to_datetime(event['timestamp_utc'], utc=True, errors='raise')
            except (ValueError, TypeError) as exc:
                raise ValueError(f'Line {line_number}: invalid timestamp_utc.') from exc
            records.append(event)
    if metadata is None:
        raise ValueError('SS7 log must start with a metadata record.')
    if not records:
        raise ValueError('SS7 log has no measurements.')
    frame = pd.DataFrame.from_records(records)
    if frame.duplicated(subset=['phase', 'run_index']).any():
        raise ValueError('Duplicate run_index within the same phase.')
    if not (frame.phase == 'benchmark').any():
        raise ValueError('At least one benchmark-phase record is required.')
    return frame, metadata


def bootstrap_ci(values: np.ndarray, seed: int = 42, resamples: int = 10000) -> tuple[float | None, float | None]:
    """Percentile bootstrap 95% CI for mean of successful software timings."""
    v = np.asarray(values, dtype=float)
    if len(v) < 2:
        return None, None
    rng = np.random.default_rng(seed)
    # Chunk sampling to avoid allocating huge arrays for larger log files.
    samples = []
    for amount in range(0, resamples, 400):
        size = min(400, resamples - amount)
        ids = rng.integers(0, len(v), size=(size, len(v)))
        samples.append(v[ids].mean(axis=1))
    boot = np.concatenate(samples)
    return float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))


def mark_outliers(frame: pd.DataFrame) -> pd.DataFrame:
    """Non-destructively flag successful benchmark outliers per input_rows group."""
    clean = frame.copy()
    clean['iqr_outlier'] = False
    clean['iqr_lower_ms'] = np.nan
    clean['iqr_upper_ms'] = np.nan
    good = clean[(clean.phase == 'benchmark') & (clean.status == 'ok')]
    for rows, group in good.groupby('input_rows'):
        durations = group['duration_ms'].astype(float)
        q25, q75 = np.percentile(durations, [25, 75])
        iqr = q75 - q25
        low, high = float(q25 - 1.5 * iqr), float(q75 + 1.5 * iqr)
        clean.loc[group.index, 'iqr_outlier'] = (durations < low) | (durations > high)
        clean.loc[group.index, 'iqr_lower_ms'] = low
        clean.loc[group.index, 'iqr_upper_ms'] = high
    return clean


def summarize(frame: pd.DataFrame, seed: int = 42, resamples: int = 10000) -> pd.DataFrame:
    """Summaries by profile plus overall; error rates include all benchmark runs."""
    benchmark = frame[frame.phase == 'benchmark']
    groups = [('overall', benchmark)]
    groups.extend((f'{p} ({rows} rows)', subset) for (p, rows), subset in
                  benchmark.groupby(['workload_profile', 'input_rows'], sort=True))
    out = []
    for i, (name, grp) in enumerate(groups):
        success = grp.loc[grp.status == 'ok', 'duration_ms'].astype(float).to_numpy()
        n, ns = len(grp), len(success)
        low, high = bootstrap_ci(success, seed + i, resamples)
        row = {
            'source': 'ss7_software_pipeline_synthetic',
            'data_origin': 'synthetic',
            'measurement_unit': 'milliseconds',
            'group': name,
            'benchmark_runs': n,
            'successful_runs': ns,
            'failed_runs': n - ns,
            'failure_rate_percent': 100 * (n-ns) / n,
            'iqr_outlier_flags': int(grp['iqr_outlier'].sum()),
            'mean_ms': float(np.mean(success)) if ns else np.nan,
            'sd_ms': float(np.std(success, ddof=1)) if ns > 1 else np.nan,
            'p25_ms': float(np.percentile(success, 25)) if ns else np.nan,
            'median_ms': float(np.median(success)) if ns else np.nan,
            'p75_ms': float(np.percentile(success, 75)) if ns else np.nan,
            'p95_ms': float(np.percentile(success, 95)) if ns else np.nan,
            'p99_ms': float(np.percentile(success, 99)) if ns else np.nan,
            'bootstrap_mean_ci95_lower_ms': low if low is not None else np.nan,
            'bootstrap_mean_ci95_upper_ms': high if high is not None else np.nan,
        }
        out.append(row)
    return pd.DataFrame.from_records(out)


def run_analysis(source: Path, output_summary: Path, output_detail: Path, output_audit: Path,
                 seed: int = 42, resamples: int = 10000) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    all_events, metadata = read_jsonl(source)
    marked = mark_outliers(all_events)
    summary = summarize(marked, seed, resamples)
    kept = marked[marked.phase == 'benchmark'].copy()
    for path in (output_summary, output_detail, output_audit):
        path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_summary, index=False, float_format='%.8f')
    kept.to_csv(output_detail, index=False)
    audit = {
        'status': 'SYNTHETIC SOFTWARE BENCHMARK ONLY — NOT HUMAN PRODUCTIVITY EVIDENCE',
        'source_file': str(source),
        'measurement_target': TARGET,
        'unit': 'milliseconds',
        'warmup_excluded': int((marked.phase == 'warmup').sum()),
        'benchmark_kept': len(kept),
        'benchmark_failures': int((kept.status == 'error').sum()),
        'benchmark_iqr_outlier_flags_not_removed': int(kept['iqr_outlier'].sum()),
        'bootstrap_resamples': resamples,
        'random_seed': seed,
        'environment_from_log': metadata.get('environment'),
        'caveat': 'IQR flags are not automatic exclusions. Timing CI describes synthetic software runs, not humans.'
    }
    output_audit.write_text(json.dumps(audit, indent=2, allow_nan=False, default=str) + '\n', encoding='utf-8')
    return summary, kept, audit


def main() -> None:
    p = argparse.ArgumentParser(description='SS8 process synthetic SS7 software JSONL into clean summaries.')
    p.add_argument('--input', type=Path, default=Path('data/sample/ss7_software_benchmark_demo.jsonl'))
    p.add_argument('--output', type=Path, default=Path('data/processed/ss8_software_metrics_summary.csv'))
    p.add_argument('--detail', type=Path, default=Path('outputs/ss8/clean_software_measurements.csv'))
    p.add_argument('--audit', type=Path, default=Path('outputs/ss8/ss8_audit.json'))
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--resamples', type=int, default=10000)
    a = p.parse_args()
    if a.resamples < 100:
        p.error('--resamples must be at least 100.')
    summary, cleaned, audit = run_analysis(a.input, a.output, a.detail, a.audit, a.seed, a.resamples)
    print('Input:', a.input)
    print('Warmup excluded:', audit['warmup_excluded'])
    print('Benchmark records:', audit['benchmark_kept'])
    print('Failures:', audit['benchmark_failures'])
    print('Outliers flagged, not deleted:', audit['benchmark_iqr_outlier_flags_not_removed'])
    print(summary[['group','benchmark_runs','successful_runs','failure_rate_percent','median_ms','p95_ms','p99_ms']].round(3).to_string(index=False))
    print('Summaries:', a.output)
    print('Clean log:', a.detail)
    print('Audit:', a.audit)


if __name__ == '__main__':
    main()
