#!/usr/bin/env python3
"""Regenerate the stage report figures from archived observations."""
import json
from pathlib import Path
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / 'results/2026-11-07'
OUT = BATCH / 'figures'


def main():
    OUT.mkdir(exist_ok=True)
    matplotlib.rcParams['svg.fonttype'] = 'none'
    pilot = json.loads((BATCH / 'pilot/runs.json').read_text())
    cases = ['CS.reorder_3_bad', 'CS.reorder_4_bad']
    values = [[r['first_error_schedule'] for r in pilot
               if r.get('phase') == 'run' and r['case'] == case] for case in cases]
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.errorbar([0, 1], [statistics.mean(v) for v in values],
                yerr=[statistics.stdev(v) for v in values], fmt='o',
                capsize=6, markersize=8, label='Pilot mean ± sample SD (3 runs)')
    ax.plot([0, 1], [6, 9], 's', markersize=7, label='Paper Table 2')
    ax.set_xticks([0, 1], ['reorder_3_bad', 'reorder_4_bad'])
    ax.set_xlim(-0.5, 1.5); ax.set_ylim(0, 16)
    ax.set_ylabel('Schedules explored up to the first failure')
    ax.set_title('PERIOD: first-failure position')
    ax.legend(loc='upper left', fontsize=9)
    fig.tight_layout(); fig.savefig(OUT / 'first_failure.svg'); plt.close(fig)
    records = json.loads((BATCH / 'followup/followup.json').read_text())
    depths = [1, 2, 3]
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for metric, fmt, label in [
            ('observed_schedule_count', 'o-', 'Explored schedules'),
            ('reported_buggy_schedules', 's-', 'Schedules reporting the assertion failure')]:
        values = [[r[metric] for r in records if r.get('phase') == 'extension'
                   and r['depth'] == depth] for depth in depths]
        ax.errorbar(depths, [statistics.mean(v) for v in values],
                    yerr=[statistics.stdev(v) for v in values], fmt=fmt, capsize=5, label=label)
    ax.set_xticks(depths); ax.set_xlabel('Depth bound')
    ax.set_ylabel('Schedule count; mean ± sample SD'); ax.set_ylim(bottom=0)
    ax.set_title('Depth-bound extension: unchanged reorder_3_bad')
    ax.legend(fontsize=9); fig.tight_layout()
    fig.savefig(OUT / 'depth_extension.svg'); plt.close(fig)


if __name__ == '__main__':
    main()
