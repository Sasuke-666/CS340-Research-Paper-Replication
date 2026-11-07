#!/usr/bin/env python3
"""Predeclared same-machine comparison; Python 3.6-compatible in the authors' image."""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
from run_period_pilot import execute, utc

PIN = 'cb8deb9a176e5bb292d70d46557dd61dc0e98069'
CASES = {'reorder_3':'reorder_3_bad','reorder_4':'reorder_4_bad','account':'account_bad','lazy01':'lazy01_bad','twostage':'twostage_bad'}
METHODS = {'period':'run_PDS.py','author_serialized':'run_OldPDS.py'}


def parse_log(text, budget=10000):
    text = re.sub(r'\x1b\[[0-9;]*m', '', text)
    seen, failed, current = [], [], None
    for line in text.splitlines():
        m = re.match(r'^test\s+(\d+)(?: for prefix [^:]+)?:\s*(.+)$', line)
        if m and int(m[1]) <= budget:
            current = int(m[1]); seen.append(current)
        if '[Error Found]:' in line:
            failed.append(current)
    total = re.search(r'(?m)^Total Error Interleavings:\s*(\d+)', text)
    rounds = re.search(r'(?m)^Round\s+\d+\s+(\d+)\s*$', text)
    errors = int(total[1]) if total else None
    valid = (bool(seen) and len(seen) == len(set(seen)) and
             seen == list(range(1, len(seen) + 1)) and rounds is not None and
             min(int(rounds[1]), budget) == len(seen) and total is not None and
             errors == len(failed) and None not in failed and 'End Testing!' in text)
    return {'schedules':len(seen),'first_error':failed[0] if failed else None,
            'buggy_schedules':errors,'error_event_count':len(failed),
            'complete_markers':valid,'inner_timeouts':len(re.findall(r'\[Timeout\s',text)),
            'budget_reached':bool(rounds and int(rounds[1]) >= budget)}


def diagnostic_source(original):
    old = 'int(Period*1.5)'
    if original.count(old) != 1:
        raise ValueError('Pinned replay calibration anchor changed')
    source = original.replace(old, 'int(Period*float(os.environ["CS340_REPLAY_SCALE"]))')
    old = '        process.communicate()\n        sys.exit()'
    if source.count(old) != 1:
        raise ValueError('Pinned replay return-code anchor changed')
    new = ('        process.communicate()\n'
           '        print("CS340_REPLAY " + __import__("json").dumps({'
           '"target_returncode":process.returncode,"calibrated_period":Period,'
           '"scale":float(os.environ["CS340_REPLAY_SCALE"])}), flush=True)\n'
           '        sys.exit()')
    return source.replace(old,new)


def method_order(repetition):
    others=[m for m in METHODS if m!='period']
    if 'period' not in METHODS or len(others)!=1:
        raise ValueError('Exactly one primary and one baseline are required')
    pair=['period',others[0]]
    return pair if repetition%2 else pair[::-1]


