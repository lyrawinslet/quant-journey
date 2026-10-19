"""W2D1 实战（2h）：AkShare 抓 1 只股票日线 + matplotlib 画收盘价（解决中文字体坑）。

严格遵守仓库 RULES.md 硬约束：
1. 路径铁律：全部使用 pathlib.Path，严禁反斜杠。
2. 数据契约：整理后的 DataFrame 包含且仅包含三列：`trade_date`, `ticker`, `close_price`。
3. 画图验收标准：
   - 显式设置中文字体 `SimHei`，并配置 `axes.unicode_minus = False`。
   - 折线图主色深海蓝 `#1f4e78`，均值线琥珀橙 `#ed7d31`（虚线）。
   - 严禁调用 `plt.show()`，直接保存至 `output/test_plot.png`，`dpi=300`。
4. 代码风格：带 Type Hints，支持在 `if __name__ == "__main__":` 中生成 20 条模拟数据兜底或抓取 AkShare 真实日线跑通全流程，最后打印 `[SUCCESS] 图表已生成至 output/test_plot.png`。

运行方式：
    python week02/scripts/akshare_plot.py                   # 默认抓取 600519 真实日线（若断网自动回退 20 条模拟数据）
    python week02/scripts/akshare_plot.py --mock            # 强制使用 20 条模拟数据跑通全流程
    python week02/scripts/akshare_plot.py --ticker 000001   # 指定抓取其他 A 股代码
"""
from __future__ import annotations

import argparse
import random
from datetime import date, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 严禁弹窗阻塞

import matplotlib.pyplot as plt
import pandas as pd

# ---------- 常量配置 ----------
DEFAULT_TICKER: str = "600519"
START_DATE: str = "20240101"
END_DATE: str = "20241231"
N_MOCK_BARS: int = 20

COLOR_PRICE: str = "#1f4e78"  # 深海蓝
COLOR_MA: str = "#ed7d31"     # 琥珀橙

# 当前运行目录下的 output/test_plot.png
OUTPUT_PNG: Path = Path("output/test_plot.png")


# ---------- 数据获取：模拟数据 & AkShare 真实日线 ----------
def make_mock_data(n: int = N_MOCK_BARS, ticker: str = DEFAULT_TICKER, seed: int = 42) -> pd.DataFrame:
    """生成 n 条模拟数据，严格包含且仅包含三列：trade_date, ticker, close_price。"""
    rng = random.Random(seed)
    start = date(2024, 1, 2)
    price = 100.0
    rows: list[dict[str, object]] = []
    for i in range(n):
        price = round(price * (1 + rng.uniform(-0.03, 0.03)), 2)
        rows.append(
            {
                "trade_date": (start + timedelta(days=i)).isoformat(),
                "ticker": ticker,
                "close_price": float(price),
            }
        )
    return pd.DataFrame(rows, columns=["trade_date", "ticker", "close_price"])


def fetch_akshare_daily(
    ticker: str = DEFAULT_TICKER,
    start_date: str = START_DATE,
    end_date: str = END_DATE,
) -> pd.DataFrame:
    """使用 AkShare 抓取 1 只 A 股日线（前复权），并清洗为契约三列：
    trade_date (str), ticker (str), close_price (float)。
    """
    import akshare as ak  # 延迟导入，方便无网时用 --mock 测试

    raw_df = ak.stock_zh_a_hist(
        symbol=ticker,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust="qfq",
    )
    if raw_df is None or raw_df.empty:
        raise ValueError(f"AkShare 返回空数据: ticker={ticker}")

    # AkShare stock_zh_a_hist 返回列包含：'日期', '收盘' 等
    df = pd.DataFrame(
        {
            "trade_date": raw_df["日期"].astype(str),
            "ticker": ticker,
            "close_price": raw_df["收盘"].astype(float),
        },
        columns=["trade_date", "ticker", "close_price"],
    )
    return df


# ---------- 画图逻辑（解决中文字体坑） ----------
def setup_chinese_font() -> None:
    """解决 matplotlib 中文方块乱码与负号显示问题。"""
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False


def plot_close_price(df: pd.DataFrame, out_path: Path = OUTPUT_PNG) -> Path:
    """绘制收盘价折线图（深海蓝 #1f4e78）与均值线（琥珀橙 #ed7d31 虚线），保存至 output/test_plot.png。"""
    setup_chinese_font()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    ticker = str(df["ticker"].iloc[0]) if not df.empty else DEFAULT_TICKER
    mean_price = float(df["close_price"].mean())

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        df["trade_date"],
        df["close_price"],
        color=COLOR_PRICE,
        linewidth=1.8,
        label="收盘价",
    )
    ax.axhline(
        mean_price,
        color=COLOR_MA,
        linestyle="--",
        linewidth=1.8,
        label=f"区间均值 ({mean_price:.2f})",
    )

    # 控制 X 轴刻度密度，避免日线太多时日期重叠成黑块
    total_bars = len(df)
    if total_bars > 20:
        step = max(1, total_bars // 10)
        ax.set_xticks(range(0, total_bars, step))
        ax.set_xticklabels(df["trade_date"].iloc[::step], rotation=45)
    else:
        fig.autofmt_xdate(rotation=45)

    ax.set_title(f"{ticker} 日线收盘价走势（共 {total_bars} 个交易日）", fontsize=14)
    ax.set_xlabel("交易日期 (trade_date)")
    ax.set_ylabel("收盘价 (close_price)")
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend()
    fig.tight_layout()

    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    return out_path


# ---------- 主流程 ----------
def main() -> None:
    parser = argparse.ArgumentParser(description="AkShare 抓 1 只股票日线 + matplotlib 画收盘价")
    parser.add_argument("--ticker", default=DEFAULT_TICKER, help="股票代码，默认 600519")
    parser.add_argument("--start", default=START_DATE, help="起始日期 YYYYMMDD，默认 20240101")
    parser.add_argument("--end", default=END_DATE, help="结束日期 YYYYMMDD，默认 20241231")
    parser.add_argument("--mock", action="store_true", help="使用 20 条模拟数据代替联网抓取")
    args = parser.parse_args()

    if args.mock:
        df = make_mock_data(n=N_MOCK_BARS, ticker=args.ticker)
    else:
        try:
            df = fetch_akshare_daily(ticker=args.ticker, start_date=args.start, end_date=args.end)
        except Exception as exc:
            print(f"[WARN] AkShare 抓取失败 ({exc})，自动回退至 20 条模拟数据...")
            df = make_mock_data(n=N_MOCK_BARS, ticker=args.ticker)

    print(df.head())
    plot_close_price(df, OUTPUT_PNG)
    print("[SUCCESS] 图表已生成至 output/test_plot.png")


if __name__ == "__main__":
    main()
