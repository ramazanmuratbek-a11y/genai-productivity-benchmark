# Evaluation Rubric for Knowledge-Based Office Tasks

**Research project:** The Impact of Generative AI Tools on Employee Productivity and Work Quality in Knowledge-Based Office Tasks

**Institution:** Narxoz University

**Research team:** Muratbek Ramazan and Tasbolatkyzy Zhanerke

**Document status:** Proposed evaluation methodology; not yet validated or applied to real participants.

## 1. Purpose

This evaluation rubric is designed to assess the quality of professional writing tasks completed under two experimental conditions:

- **Without AI:** Participants complete the task using standard writing tools without Generative AI assistance.
- **With AI:** Participants complete a comparable task with access to the specified Generative AI tool.

The purpose is to evaluate differences in output quality while preserving a fair and consistent comparison between experimental conditions.

The study's primary outcome remains human task completion time (minutes). Output quality and factual correctness are secondary outcomes. Precision, Recall, and F1-score are proposed as exploratory supplementary measures.

## 2. Overall Quality Scoring Framework

Each completed response is evaluated using four criteria. The maximum total score is 100 points.

| Criterion | Maximum Score | Description |
|---|---:|---|
| Accuracy and completeness | 30 | Correct representation of source facts and inclusion of essential information |
| Clarity and organization | 25 | Logical structure, readability, and coherent presentation |
| Relevance to task | 25 | Fulfillment of the requested purpose, audience, and task constraints |
| Language and professionalism | 20 | Grammar, appropriate terminology, tone, and professional formatting |
| **Total** | **100** | Sum of all four criteria |

Two independent reviewers assign scores using the same rubric. The reported quality score is the arithmetic mean of their total scores.

## 3. Detailed Scoring Guidelines

### 3.1 Accuracy and Completeness — 30 Points

| Score Range | Evaluation |
|---|---|
| 26–30 | All or nearly all required information is accurate and included; no material factual errors |
| 19–25 | Most information is accurate, with minor omissions or inaccuracies |
| 10–18 | Several important facts are omitted or incorrectly represented |
| 0–9 | Major factual inaccuracies, missing information, or unsupported conclusions |

Reviewers should evaluate the response against the supplied task materials rather than assumptions or external information.

### 3.2 Clarity and Organization — 25 Points

| Score Range | Evaluation |
|---|---|
| 22–25 | Clear, coherent structure; ideas flow logically and are easy to understand |
| 16–21 | Generally understandable, with minor organizational weaknesses |
| 8–15 | Inconsistent structure or unclear transitions affect readability |
| 0–7 | Disorganized response with serious readability problems |

### 3.3 Relevance to Task — 25 Points

| Score Range | Evaluation |
|---|---|
| 22–25 | Fully addresses the task purpose, intended audience, and required deliverables |
| 16–21 | Addresses most requirements, with minor omissions |
| 8–15 | Partially meets the assignment but overlooks important requirements |
| 0–7 | Fails to address the central task or essential instructions |

Reviewers should consider the required internal business update format, summary, recommendations, and word-count constraints described in `task_sets.md`.

### 3.4 Language and Professionalism — 20 Points

| Score Range | Evaluation |
|---|---|
| 18–20 | Clear professional language, appropriate tone, and minimal language errors |
| 13–17 | Generally professional, with minor grammar or style issues |
| 7–12 | Repeated language problems or inconsistent professional tone |
| 0–6 | Serious language problems that interfere with communication |

## 4. Additional Factual Evaluation Metrics

To distinguish factual correctness from coverage of required information, the following exploratory metrics are proposed:

- Precision
- Recall
- F1-score

These metrics are evaluated separately from the 100-point quality rubric. They must not be treated as additional primary outcomes.

### 4.1 Operational Definitions

Each matched task contains five predefined required source facts, referred to as **anchor facts**.

**Supported factual claim:** A distinct factual statement in the response that is correctly supported by the provided source materials.

**Unsupported or incorrect factual claim:** A distinct factual statement that contradicts the supplied facts, invents information, or cannot be verified from the permitted source materials.

**Correctly covered anchor fact:** A required anchor fact that is accurately represented in the response.

**Missed anchor fact:** A required anchor fact that is omitted or represented incorrectly.

Nonfactual opinions and recommendations should not be classified as factual claims unless they assert independently verifiable information.

Duplicate statements should be counted only once. Compound statements should be divided into individually assessable factual claims.

### 4.2 Precision

Precision measures the proportion of assessable factual claims in the response that are supported by the source materials.

**Precision = Supported Claims / (Supported Claims + Unsupported or Incorrect Claims)**

A higher Precision score indicates fewer unsupported or incorrect factual statements.

### 4.3 Recall

Recall measures the proportion of required anchor facts that the participant correctly includes.

