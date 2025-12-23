# B-PTES

Lightweight surrogate implementation of pumped thermal energy storage (PTES) utilities.
The repository mirrors the layout described in the user brief, including scanning,
sensitivity analysis, simple dynamic simulation, and paper-replication presets.

## Layout

- `ptes_final/core.py`: working-fluid and storage-material libraries plus a surrogate
  design-point evaluator.
- `ptes_final/papers.py`: deterministic reproductions/baselines for published case
  studies (Wang & Bai 2022 strict, McTigue 2022, Neises & McTigue 2025 placeholders).
- `ptes_final/analysis_tools.py`: combination scan, Spearman sensitivity, and Pareto
  utilities implemented without third-party dependencies.
- `ptes_final/plotting.py`: plotting helpers for Pareto and sensitivity visuals
  (silently skipped if matplotlib is unavailable).
- `ptes_final/dynamics.py`: zero-dimensional dynamic SOC surrogate for dispatch tests.
- `ptes_final/scripts/`: entry points for benchmarks, scanning, and dynamic demos.

## Quickstart

Run the three example scripts from the repository root:

```bash
python ptes_final/scripts/run_benchmarks.py
python ptes_final/scripts/run_scan.py --n 50 --seed 1
python ptes_final/scripts/run_dynamic_demo.py
```

Each script saves its outputs (text, CSV, or PNG when matplotlib is installed) to the
working directory. No external Python packages are required.
