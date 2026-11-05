# Final audit — Research Methods course repository (5 November 2026)

**Project:** The Impact of Generative AI Tools on Employee Productivity and Work Quality in Knowledge-Based Office Tasks
**Team:** Muratbek Ramazan; Tasbolatkyzy Zhanerke
**Repository:** https://github.com/ramazanmuratbek-a11y/genai-productivity-benchmark
**Audit basis:** Public GitHub `main` tree at `c8ffe661b9914ecfe5a53fdfcdf5823f0df39d95`, CI run 42051627235, previously supplied SS5–SS10 materials and Task 3 rubric notes. This audit checks artifact presence and reported execution, **not** grading decisions or scientific validity of data that do not exist.

## A. Verified technical evidence

| Evidence | Status | Location / limitation |
|---|---|---|
| PR #1 (SS6) merged | Verified | `/pull/1` |
| PR #2 (original Task 3 team analysis) merged | Verified | `/pull/2` |
| PR #3 (SS7 collector) merged | Verified | `/pull/3` |
| PR #4 (SS8 processing) merged | Verified | `/pull/4` |
| PR #5 (SS9 report) merged | Verified | `/pull/5` |
| PR #6 (SS10 Overleaf) merged | Verified | `/pull/6` |
| Unit tests | 44/44 passed on student's Windows machine | User-supplied terminal log, before PR #6 merge |
| GitHub Actions on main | Success | https://github.com/ramazanmuratbek-a11y/genai-productivity-benchmark/actions/runs/42051627235 |
| IEEE/Overleaf compile | Successfully displayed 3-page PDF | Screenshots of Overleaf; source `overleaf/` |
| Source, sample data, processed statistics | Present | `src/`, `data/sample/`, `data/processed/` |
| Research domain model | Present | `docs/domain_model.md` |
| Scientific figures | 4 charts (PNG and PDF) | `reports/figures/` |
| Demonstration notebooks | 2 named notebooks | `notebooks/01_data_analysis.ipynb`, `02_ss8_software_log_analysis.ipynb` |
| Paper-style analysis section | Present | `reports/paper_section_4.md` |

## B. Task 2 — assessment readiness

**Ready as a research proposal:** `docs/protocol.md`, `docs/task_sets.md`, `docs/evaluation_rubric.md`, `configs/experiment.yaml`, reproducible analysis modules, tests, and previously prepared `Task_2_Final_Updated_SS5_SS6_SS7.pdf` (separate PDF attachment for LMS). Task 2 documents a randomized, balanced human crossover experiment, but **has not recruited human participants**. SS7 is included as an engineering reproducibility supplement; whether it belongs in Task 2 is subject to the instructor's course grouping.

**Fair baseline:** without AI = the same human on a comparable task, not an LLM program, API latency or a sleep function. The sample is synthetic. Quality and factual metrics are secondary/exploratory. The provisional -5 quality margin is **not** formal statistical non-inferiority evidence.

## C. Task 3 — rubric crosswalk and remaining caution

This section follows the previously supplied Task 3 rubric topics (data 25, figures 25, notebook 20, domain model 15, repository 15). A passing grade or exact points **cannot be guaranteed** without the instructor's own review.

