"""Paired writing-task outcomes and exploratory factual claim metrics."""

from typing import Any

import numpy as np
import pandas as pd
from scipy import stats


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


def factual_claim_scores(correct: int, total: int, supported=None, unsupported=None):
    """Return (precision, recall, F1) in 0..1 or None where undefined.

    Recall is correct covered anchor facts / all anchor facts. Precision is
    supported factual claims / all assessable factual claims. An unannotated
    task, or a response with zero assessable claims, has undefined precision.
    """
    recall = correct / total
    if supported is None or unsupported is None or pd.isna(supported) or pd.isna(unsupported):
        return None, recall, None
    denominator = supported + unsupported
    if denominator == 0:
        return None, recall, None
    precision = supported / denominator
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return float(precision), float(recall), float(f1)


def _paired_optional_metric(paired: pd.DataFrame, column: str):
    """Use only participants whose AI and no-AI metric values are both defined."""
    wide = paired.pivot(index='participant_id', columns='condition', values=column)
    complete = wide.dropna(subset=['without_ai', 'with_ai'])
    if complete.empty:
        return None, 0
    return paired_statistics(complete['without_ai'], complete['with_ai']), len(complete)


def analyze_pairs(df: pd.DataFrame, quality_tolerance_points: float = 5.0):
    """Analyze complete participant pairs, transparently report missing metrics."""
    all_ids = set(df['participant_id'])
    completed = df[df['completed'] == 1].copy()
    counts = completed.groupby('participant_id')['condition'].nunique()
    keep_ids = set(counts[counts == 2].index)
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

    paired = completed[completed['participant_id'].isin(keep_ids)].copy()
    paired['quality_score'] = paired[['quality_rater_1', 'quality_rater_2']].mean(axis=1)
    paired['factual_accuracy_percent'] = 100 * paired['factual_correct'] / paired['factual_total']
    # Backward-compatible factual_accuracy_percent is anchor-fact recall.
    paired['factual_recall_percent'] = paired['factual_accuracy_percent']
    metrics = paired.apply(
        lambda row: factual_claim_scores(
            int(row['factual_correct']), int(row['factual_total']),
            row.get('supported_claims'), row.get('unsupported_claims')
        ), axis=1,
    )
    paired['factual_precision_percent'] = metrics.map(lambda x: 100*x[0] if x[0] is not None else float('nan'))
    paired['factual_f1_percent'] = metrics.map(lambda x: 100*x[2] if x[2] is not None else float('nan'))

    def wide(column):
        return paired.pivot(index='participant_id', columns='condition', values=column)

    t = wide('completion_time_minutes')
    q = wide('quality_score')
    f = wide('factual_accuracy_percent')
    t_stats = paired_statistics(t['without_ai'], t['with_ai'])
    q_stats = paired_statistics(q['without_ai'], q['with_ai'])
    f_stats = paired_statistics(f['without_ai'], f['with_ai'])
    precision_stats, precision_n = _paired_optional_metric(paired, 'factual_precision_percent')
    f1_stats, f1_n = _paired_optional_metric(paired, 'factual_f1_percent')
    mean_control = t_stats['mean_without_ai']
    outcome.update({
        'time_minutes': t_stats,
        'quality_score': q_stats,
        'factual_accuracy_percent': f_stats,
        'factual_recall_percent': f_stats,
        'factual_precision_percent': precision_stats,
        'factual_f1_percent': f1_stats,
        'claim_metric_pairs_with_valid_precision': precision_n,
        'claim_metric_pairs_with_valid_f1': f1_n,
        'relative_time_reduction_percent':
            float(100 * (mean_control - t_stats['mean_with_ai']) / mean_control),
    })
    quality_ci = q_stats['ci95_paired_difference']
    outcome['quality_noninferiority_guardrail'] = (
        'not_applicable_synthetic_data' if outcome['data_origin'] == 'synthetic'
        else ('met_in_complete_pair_analysis' if quality_ci and quality_ci[0] > -quality_tolerance_points
              else 'not_established')
    )

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
    for label, column in [
        ('factual_precision', 'factual_precision_percent'),
        ('factual_recall', 'factual_recall_percent'),
        ('factual_f1', 'factual_f1_percent'),
    ]:
        w = wide(column).reindex(index=t.index)
        per_person[f'{label}_without_ai_percent'] = w['without_ai'].to_numpy()
        per_person[f'{label}_with_ai_percent'] = w['with_ai'].to_numpy()

    if outcome['data_origin'] == 'synthetic':
        outcome['status'] = 'DEMONSTRATION ONLY: synthetic records, not empirical research findings.'
    else:
        outcome['status'] = 'Observed records; interpret with protocol and sampling limitations.'
    return outcome, per_person
