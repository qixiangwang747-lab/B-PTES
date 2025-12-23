"""0D dynamic PTES surrogate for dispatch studies."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
import math


@dataclass
class DynamicConfig:
    capacity_kwh: float
    rho_hot_kj_per_k: float = 1.8e3
    rho_cold_kj_per_k: float = 1.0e3
    tau_hot_hx_s: float = 200.0
    tau_cold_hx_s: float = 200.0
    ua_loss_kw_per_k: float = 0.001


class PTESDynamicSimulator:
    def __init__(self, config: DynamicConfig):
        self.cfg = config

    def simulate(self, power_profile_kw: List[float], timestep_s: float = 60.0) -> Tuple[List[float], List[float]]:
        soc = 0.5
        soc_trace: List[float] = []
        power_trace: List[float] = []
        cap_j = self.cfg.capacity_kwh * 3.6e6

        for p in power_profile_kw:
            energy_delta = -p * timestep_s
            soc += energy_delta / cap_j
            soc = min(1.0, max(0.0, soc))

            loss = (soc - 0.5) * self.cfg.ua_loss_kw_per_k * timestep_s / cap_j
            soc -= loss

            soc_trace.append(soc)
            power_trace.append(p)

        return power_trace, soc_trace
