"""W2D3 技术 + 数理 + 实战三合一练习脚本：
1. 技术：使用 requests 抓取公开免密 API（汇率 / 天气接口，带断网超时保护）。
2. 数理：pandas 第 5 章核心基本功能 —— reindex / drop / 算术对齐 / apply / 排序排名（自动读写 CSV）。
3. 实战：同一份股票数据，用 matplotlib（静态高清图）与 plotly（可鼠标悬停缩放的交互式网页图）各画一次！

运行方式：
    python week02/scripts/w2d3_practice.py --self-test
    python week02/scripts/w2d3_practice.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import requests

# ---------- 路径与颜色常量（严格遵守 RULES.md） ----------
CSV_PATH: Path = Path("week02/sample_quotes.csv")
OUTPUT_PNG: Path = Path("output/test_plot.png")
PLOTLY_HTML: Path = Path("output/interactive_plot.html")

COLOR_PRICE: str = "#1f4e78"  # 深海蓝
COLOR_MA: str = "#ed7d31"     # 琥珀橙


# ============================================================
# 1. 技术（2.5h）：requests 抓取公开免密接口（汇率查询）
# ============================================================
def fetch_usd_cny_rate(timeout: float = 5.0) -> float:
    """使用 requests 调用公开免密汇率接口，获取 1 美元兑人民币 (USD/CNY) 汇率。
    若网络超时或受限，返回保底参考汇率 7.12。
    """
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()  # 如果状态码不是 200（如 404/500），自动抛出异常
        data = resp.json()
        rate = float(data["rates"]["CNY"])
        return round(rate, 4)
    except Exception as exc:
        print(f"[WARN] 实时汇率接口请求受限 ({exc})，使用离线参考汇率 7.1200")
        return 7.1200


# ============================================================
# 2. 数理（1.5h）：reindex / drop / 算术对齐 / apply / 排序排名（用真实 CSV 练）
# ============================================================
def prepare_sample_csv(csv_path: Path = CSV_PATH) -> pd.DataFrame:
    """生成一份符合 RULES.md 三列契约 (trade_date, ticker, close_price) 的 20 条 CSV 数据并读取。"""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {"trade_date": f"2024-01-{i + 1:02d}", "ticker": "600519", "close_price": float(1500 + (i * 7) % 45 - 15)}
        for i in range(20)
    ]
    df = pd.DataFrame(rows, columns=["trade_date", "ticker", "close_price"])
    df.to_csv(csv_path, index=False, encoding="utf-8")
    return pd.read_csv(csv_path)


def practice_pandas_ops(df: pd.DataFrame) -> dict[str, object]:
    """演练 pandas 5 大核心基本功能：reindex / drop / 算术对齐 / apply / 排序排名。"""
    indexed = df.set_index("trade_date")

    # 1) reindex：按新日期列表重新索引，缺失的周日 "2024-01-99" 用 fill_value=0.0 填充
    reindexed = indexed.reindex(["2024-01-01", "2024-01-02", "2024-01-99"], fill_value=0.0)

    # 2) drop：删掉第一天 "2024-01-01" 这一行
    dropped = indexed.drop("2024-01-01", axis=0)

    # 3) 算术对齐：两个不同索引的 Series 相加，没有对齐的位置用 fill_value=0 补齐
    s1 = pd.Series([100.0, 200.0], index=["600519", "000001"])
    s2 = pd.Series([50.0, 300.0], index=["600519", "300750"])
    aligned_sum = s1.add(s2, fill_value=0.0)

    # 4) apply：对 close_price 每一行应用自定义函数（>= 1510 标为 "强势"，否则标为 "震荡"）
    labels = indexed["close_price"].apply(lambda p: "强势" if p >= 1510.0 else "震荡")

    # 5) 排序与排名：sort_values 按收盘价从高到低降序排列；rank 计算价格排名
    sorted_df = indexed.sort_values(by="close_price", ascending=False)
    ranks = indexed["close_price"].rank(ascending=False, method="min")

    return {
        "reindexed_missing_val": float(reindexed.loc["2024-01-99", "close_price"]),
        "dropped_len": len(dropped),
        "aligned_600519": float(aligned_sum.loc["600519"]),
        "aligned_300750": float(aligned_sum.loc["300750"]),
        "strong_count": int((labels == "强势").sum()),
        "highest_price": float(sorted_df["close_price"].iloc[0]),
        "top_rank": float(ranks.min()),
    }


# ============================================================
# 3. 实战（2h）：同一张图用 matplotlib 与 plotly 各画一次，对比体验
# ============================================================
def plot_both_matplotlib_and_plotly(
    df: pd.DataFrame,
    png_path: Path = OUTPUT_PNG,
    html_path: Path = PLOTLY_HTML,
) -> tuple[Path, Path]:
    """用 matplotlib 生成静态图 output/test_plot.png，并用 plotly 生成交互式网页图 output/interactive_plot.html。"""
    png_path.parent.mkdir(parents=True, exist_ok=True)
    mean_price = float(df["close_price"].mean())
    ticker = str(df["ticker"].iloc[0])

    # --- A. matplotlib 静态图（严格遵守 RULES.md） ---
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["trade_date"], df["close_price"], color=COLOR_PRICE, linewidth=1.8, marker="o", label="收盘价")
    ax.axhline(mean_price, color=COLOR_MA, linestyle="--", linewidth=1.8, label=f"均值线 ({mean_price:.2f})")
    ax.set_title(f"{ticker} 收盘价走势 (Matplotlib 静态图)", fontsize=14)
    ax.set_xlabel("交易日期")
    ax.set_ylabel("收盘价")
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend()
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig(png_path, dpi=300)
    plt.close(fig)

    # --- B. Plotly 交互式网页图（可在浏览器打开，鼠标悬停看具体数值、框选放大） ---
    try:
        import plotly.graph_objects as go

        pfig = go.Figure()
        pfig.add_trace(
            go.Scatter(
                x=df["trade_date"],
                y=df["close_price"],
                mode="lines+markers",
                name="收盘价",
                line={"color": COLOR_PRICE, "width": 2},
            )
        )
        pfig.add_hline(
            y=mean_price,
            line_dash="dash",
            line_color=COLOR_MA,
            annotation_text=f"均值线 ({mean_price:.2f})",
        )
        pfig.update_layout(
            title=f"{ticker} 收盘价走势 (Plotly 交互式图 — 鼠标移上去试试！)",
            xaxis_title="交易日期 (trade_date)",
            yaxis_title="收盘价 (close_price)",
            template="plotly_white",
        )
        pfig.write_html(str(html_path))
    except ImportError:
        print("[INFO] 当前环境未安装 plotly，可运行 `pip install plotly` 体验交互式网页图。")

    return png_path, html_path


def self_test() -> None:
    df = prepare_sample_csv()
    assert len(df) == 20 and list(df.columns) == ["trade_date", "ticker", "close_price"]

    res = practice_pandas_ops(df)
    assert res["reindexed_missing_val"] == 0.0
    assert res["dropped_len"] == 19
    assert res["aligned_600519"] == 150.0 and res["aligned_300750"] == 300.0
    assert res["top_rank"] == 1.0
    print("✅ [W2D3 自检] reindex / drop / 算术对齐 / apply / 排序排名 全部通过！")


def main() -> None:
    parser = argparse.ArgumentParser(description="W2D3 综合练习：requests + pandas 进阶 + matplotlib vs plotly")
    parser.add_argument("--self-test", action="store_true", help="运行自检断言")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    print("1. [requests] 正在抓取实时 USD/CNY 汇率...")
    rate = fetch_usd_cny_rate()
    print(f"   当前 1 美元 (USD) ≈ {rate} 人民币 (CNY)")

    print("\n2. [pandas] 生成并读取 CSV，运行 reindex/drop/对齐/apply/排序排名...")
    df = prepare_sample_csv()
    ops_result = practice_pandas_ops(df)
    print("   计算结果:", ops_result)

    print("\n3. [matplotlib vs plotly] 正在生成双版本图表...")
    plot_both_matplotlib_and_plotly(df)
    print("[SUCCESS] 图表已生成至 output/test_plot.png")


if __name__ == "__main__":
    main()
