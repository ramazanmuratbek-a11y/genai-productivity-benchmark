"""Create SS9 publication-ready *synthetic demonstration* report/tables from committed summaries.

This never measures humans or claims statistical evidence of an AI effect.
Usage: python src/generate_ss9_report.py [--check]
"""
import argparse
import csv
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HUMAN = ROOT / 'data/processed/metrics_summary.csv'
SOFTWARE = ROOT / 'data/processed/ss8_software_metrics_summary.csv'
REPORT = ROOT / 'reports/paper_section_4.md'
TABLES = ROOT / 'reports/ss9_tables.tex'


def fmt(row, key, places=2):
    unit = Decimal(1).scaleb(-places)
    return format(Decimal(str(row[key])).quantize(unit, rounding=ROUND_HALF_UP), f".{places}f")


def load_csv(path):
    with path.open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f'No records in {path}')
    return rows


def data_rows():
    human = load_csv(HUMAN)
    software = load_csv(SOFTWARE)
    h = {row['condition']: row for row in human}
    s = {row['group']: row for row in software}
    if set(h) != {'with_ai', 'without_ai'} or 'overall' not in s:
        raise ValueError('Required conditions or overall software group missing')
    if any(r['data_origin'] != 'synthetic' for r in human + software):
        raise ValueError('SS9 demonstration generator refuses to relabel real data as synthetic')
    if any(r.get('measurement_unit') != 'milliseconds' for r in software):
        raise ValueError('Software timings must be in milliseconds')
    if len({int(r['count']) for r in human}) != 1:
        raise ValueError('Paired study conditions need the same count')
    return h, s


def stats():
    h, s = data_rows()
    control, treatment = h['without_ai'], h['with_ai']
    overall = s['overall']
    f = lambda row, key: float(row[key])
    n = int(control['count'])
    if n <= 0 or f(control, 'mean') <= 0 or f(treatment, 'mean') <= 0:
        raise ValueError('Positive nonempty human task duration required')
    mean_saved = f(control, 'mean') - f(treatment, 'mean')
    if abs(f(control, 'paired_mean_time_saved_minutes') - mean_saved) > 1e-5:
        raise ValueError('Inconsistent paired time saving in human source table')
    if int(overall['successful_runs']) + int(overall['failed_runs']) != int(overall['benchmark_runs']):
        raise ValueError('Software success and failure totals do not match')
    if int(overall['benchmark_runs']) < 100:
        raise ValueError('SS7 sample must contain at least 100 benchmark observations')
    return {'h': h, 's': s, 'control': control, 'treatment': treatment, 'overall': overall,
            'n': n, 'saved': mean_saved,
            'speedup': f(control, 'mean') / f(treatment, 'mean'),
            'reduction': 100 * mean_saved / f(control, 'mean')}


