"""Scanning, sensitivity, and Pareto utilities with no external dependencies."""
from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, List
import math
import random

from .core import (
    COLD_STORAGE_MEDIA,
    HOT_STORAGE_MEDIA,
    HX_TYPES,
    WORKING_FLUIDS,
    DesignPointInputs,
    simulate_design_point_generic,
)


class SimpleFrame:
    """Minimal stand-in for pandas DataFrame."""

    def __init__(self, rows: List[dict]):
        self.rows = rows
        self.columns = list(rows[0].keys()) if rows else []

    def __getitem__(self, key):
        if isinstance(key, list):
            return [[row[k] for k in key] for row in self.rows]
        return [row[key] for row in self.rows]

    def to_csv(self, path: str, index: bool = False):  # pragma: no cover
        import csv

        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.columns)
            writer.writeheader()
            writer.writerows(self.rows)

    def sort_values(self, by: str, ascending: bool = True):
        return SimpleFrame(sorted(self.rows, key=lambda r: r[by], reverse=not ascending))

    def loc(self, mask):
        return SimpleFrame([row for row, keep in zip(self.rows, mask) if keep])

    def copy(self):
        return SimpleFrame(list(self.rows))


DataFrameLike = SimpleFrame


def _make_frame(rows: List[dict]) -> DataFrameLike:
    return SimpleFrame(rows)


def scan_combinations(n_samples: int = 200, seed: int | None = None) -> DataFrameLike:
    rng = random.Random(seed)
    rows = []
    for _ in range(n_samples):
        inputs = DesignPointInputs(
            working_fluid=rng.choice(WORKING_FLUIDS),
            hot_storage=rng.choice(HOT_STORAGE_MEDIA),
            cold_storage=rng.choice(COLD_STORAGE_MEDIA),
            hx_type=rng.choice(HX_TYPES),
            rp=rng.uniform(2.0, 12.0),
            eta_is=rng.uniform(0.7, 0.9),
            eps_regen=rng.uniform(0.7, 0.98),
            t_hot_max=rng.uniform(500.0, 1200.0),
            t_cold_min=rng.uniform(-60.0, 50.0),
        )
        outputs = simulate_design_point_generic(inputs)
        row = asdict(inputs) | outputs.as_dict()
        rows.append(row)
    return _make_frame(rows)


def _rank(data: List[float]) -> List[float]:
    sorted_pairs = sorted((val, idx) for idx, val in enumerate(data))
    ranks = [0.0] * len(data)
    i = 0
    while i < len(sorted_pairs):
        j = i
        total = 0.0
        while j < len(sorted_pairs) and sorted_pairs[j][0] == sorted_pairs[i][0]:
            total += j + 1
            j += 1
        avg_rank = total / (j - i)
        for k in range(i, j):
            ranks[sorted_pairs[k][1]] = avg_rank
        i = j
    return ranks


def _spearman_coeff(x: List[float], y: List[float]) -> float:
    rx = _rank(x)
    ry = _rank(y)
    mean_x = sum(rx) / len(rx)
    mean_y = sum(ry) / len(ry)
    num = sum((a - mean_x) * (b - mean_y) for a, b in zip(rx, ry))
    den_x = math.sqrt(sum((a - mean_x) ** 2 for a in rx))
    den_y = math.sqrt(sum((b - mean_y) ** 2 for b in ry))
    return num / (den_x * den_y + 1e-12)


def spearman_sensitivity(df: DataFrameLike, target: str, features: Iterable[str]):
    rows = []
    target_vals = df[target]
    for feat in features:
        rho = _spearman_coeff(df[feat], target_vals)
        rows.append({"feature": feat, "rho": float(rho), "p_value": float("nan")})
    return _make_frame(rows)


def pareto_front(df: DataFrameLike, maximize: List[str], minimize: List[str]):
    values = [[row[c] for c in maximize + minimize] for row in df.rows]
    maximize_idx = list(range(len(maximize)))
    minimize_idx = list(range(len(maximize), len(maximize) + len(minimize)))

    pareto_mask = [True] * len(values)
    for i, point in enumerate(values):
        if not pareto_mask[i]:
            continue
        for j, other in enumerate(values):
            if i == j or not pareto_mask[j]:
                continue
            better_or_equal = all(other[k] >= point[k] for k in maximize_idx) and all(
                other[k] <= point[k] for k in minimize_idx
            )
            strictly_better = any(
                other[k] > point[k] for k in maximize_idx
            ) or any(other[k] < point[k] for k in minimize_idx)
            if better_or_equal and strictly_better:
                pareto_mask[i] = False
                break
    return df.loc(pareto_mask)