| Rubric area | Present in main | Important qualification |
|---|---|---|
| Raw logging and validation | `src/collector.py`, `configs/collector.yaml`, synthetic JSONL in `data/sample/` | `data/raw/test_run.jsonl` is generated locally and ignored for privacy. The assignment's exact raw-path expectation should be checked; do not upload real participant data. |
| Data processing and statistics | `src/process_data.py` (human sample) and `src/process_ss7_logs.py` (engineering stream) | These **are separate streams**, minutes vs milliseconds. SS8 filters 5 warm-ups, tracks 0 failures, and flags 11 IQR outliers without deleting them. |
| 95% uncertainty and p95/p99 | `data/processed/metrics_summary.csv` and `ss8_software_metrics_summary.csv` | n=4 fictional human pairs, 100 software runs. Tiny-sample human percentiles are unstable; machine timings from one host may be correlated. |
| Figures and visual integrity | Human `fig1_*` / `fig2_*`; engineering `ss8_software_*`, both PNG/PDF | Legacy human filename `fig1_latency_vs_load` is misleading; actual graph is *completion time by condition*. No RPS or HTTP traffic exists in this project. |
| Notebook reproducibility | `notebooks/01_data_analysis.ipynb`, `02_ss8_software_log_analysis.ipynb` | User should open and run **Restart Kernel and Run All** once locally before LMS submission. |
| Domain model / methodology | `docs/domain_model.md`, `docs/protocol.md`, `docs/evaluation_rubric.md` | Proposed design only, not empirical evidence. |
| Results and scientific reporting | `reports/paper_section_4.md`, `reports/ss9_equations.tex`, `reports/ss9_tables.tex` | Results must be called **synthetic demonstration**, never population estimates. |
| Repository structure and CI | `README.md`, `src/`, `tests/`, `.github/workflows/tests.yml`, Dockerfile | Existing CI is green; this audit patch refreshes the README and adds submission instructions. |
| Final tagged release | No published GitHub Release observed at audit time | If the rubric explicitly requires a final release tag, create it **after** merging this documentation patch. |

### Important distinction in the reported numbers

- Human-writing illustration: **4 fictional participant pairs** and **8 synthetic task observations**; mean paired time saved **3.875 minutes**; 95% percentile bootstrap CI **[0.00, 6.25] minutes**, including zero. No demonstrated AI effect.
- Technical pipeline illustration: **100 synthetic software benchmark runs**, **5 warm-ups excluded**, **0 failed runs**, mean **24.0577 ms**, median **22.9382 ms**, p95 **31.2728 ms**, p99 **35.7356 ms**. This is **Python analysis execution**, not worker time, model-inference latency or API throughput.
- Quality difference +2.875 points (with minus without) passes only a **descriptive** margin check. Do not claim formal non-inferiority.

## D. Remaining tasks before pressing Submit in Canvas

1. Merge the updated `README.md` and this audit documentation into `main` through a new PR, with the usual tests and CI.
2. Optionally create a named **final release tag** (e.g. `task3-final-2026`) on the merged `main` if the Task 3 rubric requests it. A tag is not the same thing as a GitHub Release; the latter can also be published from the GitHub Releases UI.
3. Verify the latest `notebooks/01_data_analysis.ipynb` and `02_ss8_software_log_analysis.ipynb` render and can be run end-to-end on the user's computer. The 44 unit tests do not by themselves execute every notebook cell or verify the LMS upload.
4. Download the final **Overleaf PDF** (from the actual Overleaf editor). Record the shared Overleaf link only if the team is willing to expose it; a PDF copy is sufficient unless SS10 requires a live link.
5. For **Task 2**, attach `Task_2_Final_Updated_SS5_SS6_SS7.pdf` and add the public repository link, if the assignment accepts a PDF + repo.
6. For **Task 3**, attach the separate `Task_3_Final_Submission_Report.pdf` generated for Canvas (or `reports/paper_section_4.md` if Markdown is permitted), with public repo URL and the specific locations of processed data, notebooks, figures and domain model.
7. Check the actual Canvas assignment panels for required file extensions, due dates, whether Task 2 and Task 3 need separate uploads, and whether a final tag or screenshots are compulsory. Avoid replacing the instructor's instructions with this checklist.
8. Do not submit private raw human data, sensitive prompts, credentials or local environment files. Share the public synthetic sample and optional local generated log only when safe and required.

## E. Change-management rule

This final patch edits **documentation only**. It intentionally does not alter Zhanerke's statistical code, anyone's git authorship, sample values, CI configuration or experimental design. Until a real study is approved and conducted, the correct status is **proposal and demonstration**, not completed empirical research.
