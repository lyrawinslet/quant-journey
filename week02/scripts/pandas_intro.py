"""W2D1 数理练习（1.5h）：pandas 入门章（第 5 章）
涵盖：Series / DataFrame 创建、索引切片、loc（按标签）与 iloc（按位置）。

运行：
    python week02/scripts/pandas_intro.py
    python week02/scripts/pandas_intro.py --self-test
"""
from __future__ import annotations

import argparse
import pandas as pd


# ============================================================
# 1. Series：带标签的一维数组
# ============================================================
def create_return_series() -> pd.Series:
    """创建一个以交易日为索引（index）、日收益率（%）为值的 Series。"""
    dates = ["2026-10-13", "2026-10-14", "2026-10-15", "2026-10-16", "2026-10-19"]
    returns = [1.2, -0.5, 2.3, -1.1, 0.8]
    # TODO: 用 pd.Series(data, index=...) 创建 Series，name 设为 "daily_return"
    return pd.Series(returns, index=dates, name="daily_return")


# ============================================================
# 2. DataFrame：遵守 RULES.md 数据契约的三列表格
# ============================================================
def create_stock_df() -> pd.DataFrame:
    """创建包含 trade_date / ticker / close_price 三列的 DataFrame，
    并将 trade_date 设为行索引（index）以便练习 loc / iloc。
    """
    data = {
        "trade_date": [
            "2026-10-13",
            "2026-10-14",
            "2026-10-15",
            "2026-10-16",
            "2026-10-19",
        ],
        "ticker": ["600519"] * 5,
        "close_price": [1500.0, 1518.0, 1510.0, 1545.0, 1530.0],
    }
    df = pd.DataFrame(data, columns=["trade_date", "ticker", "close_price"])
    return df


# ============================================================
# 3. 索引切片：loc（标签索引，闭区间） vs iloc（位置索引，左闭右开）
# ============================================================
def practice_loc_iloc(df: pd.DataFrame) -> dict[str, object]:
    """给定原始三列 DataFrame，把 trade_date 设为索引后练习 loc 和 iloc。

    关键区别：
    - df.loc["2026-10-14":"2026-10-16"] -> 按标签切片，**包含**末尾 "2026-10-16"！
    - df.iloc[1:3]                      -> 按整数位置切片，**不包含**末尾索引 3（只取第 1、2 行）！
    """
    indexed = df.set_index("trade_date")

    # 1) 用 loc 取出 "2026-10-15" 这一天的 "close_price" 标量值
    price_on_1015 = float(indexed.loc["2026-10-15", "close_price"])

    # 2) 用 loc 标签切片取出 "2026-10-14" 到 "2026-10-16"（含首尾共 3 行）的 close_price Series
    loc_slice = indexed.loc["2026-10-14":"2026-10-16", "close_price"]

    # 3) 用 iloc 位置索引取出最后一行（位置 -1）的 close_price
    last_price = float(indexed.iloc[-1]["close_price"])

    # 4) 用 iloc 位置切片取出前 3 行（位置 0:3）
    first_three_rows = indexed.iloc[0:3]

    # 5) 布尔索引：筛选出 close_price > 1515.0 的所有行
    high_days = indexed.loc[indexed["close_price"] > 1515.0]

    return {
        "price_on_1015": price_on_1015,
        "loc_slice_len": len(loc_slice),
        "last_price": last_price,
        "first_three_len": len(first_three_rows),
        "high_days_count": len(high_days),
    }


def self_test() -> None:
    s = create_return_series()
    assert isinstance(s, pd.Series) and len(s) == 5
    assert s.loc["2026-10-15"] == 2.3
    assert s.iloc[0] == 1.2

    df = create_stock_df()
    assert list(df.columns) == ["trade_date", "ticker", "close_price"]

    res = practice_loc_iloc(df)
    assert res["price_on_1015"] == 1510.0
    assert res["loc_slice_len"] == 3, "loc 标签切片包含首尾两端，应有 3 行"
    assert res["last_price"] == 1530.0
    assert res["first_three_len"] == 3, "iloc[0:3] 左闭右开，应有 3 行"
    assert res["high_days_count"] == 3, "大于 1515.0 的交易日应有 3 天 (1518, 1545, 1530)"

    print("✅ [数理] pandas Series / DataFrame / loc / iloc 自检全部通过！")


def main() -> None:
    parser = argparse.ArgumentParser(description="W2D1 数理：pandas 第 5 章入门练习")
    parser.add_argument("--self-test", action="store_true", help="运行自检断言")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    print("=== 1. Series 示例 ===")
    s = create_return_series()
    print(s)
    print("loc['2026-10-15'] =", s.loc["2026-10-15"], "| iloc[0] =", s.iloc[0])

    print("\n=== 2. DataFrame 与 loc / iloc 示例 ===")
    df = create_stock_df()
    print(df)
    print("\n切片练习结果:", practice_loc_iloc(df))


if __name__ == "__main__":
    main()
