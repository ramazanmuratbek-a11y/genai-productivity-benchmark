# Supplementary factual claim metric implementation

## Scope

This code update implements the exploratory claim Precision, anchor-fact Recall,
and F1-score proposed in `docs/evaluation_rubric.md`. The primary study metric
remains **human task completion time (minutes)**. The existing 100-point quality
score and provisional quality guardrail are unchanged.

## Backward compatibility

Older CSVs without `supported_claims` / `unsupported_claims` still validate.
Precision and F1 appear as `null` in `summary.json`, with zero evaluable paired
participants. `factual_accuracy_percent` is preserved as an alias for the
required-anchor-fact Recall metric. The new sample is wholly **synthetic**.

## How to verify

From the repository root, using PowerShell:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe src\validate_data.py data\sample\example_measurements.csv
.\.venv\Scripts\python.exe src\analyze.py --input data\sample\example_measurements.csv --output-dir outputs\demo
```

Inspect `outputs/demo/summary.json` and `outputs/demo/participant_effects.csv`.

Then, with Docker Desktop running:

```powershell
docker build -t genai-writing-study .
docker run --rm genai-writing-study
```

Do not state that synthetic statistics are empirical findings. The annotation
rules and scoring system still require pilot testing before any real study.
