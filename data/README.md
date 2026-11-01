# Data policy

- `sample/example_measurements.csv`: entirely **synthetic** demonstration records,
  not real participants and not experimental findings.
- `raw/` and `private/`: reserved for actual participant records and ignored by Git.
- `outputs/`: generated statistical results, also ignored by Git.
- Never commit names, private employee documents, prompts containing personal
  information, access tokens or confidential workplace data.

## CSV fields

`participant_id` is a pseudonym; `task_set` is A/B; `task_order` is 1/2;
`condition` is `with_ai` or `without_ai`; `completed` is 1/0;
`completion_time_minutes` is elapsed minutes; `quality_rater_1` and
`quality_rater_2` are independent 0–100 scores; `factual_correct` and
`factual_total` are rubric answer-key counts; `experience_years` is relevant
experience; `data_origin` is `synthetic` or `real`.

Completed tasks require two quality scores and factual counts. Incomplete tasks
must have blank quality and factual fields; incomplete participant pairs are
excluded from the current complete-pair estimate and reported as excluded.
