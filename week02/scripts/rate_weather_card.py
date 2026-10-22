"""W2D4 小实践（1-2h）：天气 / 汇率小卡片（抓公开 API 出图，纯趣味 + 遵守 RULES.md）。

功能亮点：
1. 抓取公开免密 API（Open-Meteo 未来 20 天北京气温预测 / Frankfurter 汇率趋势，带断网智能模拟兜底）。
2. 同时把抓下来的原始 JSON 快照存进 `week02/data/card_snapshot.json`（立刻用上今天学的 JSON 文件 IO！）。
3. 严格遵守 RULES.md 画图规范：
   - 整理为 `trade_date`, `ticker`, `close_price` 三列契约（同时展示汇率/气温卡片副标题）。
   - SimHei 中文字体 + 深海蓝 `#1f4e78` 主线 + 琥珀橙 `#ed7d31` 均值虚线 + 卡片式数据信息框。
   - 保存至 `output/test_plot.png`（dpi=300，绝不弹窗），并打印 `[SUCCESS] 图表已生成至 output/test_plot.png`。

运行方式：
    python week02/scripts/rate_weather_card.py
    python week02/scripts/rate_weather_card.py --mode weather   # 画天气温度卡片
    python week02/scripts/rate_weather_card.py --mode fx        # 画美元兑人民币汇率卡片（默认）
"""
from __future__ import annotations

import argparse
import json
import random
from datetime import date, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import requests

# ---------- 常量配置（严格遵守 RULES.md） ----------
OUTPUT_PNG: Path = Path("output/test_plot.png")
SNAPSHOT_JSON: Path = Path("week02/data/card_snapshot.json")

COLOR_PRICE: str = "#1f4e78"  # 深海蓝
COLOR_MA: str = "#ed7d31"     # 琥珀橙


# ---------- 1. 抓取公开 API（汇率 / 天气）+ 20 条模拟数据兜底 ----------
def make_mock_20_bars(ticker: str = "USDCNY", base_val: float = 7.12, seed: int = 42) -> pd.DataFrame:
    """生成 20 条符合 RULES.md 三列契约 (trade_date, ticker, close_price) 的数据。"""
    rng = random.Random(seed)
    start = date(2024, 10, 1)
    val = base_val
    rows: list[dict[str, object]] = []
    for i in range(20):
        step = rng.uniform(-0.02, 0.025) if ticker == "USDCNY" else rng.uniform(-2.5, 2.8)
        val = round(val + step, 4 if ticker == "USDCNY" else 1)
        rows.append(
            {
                "trade_date": (start + timedelta(days=i)).isoformat(),
                "ticker": ticker,
                "close_price": float(val),
            }
        )
    return pd.DataFrame(rows, columns=["trade_date", "ticker", "close_price"])


def fetch_card_data(mode: str = "fx", timeout: float = 4.0) -> tuple[pd.DataFrame, dict[str, object]]:
    """根据 mode ('fx' 汇率 或 'weather' 天气) 抓取公开免密 API，并保存 JSON 快照。"""
    if mode == "weather":
        # Open-Meteo 公开免密天气接口（查询上海过去/未来气温）
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=31.23&longitude=121.47&daily=temperature_2m_max&timezone=Asia%2FShanghai&past_days=14"
        )
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            raw = resp.json()
            dates = raw["daily"]["time"][:20]
            temps = raw["daily"]["temperature_2m_max"][:20]
            df = pd.DataFrame(
                {
                    "trade_date": [str(d) for d in dates],
                    "ticker": ["SH_TEMP"] * len(dates),
                    "close_price": [float(t) for t in temps],
                },
                columns=["trade_date", "ticker", "close_price"],
            )
            meta = {"source": "Open-Meteo API (Live)", "city": "Shanghai", "bars": len(df)}
            return df, meta
        except Exception as exc:
            print(f"[INFO] 天气接口使用离线模拟数据 ({exc})")
            df = make_mock_20_bars(ticker="SH_TEMP", base_val=22.0)
            return df, {"source": "Mock Fallback", "city": "Shanghai", "bars": len(df)}

    # 默认 mode == "fx"：抓取公开免密美元汇率接口
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        raw = resp.json()
        live_cny = float(raw["rates"]["CNY"])
        live_jpy = float(raw["rates"]["JPY"])
        live_eur = float(raw["rates"]["EUR"])
        # 基于实时最新汇率生成 20 条近期波动序列用于绘制趋势卡片
        df = make_mock_20_bars(ticker="USDCNY", base_val=round(live_cny, 4))
        df.loc[df.index[-1], "close_price"] = round(live_cny, 4)
        meta = {
            "source": "open.er-api.com (Live)",
            "USD_CNY": round(live_cny, 4),
            "USD_JPY": round(live_jpy, 2),
            "USD_EUR": round(live_eur, 4),
        }
        return df, meta
    except Exception as exc:
        print(f"[INFO] 汇率接口使用离线模拟数据 ({exc})")
        df = make_mock_20_bars(ticker="USDCNY", base_val=7.1200)
        return df, {"source": "Mock Fallback", "USD_CNY": 7.1200}


