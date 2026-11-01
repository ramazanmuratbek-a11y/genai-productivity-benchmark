"""Run the proposed writing-task analysis using CSV measurements."""

import argparse
import json
from pathlib import Path
import pandas as pd
import yaml

from metrics import analyze_pairs
from validate_data import validate_dataframe


def main():
    parser = argparse.ArgumentParser(description='Analyze paired AI/no-AI writing-task data.')
    parser.add_argument('--input', type=Path, default=Path('data/sample/example_measurements.csv'))
    parser.add_argument('--config', type=Path, default=Path('configs/experiment.yaml'))
    parser.add_argument('--output-dir', type=Path, default=Path('outputs/demo'))
    args = parser.parse_args()
    config = yaml.safe_load(args.config.read_text(encoding='utf-8'))
    max_minutes = float(config['experiment']['time_limit_minutes'])
    tolerance = float(config['metrics']['quality_guardrail_tolerance_points'])
    validated = validate_dataframe(pd.read_csv(args.input), max_minutes)
    summary, participant_effects = analyze_pairs(validated, tolerance)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'summary.json').write_text(
        json.dumps(summary, indent=2, allow_nan=False) + '\n', encoding='utf-8'
    )
    participant_effects.to_csv(args.output_dir / 'participant_effects.csv', index=False)
    print('Dataset:', args.input)
    print('Data origin:', summary['data_origin'].upper())
    print('Complete participant pairs:', summary['participants_with_complete_pairs'])
    print('Excluded participants:', summary['participants_excluded_from_paired_analysis'])
    if 'time_minutes' in summary:
        print('Mean paired time difference (AI - no AI), min:',
              round(summary['time_minutes']['mean_paired_difference_with_minus_without'], 3))
    print('Research status:', summary['status'])
    print('Output:', args.output_dir.resolve())


if __name__ == '__main__':
    main()
