"""运行论文复现/基线，输出 RTE 与备注（中文说明）。"""
 
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ptes_final import papers


def main():
    results = {
        "WangBai2022": papers.reproduce_wangbai2022_table2_strict(),
        "McTigue2022": papers.reproduce_mctigue2022_baseline(),
        "Neises2025": papers.reproduce_neises2025_baseline(),
    }

    out_lines = []
    for name, res in results.items():
        out_lines.append(f"{name}: RTE={res.rte:.4f} | {res.notes}")
    output = "\n".join(out_lines)
    print(output)

    Path("benchmark_results.txt").write_text(output)


if __name__ == "__main__":
    main()
