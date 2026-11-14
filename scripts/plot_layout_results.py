#!/usr/bin/env python3
"""Plot only the independently audited, separately scoped layout observations."""
import json
from pathlib import Path


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    root = Path(__file__).resolve().parents[1]
    sources = {
        'account': 'results/2026-11-14/summaries/layout-recovery-43575584325-account/summary.json',
        'lazy01': 'results/2026-11-14/summaries/layout-43570556202-lazy01/summary.json',
    }
    cases = ('account', 'lazy01')
    groups = {}
    for case, source in sources.items():
        summary = json.loads((root / source).read_text(encoding='utf-8'))
        if not summary.get('integrity_ok'):
            raise ValueError('Refuse to plot a study with failed evidence integrity')
        for row in summary['groups']:
            if row['case'] != case:
                raise ValueError('Separate batch contains an unexpected case')
            groups[(case, row['condition'])] = row
    if set(groups) != {(case, condition) for case in cases
                       for condition in ('capacity1990', 'capacity3964')}:
        raise ValueError('Unexpected case/condition design')
    metrics = [('schedules', 'Explored schedules', [65, 39]),
               ('first_error', 'First failing schedule', [2, 3]),
               ('buggy_schedules', 'Failure-producing schedules', [26, 12])]
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                         'svg.fonttype': 'none', 'axes.spines.top': False,
                         'axes.spines.right': False})
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.35))
    x = np.arange(len(cases))
    colors = ('#315D7D', '#B76D37')
    for ax, (metric, title, paper) in zip(axes, metrics):
        for offset, condition, label, color in zip(
                (-.24, 0), ('capacity1990', 'capacity3964'),
                ('Released capacity 1990', 'Corrected capacity 3964'), colors):
            stats = [groups[(case, condition)][metric] for case in cases]
            values = [s['mean'] if s['mean'] is not None else np.nan for s in stats]
            sd = [s['sample_sd'] if s['sample_sd'] is not None else 0 for s in stats]
            ax.bar(x + offset, values, width=.21, yerr=sd, capsize=3,
                   label=label, color=color, error_kw={'linewidth': 1})
            for index, stat in enumerate(stats):
                if stat['mean'] is None:
                    ax.annotate('n/a', (x[index] + offset, 0), xytext=(0, 5),
                                textcoords='offset points', ha='center',
                                fontsize=10, color=color)
        ax.scatter(x + .24, paper, color='#252A30', marker='D', s=30,
                   label='Paper reference', zorder=4)
        labels = []
        for case in cases:
            counts = [groups[(case, condition)][metric]['n']
                      for condition in ('capacity1990', 'capacity3964')]
            labels.append('{}\nn={}/{}'.format(case, *counts))
        ax.set_xticks(x, labels)
        ax.set_title(title, loc='left', fontsize=12, fontweight='bold', pad=10)
        ax.set_ylim(bottom=0)
        ax.set_axisbelow(True)
        ax.grid(axis='y', color='#E1E5E8', linewidth=.7)
        ax.margins(y=.18)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=3, frameon=False,
               bbox_to_anchor=(.5, 1.02))
    fig.text(.02, .025, 'Mean ± sample SD. Separate batches: account recovery; original lazy01. Original account is missing.', fontsize=10)
    fig.tight_layout(rect=(0, .085, 1, .88), w_pad=1.8)
    output = root / 'results/2026-11-14/figures'
    output.mkdir(parents=True, exist_ok=True)
    path = output / 'layout_comparison.svg'
    fig.savefig(path, metadata={'Date': None, 'Creator': 'CS340 project repository'})
    plt.close(fig)
    print(path.relative_to(root))


if __name__ == '__main__':
    main()