def markdown_report(v):
    c, a, t = v['control'], v['treatment'], v['overall']
    f = lambda row, key: float(row[key])
    return rf'''# 4. Experimental Results & Discussion — Synthetic Demonstration Only

**Project:** The Impact of Generative AI Tools on Employee Productivity and Work Quality in Knowledge-Based Office Tasks
**Authors:** Muratbek Ramazan and Tasbolatkyzy Zhanerke · Narxoz University
**Status:** SOFTWARE/ANALYSIS DEMONSTRATION — **NO RECRUITED PARTICIPANTS OR EMPIRICAL AI-PRODUCTIVITY RESULTS.**

## 4.1 Research status and data provenance

The proposed scientific study is a randomized counterbalanced crossover of professional-writing tasks with AI versus without AI. The primary outcome is **human task completion time in minutes**. The supplied `data/sample/example_measurements.csv` contains **{v['n']} fictional paired participants** ({2*v['n']} synthetic task records). It illustrates the analysis, not observations of workers. The companion SS7/SS8 material measures *execution of the Python validation-and-analysis pipeline* on generated test workloads in **milliseconds**. It is not AI response latency, human writing speed, or another experimental condition. These two data streams must never be pooled.

Data inputs: [`data/processed/metrics_summary.csv`](../data/processed/metrics_summary.csv) and [`data/processed/ss8_software_metrics_summary.csv`](../data/processed/ss8_software_metrics_summary.csv). The human analysis scripts were prepared by the research team; the SS7/SS8 technical instrumentation is a separately documented extension. See [`docs/domain_model.md`](../docs/domain_model.md) and [`docs/SS8_DATA_PROCESSING.md`](../docs/SS8_DATA_PROCESSING.md).

## 4.2 Formal notation and estimands

Let $n$ be the number of paired participant records, $T_{{i,0}}$ the without-AI completion time in **minutes**, and $T_{{i,1}}$ the with-AI time in **minutes**. Let $Q_{{i,0}}$ and $Q_{{i,1}}$ denote corresponding quality scores on a 0–100 scale.

$$
D_i = T_{{i,0}} - T_{{i,1}}, \qquad
\overline{{D}} = \frac{{1}}{{n}}\sum_{{i=1}}^n D_i.
$$

Positive $D_i$ indicates time saved. The descriptive speedup ratio and relative reduction are

$$
S = \frac{{\overline{{T}}_0}}{{\overline{{T}}_1}}, \qquad
R_T = 100\left(1-\frac{{\overline{{T}}_1}}{{\overline{{T}}_0}}\right)\%.
$$

The $q$th percentile $p_q$ is the empirical quantile at cumulative probability $q/100$. For a percentile-bootstrap confidence interval on a **mean**, draw $B=10{{,}}000$ samples of the relevant observation unit with replacement using seed 42, recompute the mean, and take its 2.5th and 97.5th percentiles. For the paired human demonstration, the resampling unit is the participant-level **paired difference** $D_i$; for the software illustration, it is a successful benchmark run. These two uncertainty calculations have different meanings and assumptions.

| Symbol | Meaning | Units |
|:--|:--|:--|
| $n$ | Number of fictional paired participants | pairs |
| $T_{{i,0}}, T_{{i,1}}$ | Writing duration without / with AI | minutes |
| $D_i$ | Paired time saving | minutes |
| $Q_{{i,0}}, Q_{{i,1}}$ | Independent-rater mean quality scores | points (0–100) |
| $S$ | Ratio of control to intervention mean time | dimensionless |
| $R_T$ | Relative mean time reduction | % |
| $p_{{50}}, p_{{95}}, p_{{99}}$ | Empirical median and tail quantiles | minutes or ms, separately |
| $L_j$ | Successful execution duration in SS7/SS8 technical benchmark | ms |
| $B$ | Number of bootstrap replicates | samples |

Reusable LaTeX source with equation labels is available in [`ss9_equations.tex`](ss9_equations.tex). Publication tables with `booktabs` appear in [`ss9_tables.tex`](ss9_tables.tex).

## 4.3 Synthetic writing-task comparison (minutes)

**Table 1 — Demonstration comparison of the two human-task conditions.** Values are **Mean ± sample SD**, calculated across {v['n']} fictional participant records per condition; these are **not empirical findings**.

| Metric | Without AI (synthetic) | With AI (synthetic) |
|:--|--:|--:|
| Completion time (min), mean ± SD | {fmt(c, 'mean')} ± {fmt(c, 'std')} | {fmt(a, 'mean')} ± {fmt(a, 'std')} |
| Completion time (min), median | {fmt(c, 'median')} | {fmt(a, 'median')} |
| Quality (0–100), mean ± SD | {fmt(c, 'quality_mean')} ± {fmt(c, 'quality_std')} | {fmt(a, 'quality_mean')} ± {fmt(a, 'quality_std')} |
| Correct anchor facts (%) | {fmt(c, 'factual_accuracy_mean')} | {fmt(a, 'factual_accuracy_mean')} |

In these synthetic pairs, mean paired time saving was **{v['saved']:.3f} min** (with-AI minus without-AI difference: **{-v['saved']:.3f} min**). The demonstration speedup ratio was $S={v['speedup']:.2f}$× and the mean relative time reduction was **{v['reduction']:.2f}%**. The *paired* 95% percentile-bootstrap interval for time saved was **[{fmt(c, 'paired_ci_lower_minutes')}, {fmt(c, 'paired_ci_upper_minutes')}] min** (10,000 draws, seed 42). Because this interval includes zero and all records are fictional, **no empirical productivity benefit can be inferred**.

The difference in mean quality was **{f(c,'quality_difference_points'):+.3f} points** (AI minus no AI). The mean difference exceeds the provisional −5-point quality tolerance, but a descriptive comparison **does not establish non-inferiority**; a formal interval-based guardrail assessment requires real observations and a justified margin. Factual accuracy and unsupported-claim measurements are likewise illustrative only.

![Figure 1: Mean writing-task completion time by condition](figures/fig1_latency_vs_load.png)

**Figure 1. Synthetic writing-task completion time by condition.** The horizontal axis identifies without-AI and with-AI writing conditions; the vertical axis is mean human-task duration (**minutes**). Point estimates are condition means, and error bars denote condition-level 95% percentile-bootstrap intervals, **not** the paired-difference interval reported above. Only {v['n']} fictional participants are represented. The legacy filename `fig1_latency_vs_load` does not describe its contents; no workload-rate/HTTP latency data are plotted.

![Figure 2: Synthetic writing-task time distribution](figures/fig2_distribution_boxplot.png)

**Figure 2. Synthetic completion-time distributions.** Box plots compare the two writing conditions; black points show observed synthetic times and black diamonds indicate condition means with 95% bootstrap confidence intervals. The vertical axis is completion time in **minutes**. These distributions are descriptive only and do not establish a causal effect.

## 4.4 Technical software-benchmark measurements (milliseconds)

**Table 2 — SS7/SS8 synthetic software-processing summary.** The "overall" group contains {int(t['benchmark_runs'])} software runs, not employees; {int(t['failed_runs'])} runs failed. The {int(t['iqr_outlier_flags'])} IQR-flagged points were *retained* rather than removed.

| Measure (software runtime only) | Published SS7/SS8 sample |
|:--|--:|
| Mean ± sample SD (ms) | {fmt(t, 'mean_ms')} ± {fmt(t, 'sd_ms')} |
| Median (p25–p75), ms | {fmt(t, 'median_ms')} ({fmt(t, 'p25_ms')}–{fmt(t, 'p75_ms')}) |
| p95, ms | {fmt(t, 'p95_ms')} |
| p99, ms | {fmt(t, 'p99_ms')} |
| 95% bootstrap CI for mean (ms) | [{fmt(t, 'bootstrap_mean_ci95_lower_ms')}, {fmt(t, 'bootstrap_mean_ci95_upper_ms')}] |
| Failure rate (%) | {fmt(t, 'failure_rate_percent')} |
| IQR outlier flags (retained) | {int(t['iqr_outlier_flags'])} |

Five warm-up runs were excluded *from software timing summaries* before calculating these statistics. The `overall` group contains {int(t['successful_runs'])} successful measured runs. A failure, if one occurs in future data, must still be included in the failure-rate denominator; p95/p99 are computed among successes and accompanied by the failure rate to avoid selection bias. Per-workload grouping uses input CSV row counts of **8, 16, and 32**, rather than requests per second (RPS). Timing estimates are subject to CPU/OS noise and within-machine dependence, so the numerical confidence interval is diagnostic, not a generalizable inferential claim.

![Figure 3: Technical runtime percentiles by workload](figures/ss8_software_percentiles.png)

**Figure 3. Successful Python analysis runtime against synthetic workload size.** The horizontal axis is number of synthetic input CSV rows, and the vertical axis is Python-pipeline execution duration in **milliseconds**. p50, p95, and p99 describe successful software runs; black diamond-and-cap markers show mean runtimes with 95% percentile-bootstrap intervals. No user typing speed, model API latency, or request rate is present.

![Figure 4: Technical runtime distributions and outliers](figures/ss8_software_distribution.png)

**Figure 4. Technical runtime distributions by synthetic workload size.** The vertical axis is execution duration in **milliseconds**. Boxplots describe successful-run dispersion; orange diamonds flag IQR outliers *without excluding them*. Black squares and capped intervals show means and 95% percentile-bootstrap intervals. Failure counts are separately reported in Table 2.

## 4.5 Discussion, assumptions and limitations

1. **Human study not conducted.** The fictional paired records demonstrate analysis logic only. No participants were recruited, and no substantive GenAI productivity claim is supported.
2. **Small synthetic human sample.** The {v['n']} illustrative pairs do not validate normality, task equivalence, learning/carryover effects, quality-rating reliability, or a definitive quality non-inferiority margin.
3. **Different measurement systems.** Human task duration (minutes) and software execution time (milliseconds) measure different constructs; pooling them would invalidate the study.
4. **Technical noise and dependence.** Repeated timings of the same program on one development machine may be autocorrelated. The software bootstrap interval is a reproducibility demonstration, not a confidence interval about employee effects.
5. **Outliers and failures.** IQR flags were retained; a zero observed software failure rate over 100 runs does not prove a zero failure probability under other loads.
6. **No comparative system throughput.** The Python benchmark contains no HTTP requests or request-rate data. Figure captions deliberately avoid asserting the course handout's generic RPS/latency examples were measured.

## 4.6 Reproducibility and artefacts

The repository contains source data, processing code, the exact scripts for SS7/SS8, executed Jupyter notebooks, seeded bootstrap demonstrations, unit tests, and four scientific plots in both PNG (300 dpi) and vector PDF form. Technical log artifacts are public only when explicitly labeled synthetic. The raw local `data/raw/` folder remains Git-ignored to protect future real data. Execute `python src/generate_ss9_report.py` to regenerate this report and its LaTeX tables from the committed aggregated source CSV files. Execute `python src/generate_ss9_report.py --check` to verify they remain consistent.

**Interpretation:** The research methodology and reproducible analysis are ready for further evaluation; **no real-world effect of Generative AI has yet been measured by this team.**
'''


