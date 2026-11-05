"""SS8 scientific figures for synthetic SS7 *software milliseconds*, not human minutes."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def make_figures(summary: pd.DataFrame, detail: pd.DataFrame, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.size': 10, 'axes.titlesize': 12, 'axes.labelsize': 11,
                         'savefig.dpi': 300})
    saved = []
    groups = summary.loc[summary.group != 'overall'].copy()
    if groups.empty:
        raise ValueError('At least one synthetic workload group is required.')
    groups['rows'] = groups.group.str.extract(r'\((\d+) rows\)').astype(float)
    groups = groups.sort_values('rows')

    # Plot 1 — percentile curves + mean bootstrap CI; workload in input rows, not RPS.
    fig, ax = plt.subplots(figsize=(8.5, 5.6))
    colors = ['#0072B2', '#D55E00', '#009E73']  # Okabe–Ito colorblind-safe
    for key, label, color, marker, ls in [
        ('median_ms','p50 (median)', colors[0], 'o', '-'),
        ('p95_ms','p95', colors[1], 's', '--'),
        ('p99_ms','p99', colors[2], '^', ':')]:
        ok = groups.dropna(subset=[key])
        ax.plot(ok['rows'], ok[key], label=label, color=color, marker=marker,
                linestyle=ls, linewidth=1.8, markersize=6)
    with_ci = groups.dropna(subset=['bootstrap_mean_ci95_lower_ms', 'bootstrap_mean_ci95_upper_ms', 'mean_ms'])
    if not with_ci.empty:
        low = (with_ci.mean_ms - with_ci.bootstrap_mean_ci95_lower_ms).to_numpy()
        high = (with_ci.bootstrap_mean_ci95_upper_ms - with_ci.mean_ms).to_numpy()
        ax.errorbar(with_ci.rows.to_numpy(), with_ci.mean_ms.to_numpy(),
                    yerr=[np.maximum(low,0), np.maximum(high,0)], label='Mean ± 95% bootstrap CI',
                    fmt='D', color='#333333', elinewidth=1.4, capsize=4)
    ax.set_xlabel('Synthetic workload size (input CSV rows)')
    ax.set_ylabel('Python analysis execution time (ms)')
    ax.set_title('SS8: Synthetic software runtime by workload size')
    ax.set_ylim(bottom=0)
    ax.grid(axis='y', linestyle='--', alpha=.28)
    ax.legend(loc='best', fontsize=9)
    fig.text(.5,.01, 'SS7 software timing; IQR flags retained. Not employee task time.',
             ha='center', fontsize=9)
    fig.tight_layout(rect=[0,.05,1,1])
    for ext in ('png','pdf'):
        p=out_dir/f'ss8_software_percentiles.{ext}'
        fig.savefig(p, dpi=300, bbox_inches='tight')
        saved.append(p)
    plt.close(fig)

    # Plot 2 — distribution, outliers retained with separate diamond markers.
    ok = detail[(detail.status == 'ok') & (detail.phase == 'benchmark')].copy()
    if ok.empty:
        raise ValueError('No successful benchmark software durations available to plot.')
    profile_groups = list(ok.groupby('input_rows', sort=True))
    data = [g.duration_ms.astype(float).to_numpy() for _,g in profile_groups]
    labels = [f'{rows} rows' for rows,_ in profile_groups]
    fig,ax=plt.subplots(figsize=(8.5,5.6))
    ax.boxplot(data, tick_labels=labels, showfliers=False, patch_artist=True,
               boxprops={'facecolor':'#BDD7E7','edgecolor':'#3E5267'},
               whiskerprops={'color':'#3E5267'}, capprops={'color':'#3E5267'},
               medianprops={'color':'#D55E00','linewidth':2})
    rng=np.random.default_rng(42)
    for i,(rows,g) in enumerate(profile_groups,1):
        normal=g[~g['iqr_outlier']]
        flagged=g[g['iqr_outlier']]
        if len(normal):
            x=rng.normal(i, .045, len(normal))
            ax.scatter(x, normal.duration_ms, s=11, alpha=.45, color='#0072B2',
                       label='Non-flagged successful run' if i==1 else None)
        if len(flagged):
            ax.scatter([i]*len(flagged), flagged.duration_ms, s=35, alpha=.9,
                       color='#D55E00', marker='D', label='IQR-flagged (retained)' if i==1 else None)
        sm=summary.loc[summary.group.str.endswith(f'({rows} rows)')]
        if len(sm) and np.isfinite(sm.iloc[0].get('bootstrap_mean_ci95_lower_ms',float('nan'))):
            rec=sm.iloc[0]
            ax.errorbar(i,rec['mean_ms'],yerr=[[max(0,rec['mean_ms']-rec['bootstrap_mean_ci95_lower_ms'])],
                           [max(0,rec['bootstrap_mean_ci95_upper_ms']-rec['mean_ms'])]],
                        fmt='s',color='#222222',capsize=5,markersize=5,
                        label='Mean ± 95% CI' if i==1 else None,zorder=5)
    ax.set_xlabel('Synthetic workload size')
    ax.set_ylabel('Python analysis execution time (ms)')
    ax.set_title('SS8: Software timing distributions and IQR flags')
    ax.set_ylim(bottom=0)
    ax.grid(axis='y',linestyle='--',alpha=.25)
    handles,legends=ax.get_legend_handles_labels()
    if handles: ax.legend(fontsize=8,loc='best')
    fig.text(.5,.01,'All successful benchmark runs retained; errors counted separately in summary.',
             ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.05,1,1])
    for ext in ('png','pdf'):
        p=out_dir/f'ss8_software_distribution.{ext}'
        fig.savefig(p,dpi=300,bbox_inches='tight')
        saved.append(p)
    plt.close(fig)
    return saved


def main():
    p=argparse.ArgumentParser(description='Render scientific plots for SS7 synthetic software benchmark.')
    p.add_argument('--summary',type=Path,default=Path('data/processed/ss8_software_metrics_summary.csv'))
    p.add_argument('--detail',type=Path,default=Path('outputs/ss8/clean_software_measurements.csv'))
    p.add_argument('--output-dir',type=Path,default=Path('reports/figures'))
    args=p.parse_args()
    figfiles=make_figures(pd.read_csv(args.summary),pd.read_csv(args.detail),args.output_dir)
    for file in figfiles:print('Saved:',file)


if __name__=='__main__':
    main()
