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

## 运行教程（从零开始的全流程）

### 1. 环境准备

- 需要 Python ≥3.8，完全使用标准库，无需额外依赖；系统自带 python3 即可运行。
- 建议在仓库根目录下操作，输出文件会直接写到当前工作目录。
- **是否必须本地部署？** 不需要额外部署，只要有 Python 的环境即可运行：
  - 本地电脑：直接按下方命令运行即可；无需数据库、无需外部服务。
  - 远程/服务器：同样只需把仓库代码放上去并运行 python 脚本（无 GUI 依赖，SSH 环境即可）。
  - 若要绘图（保存 PNG/PDF），可选 `pip install matplotlib`，但不是必须条件。

### 2. 获取代码

```bash
git clone <本仓库地址>
cd B-PTES
```

### 3. 运行论文复现基准

```bash
python ptes_final/scripts/run_benchmarks.py
```

输出：

- `benchmark_results.txt`：文本汇总 Wang & Bai 2022 严格复现的 RTE=0.6273，以及 McTigue 2022、Neises & McTigue 2025 的近似基线结果。
- 终端同步打印同样内容，便于快速查看。

### 4. 执行组合扫描 + 敏感性 + Pareto

```bash
python ptes_final/scripts/run_scan.py --n 200 --seed 1
```

参数说明：

- `--n`：抽样组合数量（默认 100，可根据时间与精度调整）。
- `--seed`：随机种子，保证可复现。

输出文件（均在当前目录）：

- `scan_results.csv`：原始组合与指标。
- `scan_results_with_pareto.csv`：标记 Pareto 前沿的结果。
- 若已安装 matplotlib：
  - `pareto_scatter.png/.pdf`：RTE–LCOS–能量密度散点图。
  - `sensitivity_RTE.png/.pdf`：RTE 对关键参数的 Spearman 敏感性条形图。
- 若未安装 matplotlib，脚本会提示并跳过绘图，但 CSV 仍正常生成。

#### 查看抽样分布（无第三方依赖）

运行完 `run_scan.py` 后，可用标准库快速浏览抽样的参数分布，例如统计各工质/储热材料的出现频次：

```bash
python - <<'PY'
import csv
from collections import Counter

with open('scan_results.csv', newline='') as f:
    reader = csv.DictReader(f)
    fluids = Counter()
    hot = Counter()
    cold = Counter()
    for row in reader:
        fluids[row['working_fluid']] += 1
        hot[row['hot_storage']] += 1
        cold[row['cold_storage']] += 1

print('工质分布:', fluids)
print('储热材料分布:', hot)
print('储冷材料分布:', cold)
PY
```

上述命令仅依赖标准库，便于验证抽样是否覆盖预期组合；也可用同样方法对 `scan_results_with_pareto.csv` 做筛选统计。

### 5. 运行零维动态调峰示例

```bash
python ptes_final/scripts/run_dynamic_demo.py
```

输出：

- `dynamic_demo.csv`：时间序列的 SOC、功率、热/冷储能状态。
- 若安装 matplotlib：`dynamic_soc.png/.pdf` 展示 SOC 轨迹。

### 6. 自定义/二次开发提示

- 想快速查看模块接口，可打开各文件顶部中文注释/文档串。
- 若要集成到 GUI 或优化：
  - 调用 `core.simulate_design_point_generic` 进行单点评估。
  - 使用 `analysis_tools.scan_combinations` 生成训练数据，再通过代理模型实现秒级预测。
  - 用 `dynamics.PTESDynamicSimulator` 作为强化学习或 MPC 环境的核心能量平衡模块。
- 默认所有脚本无依赖，可在任何无网环境运行；若需绘图，只需额外 `pip install matplotlib`。