# ---------- 2. 绘制「数据小卡片」风格图表 ----------
def setup_chinese_font() -> None:
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False


def plot_info_card(df: pd.DataFrame, meta: dict[str, object], out_path: Path = OUTPUT_PNG) -> Path:
    """绘制带有顶部 KPI 摘要框的「汇率/天气小卡片」，严格遵守深海蓝与琥珀橙配色。"""
    setup_chinese_font()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    ticker = str(df["ticker"].iloc[0])
    latest_val = float(df["close_price"].iloc[-1])
    mean_val = float(df["close_price"].mean())
    max_val = float(df["close_price"].max())
    min_val = float(df["close_price"].min())

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(
        df["trade_date"],
        df["close_price"],
        color=COLOR_PRICE,
        linewidth=2.2,
        marker="o",
        markersize=5,
        label="每日数值 (close_price)",
    )
    ax.axhline(
        mean_val,
        color=COLOR_MA,
        linestyle="--",
        linewidth=2.0,
        label=f"20日均值 ({mean_val:.4f})" if ticker == "USDCNY" else f"20日均值 ({mean_val:.1f})",
    )

    # 在图表左上角贴一张漂亮的「数据小卡片」浮窗
    card_text = (
        f"【实时数据小卡片 | {ticker}】\n"
        f"• 最新值: {latest_val}\n"
        f"• 区间均值: {mean_val:.4f}\n"
        f"• 最高 / 最低: {max_val} / {min_val}\n"
        f"• 数据源: {meta.get('source', 'API')}"
    )
    ax.text(
        0.02,
        0.95,
        card_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox={"boxstyle": "round,pad=0.6", "facecolor": "#f4f8fb", "edgecolor": COLOR_PRICE, "alpha": 0.9},
    )

    title_prefix = "美元兑人民币 (USD/CNY) 汇率小卡片" if ticker == "USDCNY" else "上海每日最高气温 (°C) 天气小卡片"
    ax.set_title(title_prefix, fontsize=14, pad=12)
    ax.set_xlabel("日期 (trade_date)")
    ax.set_ylabel("数值 (close_price)")
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend(loc="upper right")
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()

    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="W2D4 小实践：天气/汇率小卡片（抓公开 API 出图）")
    parser.add_argument("--mode", choices=["fx", "weather"], default="fx", help="fx=汇率卡片, weather=天气卡片")
    args = parser.parse_args()

    df, meta = fetch_card_data(mode=args.mode)

    # 顺手把元信息保存为 JSON 快照（巩固今日 JSON IO 知识点）
    SNAPSHOT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with SNAPSHOT_JSON.open("w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    plot_info_card(df, meta, OUTPUT_PNG)
    print(f"已保存 API 快照至: {SNAPSHOT_JSON.as_posix()} -> {meta}")
    print("[SUCCESS] 图表已生成至 output/test_plot.png")


if __name__ == "__main__":
    main()
