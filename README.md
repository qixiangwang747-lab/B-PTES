# B-PTES

轻量级的抽水式热储能（PTES）代理模型与工具集，覆盖组合扫描、敏感性分析、零维动态仿真，以及论文结果复现。全部代码仅依赖标准库，方便在任何环境快速运行或集成到后续 GUI/优化工作流中。

## 目录/文件说明

- `ptes_final/core.py`：**核心设计点代理模型**。包含工质、储热/储冷材料、换热器类型库，并提供设计点计算函数和随机样本生成器。
- `ptes_final/papers.py`：**论文复现与基线**。严格复现 Wang & Bai (2022) Table 2 + Eq.(16)-(19)，并给出 McTigue 2022、Neises & McTigue 2025 的可运行基线。
- `ptes_final/analysis_tools.py`：**组合扫描与敏感性**。无第三方依赖的“简化 DataFrame”实现，提供组合抽样、Spearman 敏感性、Pareto 前沿筛选。
- `ptes_final/plotting.py`：**科研绘图助手**。Pareto 散点、敏感性条形、理想气体 T-s 图；若未安装 matplotlib 会友好提示并跳过。
- `ptes_final/dynamics.py`：**零维动态 SOC 代理**。基于容量与时间序列功率的简单 SOC 演化，可用于调峰/运行策略原型。
- `ptes_final/scripts/`：示例脚本集合，便于快速跑通：
  - `run_benchmarks.py`：运行论文复现基准，输出 RTE 与备注到 `benchmark_results.txt`。
  - `run_scan.py`：执行组合扫描、Spearman 敏感性、Pareto 前沿，输出 CSV/PNG。
  - `run_dynamic_demo.py`：给定正弦功率曲线生成 SOC 轨迹，输出 CSV。

## 快速开始

在仓库根目录运行以下示例脚本即可：

```bash
python ptes_final/scripts/run_benchmarks.py
python ptes_final/scripts/run_scan.py --n 50 --seed 1
python ptes_final/scripts/run_dynamic_demo.py
```

每个脚本会在当前工作目录写出结果（文本、CSV、若安装 matplotlib 则额外生成 PNG）。无需安装任何额外 Python 第三方库。
