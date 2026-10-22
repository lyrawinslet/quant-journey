"""W2D4 技术（2.5h）：文件 IO（csv / json / pathlib）—— 封装数据落地与读取模块。

为什么量化需要「数据落地（持久化）」？
每次从 AkShare 或网络接口抓数据都很慢，还容易被封 IP。
标准做法是：第一次抓下来后，立刻存成本地的 CSV（存表格行情）或 JSON（存配置/股票元信息），
以后跑回测直接从本地硬盘秒读！

严格遵守 RULES.md：
1. 全部使用 pathlib.Path 处理路径，严禁反斜杠 `\\`。
2. 行情表格严格遵守三列契约：`trade_date`, `ticker`, `close_price`。

运行方式：
    python week02/scripts/storage_io.py --self-test
    python week02/scripts/storage_io.py
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import pandas as pd

# ---------- 1. 用 pathlib.Path 定义标准路径 ----------
DATA_DIR: Path = Path("week02/data")
DEFAULT_CSV_PATH: Path = DATA_DIR / "quotes_600519.csv"
DEFAULT_JSON_PATH: Path = DATA_DIR / "stock_meta.json"


# ============================================================
# 2. CSV 读写封装（标准库 csv.DictWriter / csv.DictReader 与 pandas 互操作）
# ============================================================
def save_quotes_to_csv(rows: list[dict[str, object]], csv_path: Path = DEFAULT_CSV_PATH) -> Path:
    """将符合三列契约 (trade_date, ticker, close_price) 的字典列表写入 CSV 文件。

    关键细节：
    - `csv_path.parent.mkdir(parents=True, exist_ok=True)`：如果文件夹不存在，自动创建！
    - `newline=""`：Windows 下写 CSV 必加，否则每写一行会多出一个空行！
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["trade_date", "ticker", "close_price"]

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # 写入表头：trade_date,ticker,close_price
        writer.writerows(rows)

    return csv_path


def load_quotes_from_csv(csv_path: Path = DEFAULT_CSV_PATH) -> list[dict[str, object]]:
    """使用标准库 csv.DictReader 从本地 CSV 读取行情，并把 close_price 转回 float。"""
    if not csv_path.is_file():
        raise FileNotFoundError(f"找不到 CSV 文件: {csv_path}")

    result: list[dict[str, object]] = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            result.append(
                {
                    "trade_date": str(row["trade_date"]),
                    "ticker": str(row["ticker"]),
                    "close_price": float(row["close_price"]),
                }
            )
    return result


# ============================================================
# 3. JSON 读写封装（用于保存策略参数、股票池配置、接口返回快照）
# ============================================================
def save_meta_to_json(meta: dict[str, object], json_path: Path = DEFAULT_JSON_PATH) -> Path:
    """将字典保存为排版整齐的 JSON 文件。

    关键细节：
    - `ensure_ascii=False`：必加！否则中文字符（如“贵州茅台”）会变成 `\\u8d35\\u5dde...` 乱码！
    - `indent=2`：自动缩进 2 个空格，人类打开文件也能轻松阅读。
    """
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return json_path


def load_meta_from_json(json_path: Path = DEFAULT_JSON_PATH) -> dict[str, object]:
    """从本地 JSON 文件读取字典。"""
    if not json_path.is_file():
        raise FileNotFoundError(f"找不到 JSON 文件: {json_path}")

    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# 4. 结合真实 CSV 巩固 pandas 基本功能（reindex / drop / 对齐 / apply / 排序排名）
# ============================================================
def analyze_saved_csv(csv_path: Path = DEFAULT_CSV_PATH) -> pd.DataFrame:
    """直接用 pd.read_csv 读取刚才落地的 CSV，并计算价格排名与强弱标签。"""
    df = pd.read_csv(csv_path)
    mean_p = float(df["close_price"].mean())
    df["status"] = df["close_price"].apply(lambda p: "高于均值" if p >= mean_p else "低于均值")
    df["price_rank"] = df["close_price"].rank(ascending=False, method="min").astype(int)
    return df.sort_values(by="close_price", ascending=False)


def self_test() -> None:
    sample_rows: list[dict[str, object]] = [
        {"trade_date": "2024-01-02", "ticker": "600519", "close_price": 1500.0},
        {"trade_date": "2024-01-03", "ticker": "600519", "close_price": 1525.5},
        {"trade_date": "2024-01-04", "ticker": "600519", "close_price": 1510.0},
    ]
    saved_csv = save_quotes_to_csv(sample_rows)
    loaded_rows = load_quotes_from_csv(saved_csv)
    assert len(loaded_rows) == 3 and loaded_rows[1]["close_price"] == 1525.5

    sample_meta: dict[str, object] = {
        "ticker": "600519",
        "name": "贵州茅台",
        "lot_size": 100,
        "commission_rate": 0.0003,
    }
    saved_json = save_meta_to_json(sample_meta)
    loaded_meta = load_meta_from_json(saved_json)
    assert loaded_meta["name"] == "贵州茅台" and loaded_meta["lot_size"] == 100

    ranked_df = analyze_saved_csv(saved_csv)
    assert ranked_df.iloc[0]["close_price"] == 1525.5
    assert ranked_df.iloc[0]["price_rank"] == 1

    print("✅ [W2D4 技术+数理自检] pathlib / CSV 读写 / JSON 读写 / CSV 排序排名 全部通过！")


def main() -> None:
    parser = argparse.ArgumentParser(description="W2D4 文件 IO：csv / json / pathlib 数据落地与读取模块")
    parser.add_argument("--self-test", action="store_true", help="运行自检断言")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    # 1. 造 5 条行情数据并落地到 CSV
    rows: list[dict[str, object]] = [
        {"trade_date": f"2024-01-0{i}", "ticker": "600519", "close_price": float(1500 + i * 12 * (-1) ** i)}
        for i in range(1, 6)
    ]
    csv_file = save_quotes_to_csv(rows)
    print(f"1. [CSV 落地] 已写入 {csv_file.as_posix()}，读回第 1 条: {load_quotes_from_csv(csv_file)[0]}")

    # 2. 保存策略配置到 JSON
    meta = {"strategy": "MA5_Cross", "ticker": "600519", "name": "贵州茅台", "initial_cash": 100000}
    json_file = save_meta_to_json(meta)
    print(f"2. [JSON 落地] 已写入 {json_file.as_posix()}，读回内容: {load_meta_from_json(json_file)}")

    # 3. 用 pandas 读取 CSV 做排序与排名分析
    print("\n3. [pandas 读取 CSV 并按收盘价降序排名]：")
    print(analyze_saved_csv(csv_file).to_string(index=False))


if __name__ == "__main__":
    main()
