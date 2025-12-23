"""PTES 设计点核心数据与代理计算函数（中文注释版）。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple
import math
import random

# 组合扫描可用的工质与储热/储冷材料列表（可按需扩展）。
WORKING_FLUIDS: List[str] = [
    "Air",
    "N2",
    "CO2",
    "He",
    "Ar",
    "Xe",
    "H2",
    "CH4",
    "O2",
]

HOT_STORAGE_MEDIA: List[str] = [
    "SolarSalt",
    "Hitec",
    "Chloride",
    "Concrete",
    "Ceramic",
    "Alumina",
    "Steel",
    "Graphite",
    "SandBed",
]

COLD_STORAGE_MEDIA: List[str] = [
    "Methanol",
    "Ethanol",
    "Propane",
    "CO2liq",
    "Glycol30",
    "Water",
    "IcePCM",
    "ParaffinPCM",
]

HX_TYPES: List[str] = ["plate-fin", "shell-tube", "printed-circuit"]


@dataclass
class DesignPointInputs:
    working_fluid: str
    hot_storage: str
    cold_storage: str
    hx_type: str
    rp: float  # 压缩比
    eta_is: float  # 绝热效率（压缩机/透平）
    eps_regen: float  # 回热器效率
    t_hot_max: float
    t_cold_min: float


@dataclass
class DesignPointResult:
    rte: float
    lcos: float
    rho_e_kwh_m3: float
    rho_p_kw_m3: float
    rho_e_kwh_per_t: float
    rho_p_kw_per_t: float
    phi_ss: float

    def as_dict(self) -> Dict[str, float]:
        return {
            "RTE": self.rte,
            "LCOS": self.lcos,
            "rho_E_kWh_m3": self.rho_e_kwh_m3,
            "rho_P_kW_m3": self.rho_p_kw_m3,
            "rho_E_kWh_per_t": self.rho_e_kwh_per_t,
            "rho_P_kW_per_t": self.rho_p_kw_per_t,
            "Phi_ss": self.phi_ss,
        }


def _safety_factor(fluid: str, t_hot_max: float, t_cold_min: float) -> float:
    """针对工质与温度窗口给出简化安全系数。"""

    heavy_penalty = {"Xe": 0.9, "Ar": 0.93, "CO2": 0.95}.get(fluid, 1.0)
    hot_window = max(0.0, min(1.0, (t_hot_max - 400.0) / 800.0))
    cold_window = max(0.0, min(1.0, (20.0 - t_cold_min) / 80.0))
    return heavy_penalty * (0.6 + 0.4 * hot_window + 0.2 * cold_window)


def simulate_design_point_generic(inputs: DesignPointInputs) -> DesignPointResult:
    """在给定输入下返回 RTE/LCOS/能量密度等“快速估算值”。"""

    rp_effect = math.log(max(1.01, inputs.rp)) / math.log(12.0)
    regen_boost = 0.4 * inputs.eps_regen + 0.6 * inputs.eta_is
    safety = _safety_factor(inputs.working_fluid, inputs.t_hot_max, inputs.t_cold_min)

    rte = max(0.05, min(0.8, regen_boost * rp_effect * safety))

    hot_density = 1600 if inputs.hot_storage in {"Concrete", "Ceramic", "Alumina"} else 1800
    cold_density = 900 if "PCM" in inputs.cold_storage else 1000
    rho_e_kwh_m3 = (inputs.t_hot_max - inputs.t_cold_min) * 0.15 * rte
    rho_p_kw_m3 = rho_e_kwh_m3 * (0.4 + 0.6 * inputs.eta_is)

    rho_e_kwh_per_t = rho_e_kwh_m3 / (hot_density / 1000)
    rho_p_kw_per_t = rho_p_kw_m3 / (cold_density / 1000)

    mu_hot = max(0.1, min(2.0, (inputs.t_hot_max - 300) / 300))
    mu_cold = max(0.1, min(2.0, (300 - inputs.t_cold_min) / 300))
    phi_ss = math.exp(-0.5 * (abs(math.log(mu_hot)) + abs(math.log(mu_cold))))
    phi_ss *= 1.0 - 0.1 * (1.0 - inputs.eps_regen)

    lcos = 150 / max(0.1, rte) * 1e3 / max(1.0, rho_e_kwh_m3)

    return DesignPointResult(
        rte=rte,
        lcos=lcos,
        rho_e_kwh_m3=rho_e_kwh_m3,
        rho_p_kw_m3=rho_p_kw_m3,
        rho_e_kwh_per_t=rho_e_kwh_per_t,
        rho_p_kw_per_t=rho_p_kw_per_t,
        phi_ss=phi_ss,
    )


def random_design_point(seed: int | None = None) -> Tuple[DesignPointInputs, DesignPointResult]:
    """生成一组随机设计点与对应的代理计算结果，便于测试/扫描。"""

    rng = random.Random(seed)
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
    return inputs, simulate_design_point_generic(inputs)
