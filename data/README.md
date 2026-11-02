# Data policy

- `sample/example_measurements.csv` contains entirely **synthetic** records;
  values are fictional and are not research findings.
- `raw/` and `private/` are reserved for participant records and ignored by Git.
- `outputs/` holds generated analyses and is ignored by Git.
- Never commit names, real participant data, access tokens, confidential
  materials, or prompts containing personal information.

## CSV data schema

The original fields are unchanged:

- `participant_id`: pseudonym; `task_set`: `A`/`B`; `task_order`: `1`/`2`;
  `condition`: `with_ai`/`without_ai`; `completed`: `1`/`0`.
- `completion_time_minutes`: elapsed minutes (including AI interaction time).
- `quality_rater_1`, `quality_rater_2`: independent reviewer totals (0–100).
- `factual_correct`: correctly covered required anchor facts.
- `factual_total`: total required anchor facts (five in the proposed tasks).
- `experience_years`: relevant professional experience.
- `data_origin`: `synthetic` or `real` (must be consistent within a file).

Two additional **optional** integer fields implement the exploratory claim
metrics defined in `docs/evaluation_rubric.md`:

- `supported_claims`: number of distinct factual claims supported by provided sources.
- `unsupported_claims`: number of distinct factual claims that are unsupported,
  incorrect, or contradictory.

If one claim-count column is present, both must be present. On a completed
response, the pair of values is either both nonnegative integers or both blank
when the claim annotation has not been performed. `supported_claims` must be at
least `factual_correct`. For incomplete responses, quality and all factual/claim
counts must be blank.

**Exploratory measures (percent):**

- Precision = `100 * supported_claims / (supported_claims + unsupported_claims)`.
- Recall = `100 * factual_correct / factual_total`.
- F1 = harmonic mean of Precision and Recall (either both in proportions or
  both in percent).

Zero assessable factual claims make Precision and F1 **undefined** (`null`/N/A),
not 0. Likewise, absent claim annotations yield undefined Precision and F1,
while Recall is still computed. Do not silently replace undefined values with
zero. Paired Precision/F1 estimates use only complete participant pairs with
both condition values defined; their own `n_pairs` must be reported.

The previous name `factual_accuracy_percent` is retained for compatibility and
is equivalent to anchor-fact Recall. Unsupported extra claims affect Precision
but not this legacy metric.

Completed tasks require independent reviewer scores and anchor-fact counts.
Participant pairs with unfinished tasks are excluded from the current paired
analysis, with the number excluded reported separately. Missing optional claim
annotations do **not** invalidate a participant's primary time outcome.

Before real data collection, the reviewers must agree on claim segmentation,
unique fact counting, ground-truth sources, and the adjudication process. These
metrics do not themselves prove that AI increases employee productivity.
