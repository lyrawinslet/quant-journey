"""W2D2 技术 + 实战：异常处理 (try/except) + logging 日志 + argparse + 保存图表至 assets/。

核心目标：
1. 让命令行工具 (CLI) 不再打满屏吓人的红字 Traceback，而是用 logging 输出带时间戳的清晰日志与友好报错。
2. 支持把画好的收盘价走势图同时保存到 RULES.md 要求的 `output/test_plot.png` 以及仓库门面 `assets/maotai_close.png`，方便嵌进 README.md！

运行示例：
    python week02/scripts/cli_logging.py --self-test
    python week02/scripts/cli_logging.py --ticker 600519 --days 20
    python week02/scripts/cli_logging.py --ticker INVALID_CODE   # 体验友好报错！
"""
from __future__ import annotations

import argparse
import logging
import random
import shutil
from datetime import date, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

# ---------- 1. 配置 logging 日志 ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("quant_cli")

# ---------- 常量 ----------
COLOR_PRICE: str = "#1f4e78"  # 深海蓝
COLOR_MA: str = "#ed7d31"     # 琥珀橙
OUTPUT_PNG: Path = Path("output/test_plot.png")
ASSETS_PNG: Path = Path("assets/maotai_close.png")


# ---------- 2. 参数校验与异常处理 ----------
def validate_ticker(ticker: str) -> str:
    """校验 A 股股票代码是否合法（必须是 6 位纯数字）。
    如果不合法，主动抛出 ValueError 异常。
    """
    cleaned = ticker.strip()
    if len(cleaned) != 6 or not cleaned.isdigit():
        raise ValueError(f"股票代码 '{ticker}' 格式错误！A 股代码必须是 6 位纯数字（如 600519 或 000001）。")
    return cleaned


def make_mock_data(ticker: str = "600519", n: int = 20, seed: int = 42) -> pd.DataFrame:
    """生成 n 条符合 RULES.md 三列契约 (trade_date, ticker, close_price) 的模拟日线。"""
    if n <= 0:
        raise ValueError(f"交易日天数 days 必须大于 0（当前传入: {n}）")

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


# ---------- 3. 画图并同步到 assets/ ----------
def setup_chinese_font() -> None:
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False


def plot_and_export(
    df: pd.DataFrame,
    out_path: Path = OUTPUT_PNG,
    assets_path: Path = ASSETS_PNG,
) -> Path:
    """画收盘价与均值线，保存至 output/test_plot.png，并复制一份到 assets/ 供 README 展示。"""
    setup_chinese_font()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    assets_path.parent.mkdir(parents=True, exist_ok=True)

    ticker = str(df["ticker"].iloc[0])
    mean_price = float(df["close_price"].mean())

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        df["trade_date"],
        df["close_price"],
        color=COLOR_PRICE,
        linewidth=1.8,
        marker="o",
        markersize=4,
        label="收盘价",
    )
    ax.axhline(
        mean_price,
        color=COLOR_MA,
        linestyle="--",
        linewidth=1.8,
        label=f"均值线 ({mean_price:.2f})",
    )

    ax.set_title(f"{ticker} 收盘价走势与均值线", fontsize=14)
    ax.set_xlabel("交易日期 (trade_date)")
    ax.set_ylabel("收盘价 (close_price)")
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend()
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()

    fig.savefig(out_path, dpi=300)
    plt.close(fig)

    # 复制一份到 assets/ 目录，方便嵌进 README.md
    shutil.copyfile(out_path, assets_path)
    return out_path


# ---------- 4. 自检与 CLI 主入口 ----------
def self_test() -> None:
    # 正常代码应通过校验
    assert validate_ticker("600519") == "600519"

    # 错误代码应触发 ValueError
    caught = False
    try:
        validate_ticker("ABC")
    except ValueError:
        caught = True
    assert caught, "传入非法股票代码时应当抛出 ValueError"

    df = make_mock_data("600519", n=20)
    assert len(df) == 20
    logger.info("✅ [W2D2 技术自检] 异常处理 + logging + 参数校验全部通过！")


def main() -> None:
    parser = argparse.ArgumentParser(description="W2D2：带 logging 与友好异常处理的股票画图 CLI")
    parser.add_argument("--ticker", default="600519", help="6 位 A 股代码，默认 600519")
    parser.add_argument("--days", type=int, default=20, help="生成数据天数，默认 20")
    parser.add_argument("--self-test", action="store_true", help="运行自检")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    # 使用 try...except 捕获异常，输出友好日志而不是崩溃堆栈
    try:
        logger.info("开始校验参数: ticker=%s, days=%s", args.ticker, args.days)
        valid_code = validate_ticker(args.ticker)

        logger.info("正在生成 %s 的 %d 条行情数据...", valid_code, args.days)
        df = make_mock_data(ticker=valid_code, n=args.days)

        logger.info("正在绘制图表并导出至 %s 和 %s ...", OUTPUT_PNG, ASSETS_PNG)
        plot_and_export(df, OUTPUT_PNG, ASSETS_PNG)

        logger.info("图表导出成功！现在可以在 README.md 中嵌入 assets/maotai_close.png 了。")
        print("[SUCCESS] 图表已生成至 output/test_plot.png")

    except ValueError as err:
        # 友好报错：只打印清晰的错误原因，不打印吓人的满屏 Traceback
        logger.error("❌ 参数有误，程序已安全中止：%s", err)
    except Exception as exc:
        logger.error("❌ 发生未预期的运行错误：%s", exc)


if __name__ == "__main__":
    main()
