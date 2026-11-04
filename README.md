# Generative AI and Knowledge-Worker Productivity

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Status: Experimental proposal](https://img.shields.io/badge/Status-Experimental%20Proposal-yellow.svg)
![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)

**Full title:** The Impact of Generative AI Tools on Employee Productivity and Work Quality in Knowledge-Based Office Tasks
**Institution:** Narxoz University
**Research team:** Muratbek Ramazan and Tasbolatkyzy Zhanerke
**Study status:** Methodology and reproducibility demonstration only; **no real participants or empirical results yet**.

## Project overview and research aim

This repository supports a **proposed** randomized counterbalanced crossover
study of human professional writing tasks **with versus without Generative AI**.
It measures *human task completion time*, not LLM API latency or HumanEval code
accuracy. The fair baseline is a human writer using standard tools without AI.

**Primary research question (RQ2):** Does AI assistance reduce task completion
time on equivalent professional writing tasks? **H0:** no reduction in mean
paired completion time. **H1:** a reduction in mean paired completion time.

**Secondary outcomes:** output quality (0–100, two blinded raters if feasible)
and factual accuracy (%). **Provisional quality guardrail:** the quality-score
difference with-AI minus without-AI should not be lower than -5 points; the
margin requires justification before a formal non-inferiority test.

**RQ3** explores differences by professional experience. **RQ1**, which asks
how workers integrate AI into daily workflows, requires a separate descriptive
survey/observational component and is not answered by this experiment.

## Authors and contributions

- **Muratbek Ramazan** — study methodology, research analysis pipeline,
  reproducible infrastructure.
- **Tasbolatkyzy Zhanerke** — evaluation rubric design,
  factual evaluation metrics, scoring guidelines,
  and research documentation.

## Repository structure

```text
configs/experiment.yaml             Proposed settings, no secrets
data/sample/example_measurements.csv Synthetic demonstration only
data/README.md                     Data schema and privacy
src/analyze.py                     Calculates outcomes from CSV
src/randomize.py                   Reproducible counterbalanced assignment generator
src/metrics.py                     Paired statistics and quality guardrail
src/validate_data.py               Input validation and exclusion checks
tests/test_metrics.py              Automated unit tests
docs/protocol.md                   Study design and constraints
docs/task_sets.md                  Illustrative matched writing tasks
docs/evaluation_rubric.md          Scoring criteria
notebooks/analysis.ipynb           Optional exploratory demonstration
Dockerfile                         Pinned Python base image
requirements.txt                   Pinned Python packages
LICENSE                            MIT code license
```

## System requirements

Docker Desktop with Linux containers (Windows, macOS or Linux) **or** Python
3.11 and pip. CPU-only laptop/desktop sufficient; **no CUDA, GPU or OpenAI API
key is required**. The AI intervention is conducted in a separate browser-based
human study, not by the CSV analysis pipeline. JupyterLab runs locally on port
8888 if launched manually.

## Quickstart: reproducible demonstration

**Docker — two commands from the repository root:**

```bash
docker build -t genai-writing-study .
docker run --rm genai-writing-study
```

The container validates the synthetic CSV, computes paired metrics, labels the
output as a **synthetic demonstration**, and prints the derived mean time
difference. Outputs are generated inside the ephemeral container; to keep them
locally, use a bind mount (on Bash/macOS/Linux):

```bash
docker run --rm -v "$(pwd)/outputs:/app/outputs" genai-writing-study
```

**Local Python 3.11:**

```bash
python -m pip install -r requirements.txt
python src/randomize.py --count 8
python src/validate_data.py data/sample/example_measurements.csv
python src/analyze.py --input data/sample/example_measurements.csv --output-dir outputs/demo
python -m unittest discover -s tests -v
```

**JupyterLab in Docker (local computer):**

```bash
docker run --rm -p 127.0.0.1:8888:8888 genai-writing-study \
  jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

Open the tokenized local URL shown by Jupyter. Never expose a token-free Jupyter
server publicly. For local Python, `jupyter lab` opens the same notebook environment.

## Expected output (not experimental findings)

The analysis writes `outputs/demo/summary.json` and
`outputs/demo/participant_effects.csv`. It includes these metrics:

| Metric | Unit | Definition |
|---|---|---|
| Mean paired time difference | minutes | With AI minus without AI |
| Relative time reduction | percent | (mean no-AI time - mean AI time) / mean no-AI time × 100 |
| Output quality difference | points | Difference in mean paired 0–100 quality score |
| Factual accuracy difference | percentage points | Difference in correct facts / total facts × 100 |
| Factual Precision | percent | Supported claims / all assessable factual claims × 100 |
| Factual Recall | percent | Correctly covered anchor facts / total required anchor facts × 100 |
| Factual F1-score | percent | Harmonic mean of Precision and Recall |
| Guardrail assessment | categorical | 95% CI lower quality difference > -5 required; otherwise not established |
| Excluded pairs | participants | Paired records with incomplete task(s) |

The supplied CSV contains fictional observations labelled `synthetic`. Any
result computed from this file **only tests that the software runs**; it is not
evidence that AI improves productivity. Do not present illustrative output as
actual findings.

## Reproducibility and limitations

Study design and the paired data schema are documented in `docs/protocol.md`,
`docs/evaluation_rubric.md`, and `data/README.md`. Versions are pinned in
`requirements.txt`, and the Docker base image uses a patch-specific tag plus
immutable digest. Random assignment must be saved using the seed specified in
`configs/experiment.yaml` when the real study is conducted. Hosted GenAI
responses may vary and cannot be guaranteed bit-for-bit identical. With no
recruited participants, no causal conclusions are supported yet.

Never commit identifiable participant data, proprietary source materials,
credentials or local .env files. For real studies obtain informed consent and
comply with institutional data-protection requirements.

## Citation

```bibtex
@misc{muratbek_tasbolatkyzy_2026_genai_productivity,
  author = {Muratbek, Ramazan and Tasbolatkyzy, Zhanerke},
  title = {The Impact of Generative AI Tools on Employee Productivity and Work Quality in Knowledge-Based Office Tasks},
  year = {2026},
  howpublished = {GitHub repository},
  url = {https://github.com/ramazanmuratbek-a11y/genai-productivity-benchmark}
}
```

## License

Source code is distributed under the repository's [MIT License](LICENSE).
The license does not override participant consent or grant permission to
redistribute confidential or third-party research data.

## Verified Reproducibility

The research analysis pipeline has been verified in three environments:

- Local Windows Python environment: 20 unit tests passed.
- GitHub Actions: automated reproducibility checks passed.
- Docker Desktop with WSL 2: Docker image built and executed successfully.

The Docker demonstration processed 4 complete synthetic participant pairs
and reported a mean paired time difference of -3.875 minutes.

These are synthetic demonstration records, not empirical research findings.



---

## Task 3: Research Results and Scientific Visualization

### Study Status

This project currently uses synthetic demonstration data, not real experimental results.

The dataset contains 8 observations from 4 paired participants.

### Statistical Results

| Metric | Without AI | With AI |
|---|---:|---:|
| Mean completion time (minutes) | 23.38 | 19.50 |
| Median completion time (minutes) | 23.75 | 19.50 |
| Standard deviation (minutes) | 2.56 | 2.38 |
| p95 (minutes) | 25.78 | 21.85 |
| p99 (minutes) | 25.96 | 21.97 |
| Quality score | 81.63 | 84.50 |
| Factual accuracy (%) | 85.00 | 95.00 |
| Unsupported claim rate (%) | 9.17 | 15.71 |

### Paired Bootstrap Analysis

Mean paired time saved: **3.875 minutes**.

95% bootstrap confidence interval: **[0.00, 6.25] minutes**.

The analysis uses 10,000 paired bootstrap resamples and random seed 42.

The interval includes zero, so a positive time-saving effect is not conclusively established.

### Quality Guardrail

The observed mean quality difference is +2.875 points (with AI minus without AI).

The descriptive -5-point tolerance is satisfied, but formal statistical non-inferiority has not been established.

### Scientific Figures

**Figure 1 — Mean Completion Time**

![Mean completion time](reports/figures/fig1_latency_vs_load.png)

**Figure 2 — Completion Time Distribution**

![Completion time distribution](reports/figures/fig2_distribution_boxplot.png)

Both figures are available as 300 DPI PNG and PDF files.

### Reproducibility

Run the following commands from the repository root:

    python -m pip install -r requirements.txt
    python src/process_data.py
    python src/visualize.py
    jupyter lab

Notebook: `notebooks/01_data_analysis.ipynb`

Domain model: `docs/domain_model.md`

Processed statistics: `data/processed/metrics_summary.csv`

### Limitations

All observations are synthetic and the dataset contains only four paired participants.

Warm-up filtering is not applied because the dataset contains no separately labeled warm-up runs.

Task-order, learning, and carryover effects are not estimated. Extreme percentiles are unstable at this sample size.

These results demonstrate the analysis pipeline, not empirical evidence that AI improves productivity.