**Recall = Correctly Covered Anchor Facts / Total Required Anchor Facts**

For the current proposed tasks, the denominator is five.

The existing dataset fields `factual_correct` and `factual_total` represent this anchor-fact coverage measure.

### 4.4 F1-score

The F1-score combines Precision and Recall using their harmonic mean.

**F1 = 2 × (Precision × Recall) / (Precision + Recall)**

This measure summarizes the balance between factual correctness and coverage of required information.

These definitions are an operational adaptation for professional writing evaluation, rather than a conventional binary classification confusion matrix.

### 4.5 Illustrative Example

Assume a task contains five required anchor facts.

A participant correctly represents four anchor facts, omits one, and adds one unsupported factual claim.

The response contains four supported factual claims and one unsupported claim.

| Metric | Calculation | Result |
|---|---|---|
| Precision | 4 / (4 + 1) | 0.80 |
| Recall | 4 / 5 | 0.80 |
| F1-score | 2 × (0.80 × 0.80) / (0.80 + 0.80) | 0.80 |

**Note:** This example is fictional and is provided only to illustrate the evaluation procedure. It is not an empirical study result.

### 4.6 Special Cases and Annotation Rules

- If a response contains no assessable factual claims, Precision is reported as undefined (N/A).
- If Precision or Recall is undefined, F1-score is also reported as undefined.
- If Precision and Recall are both defined and equal to zero, F1-score is reported as zero.
- A required anchor fact stated incorrectly counts as a missed anchor fact for Recall and an incorrect claim for Precision.
- Reviewers should document disputed factual classifications.
- Claim segmentation and classification guidelines must be finalized before real data collection.

## 5. Independent Reviewer Assessment

Two reviewers independently assess each completed response.

To reduce assessment bias:

1. Reviewers use the same predefined evaluation rubric.
2. Responses should be anonymized where feasible.
3. Reviewers should not be informed whether the response was created with or without AI assistance.
4. Reviewers assign scores independently before discussing their evaluations.
5. Both original reviewer scores must be preserved.

Perfect blinding cannot be guaranteed because writing style may sometimes reveal aspects of the production process.

The following values are recorded for each completed task:

- `quality_rater_1`: Total quality score assigned by Reviewer 1.
- `quality_rater_2`: Total quality score assigned by Reviewer 2.
- `quality_score`: Arithmetic mean of the two totals.

For incomplete tasks, quality and factual evaluation fields remain blank according to the experimental data protocol.

## 6. Reviewer Disagreement and Reliability

Reviewer disagreement should be assessed before interpreting the quality results.

A provisional review trigger is an absolute difference greater than 15 points between the two total quality scores.

If the threshold is exceeded:

1. Preserve both original scores.
2. Ask reviewers to provide written justifications.
3. Review differences against the predefined scoring criteria.
4. Document any adjudication separately rather than silently overwriting the original scores.

The 15-point trigger is a proposed operational rule, not an empirically validated threshold.

When sufficient real evaluation data become available, inter-rater reliability should be reported using a suitable statistic, such as an intraclass correlation coefficient (ICC) for total scores.

## 7. Quality Guardrail

The proposed study uses a provisional five-point quality tolerance.

**Quality difference = Mean Quality With AI − Mean Quality Without AI**

The quality non-inferiority guardrail requires the lower confidence bound for the paired quality difference to exceed −5 points.

This margin must be justified and specified before collecting real experimental data.

A successful demonstration using synthetic data does not establish that this guardrail is satisfied in real-world conditions.

## 8. Reproducibility and Data Requirements

The existing research pipeline records overall quality scores and required-fact coverage.

To calculate the additional exploratory Precision and F1-score metrics, future data collection and analysis should also record:

- `supported_claims`
- `unsupported_claims`

The calculation methods, annotation rules, data schema, and automated tests must be updated together before these metrics are used for real research conclusions.

All evaluations should follow a predefined protocol, and any methodological adjustments must be documented.

## 9. Limitations

This rubric is a proposed methodological framework.

The criteria and scoring ranges have not yet undergone pilot validation.

Precision and Recall depend on the consistency of human claim annotation and the adequacy of the provided source facts.

Quality scoring may contain subjective judgments even with independent reviewers.

The research repository currently contains synthetic demonstration data only. No empirical conclusions about Generative AI and employee productivity are claimed.

## 10. Conclusion

The proposed evaluation framework combines a structured 100-point quality rubric with supplementary factual Precision, Recall, and F1-score measures.

It is intended to support fair, transparent, and reproducible assessment of professional writing tasks under AI-assisted and non-AI-assisted conditions.

Before actual experimental use, the team should pilot-test the rubric, refine reviewer instructions, and validate the additional factual metrics.
