

## 1. Research Objective

This project evaluates the effect of AI assistance on professional writing completion time, quality, and factual accuracy.

The study follows a randomized crossover design: each participant completes tasks both with and without AI assistance.

## 2. Mathematical Notation

Let:

- \(n\): number of paired participants.
- \(T_{i,0}\): completion time without AI, in minutes.
- \(T_{i,1}\): completion time with AI, in minutes.
- \(Q_{i,0}\): writing quality score without AI.
- \(Q_{i,1}\): writing quality score with AI.

The time saved for participant \(i\) is:

$$
D_i = T_{i,0} - T_{i,1}
$$

Positive values indicate time saved with AI.

## 3. Primary Estimand

The mean paired time saving is:

$$
\widehat{\Delta}_T = \frac{1}{n}\sum_{i=1}^{n}D_i
$$

For the synthetic demonstration data:

$$
\widehat{\Delta}_T = 3.875 \text{ minutes}
$$

## 4. Bootstrap Confidence Interval

We apply a paired bootstrap with 10,000 resamples and random seed 42.

Each resample draws participant-level differences with replacement. The confidence interval is calculated using the 2.5th and 97.5th percentiles.

The synthetic example produces:

$$
95\%\,CI = [0.00,\ 6.25]\text{ minutes}
$$

## 5. Quality Guardrail

The mean quality difference is:

$$
\widehat{\Delta}_Q =
\frac{1}{n}\sum_{i=1}^{n}(Q_{i,1}-Q_{i,0})
$$

The predefined tolerance is five quality points:

$$
\widehat{\Delta}_Q \geq -5
$$

The demonstration dataset has:

$$
\widehat{\Delta}_Q = +2.875
$$

This is a descriptive guardrail check, not a formal non-inferiority test.

## 6. Secondary Metrics

Factual accuracy:

$$
F_{i,c} =
100 \times
\frac{\mathrm{factual\_correct}_{i,c}}
{\mathrm{factual\_total}_{i,c}}
$$

Unsupported claim rate:

$$
U_{i,c} =
100 \times
\frac{\mathrm{unsupported\_claims}_{i,c}}
{\mathrm{supported\_claims}_{i,c}+\mathrm{unsupported\_claims}_{i,c}}
$$

Both calculations require nonzero denominators.



The current dataset consists of eight synthetic observations representing four participant pairs.

These values are intended to demonstrate a reproducible analysis pipeline rather than provide empirical evidence.

No warm-up runs are labeled in the dataset, so no warm-up filtering is performed.

The small demonstration does not estimate task-order, learning, or carryover effects.
