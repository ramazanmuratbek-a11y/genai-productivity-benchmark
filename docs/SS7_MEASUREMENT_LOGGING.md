# SS7 / Course Laboratory 6 — Measurement Integrity and JSONL Logging

**Source handout:** `ss7.docx.pdf` (internally headed **Week 7**). The course may group this laboratory with Task 2; confirm course submission grouping separately. This document implements its practical software-benchmark checklist without changing the human-subject experiment's research question.

## What is timed — and what is not

- **Timed:** execution of the *existing* `validate_dataframe` + `analyze_pairs` Python pipeline on synthetic paired writing-task CSV data.
- **Not timed:** loading CSV, generating synthetic workloads, serialization to JSONL, printing, or writing summaries. I/O duration is recorded separately.
- **Not claimed:** LLM HTTP latency, user typing time, actual employee productivity, an intervention effect, or a newly recruited participant sample.
- The Task 2 scientific **primary outcome remains human task completion time in minutes**. This additional lab measures **software execution in milliseconds** to demonstrate measurement hygiene and reproducibility. Do not mix them in any analysis.

## Requirements traced to the uploaded lab

| Requirement | Implementation |
|---|---|
| Collection script (`src/collector.py` or `benchmark.py`) | `src/collector.py` wraps actual Task 2 Python validation and paired analysis |
| Machine-readable measurements | `data/raw/test_run.jsonl` created locally; this path is deliberately `.gitignore`d |
| Warmup vs benchmark | Configured `5` warmups and `100` measured runs; every record is tagged `phase` |
| At least 100 measurements | `100` `benchmark` records, plus `5` warmup records and a metadata record |
| Isolate I/O from timing | Workloads prepared before the timer; measurements are buffered in memory and written after timings; write time logged separately |
| Error and timeout awareness | Each failure is recorded as `status=error` with error type; aggregate failure rate reported; failed runs never masquerade as successes |
| p95/p99 and median | Computed from successful benchmark durations, with explicit failed count and denominator |
| Reproducible workload | `configs/collector.yaml`, fixed seed `42`, weighted small/medium/large synthetic workloads |
| Hardware/software metadata | Platform, OS version, CPU model/count, available RAM, Python/pandas/numpy/scipy versions |
| Self-audit | `tests/test_collector.py` tests seed schedule, phase counts, failure recording, input protection and log schema |

The uploaded handout discusses HTTP 429/500/504, retries, and HTTP rate limiting. **Those are not relevant to this local CSV pipeline because it makes no HTTP calls**. We record Python exceptions and failures instead. If the future study uses an external AI service, its API errors and participant experience must be documented separately.

The handout also discusses Pareto/Zipf and uniform load generation. The weighted processing workloads here are **illustrative engineering stress profiles**, not a scientifically validated model of human office work or real service traffic. `random_seed=42` fixes which workload is selected, but **does not make wall-clock timings identical across computers**.

## How to run from the repository root (PowerShell)

```powershell
# If you are using the Windows virtual environment already created for this project:
.\.venv\Scripts\python.exe src\collector.py --config configs\collector.yaml

# Check logs and aggregate statistics:
notepad outputs\ss6\collector_summary.json
(Get-Content data\raw\test_run.jsonl | Measure-Object -Line).Lines

# All repository tests, including these new collector tests:
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The JSONL file should have **106 lines**: one metadata line + five warmup measurements + 100 measured runs. Do not count the five warmups in software performance summaries. Sample schema:

```json
{"event_type":"measurement","timestamp_utc":"2026-11-05T12:00:00.000000+00:00","phase":"benchmark","run_index":1,"workload_profile":"small","input_rows":8,"duration_ms":16.25,"status":"ok","error_type":null,"error_message":null,"data_origin":"synthetic","measurement_target":"task2_python_validation_and_analysis"}
```

The above single-line JSON is a **format illustration**, not an actual recorded timing. Actual latency varies by machine and workload.

## Audit and caveats

1. Keep source data outside the timer and buffer all log records until all iterations finish.
2. The first five software runs are labeled `warmup`; **this does not justify discarding a human participant's first task**. Human-task order effects must be handled with the randomized counterbalanced protocol, not with JIT-style warmup removal.
3. Record `status=error` even if a run fails; do not silently exclude errors from failure rates. p95/p99 are estimated only among successes, and their interpretation requires the reported failure rate.
4. Keep participant data private: this script rejects `data_origin=real`, and `data/raw/` is excluded from Git and Docker build context.
5. Never interpret this synthetic software benchmark as evidence that Generative AI improves human productivity. Real completion times are in **minutes**, recorded through the separate human experiment protocol.
6. The course asks for 100 test measurements; that quantity is suitable here as a software logging demonstration, **not** as a sample size calculation for the proposed human study.

## Git workflow and relation to Task 3

Commit the **script, YAML, tests and this documentation** to a new feature branch from `main`. `data/raw/test_run.jsonl` is local-only by design. For a shareable evidence log, a clearly labeled sample of synthetic JSONL can be placed under `data/sample/`, after removing local identifiers and checking it contains no real participant data. Any such file must explicitly describe its synthetic origin.

Existing Task 3 files (`src/process_data.py`, `src/visualize.py`, `reports/figures/`, `notebooks/01_data_analysis.ipynb`) are **untouched**. They work on the writing-task CSV, whereas this engineering JSONL trace measures execution of the Python analysis code. Do not feed these milliseconds into the existing Task 3 human task completion time plots.

## Public demonstration artifact

A small non-sensitive reproducibility artifact is shipped as
`data/sample/ss7_software_benchmark_demo.jsonl` (106 lines) and
`data/sample/ss7_software_benchmark_summary.json`. These measurements were
recorded in the development environment, **not on the student's computer**.
Do not treat their millisecond runtimes as empirical employee measurements.
Re-run `src/collector.py` to create local `data/raw/test_run.jsonl` and
`outputs/ss6/collector_summary.json`; absolute times will change with hardware.

The updated `.github/workflows/tests.yml` runs both the existing regression
tests and an SS7 log-count smoke test on every push.
