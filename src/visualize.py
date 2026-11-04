
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample" / "example_measurements.csv"
FIGURE_DIR = ROOT / "reports" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

conditions = ["without_ai", "with_ai"]
labels = ["Without AI", "With AI"]

rng = np.random.default_rng(42)

means = []
ci_lower = []
ci_upper = []

for condition in conditions:
    values = df.loc[
        df["condition"] == condition,
        "completion_time_minutes"
    ].dropna().to_numpy()

    boot_means = np.array([
        rng.choice(values, size=len(values), replace=True).mean()
        for _ in range(10000)
    ])

    mean = values.mean()
    lower, upper = np.percentile(boot_means, [2.5, 97.5])

    means.append(mean)
    ci_lower.append(mean - lower)
    ci_upper.append(upper - mean)

fig, ax = plt.subplots(figsize=(7, 5))

ax.errorbar(
    labels,
    means,
    yerr=[ci_lower, ci_upper],
    fmt="o",
    markersize=9,
    capsize=6,
    linewidth=2,
    color="#0072B2"
)

ax.set_ylabel("Mean completion time (minutes)")
ax.set_xlabel("Experimental condition")
ax.set_title("Professional Writing: Completion Time by Condition")

ax.grid(axis="y", linestyle="--", alpha=0.3)

fig.text(
    0.5, 0.01,
    "Synthetic demonstration data (n=4 paired participants)",
    ha="center",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.05, 1, 1])

fig.savefig(
    FIGURE_DIR / "fig1_latency_vs_load.png",
    dpi=300,
    bbox_inches="tight"
)
fig.savefig(
    FIGURE_DIR / "fig1_latency_vs_load.pdf",
    bbox_inches="tight"
)

plt.close(fig)

print("Figure 1 saved successfully.")




import seaborn as sns

fig, ax = plt.subplots(figsize=(8, 5))

palette = {
    "without_ai": "#D55E00",
    "with_ai": "#0072B2"
}

sns.boxplot(
    data=df,
    x="condition",
    y="completion_time_minutes",
    order=conditions,
    hue="condition",
    palette=palette,
    dodge=False,
    width=0.45,
    legend=False,
    ax=ax
)

sns.stripplot(
    data=df,
    x="condition",
    y="completion_time_minutes",
    order=conditions,
    color="black",
    size=6,
    jitter=0.08,
    ax=ax
)

for i, condition in enumerate(conditions):
    values = df.loc[
        df["condition"] == condition,
        "completion_time_minutes"
    ].to_numpy()

    rng_local = np.random.default_rng(42 + i)

    bootstrap_means = np.array([
        rng_local.choice(values, size=len(values), replace=True).mean()
        for _ in range(10000)
    ])

    lower, upper = np.percentile(bootstrap_means, [2.5, 97.5])
    mean = values.mean()

    ax.errorbar(
        i,
        mean,
        yerr=[[mean - lower], [upper - mean]],
        fmt="D",
        color="black",
        markersize=6,
        capsize=6,
        linewidth=2,
        zorder=10
    )

ax.set_xticks(range(len(conditions)))
ax.set_xticklabels(labels)

ax.set_xlabel("Experimental condition")
ax.set_ylabel("Completion time (minutes)")
ax.set_title("Completion Time Distribution: With AI vs Without AI")

ax.grid(axis="y", linestyle="--", alpha=0.3)

fig.text(
    0.5, 0.01,
    "Diamonds = means; error bars = bootstrap 95% CI. Synthetic data (n=4 pairs).",
    ha="center",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.05, 1, 1])

fig.savefig(
    FIGURE_DIR / "fig2_distribution_boxplot.png",
    dpi=300,
    bbox_inches="tight"
)

fig.savefig(
    FIGURE_DIR / "fig2_distribution_boxplot.pdf",
    bbox_inches="tight"
)

plt.close(fig)

print("Figure 2 saved successfully.")
