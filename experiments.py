#!/usr/bin/env python3
"""Generate repeatable, machine-specific OS Assignment 3 experiment evidence."""
import csv, os, random, subprocess, time, pathlib, shutil, statistics
ROOT = pathlib.Path(__file__).resolve().parent
OUT = {f'Task{i:02d}': ROOT/f'Task{i:02d}'/'outputs' for i in range(1,8)}
for p in OUT.values(): p.mkdir(parents=True, exist_ok=True)
def run(cmd, cwd=None, timeout=30):
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
def save(task, name, text): (OUT[f'Task{task:02d}']/name).write_text(text, encoding='utf-8')
def graph_svg(path, title, xs, ys, xlabel, ylabel):
    w,h=760,440; left,right,top,bottom=85,30,55,75
    xmin,xmax=min(xs),max(xs); ymin,ymax=0,max(ys)*1.12 or 1
    pts=[]
    for x,y in zip(xs,ys):
        px=left+(x-xmin)/(xmax-xmin or 1)*(w-left-right); py=h-bottom-y/ymax*(h-top-bottom); pts.append((px,py))
    poly=' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
    circles=''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5"/><text x="{x:.1f}" y="{y+22:.1f}" text-anchor="middle" font-size="12">{v}</text>' for (x,y),v in zip(pts,ys))
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="white"/><text x="{w/2}" y="30" text-anchor="middle" font-size="20">{title}</text><path d="M{left} {top} V{h-bottom} H{w-right}" stroke="black" fill="none"/><polyline points="{poly}" fill="none" stroke="#1769aa" stroke-width="3"/>{circles}<text x="{w/2}" y="{h-18}" text-anchor="middle" font-size="14">{xlabel}</text><text transform="translate(20 {h/2}) rotate(-90)" text-anchor="middle" font-size="14">{ylabel}</text></svg>'''
    path.write_text(svg, encoding='utf-8')

# Q1: startup/RSS, replacement without relink, missing-library handling, shared mappings
p=ROOT/'Task01'; lines=['Q1 EXPERIMENTAL INVESTIGATION','============================']
for exe in ('bank_static','bank_dynamic'):
    r=run(['/usr/bin/time','-f','elapsed_seconds=%e\nmax_rss_kb=%M','./'+exe],cwd=p)
    lines += [f'[{exe}] exit={r.returncode}',r.stdout.strip()]
# runtime replacement
lib=p/'libcrypto_demo.so'; backup=p/'libcrypto_demo.so.original'
try:
    shutil.copy2(lib,backup)
    (p/'crypto_v2.c').write_text('#include <stdio.h>\nint encrypt_value(int value) { return value ^ 0x1234; }\n')
    r=run(['gcc','-std=c11','-Wall','-Wextra','-O2','-fPIC','-shared','-o',str(lib),str(p/'crypto_v2.c')])
    before=run(['./bank_dynamic'],cwd=p,timeout=5)
    lines += ['[shared library replacement; executable was NOT relinked]',before.stdout.strip(),f'compile_status={r.returncode}']
finally:
    if backup.exists(): shutil.move(str(backup),str(lib))
# Missing shared object: temporarily hide the library
hidden=p/'libcrypto_demo.so.hidden'
try:
    lib.rename(hidden); r=run(['./bank_dynamic'],cwd=p,timeout=5)
    lines += ['[missing shared library test]',f'exit={r.returncode}',r.stdout.strip()]
finally:
    if hidden.exists(): hidden.rename(lib)
# Two processes mapping the same shared object
hold=p/'hold_maps'; build=run(['gcc','-std=c11','-Wall','-Wextra','-O2','-o',str(hold),str(p/'hold_maps.c'),'-L.', '-lcrypto_demo',"-Wl,-rpath,$ORIGIN"],cwd=p)
if build.returncode==0:
    procs=[]
    try:
        for _ in range(2): procs.append(subprocess.Popen([str(hold)],cwd=p,stdout=subprocess.PIPE,text=True))
        time.sleep(1)
        for pr in procs:
            pid=pr.stdout.readline().strip().split()[0].split('=')[1]
            maps=pathlib.Path(f'/proc/{pid}/maps').read_text()
            smaps=pathlib.Path(f'/proc/{pid}/smaps').read_text()
            matching=[x for x in maps.splitlines() if 'libcrypto_demo.so' in x]
            blocks=smaps.split('\n')
            in_lib=False; shared_clean=0; private_clean=0
            for row in blocks:
                if row and '-' in row.split()[0] and len(row.split()[0]) >= 9:
                    in_lib='libcrypto_demo.so' in row
                elif in_lib and row.startswith('Shared_Clean:'):
                    shared_clean += int(row.split()[1])
                elif in_lib and row.startswith('Private_Clean:'):
                    private_clean += int(row.split()[1])
            lines += [f'[process {pid}] shared-library map entries:',*matching[:5],f'library Shared_Clean (kB)={shared_clean}',f'library Private_Clean (kB)={private_clean}']
    except Exception as e: lines.append(f'process map experiment note: {e}')
    finally:
        for pr in procs: pr.terminate()
        for pr in procs:
            try: pr.wait(timeout=3)
            except subprocess.TimeoutExpired: pr.kill()
else: lines.append('hold_maps build failed: '+build.stdout)
save(1,'experiments.txt','\n'.join(lines)+'\n')

# Q2: 100 reproducible process sizes and fragmentation
rng=random.Random(20261119); sizes=[rng.randint(1,64*1024*1024) for _ in range(100)]
rows=[]; report=['Q2 – 100 RANDOM PROCESS SIZES (seed=20261119)','process_id,size_bytes']
for i,n in enumerate(sizes,1): report.append(f'{i},{n}')
for ps in (1024,4096,2*1024*1024):
    waste=sum((ps-n%ps)%ps for n in sizes); rows.append((ps,waste,waste/1024/1024))
report += ['', 'page_size_bytes,total_internal_fragmentation_bytes,total_MB']+[f'{a},{b},{c:.6f}' for a,b,c in rows]
report += ['', 'TLB effective access time (serial lookup; memory=100ns, TLB=10ns)', 'hit_ratio,EAT_ns']
for h in (.80,.95,.99): report.append(f'{h:.0%},{h*110+(1-h)*210:.2f}')
report.append(f'Linux page size from getconf: {os.sysconf("SC_PAGE_SIZE")} bytes')
save(2,'random_100_processes.csv','process_id,size_bytes\n'+'\n'.join(f'{i},{n}' for i,n in enumerate(sizes,1))+'\n')
save(2,'experiments.txt','\n'.join(report)+'\n')

# Q3: simulate 20 random segments in a simple contiguous free-list allocator
rng=random.Random(303); total=2*1024*1024; free=[(0,total)]; allocated=[]; events=[]
for i in range(20):
    size=rng.randint(8*1024,96*1024); fit=next((j for j,(b,l) in enumerate(free) if l>=size),None)
    if fit is None: break
    b,l=free.pop(fit); allocated.append((b,size)); events.append(f'load segment {i+1}: {size} bytes at {b}')
    if l>size: free.insert(fit,(b+size,l-size))
# remove every third allocated segment and coalesce
for idx in range(len(allocated)-1,-1,-1):
    if (idx+1)%3==0:
        b,s=allocated[idx]; free.append((b,s)); events.append(f'remove segment {idx+1}: {s} bytes'); allocated.pop(idx)
free.sort(); merged=[]
for b,l in free:
    if merged and merged[-1][0]+merged[-1][1]==b: merged[-1]=(merged[-1][0],merged[-1][1]+l)
    else: merged.append((b,l))
external=sum(l for _,l in merged)-max((l for _,l in merged),default=0)
events += ['',f'allocated segments remaining={len(allocated)}',f'free holes={len(merged)}',f'total free bytes={sum(l for _,l in merged)}',f'largest free block={max((l for _,l in merged),default=0)}',f'external fragmentation (free total - largest hole)={external} bytes','Note: deterministic first-fit simulation; not a measurement of Linux kernel segment allocation.']
save(3,'random_20_segments.txt','Q3 – 20 RANDOM SEGMENT ALLOCATION SIMULATION\n'+'\n'.join(events)+'\n')

# Q4: EAT and sequential/random page-touch tests using bounded memory
mem=100; fault=8_000_000; q4=['Q4 – PAGE FAULT EFFECTIVE ACCESS TIME','memory_access_ns=100; page_fault_service_ns=8000000']
for rate in (1/1000,1/100000,1/1000000): q4.append(f'fault_rate={rate:g}; EAT_ns={(1-rate)*mem+rate*fault:.2f}')
q4 += ['', 'Maximum fault rate for 10% slowdown: solve 100 + p*(8,000,000-100)=110 ns',f'p={10/(fault-mem):.12g} (approximately one fault per {int((fault-mem)/10):,} accesses)']
save(4,'calculations.txt','\n'.join(q4)+'\n')
vm=ROOT/'Task04'/'vm_access'
if vm.exists():
    r=run([str(vm),'32'],timeout=60); save(4,'sequential_access.txt',r.stdout+f'\nexit={r.returncode}\n')
    # randomized page access through a compact Python mmap experiment
    import mmap
    size=32*1024*1024; page=os.sysconf('SC_PAGE_SIZE'); mm=mmap.mmap(-1,size)
    order=list(range(0,size,page)); random.Random(404).shuffle(order)
    t=time.perf_counter()
    for off in order: mm[off:off+1]=b'X'
    qtime=time.perf_counter()-t; mm.close()
    save(4,'random_access.txt',f'Randomly touched {len(order)} pages ({size//1024//1024} MB) in {qtime:.6f} seconds.\nPython mmap experiment; timing is machine-specific.\n')

# Q5: page fault counts 3–10 frames for FIFO/LRU/Optimal, with CSV + SVG
rng=random.Random(505); ref=[rng.randrange(12) for _ in range(500)]
def faults(policy, frames):
    mem=[]; last={}; count=0; hand=0
    for i,x in enumerate(ref):
        if x in mem: last[x]=i; continue
        count+=1
        if len(mem)<frames: mem.append(x)
        elif policy=='FIFO': mem[hand]=x; hand=(hand+1)%frames
        elif policy=='LRU': mem[mem.index(min(mem,key=lambda z:last.get(z,-1)))]=x
        else:
            def nxt(z):
                try:return ref.index(z,i+1)
                except ValueError:return 10**9
            mem[mem.index(max(mem,key=nxt))]=x
        last[x]=i
    return count
csvp=OUT['Task05']/'frame_faults.csv'; data=[]
for f in range(3,11): data.append((f,faults('FIFO',f),faults('LRU',f),faults('OPT',f)))
with csvp.open('w',newline='') as fp:
    wr=csv.writer(fp); wr.writerow(['frames','FIFO_faults','LRU_faults','Optimal_faults']); wr.writerows(data)
for j,name in ((1,'FIFO'),(2,'LRU'),(3,'Optimal')): graph_svg(OUT['Task05']/f'{name.lower()}_faults.svg',f'{name} page faults vs frame count',[r[0] for r in data],[r[j] for r in data],'Number of frames','Page faults')
save(5,'experiment_summary.txt','Q5 – RANDOM REFERENCE STRING (seed=505; 500 references; pages 0–11)\n'+'\n'.join(f'{f} frames: FIFO={a}, LRU={b}, Optimal={c}' for f,a,b,c in data)+'\nCSV and SVG graphs are in this outputs folder.\n')

# Q6: capture system disk layout and swap status without changing disks
q6=['Q6 – DISK AND SWAP INSPECTION']
for cmd in (['lsblk','-o','NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS'],['cat','/proc/swaps'],['df','-hT']):
    r=run(cmd); q6 += ['$ '+' '.join(cmd),r.stdout.strip()]
save(6,'system_disk_report.txt','\n'.join(q6)+'\n')

# Q7: calculations + mlock program output already produced by standard run_all
q7=['Q7 – MEMORY PLAN AND CAPACITY CHECK','RAM budget=2048 MB','Control=128 MB (locked/pre-faulted)','ML=1536 MB','Logging=128 MB','OS reserve=256 MB','Total planned=2048 MB','Adding a 500 MB task creates a 500 MB overcommit.','The mlock timing is reported in Task07/outputs/run.txt; results depend on permissions and system load.']
save(7,'design_check.txt','\n'.join(q7)+'\n')

# Additional assignment-specific evidence not covered by the first run.
# Q2: hand-check translation with PAGE_SIZE=2048 and theoretical table sizes.
q2b=['Q2 – PAGE_SIZE=2048 RE-CALCULATION (same page table)', 'logical,page,offset,result']
pt=[5,2,-1,7,0,-1,3,-1]
for a in (0,1500,3100,6200,9000,2049):
    pg,off=divmod(a,2048)
    if pg>=len(pt): res='invalid address'
    elif pt[pg]<0: res='page fault'
    else: res=f'physical {pt[pg]*2048+off}'
    q2b.append(f'{a},{pg},{off},{res}')
q2b += ['', 'Page-table entries with 4 KB pages (one entry per virtual page):',
        f'32-bit address space: {(2**32)//4096:,} entries',
        f'48-bit address space: {(2**48)//4096:,} entries',
        'Assumption: 4-byte page-table entry; single-level table size = entries × 4 bytes.',
        f'32-bit table size = {(2**32)//4096*4:,} bytes',
        f'48-bit table size = {(2**48)//4096*4:,} bytes']
save(2,'page_size_2048_and_table_sizes.txt','\n'.join(q2b)+'\n')

# Q3: page/segment table size comparison with explicitly stated assumptions.
q3b=['Q3 – TABLE SIZE COMPARISON (illustrative assumptions)',
     'Assume 32-bit virtual address, 4 KB pages, 4-byte PTE, 3 logical segments/process.',
     f'Pure paging: {(2**32)//4096:,} PTEs; {(2**32)//4096*4:,} bytes for a flat page table.',
     'Pure segmentation: 3 descriptors × 8 bytes = 24 bytes per process (base, limit, protection metadata).',
     'Segmented paging: 3 segment descriptors plus page tables only for pages actually mapped; size depends on each segment length.',
     'Translation: paging uses page-number lookup; segmentation checks limit then adds base; segmented paging checks segment then translates page.',
     'These are model calculations, not measurements of Linux internal kernel structures.']
save(3,'table_size_comparison.txt','\n'.join(q3b)+'\n')

# Q4: measure minor/major faults for bounded sequential and randomized page touching.
# resource.getrusage reports process-wide fault counters; values are deltas around each test.
import resource
try:
    import mmap
    size=64*1024*1024; page=os.sysconf('SC_PAGE_SIZE')
    def touch_order(order, label):
        mm=mmap.mmap(-1,size)
        before=resource.getrusage(resource.RUSAGE_SELF); t=time.perf_counter()
        for off in order: mm[off:off+1]=b'Z'
        elapsed=time.perf_counter()-t; after=resource.getrusage(resource.RUSAGE_SELF); mm.close()
        return f'{label}: bytes={size}; pages={len(order)}; seconds={elapsed:.6f}; minor_fault_delta={after.ru_minflt-before.ru_minflt}; major_fault_delta={after.ru_majflt-before.ru_majflt}\n'
    offsets=list(range(0,size,page))
    save(4,'page_fault_access_comparison.txt',touch_order(offsets,'Sequential')+touch_order(random.Random(404).sample(offsets,len(offsets)),'Random'))
except Exception as e:
    save(4,'page_fault_access_comparison.txt',f'Access experiment unavailable: {e}\n')

# Q5: strong-locality and random workload, FIFO/LRU/Optimal faults for 3–10 frames,
# plus timing all policies on 100,000 references. Optimal uses next-use queues.
def make_workloads():
    rr=random.Random(505)
    strong=[]
    for _ in range(10000):
        base=rr.randrange(0,20)
        strong.extend([base+rr.randrange(0,5) for _ in range(8)])
    random_work=[rr.randrange(100) for _ in range(100000)]
    return strong[:100000], random_work

def policy_fault_count(refs, cap, policy):
    from collections import defaultdict, deque
    future=defaultdict(deque)
    if policy=='OPT':
        for idx,v in enumerate(refs): future[v].append(idx)
    frames=[]; last={}; fifo_idx=0; misses=0
    for i,v in enumerate(refs):
        if policy=='OPT':
            future[v].popleft()
        if v in frames:
            last[v]=i; continue
        misses+=1
        if len(frames)<cap: frames.append(v)
        elif policy=='FIFO':
            frames[fifo_idx]=v; fifo_idx=(fifo_idx+1)%cap
        elif policy=='LRU':
            victim=min(frames,key=lambda x:last.get(x,-1)); frames[frames.index(victim)]=v
        else:
            def next_use(x): return future[x][0] if future[x] else float('inf')
            victim=max(frames,key=next_use); frames[frames.index(victim)]=v
        last[v]=i
    return misses

strong, random_refs=make_workloads(); lines=['Q5 – LOCALITY AND RANDOM WORKLOAD COMPARISON', 'References per workload=100000; frames=3..10']
for label, refs in (('strong_locality',strong),('random',random_refs)):
    lines.append(f'[{label}]')
    rows=[]
    for f in range(3,11):
        vals=[policy_fault_count(refs,f,pol) for pol in ('FIFO','LRU','OPT')]
        rows.append((f,*vals)); lines.append(f'{f} frames: FIFO={vals[0]}, LRU={vals[1]}, Optimal={vals[2]}')
    with (OUT['Task05']/f'{label}_faults.csv').open('w',newline='') as fp:
        wr=csv.writer(fp); wr.writerow(['frames','FIFO','LRU','Optimal']); wr.writerows(rows)
    for col,pol in ((1,'FIFO'),(2,'LRU'),(3,'Optimal')):
        graph_svg(OUT['Task05']/f'{label}_{pol.lower()}_faults.svg',f'{label.replace("_"," ").title()} – {pol} faults',[r[0] for r in rows],[r[col] for r in rows],'Number of frames','Page faults')
# 100k timing: FIFO and LRU + OPT (OPT may take longer but next-use queues keep it efficient).
timing=[]
for label, refs in (('strong_locality',strong),('random',random_refs)):
    for pol in ('FIFO','LRU','OPT'):
        t0=time.perf_counter(); count=policy_fault_count(refs,8,pol); elapsed=time.perf_counter()-t0
        timing.append(f'{label},{pol},100000,8,{count},{elapsed:.6f}')
save(5,'100k_algorithm_timings.csv','workload,algorithm,references,frames,page_faults,seconds\n'+'\n'.join(timing)+'\n')
save(5,'locality_random_comparison.txt','\n'.join(lines)+'\n')

# Q6: reliability probability model and a safe local-file read benchmark.
# Assumption for illustration: independent annual disk failure probability q=2%.
q=.02
p_loss_raid1=q*q
p_loss_raid5=6*(q**2)*(1-q)**4 + 15*(q**2)*(q**2)*(1-q)**2 + 20*(q**3)*(1-q)**3 + 15*(q**4)*(1-q)**2 + 6*(q**5)*(1-q) + q**6
# For RAID5, data loss occurs at 2 or more failures; exact binomial tail.
p_loss_raid5=sum(__import__('math').comb(6,k)*q**k*(1-q)**(6-k) for k in range(2,7))
q6b=['Q6 – DISK FAILURE PROBABILITY MODEL','Assumption: independent annual per-disk failure probability q=2%; simplified model ignores rebuild window and correlated failures.',f'RAID1 two-disk mirror data-loss probability (both fail in same year): {p_loss_raid1:.8%}',f'RAID5 six-disk array data-loss probability (2 or more fail in same year): {p_loss_raid5:.8%}', 'RAID5 calculation is a binomial tail for >=2 failed disks; actual risk depends on rebuild time and correlated failures.']
try:
    test=pathlib.Path('/tmp/os_assignment3_read_test.bin'); block=os.urandom(1024*1024)
    with test.open('wb') as fp:
        for _ in range(32): fp.write(block)
    t0=time.perf_counter()
    with test.open('rb') as fp:
        while fp.read(1024*1024): pass
    elapsed=time.perf_counter()-t0; q6b.append(f'Local filesystem sequential read: 32 MiB in {elapsed:.6f} s ({32/elapsed:.2f} MiB/s); this is not an SSD-vs-HDD comparison.')
    test.unlink(missing_ok=True)
except Exception as e: q6b.append(f'Local read benchmark unavailable: {e}')
save(6,'reliability_and_read_test.txt','\n'.join(q6b)+'\n')

# Q7: simple page-replacement simulation for three task streams, preserving control pages.
q7b=['Q7 – THREE-TASK MEMORY-USE SIMULATION','Model: 32 frames; control task is preloaded and pinned in 4 frames; ML and logging share remaining 28 frames.']
streams={'control':[0,1,2,3]*25,'machine_learning':[10,11,12,13,14,15,16,17]*12,'logging':[30,31,32,33,34]*20}
for name,refs in streams.items():
    if name=='control': q7b.append(f'{name}: {len(refs)} references; pinned resident set=4 pages; page faults after preload=0 (by design).')
    else:
        misses=policy_fault_count(refs,28,'LRU')
        q7b.append(f'{name}: {len(refs)} references; LRU faults in 28-frame model={misses}.')
q7b += ['Interpretation: this is a deterministic allocation model, not a hard-real-time guarantee. A real deployment must reserve/pre-fault/lock control memory and validate scheduling, interrupt and I/O latency.']
save(7,'three_task_memory_simulation.txt','\n'.join(q7b)+'\n')

print('Additional experimental evidence generated in Task01–Task07/outputs/.')
