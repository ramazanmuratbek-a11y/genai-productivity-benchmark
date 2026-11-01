# Evaluation rubric (proposed; not yet validated)

Two reviewers independently assign each criterion and record a total from 0 to
100. Reviewers should not know the AI condition when feasible.

| Criterion | Maximum score | Definition |
|---|---:|---|
| Accuracy and completeness | 30 | Required facts correct; important information included |
| Clarity and organization | 25 | Coherent flow, comprehensible structure and headings |
| Relevance to task | 25 | Responds to the stated recipient, purpose and constraints |
| Language and professionalism | 20 | Appropriate grammar, tone and professional formatting |
| **Total** | **100** | Sum of all four criteria |

Use a common scoring guide established **before** the study. Independently
record `quality_rater_1` and `quality_rater_2` as their 0–100 totals; the
analysis takes the arithmetic mean. Discuss large reviewer disagreements and
report inter-rater reliability in the real study.

For factual accuracy, define 5 independently assessable required facts per
matched task. `factual_correct` must be between 0 and `factual_total` (5 in
the current proposal). Accuracy = 100 × correct / total. Do not invent factual
scores for open-ended tasks without an assessable factual answer key.

**Quality guardrail:** provisional tolerance is 5/100 points for the mean
AI-minus-no-AI difference. This is not an empirically validated threshold.
