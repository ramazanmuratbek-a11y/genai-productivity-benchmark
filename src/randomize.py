"""Generate reproducible balanced *planned* task assignments, not study results."""

import argparse
import csv
import random
from pathlib import Path
import yaml

SEQUENCES = [
    [('A', 'without_ai'), ('B', 'with_ai')],
    [('A', 'with_ai'), ('B', 'without_ai')],
    [('B', 'without_ai'), ('A', 'with_ai')],
    [('B', 'with_ai'), ('A', 'without_ai')],
]


def balanced_assignments(count: int, seed: int):
    """Return randomized order, balanced across four sequences when count is 4k."""
    if count < 4 or count % 4:
        raise ValueError('For perfect four-sequence balance, count must be a positive multiple of 4.')
    rng = random.Random(seed)
    assignments = (SEQUENCES * (count // 4)).copy()
    rng.shuffle(assignments)
    rows = []
    for i, sequence in enumerate(assignments, 1):
        for order, (task_set, condition) in enumerate(sequence, 1):
            rows.append({
                'participant_id': f'PLANNED_{i:03d}',
                'task_set': task_set,
                'task_order': order,
                'condition': condition,
            })
    return rows


def main():
    p = argparse.ArgumentParser(description='Create randomized assignments (no outcomes).')
    p.add_argument('--config', default='configs/experiment.yaml')
    p.add_argument('--count', type=int, default=8)
    p.add_argument('--output', type=Path, default=Path('outputs/demo/assignments.csv'))
    args = p.parse_args()
    config = yaml.safe_load(Path(args.config).read_text(encoding='utf-8'))
    seed = int(config['experiment']['random_seed'])
    rows = balanced_assignments(args.count, seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['participant_id','task_set','task_order','condition'])
        writer.writeheader()
        writer.writerows(rows)
    print(f'Wrote {len(rows)} planned task assignments; seed={seed}; file={args.output}')


if __name__ == '__main__':
    main()
