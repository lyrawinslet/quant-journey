"""按 RULES.md 写的最小可跑脚本：生成 20 条模拟数据 -> 算 5 日均线 -> 存图。

运行（在本文件所在目录）：
    python test_ma.py

输出：
    output/test_plot.png   （dpi=300，不弹窗）
"""
from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 无界面后端：绝不弹窗阻塞

import matplotlib.pyplot as plt
import pandas as pd

# ---------- 常量 ----------

N_BARS: int = 20                      # 模拟数据条数
MA_WINDOW: int = 5                    # 均线窗口：5 日
TICKER: str = "600519"                # 标的名，放进 ticker 列
START_DATE: str = "2024-01-02"        # 第一根 K 线日期
START_PRICE: float = 100.0            # 起始收盘价
RANDOM_SEED: int = 42                 # 固定种子，结果可复现

BASE_DIR: Path = Path(__file__).resolve().parent
OUTPUT_DIR: Path = BASE_DIR / "output"
OUTPUT_PNG: Path = OUTPUT_DIR / "test_plot.png"

COLOR_PRICE: str = "#1f4e78"          # 深海蓝：收盘价折线
COLOR_MA: str = "#ed7d31"             # 琥珀橙：均值线（虚线）


# ---------- 数据 ----------

def make_mock_data(n: int = N_BARS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """生成 n 条模拟数据，固定三列：trade_date / ticker / close_price。"""
    rng = random.Random(seed)
    start = date.fromisoformat(START_DATE)

    rows: list[dict[str, object]] = []
    price = START_PRICE
    for i in range(n):
        price = round(price * (1 + rng.uniform(-0.03, 0.03)), 2)
        rows.append(
            {
                "trade_date": (start + timedelta(days=i)).isoformat(),
                "ticker": TICKER,
                "close_price": price,
            }
        )
    return pd.DataFrame(rows, columns=["trade_date", "ticker", "close_price"])


def add_ma(df: pd.DataFrame, window: int = MA_WINDOW) -> pd.DataFrame:
    """加一列 ma5：close_price 的 window 日简单移动平均（前 window-1 行为 NaN）。"""
    out = df.copy()
    out["ma5"] = out["close_price"].rolling(window=window).mean()
    return out


# ---------- 画图 ----------

def setup_chinese_font() -> None:
    """中文字体 SimHei + 负号正常显示。"""
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False


def plot_ma(df: pd.DataFrame, out_path: Path = OUTPUT_PNG) -> Path:
    """画收盘价 + 5 日均线，保存到 out_path（dpi=300）。返回文件路径。"""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        df["trade_date"], df["close_price"],
        color=COLOR_PRICE, linewidth=1.8, marker="o", markersize=4, label="收盘价",
    )
    ax.plot(
        df["trade_date"], df["ma5"],
        color=COLOR_MA, linewidth=2.0, linestyle="--", label=f"{MA_WINDOW} 日均线",
    )

    ax.set_title(f"{TICKER} 收盘价与 {MA_WINDOW} 日均线", fontsize=14)
    ax.set_xlabel("交易日期")
    ax.set_ylabel("价格")
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend()
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()

    fig.savefig(out_path, dpi=300)
    plt.close(fig)  # 关掉画布，绝不 plt.show()
    return out_path


# ---------- 主流程 ----------

def main() -> None:
    setup_chinese_font()

    df = add_ma(make_mock_data())
    print(df.to_string(index=False))

    saved = plot_ma(df)
    assert saved.is_file(), f"图表没有落盘：{saved}"
    print("[SUCCESS] 图表已生成至 output/test_plot.png")


if __name__ == "__main__":
    main()
