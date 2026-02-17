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

    # 基准值用于“脚本层健康检查”：只要机理计算被不小心改坏，断言会立即报错。
    expected = {
        "WangBai2022": 0.6272287390029324,
        "McTigue2022": 0.58,
        "Neises2025": 0.61,
    }

    for name, res in results.items():
        target = expected[name]
        if abs(res.rte - target) > 1e-6:
            raise ValueError(
                f"{name} RTE 偏离基准值：当前 {res.rte:.6f}，应为 {target:.6f}；请检查机理模型或输入。"
            )

    out_lines = []
    for name, res in results.items():
        out_lines.append(f"{name}: RTE={res.rte:.4f} | {res.notes}")
    output = "\n".join(out_lines)
    print(output)

    print("\n健康检查：全部 RTE 与基准一致，无偏差。")

    Path("benchmark_results.txt").write_text(output)


if __name__ == "__main__":
    main()