def latex_tables(v):
    c, a, t = v['control'], v['treatment'], v['overall']
    f = lambda row, key: float(row[key])
    return r'''% SS9 tables derived from the committed SYNTHETIC aggregates. Requires \usepackage{booktabs}.
% No claims about measured employees or actual AI performance are supported.
\begin{table}[htbp]
\centering
\caption{Synthetic professional-writing comparison: fictional paired observations (mean $\pm$ SD).}
\label{tab:ss9:human}
\begin{tabular}{lrr}
\toprule
Metric & Without AI & With AI \\
\midrule
''' + (
        f"Completion time (min) & {fmt(c, 'mean')} $\\pm$ {fmt(c, 'std')} & {fmt(a, 'mean')} $\\pm$ {fmt(a, 'std')} " + r"\\" + "\n" +
        f"Quality (0--100) & {fmt(c, 'quality_mean')} $\\pm$ {fmt(c, 'quality_std')} & {fmt(a, 'quality_mean')} $\\pm$ {fmt(a, 'quality_std')} " + r"\\" + "\n" +
        f"Anchor-fact recall (\\%) & {fmt(c, 'factual_accuracy_mean')} & {fmt(a, 'factual_accuracy_mean')} " + r"\\" + "\n"
    ) + r'''\bottomrule
\end{tabular}
\end{table}

\begin{table}[htbp]
\centering
\caption{Synthetic SS7/SS8 software-runtime summary; 100 measured runs; timings in ms.}
\label{tab:ss9:software}
\begin{tabular}{lr}
\toprule
Statistic & Value \\
\midrule
''' + (
        f"Mean $\\pm$ SD (ms) & {fmt(t, 'mean_ms')} $\\pm$ {fmt(t, 'sd_ms')} " + r"\\" + "\n" +
        f"Median (p25--p75, ms) & {fmt(t, 'median_ms')} ({fmt(t, 'p25_ms')}--{fmt(t, 'p75_ms')}) " + r"\\" + "\n" +
        f"p95 (ms) & {fmt(t, 'p95_ms')} " + r"\\" + "\n" +
        f"p99 (ms) & {fmt(t, 'p99_ms')} " + r"\\" + "\n" +
        f"Error rate (\\%) & {fmt(t, 'failure_rate_percent')} " + r"\\" + "\n"
    ) + r'''\bottomrule
\end{tabular}
\end{table}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail when saved SS9 artifacts differ from the deterministic source CSVs.')
    args = parser.parse_args()
    values = stats()
    rendered = [(REPORT, markdown_report(values)), (TABLES, latex_tables(values))]
    if args.check:
        changed = [str(path) for path, content in rendered if not path.exists() or path.read_text(encoding='utf-8') != content]
        if changed:
            print('SS9 OUT OF DATE:', ', '.join(changed), file=sys.stderr)
            return 1
        print('SS9 report and tables match the committed synthetic source summaries.')
    else:
        for path, content in rendered:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            print('Created:', path.relative_to(ROOT))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
