#!/usr/bin/env python3
"""Draw the expanded study's figures from independently audited measurements."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def save_svg(fig, path):
    fig.savefig(path, metadata={'Date': None})
    path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8')
    plt.close(fig)


def main():
    root=Path(__file__).resolve().parents[1]
    summary=json.loads((root/'results/2026-11-07/summaries/comparison-42381922637/summary.json').read_text())
    if not summary['integrity_ok']:raise ValueError('Refuse to plot unaudited measurements')
    primary={(x['case'],x['method']):x for x in summary['groups']}
    follow=json.loads((root/'results/2026-11-07/summaries/comparison-42384122902/summary.json').read_text())
    if not follow['integrity_ok']:raise ValueError('Unaudited follow-up')
    groups=dict(primary);groups.update({(x['case'],x['method']):x for x in follow['groups']})
    cases=['reorder_3','reorder_4','account','lazy01','twostage']
    if any(groups[(c,m)]['eligible_n']!=(3 if c=='reorder_4' else 10) for c in cases for m in ['period','author_serialized_abi16']):
        raise ValueError('Figure requires the registered complete sample from each matched batch')
    out=root/'results/2026-11-07/figures';out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                         'axes.spines.right':False,'svg.hashsalt':'cs340-period-20261107'})
    y=np.arange(len(cases));height=.32
    fig,ax=plt.subplots(figsize=(8.2,3.9),layout='constrained')
    for label,method,offset,color,hatch in [
        ('PERIOD','period',-height/2,'#276478',None),
        ('Serialized (ABI-compatible)','author_serialized_abi16',height/2,'#C6C6C6','//')]:
        values=[groups[(c,method)]['schedules']['mean'] for c in cases]
        sd=[groups[(c,method)]['schedules']['sample_sd'] for c in cases]
        bars=ax.barh(y+offset,values,height,label=label,color=color,hatch=hatch,edgecolor='#333333',linewidth=.5,xerr=sd)
        ax.bar_label(bars,labels=['{:g}'.format(x) for x in values],padding=4,fontsize=9)
    ax.set_yticks(y,cases);ax.invert_yaxis();ax.set_xlabel('Explored schedules (mean ± sample SD; n = 10; reorder_4 follow-up n = 3)')
    ax.set_xlim(0,max(groups[(c,'author_serialized_abi16')]['schedules']['mean'] for c in cases)*1.15)
    ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True);ax.legend(loc='lower right',frameon=False)
    save_svg(fig, out/'expanded_schedule_comparison.svg')
    groups=primary
    fig,axes=plt.subplots(1,2,figsize=(8.2,4.0),layout='constrained')
    for ax,metric,label in zip(axes,['first_error','buggy_schedules'],['First failing schedule','Buggy schedules']):
        paper=[groups[(c,'period')]['paper_table_2_gaps'][metric]['reference'] for c in cases]
        ours=[groups[(c,'period')][metric]['mean'] for c in cases]
        sd=[groups[(c,'period')][metric]['sample_sd'] for c in cases]
        ax.plot(paper,y-.1,'s',color='#555555',label='Paper Table 2',markersize=5)
        ax.errorbar(ours,y+.1,xerr=sd,fmt='o',color='#276478',capsize=3,label='Ours (n = 10)',markersize=5)
        ax.set_yticks(y,cases);ax.invert_yaxis();ax.set_xlabel(label);ax.set_xlim(left=0);ax.grid(axis='x',alpha=.2)
    axes[1].legend(loc='lower right',frameon=False,fontsize=9)
    save_svg(fig, out/'expanded_paper_gaps.svg')
    print('Wrote expanded_schedule_comparison.svg and expanded_paper_gaps.svg')


if __name__=='__main__':main()
