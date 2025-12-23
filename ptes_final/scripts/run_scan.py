import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ptes_final.analysis_tools import pareto_front, scan_combinations, spearman_sensitivity
from ptes_final.plotting import bar_sensitivity, scatter_pareto


def save_frame(df, path: str):
    if hasattr(df, "to_csv"):
        df.to_csv(path, index=False)
    else:  # pragma: no cover
        import csv

        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(df.columns)
            for row in df.rows:
                writer.writerow([row[c] for c in df.columns])


def main():
    parser = argparse.ArgumentParser(description="Run PTES combination scan")
    parser.add_argument("--n", type=int, default=200, help="Number of samples")
    parser.add_argument("--seed", type=int, default=1, help="Random seed")
    args = parser.parse_args()

    df = scan_combinations(n_samples=args.n, seed=args.seed)
    save_frame(df, "scan_results.csv")

    sens = spearman_sensitivity(
        df,
        target="RTE",
        features=["rp", "eta_is", "eps_regen", "t_hot_max", "t_cold_min"],
    )
    save_frame(sens, "sensitivity_spearman.csv")
    bar_sensitivity(sens, output="sensitivity_RTE.png")

    pareto = pareto_front(df, maximize=["RTE", "Phi_ss", "rho_E_kWh_m3"], minimize=["LCOS"])
    save_frame(pareto, "scan_results_with_pareto.csv")
    scatter_pareto(pareto, x="RTE", y="LCOS", c="Phi_ss", output="pareto_scatter.png")

    print("Scan complete. Outputs saved to current directory.")


if __name__ == "__main__":
    main()