def new_output_folders(directory, binary, previous_names):
    """A failed invocation must never inherit an earlier invocation's witnesses."""
    return sorted((p for p in directory.glob('out_'+binary+'_*')
                   if p.is_dir() and p.name not in previous_names),
                  key=lambda p:p.stat().st_mtime)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path('/workdir/PERIOD'))
    ap.add_argument('--output',type=Path,default=Path('/evidence'))
    ap.add_argument('--case',required=True,choices=sorted(CASES))
    ap.add_argument('--repetitions',type=int,default=10)
    ap.add_argument('--comparison-timeout',type=int,default=120)
    args=ap.parse_args();root,out=args.root,args.output
    if args.repetitions<1 or args.comparison_timeout<1:
        ap.error('Repetitions and comparison timeout must be positive')
    out.mkdir(parents=True,exist_ok=True)
    if (out/'records.json').exists():raise ValueError('Refuse to overwrite a measured batch')
    case,binary=args.case,CASES[args.case]
    directory=root/'evaluation/CS'/case;records=[]
    def save():
        (out/'records.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    def run(cmd,log,phase,timeout=120,**extra):
        r=execute(cmd,directory,out/log,timeout)
        r.update(phase=phase,case=case,**extra);records.append(r);save();return r
    env={'captured_utc':utc(),'source_commit':PIN,'platform':platform.platform(),
         'python':platform.python_version(),'cpu_affinity':sorted(os.sched_getaffinity(0)),
         'cpu_models':sorted(set(l.split(':',1)[1].strip() for l in Path('/proc/cpuinfo').read_text(encoding='utf-8').splitlines() if l.startswith('model name'))),
         'os_release':Path('/etc/os-release').read_text(encoding='utf-8'),'paired_methods_same_built_binary':True,
         'comparison_settings':{'repetitions_per_method':args.repetitions,'outer_timeout_seconds':args.comparison_timeout,'depth':3,'schedule_budget':10000}}
    (out/'environment.json').write_text(json.dumps(env,indent=2)+'\n',encoding='utf-8')
    source_dir=out/'source';source_dir.mkdir()
    for path in (root/'tool/DBDS').glob('*.py'):shutil.copy2(str(path),str(source_dir/path.name))
    shutil.copy2(str(root/'LICENSE'),str(source_dir/'LICENSE.txt'))
    diff=difflib.unified_diff((root/'tool/DBDS/run_OldPDS.py').read_text(encoding='utf-8').splitlines(True),(root/'tool/DBDS/run_PDS.py').read_text(encoding='utf-8').splitlines(True),fromfile='run_OldPDS.py',tofile='run_PDS.py')
    (out/'driver_comparison.diff').write_text(''.join(diff),encoding='utf-8')
    r=run(['bash','build.sh'],'build.txt','build',180)
    if r['exit_code']!=0 or not (directory/binary).is_file():return 2
    env['binary_sha256']=hashlib.sha256((directory/binary).read_bytes()).hexdigest()
    env['drivers']={m:hashlib.sha256((root/'tool/DBDS'/p).read_bytes()).hexdigest() for m,p in METHODS.items()}
    for path in directory.iterdir():
        if path.is_file() and (path.suffix in ('.c','.cpp','.sh') or path.name.startswith('ConConfig.')):
            shutil.copy2(str(path),str(source_dir/path.name))
    (out/'environment.json').write_text(json.dumps(env,indent=2)+'\n',encoding='utf-8')
    for repetition in range(1,args.repetitions+1):
        order=method_order(repetition)
        for position,method in enumerate(order,1):
            log='{}_r{:02d}.txt'.format(method,repetition)
            cmd=['python3',str(root/'tool/DBDS'/METHODS[method]),'-y','-d','3','-f','10000','./'+binary]
            previous_names={p.name for p in directory.glob('out_'+binary+'_*')}
            r=run(cmd,log,'comparison',args.comparison_timeout,method=method,repeat=repetition,position=position,timeout_seconds=args.comparison_timeout)
            r.update(parse_log((out/log).read_text(encoding='utf-8',errors='replace')))
            r['status']='complete' if not r['timed_out'] and r['exit_code']==0 and r['complete_markers'] else 'incomplete'
            folders=new_output_folders(directory,binary,previous_names)
            r['new_witness_folders']=[p.name for p in folders]
            if folders:
                for p in sorted((folders[-1]/'Errors').glob('*')):
                    if p.is_file() and p.stat().st_size<100000:
                        dest=out/'witnesses'/method/('r%02d'%repetition)/p.name
                        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(str(p),str(dest))
            save()
    if case=='reorder_3':
        original=(root/'tool/DBDS/run_PDS.py').read_text(encoding='utf-8');instrumented=diagnostic_source(original)
        driver=root/'tool/DBDS/run_PDS_diagnostic.py';driver.write_text(instrumented,encoding='utf-8')
        (out/'diagnostic_driver.diff').write_text(''.join(difflib.unified_diff(original.splitlines(True),instrumented.splitlines(True),fromfile='original',tofile='diagnostic')),encoding='utf-8')
        witness=out/'fixed_witness.txt';witness.write_text('[[0, 2], [2, 0], [1, 0]]\n',encoding='utf-8')
        for repetition in range(1,21):
            scales=[1.5,6.0] if repetition%2 else [6.0,1.5]
            for position,scale in enumerate(scales,1):
                label='default' if scale==1.5 else 'expanded';log='diagnostic_{}_r{:02d}.txt'.format(label,repetition)
                cmd=['env','CS340_REPLAY_SCALE='+str(scale),'python3',str(driver),'-y','-r',str(witness),'./'+binary]
                r=run(cmd,log,'diagnostic',20,condition=label,repeat=repetition,position=position,scale=scale)
                text=(out/log).read_text(encoding='utf-8',errors='replace');found=re.search(r'(?m)^CS340_REPLAY (.+)$',text)
                r['target_observation']=json.loads(found[1]) if found else None
                r['expected_assertion']=bool(re.search(r'Assertion[^\n]*failed',text))
                r['status']='complete' if found and not r['timed_out'] and r['exit_code']==0 else 'incomplete';save()
    manifest=[]
    for p in sorted(out.rglob('*')):
        if p.is_file() and p.name not in ('container_console.txt','container_exit_code.txt','manifest.json'):
            raw=p.read_bytes();manifest.append({'path':p.relative_to(out).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    (out/'manifest.json').write_text(json.dumps({'files':manifest,'created_utc':utc()},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'case':case,'commands':len(records),'complete':sum(r.get('status')=='complete' for r in records)}))
    return 0 if all(r.get('status','complete')=='complete' for r in records) else 1


if __name__=='__main__':raise SystemExit(main())
