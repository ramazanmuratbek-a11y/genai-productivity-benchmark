"""Validate paired writing-task measurements before statistical analysis."""

import argparse
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    'participant_id', 'task_set', 'task_order', 'condition', 'completed',
    'completion_time_minutes', 'quality_rater_1', 'quality_rater_2',
    'factual_correct', 'factual_total', 'experience_years', 'data_origin',
}
CLAIM_COLUMNS = ('supported_claims', 'unsupported_claims')
CONDITIONS = {'with_ai', 'without_ai'}


def validate_dataframe(frame: pd.DataFrame, maximum_minutes: float = 30.0) -> pd.DataFrame:
    """Return a typed, validated copy; raise ValueError for invalid measurements.

    Claim counts are optional for backward compatibility. Both columns must be
    supplied together; an entirely blank pair means 'not annotated yet'.
    """
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f'Missing required columns: {", ".join(sorted(missing))}')
    if frame.empty:
        raise ValueError('Input dataset is empty.')
    if (CLAIM_COLUMNS[0] in frame.columns) != (CLAIM_COLUMNS[1] in frame.columns):
        raise ValueError('supported_claims and unsupported_claims must be supplied together.')

    df = frame.copy()
    for name in ['participant_id', 'task_set', 'condition', 'data_origin']:
        if df[name].isna().any() or df[name].astype(str).str.strip().eq('').any():
            raise ValueError(f'Empty {name} values are not allowed.')
        df[name] = df[name].astype(str).str.strip()
    if not df['condition'].isin(CONDITIONS).all():
        raise ValueError('condition must be with_ai or without_ai.')
    if not df['task_set'].isin(['A', 'B']).all():
        raise ValueError('task_set must be A or B.')
    if not df['data_origin'].isin(['synthetic', 'real']).all() or df['data_origin'].nunique() != 1:
        raise ValueError('data_origin must be consistently synthetic or real.')

    numeric = [
        'task_order', 'completed', 'completion_time_minutes',
        'quality_rater_1', 'quality_rater_2', 'factual_correct',
        'factual_total', 'experience_years',
    ]
    for name in numeric:
        original = df[name]
        converted = pd.to_numeric(original, errors='coerce')
        if (original.notna() & converted.isna()).any():
            raise ValueError(f'{name} contains a nonnumeric value.')
        df[name] = converted

    for name in CLAIM_COLUMNS:
        if name not in df.columns:
            df[name] = float('nan')
        else:
            original = df[name]
            converted = pd.to_numeric(original, errors='coerce')
            if (original.notna() & converted.isna()).any():
                raise ValueError(f'{name} contains a nonnumeric value.')
            df[name] = converted

    if df[['task_order', 'completed', 'completion_time_minutes', 'experience_years']].isna().any().any():
        raise ValueError('Task order, completion status, time and experience must be numeric.')
    if not df['task_order'].isin([1, 2]).all() or not df['completed'].isin([0, 1]).all():
        raise ValueError('task_order must be 1/2 and completed must be 0/1.')
    if (~df['completion_time_minutes'].between(0, maximum_minutes, inclusive='right')).any():
        raise ValueError(f'Completion time must be > 0 and <= {maximum_minutes} minutes.')
    if (df['experience_years'] < 0).any():
        raise ValueError('Professional experience cannot be negative.')

    for participant, group in df.groupby('participant_id'):
        if len(group) != 2 or set(group['condition']) != CONDITIONS:
            raise ValueError(f'{participant}: exactly one record per condition is required.')
        if set(group['task_set']) != {'A', 'B'} or set(group['task_order']) != {1, 2}:
            raise ValueError(f'{participant}: use different task sets and orders 1 and 2.')
        if group['experience_years'].nunique() != 1:
            raise ValueError(f'{participant}: experience_years must be constant.')

    complete = df[df['completed'] == 1]
    for col in ['quality_rater_1', 'quality_rater_2']:
        if complete[col].isna().any() or not complete[col].between(0, 100).all():
            raise ValueError(f'{col} must be 0..100 for completed tasks.')
    if complete[['factual_correct', 'factual_total']].isna().any().any():
        raise ValueError('Completed tasks need factual counts.')
    if ((complete['factual_total'] <= 0) | (complete['factual_correct'] < 0) |
            (complete['factual_correct'] > complete['factual_total'])).any():
        raise ValueError('Factual counts must satisfy 0 <= correct <= total and total > 0.')

    for name in ['factual_correct', 'factual_total', *CLAIM_COLUMNS]:
        present = complete[name].dropna()
        if ((present < 0) | (present % 1 != 0)).any():
            raise ValueError(f'{name} must be a nonnegative integer count.')

    supported_present = complete['supported_claims'].notna()
    unsupported_present = complete['unsupported_claims'].notna()
    if not supported_present.equals(unsupported_present):
        raise ValueError('Both claim counts must be provided or both left blank.')
    annotated = complete[supported_present]
    if (annotated['supported_claims'] < annotated['factual_correct']).any():
        raise ValueError('supported_claims cannot be less than correctly covered anchor facts.')

    incomplete = df[df['completed'] == 0]
    absent_if_incomplete = [
        'quality_rater_1', 'quality_rater_2', 'factual_correct', 'factual_total',
        *CLAIM_COLUMNS,
    ]
    if not incomplete.empty and incomplete[absent_if_incomplete].notna().any().any():
        raise ValueError('Incomplete tasks must have blank quality, factual and claim counts.')
    return df


def main():
    parser = argparse.ArgumentParser(description='Validate paired-task research measurements.')
    parser.add_argument('csv_file', type=Path)
    parser.add_argument('--max-minutes', type=float, default=30)
    args = parser.parse_args()
    frame = validate_dataframe(pd.read_csv(args.csv_file), args.max_minutes)
    print(f'VALID: {len(frame)} records from {frame.participant_id.nunique()} participants; '
          f'data_origin={frame.data_origin.iloc[0]}.')


if __name__ == '__main__':
    main()
