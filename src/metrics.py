"""Real paired-time and quality metrics. No hard-coded experimental outcomes."""

import math
from typing import Any
import numpy as np
from scipy import stats
import pandas as pd


def paired_statistics(without_values, with_values) -> dict[str, Any]:
    """95% two-sided CI for the mean paired difference (with - without)."""
    a = np.asarray(without_values, dtype=float)
    b = np.asarray(with_values, dtype=float)
    if not len(a) or len(a) != len(b):
        raise ValueError('Non-empty equal-length paired samples are required.')
    if not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError('Measurements must be finite.')
    delta = b - a
    n = len(delta)
    avg = float(np.mean(delta))
    result = {
        'n_pairs': n,
        'mean_without_ai': float(np.mean(a)),
        'mean_with_ai': float(np.mean(b)),
        'mean_paired_difference_with_minus_without': avg,
        'ci95_paired_difference': None,
        'paired_t_p_value_two_sided': None,
    }
    if n >= 2 and np.std(delta, ddof=1) > 0:
        interval = stats.t.interval(0.95, n - 1, loc=avg, scale=stats.sem(delta))
        result['ci95_paired_difference'] = [float(interval[0]), float(interval[1])]
        result['paired_t_p_value_two_sided'] = float(stats.ttest_rel(b, a).pvalue)
    return result


def analyze_pairs(df: pd.DataFrame, quality_tolerance_points: float = 5.0):
    """Analyze only participants who completed both tasks; retain exclusion counts."""
    all_ids = set(df['participant_id'])
    completed = df[df['completed'] == 1].copy()
    counts = completed.groupby('participant_id')['condition'].nunique()
    keep_ids = set(counts[counts == 2].index)
    paired = completed[completed['participant_id'].isin(keep_ids)].copy()
    paired['quality_score'] = paired[['quality_rater_1', 'quality_rater_2']].mean(axis=1)
    paired['factual_accuracy_percent'] = (
        100 * paired['factual_correct'] / paired['factual_total']
    )
    outcome = {
        'data_origin': df['data_origin'].iloc[0],
        'participants_total': len(all_ids),
        'participants_with_complete_pairs': len(keep_ids),
        'participants_excluded_from_paired_analysis': len(all_ids - keep_ids),
        'quality_guardrail_tolerance_points': quality_tolerance_points,
    }
    if not keep_ids:
        outcome['status'] = 'No complete pairs; no paired estimate is available.'
        return outcome, pd.DataFrame()

    t = paired.pivot(index='participant_id', columns='condition', values='completion_time_minutes')
    q = paired.pivot(index='participant_id', columns='condition', values='quality_score')
    f = paired.pivot(index='participant_id', columns='condition', values='factual_accuracy_percent')
    t_stats = paired_statistics(t['without_ai'], t['with_ai'])
    q_stats = paired_statistics(q['without_ai'], q['with_ai'])
    f_stats = paired_statistics(f['without_ai'], f['with_ai'])
    mean_control = t_stats['mean_without_ai']
    outcome.update({
        'time_minutes': t_stats,
        'quality_score': q_stats,
        'factual_accuracy_percent': f_stats,
        'relative_time_reduction_percent':
            float(100 * (mean_control - t_stats['mean_with_ai']) / mean_control),
    })
    quality_ci = q_stats['ci95_paired_difference']
    outcome['quality_noninferiority_guardrail'] = (
        'not_applicable_synthetic_data' if outcome['data_origin'] == 'synthetic'
        else ('met_in_complete_pair_analysis' if quality_ci and quality_ci[0] > -quality_tolerance_points
              else 'not_established')
    )
    # Descriptive data for exploratory experience-related analysis only.
    exp = paired.groupby('participant_id')['experience_years'].first()
    per_person = pd.DataFrame({
        'participant_id': t.index,
        'experience_years': exp.loc[t.index].to_numpy(),
        'time_without_ai': t['without_ai'].to_numpy(),
        'time_with_ai': t['with_ai'].to_numpy(),
        'time_difference_with_minus_without': (t['with_ai'] - t['without_ai']).to_numpy(),
        'relative_time_reduction_percent': (100 * (t['without_ai'] - t['with_ai']) / t['without_ai']).to_numpy(),
        'quality_without_ai': q['without_ai'].to_numpy(),
        'quality_with_ai': q['with_ai'].to_numpy(),
    })
    if outcome['data_origin'] == 'synthetic':
        outcome['status'] = 'DEMONSTRATION ONLY: synthetic records, not empirical research findings.'
    else:
        outcome['status'] = 'Observed records; interpret with protocol and sampling limitations.'
    return outcome, per_person
