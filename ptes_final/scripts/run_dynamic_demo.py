import math
import sys
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ptes_final.dynamics import DynamicConfig, PTESDynamicSimulator


def main():
    profile = [200 * math.sin(x) for x in [i * (4 * math.pi) / 200 for i in range(200)]]
    cfg = DynamicConfig(capacity_kwh=1000.0)
    sim = PTESDynamicSimulator(cfg)
    power, soc = sim.simulate(profile, timestep_s=60.0)

    with open("dynamic_demo.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["power_kw", "soc"])
        writer.writerows(zip(power, soc))
    print("Dynamic simulation complete. Results saved to dynamic_demo.csv")


if __name__ == "__main__":
    main()
