# Operating Systems – Assignment 3 (CO3)

## One-run implementation pack (Ubuntu on WSL2)

This repository pack contains the C programs, Makefiles, shell scripts and experiment generator for all seven questions. The goal is that you only need to install the build tools once and execute **one command**. The run creates the text/CSV/SVG evidence under each task's `outputs/` folder.

### 1. Extract and open in Ubuntu (WSL)

Open this folder in VS Code connected to **Ubuntu (WSL)**. The terminal prompt should show your normal Linux user, for example `mrudhula@...$` (not `root@...#` and not `MINGW`).

### 2. Install tools once

```bash
sudo apt update
sudo apt install -y build-essential gcc make python3 time procps util-linux
```

### 3. Run everything

From the main folder containing this README and `run_all.sh`, run:

```bash
chmod +x run_all.sh
./run_all.sh
```

**You do not need to compile or run each task separately.** The script builds every C program, executes Task01–Task07, performs the extra experiments, and writes the evidence files. It is safe to run again; generated outputs are refreshed.

## Output map

| Folder | Automatically generated evidence |
|---|---|
| `Task01/outputs/` | static/shared executable run and sizes, `ldd`, `dlopen` output, `/proc` mappings, startup/RSS measurements, shared-library replacement without relinking, missing-library failure, two-process library mappings and clean-page accounting |
| `Task02/outputs/` | completed paging TODO output, 100 reproducible random process sizes, internal fragmentation for 1 KB/4 KB/2 MB, TLB hit-ratio EAT, Linux page size, 2 KB page-size address translations and flat page-table size calculations |
| `Task03/outputs/` | eight address translations, protection/limit checks, `/proc` maps, deliberate segmentation fault (exit 139 is expected), deterministic 20-segment first-fit fragmentation simulation, illustrative table-size comparison |
| `Task04/outputs/` | sequential/reverse memory touch, random access, minor/major fault deltas, `/usr/bin/time -v`, fork copy-on-write measurements and page-fault EAT calculations |
| `Task05/outputs/` | completed LRU TODO and expected-output verification, FIFO/LRU/Optimal counts, Belady's anomaly, 3–10 frame CSV data, strong-locality and random workloads, SVG graphs and 100,000-reference timing measurements |
| `Task06/outputs/` | RAID capacity calculations for six 4 TB disks, Linux block device/partition/swap report, explicit RAID1/RAID5 probability model and a safe local sequential-read benchmark |
| `Task07/outputs/` | `mlock()` timing attempt, memory-budget calculation, three-task page-replacement model and 500 MB additional-task impact |

Open `.svg` files in a browser. Open `.csv` files in Excel or LibreOffice. Text outputs are readable directly in VS Code.

## Screenshot folder

Every task contains a `screenshots/` folder. The script does **not** create fake screenshots. After the run, capture your own terminal/editor screenshots and save them in the matching folder. Suggested evidence:

- Task01: complete `Task01/outputs/experiments.txt` and executable/`ldd` output.
- Task02: paging output and the 100-process/2 KB calculation files.
- Task03: segment translation, 20-segment result and expected segmentation-fault output.
- Task04: `/usr/bin/time -v`, sequential/random fault comparison and COW output.
- Task05: expected FIFO/LRU/Optimal + Belady output and the three policy graphs.
- Task06: RAID capacity output and system disk/swap report.
- Task07: `mlock()` result and memory-plan/simulation outputs.

## Important experimental limitations (read before writing the report)

- Timing, RSS, page-fault counts, page size, disk layout and `mlock()` permissions are machine-specific. Use the values generated on **your own Ubuntu WSL system** in the final report.
- The Q1 static build statically incorporates the application's demonstration crypto object; normal Ubuntu runtime libraries may still be dynamically linked. The shared build uses a `.so` and is compared with `ldd`.
- The Q1 two-process test reports each process's mapping and `/proc/<pid>/smaps` clean-page accounting. This is evidence of the same shared-object file being mapped; exact physical page sharing depends on kernel accounting and should not be overstated.
- Q3's 20-segment allocator is a deterministic first-fit **simulation** to demonstrate external fragmentation. It is not a claim that Linux uses a pure segmentation memory manager.
- Q4 memory-touch tests are deliberately bounded to avoid exhausting WSL RAM. The assignment's run-beyond-free-RAM test should only be done in a VM with an intentional memory limit; this pack does not risk freezing your laptop.
- Q6 probability output uses an explicitly stated simplified independent annual disk failure assumption (2% per disk). The local read benchmark is not an SSD-versus-HDD comparison unless you run it on separate known devices.
- Q7's page replacement and `mlock()` programs are demonstrations, not a proof of hard real-time guarantees. On WSL, `mlock()` may fail due to `RLIMIT_MEMLOCK`; the program records the failure. Do not claim the real-time task is guaranteed never to be delayed solely from this demonstration.
- This pack automates implementation and measured/simulated evidence. The report still needs the explanations, diagrams, comparisons, conclusions and alternative-concept/complexity analyses asked in the assignment. We will prepare that separately using the actual outputs.

## Environment information to record

The README for submission must include your own name and register number. The script captures task outputs; record your actual versions with:

```bash
gcc --version
lsb_release -a
getconf PAGESIZE
```

The C programs use `gcc -std=c11 -Wall -Wextra -O2`; shared-library builds add `-fPIC -shared`, and the `dlopen()` program links with `-ldl`.

## GitHub submission

The assignment requires repository name `CSA0405-<RegisterNumber>-Assignment3` and at least one progressive commit per task. After you run and check the generated files, use these commands (replace the register number and remote URL):

```bash
git init
git add README.md Makefile run_all.sh experiments.py .gitignore
git commit -m "Add assignment setup and experiment runner"
git add Task01 && git commit -m "Complete Task 1 - Linking"
git add Task02 && git commit -m "Complete Task 2 - Paging"
git add Task03 && git commit -m "Complete Task 3 - Segmentation"
git add Task04 && git commit -m "Complete Task 4 - Virtual memory"
git add Task05 && git commit -m "Complete Task 5 - Page replacement"
git add Task06 && git commit -m "Complete Task 6 - Disk management"
git add Task07 && git commit -m "Complete Task 7 - Memory plan"
git branch -M main
git remote add origin https://github.com/<GitHubUsername>/CSA0405-<RegisterNumber>-Assignment3.git
git push -u origin main
```

Do not push until you have reviewed the output and added your screenshots. Keep the register number and GitHub link accurate; do not leave placeholders in the submitted README.
