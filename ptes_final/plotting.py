"""PTES 绘图小工具：Pareto、敏感性、理想气体 T-s 图。

Matplotlib 不是硬依赖；若未安装会打印提示并直接返回 None。
"""
from __future__ import annotations


def _col(df, key):
    return [row[key] for row in df.rows]


def scatter_pareto(df, x: str, y: str, c: str | None = None, output: str | None = None):
    try:
        import matplotlib.pyplot as plt
    except ImportError:  # pragma: no cover
        print("matplotlib not installed; skipping scatter plot")
        return None, None

    xvals = _col(df, x)
    yvals = _col(df, y)
    cvals = _col(df, c) if c else None

    fig, ax = plt.subplots(figsize=(6, 4))
    scatter = ax.scatter(xvals, yvals, c=cvals, cmap="viridis", alpha=0.8)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    if c:
        cbar = fig.colorbar(scatter, ax=ax)
        cbar.set_label(c)
    fig.tight_layout()
    if output:
        fig.savefig(output, dpi=200)
    return fig, ax


def bar_sensitivity(df, feature_col: str = "feature", value_col: str = "rho", output: str | None = None):
    try:
        import matplotlib.pyplot as plt
    except ImportError:  # pragma: no cover
        print("matplotlib not installed; skipping bar plot")
        return None, None

    order = sorted(df.rows, key=lambda r: r[value_col], reverse=True)
    features = [r[feature_col] for r in order]
    values = [r[value_col] for r in order]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(features, values)
    ax.set_ylabel(value_col)
    ax.set_xticklabels(features, rotation=45, ha="right")
    fig.tight_layout()
    if output:
        fig.savefig(output, dpi=200)
    return fig, ax


def ts_diagram_ideal_gas(s, T, output: str | None = None):
    try:
        import matplotlib.pyplot as plt
    except ImportError:  # pragma: no cover
        print("matplotlib not installed; skipping T-s diagram")
        return None, None

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(s, T, marker="o")
    ax.set_xlabel("s (kJ/kg-K)")
    ax.set_ylabel("T (K)")
    ax.set_title("Ideal-gas T-s diagram (surrogate)")
    fig.tight_layout()
    if output:
        fig.savefig(output, dpi=200)
    return fig, ax
