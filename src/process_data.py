
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample" / "example_measurements.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

print("\nConditions:")
print(df["condition"].value_counts())

print("\nData origin:")
print(df["data_origin"].value_counts())


summary = (
    df.groupby("condition")["completion_time_minutes"]
    .agg(
        count="count",
        mean="mean",
        median="median",
        std="std",
        min="min",
        max="max",
    )
    .reset_index()
)

percentiles = (
    df.groupby("condition")["completion_time_minutes"]
    .quantile([0.95, 0.99])
    .unstack()
    .reset_index()
)

percentiles.columns = ["condition", "p95", "p99"]

summary = summary.merge(percentiles, on="condition")

print("\nStatistical summary:")
print(summary.round(2).to_string(index=False))



paired = df.pivot(
    index="participant_id",
    columns="condition",
    values="completion_time_minutes"
).dropna()

paired["time_saved"] = (
    paired["without_ai"] - paired["with_ai"]
)

print("\nPaired differences:")
print(paired.round(2))

import numpy as np

rng = np.random.default_rng(42)

differences = paired["time_saved"].to_numpy()

n_bootstrap = 10000

bootstrap_means = np.array([
    rng.choice(
        differences,
        size=len(differences),
        replace=True
    ).mean()
    for _ in range(n_bootstrap)
])

ci_lower, ci_upper = np.percentile(
    bootstrap_means, [2.5, 97.5]
)

mean_difference = differences.mean()

print("\nPaired bootstrap results:")
print(f"Mean time saved: {mean_difference:.2f} minutes")
print(f"95% CI: [{ci_lower:.2f}, {ci_upper:.2f}] minutes")




df["quality_score"] = (
    df["quality_rater_1"] + df["quality_rater_2"]
) / 2

df["factual_accuracy_percent"] = (
    df["factual_correct"] / df["factual_total"]
) * 100

df["unsupported_claim_rate_percent"] = (
    df["unsupported_claims"] /
    (df["supported_claims"] + df["unsupported_claims"])
) * 100

secondary_summary = (
    df.groupby("condition")[
        [
            "quality_score",
            "factual_accuracy_percent",
            "unsupported_claim_rate_percent"
        ]
    ]
    .agg(["mean", "std"])
    .round(2)
)

print("\nSecondary metrics summary:")
print(secondary_summary)




quality_with_ai = df.loc[
    df["condition"] == "with_ai", "quality_score"
].mean()

quality_without_ai = df.loc[
    df["condition"] == "without_ai", "quality_score"
].mean()

quality_difference = quality_with_ai - quality_without_ai

quality_tolerance = 5

guardrail_passed = quality_difference >= -quality_tolerance

print("\nQuality guardrail:")
print(f"Quality difference: {quality_difference:.2f} points")
print(f"Tolerance: {quality_tolerance} points")
print(f"Guardrail passed: {guardrail_passed}")

from pathlib import Path

output_path = ROOT / "data" / "processed" / "metrics_summary.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)


secondary_flat = (
    df.groupby("condition")
    .agg(
        quality_mean=("quality_score", "mean"),
        quality_std=("quality_score", "std"),
        factual_accuracy_mean=("factual_accuracy_percent", "mean"),
        factual_accuracy_std=("factual_accuracy_percent", "std"),
        unsupported_claim_rate_mean=("unsupported_claim_rate_percent", "mean"),
        unsupported_claim_rate_std=("unsupported_claim_rate_percent", "std"),
    )
    .reset_index()
)

final_summary = summary.merge(
    secondary_flat,
    on="condition",
    how="left"
)


final_summary["paired_mean_time_saved_minutes"] = mean_difference
final_summary["paired_ci_lower_minutes"] = ci_lower
final_summary["paired_ci_upper_minutes"] = ci_upper
final_summary["quality_difference_points"] = quality_difference
final_summary["quality_guardrail_passed"] = guardrail_passed
final_summary["data_origin"] = "synthetic"

final_summary.to_csv(output_path, index=False)

print(f"\nSaved summary to: {output_path}")
