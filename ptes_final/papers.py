"""论文复现与基线预设（中文注释版）。

保持完全可读、轻量化，实现文献中的 RTE 计算逻辑，便于脚本调用或 GUI 切换。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class PaperResult:
    rte: float
    notes: str

    def as_dict(self) -> Dict[str, float | str]:
        return {"RTE": self.rte, "notes": self.notes}


def reproduce_wangbai2022_table2_strict() -> PaperResult:
    """按 Table 2 + Eq.(16)-(19) 严格复现 Wang & Bai (2022) 的功率平衡。"""

    p_ch = 108.0
    p_tl = 39.8
    p_th = 95.0
    p_cl = 50.0
    eta_m = 0.98
    eta_g = 0.97

    p_s = (p_ch - p_tl) / eta_m
    p_g = eta_g * (p_th - p_cl)
    rte = p_g / p_s
    return PaperResult(rte=rte, notes="Strict recreation of Table 2 power balance")


def reproduce_mctigue2022_baseline() -> PaperResult:
    """McTigue (2022) 的近似基线：因缺少压降/成本细节，暂用占位实现。"""

    rte = 0.58  # representative mid-range value
    notes = "Approximate baseline pending detailed pressure-drop and UA data"
    return PaperResult(rte=rte, notes=notes)


def reproduce_neises2025_baseline() -> PaperResult:
    """Neises & McTigue (2025) 的近似基线，占位以保持接口一致。"""

    rte = 0.61
    notes = "Approximate baseline pending CAPEX split and efficiency assumptions"
    return PaperResult(rte=rte, notes=notes)
