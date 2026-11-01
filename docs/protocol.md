# Experimental protocol (proposal; not yet conducted)

## Aim and population
Investigate how optional Generative AI assistance changes completion time and
output quality on professional writing and information-processing tasks.
Target population: knowledge workers with relevant professional writing experience.
No participants have been recruited or measured at the time this protocol was written.

## Design
A randomized, counterbalanced two-condition crossover design. Each participant
completes one task with AI and one without AI, using different but matched task
sets A and B. Balance **both** condition order and task-set assignment across
participants, ideally across four sequences:

| Sequence | First task | Second task |
|---|---|---|
| S1 | A without AI | B with AI |
| S2 | A with AI | B without AI |
| S3 | B without AI | A with AI |
| S4 | B with AI | A without AI |

Use `python src/randomize.py --count 8` to demonstrate balanced random
assignments using a prespecified seed (a multiple of four participants is
required for exact balance). Retain the assignment log for the actual study. Recruit and consent participants before conducting sessions.
The recruitment size must be specified before data collection, informed by
feasibility and a statistical power assessment when possible.

## Tasks and permitted tools
Use two realistic, matched professional information-synthesis/report-writing
assignments with similar numbers of facts, formatting requirements and expected
lengths. Pilot-test equivalence of difficulty. In both conditions participants
have identical reference materials and a text editor. External web browsing
and other AI tools are forbidden in both conditions except for the study's
specified AI interface in the intervention condition. Use a specified model,
record the available model/version/date, and capture permitted prompting details
without collecting personal data. The participants must verify AI claims.

## Timing and outcome handling
Start time when the participant sees the prompt; end time at final submission.
Include prompts, corrections and final editing in AI-assisted time. Maximum
30 minutes per task (provisional). Mark unfinished tasks `completed=0`, store
time spent up to cutoff, and leave quality/factual fields blank in that case.
**Do not interpret capped times as successful completion.** Complete-pair
analysis excludes pairs with an unfinished task; report how many were excluded
and include a sensitivity analysis in a future full research study.

## Assessment
Two blinded reviewers independently score each completed output using the
100-point rubric in `evaluation_rubric.md`. The quality score is the mean of
the two reviewer totals. Reviewers also check a predefined factual key; record
`factual_correct` and `factual_total` for every completed response.

## Outcomes and analysis
- Primary: mean within-participant difference in task time, with AI minus without AI.
- Secondary: differences in quality and factual accuracy.
- Guardrail: provisional five-point lower quality margin. Statistical support
  requires the lower bound of the 95% confidence interval for the quality
  difference to exceed -5 points; the margin needs substantive justification
  before recruiting participants.
- Exploratory: experience-related heterogeneity, interpreted cautiously.

A paired t-based estimate and 95% CI are calculated for complete pairs.
Before analyzing real data, inspect paired differences, outliers, assumptions,
order/task effects, missingness, and whether a repeated-measures model is more
appropriate. If assumptions fail, specify a robust alternative. The tiny sample
data in this repository are synthetic and cannot validate causal hypotheses.

## Ethics and transparency
Obtain informed consent, do not upload confidential business documents, and
avoid names/emails in task files. Publish anonymized outputs only when consent
and institutional requirements permit. Synthetic sample data are clearly marked.
