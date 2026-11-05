# SS9 — Scientific Reporting and Publication-Ready Mathematics

**Research project:** The Impact of Generative AI Tools on Employee Productivity and Work Quality in Knowledge-Based Office Tasks
**Status:** Documentation of **synthetic software/analysis demonstrations only**. No actual human study has been carried out.

## Deliverables

| SS9 requirement | File or explanation |
|:--|:--|
| Formal metrics, notation and equations | `reports/paper_section_4.md`, `reports/ss9_equations.tex` |
| Clean comparison tables (booktabs) | `reports/ss9_tables.tex`, generated from committed processed CSV |
| Captions with metrics and uncertainty explanations | `reports/paper_section_4.md`, Figures 1–4 |
| PDF and high-resolution PNG | Existing figures in `reports/figures/` from Task 3 and SS8; unchanged |
| Scientific Section 4: Results & Discussion | `reports/paper_section_4.md` |
| Automatic consistency check | `src/generate_ss9_report.py --check`, `tests/test_ss9_reporting.py`, CI step |

## Extremely important: two different units and outcomes

1. **Human-writing demonstration:** n=4 fictional participant pairs; human task time is in **minutes**. The two conditions (without AI / with AI) have a simulated mean paired time saving of 3.875 min. The 95% paired-bootstrap confidence interval [0, 6.25] includes zero. There are **no real participants**; no claim that AI improves employee productivity can be made.
2. **Technical pipeline demonstration:** n=100 repeated synthetic software runs; Python execution time is in **milliseconds**. This measures the research code, not workers, not ChatGPT API latency and not HTTP request throughput. The technical bootstrap is over runs, not human pairs.

The SS9 report keeps the data sources and captions separate; do **not** combine minutes and milliseconds in a single analysis.

## Generated formulas and presentation

The LaTeX source includes equation labels `eq:ss9:paired-saving`, `eq:ss9:average-saving`, `eq:ss9:speedup`, `eq:ss9:quality`, `eq:ss9:bootstrap` and `eq:ss9:percentiles`. The Markdown report contains a notation table. `reports/ss9_tables.tex` uses `\toprule`, `\midrule`, `\bottomrule`, **no vertical grid lines**, and explicit unit labels.

When later moving to an Overleaf/IEEE or ACM document (the separate SS10 assignment), add `\usepackage{amsmath,amssymb,booktabs,graphicx,hyperref}` and import the relevant `.tex` files using `\input`. Those `.tex` files are components, **not a complete stand-alone LaTeX paper**. We make no claim to have created or compiled an Overleaf project yet.

## Run / verify on Windows PowerShell

From the root of the Git repository (using your existing virtual environment):

```powershell
.\.venv\Scripts\python.exe src\generate_ss9_report.py --check
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

To regenerate if the **committed synthetic source summaries** change:

```powershell
.\.venv\Scripts\python.exe src\generate_ss9_report.py
.\.venv\Scripts\python.exe src\generate_ss9_report.py --check
```

The generated Markdown includes links to the existing figures in `reports/figures/`. Do not regenerate the `data/processed/` source tables here: they are owned by the prior Task 3 and SS8 processing workflows.

## SS9 audit

- [x] Distinguish sources: fictional human paired data vs synthetic software timings.
- [x] Preserve explicit units (minutes, milliseconds, % and 0–100 points).
- [x] Present mean ± sample SD and clarify bootstrap confidence intervals.
- [x] Write paired formula, percentiles, speedup ratio and full notation.
- [x] Use booktabs tables with captions and labels; supply figure captions.
- [x] Reuse all four existing figure pairs (PNG/PDF); no changes to Zhanerke's images.
- [x] Prevent false claims of causal effects and unsupported non-inferiority.
- [x] Validate generated report consistency via 4 new unit tests and CI.

**Limitations:** Source CSVs are synthetic; four fictional human pairs are too few to support real inference. SS7/SS8 technical timings are from a development environment, may be autocorrelated and vary by hardware. The four figures are reused and remain informative demonstrations, not empirical outcomes. SS10 Overleaf/LaTeX paper compilation is not part of this SS9 package.
