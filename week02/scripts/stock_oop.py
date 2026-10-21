"""W2D1 技术练习：函数参数、作用域、类与 __repr__（用 @dataclass 写 Stock 类）。

练习方式：
1. 阅读每个部分的注释说明，把标有 `# TODO` 的地方补充完整（或者修改默认实现来实验）。
2. 运行 `python week02/scripts/stock_oop.py --self-test` 检查是否全部通过。
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass

# 全局默认手续费率（用于演示 LEGB 作用域）
DEFAULT_COMMISSION_RATE: float = 0.0003


# ============================================================
# 1. 函数参数：位置参数、默认参数、关键字参数、*args / **kwargs
# ============================================================
def calc_position_value(
    price: float,
    shares: int = 100,
    commission_rate: float = DEFAULT_COMMISSION_RATE,
) -> float:
    """计算买入持仓总成本（含手续费），结果保留 2 位小数。

    公式：总成本 = price * shares * (1 + commission_rate)
    - price: 成交价（必填位置参数）
    - shares: 股数（默认 100 股，即 1 手）
    - commission_rate: 佣金费率（默认万三 0.0003）
    """
    # TODO: 确认或手敲下面的计算公式
    gross = price * shares
    total = gross * (1 + commission_rate)
    return round(total, 2)


# ============================================================
# 2. 作用域（LEGB）：Local（局部） vs Global（全局）
# ============================================================
def demo_scope(custom_rate: float) -> tuple[float, float]:
    """演示局部变量不会污染全局变量。

    返回 (函数内局部费率, 全局默认费率 DEFAULT_COMMISSION_RATE)
    """
    # 在函数内部定义同名局部变量，仅在函数内部（Local）生效
    local_rate = custom_rate
    return local_rate, DEFAULT_COMMISSION_RATE


# ============================================================
# 3. 传统 class 与手写 __repr__ vs @dataclass 自动生成
# ============================================================
class ManualStock:
    """传统手写类：需要自己写 __init__ 和 __repr__。"""

    def __init__(self, ticker: str, name: str, close_price: float) -> None:
        self.ticker = ticker
        self.name = name
        self.close_price = close_price

    def __repr__(self) -> str:
        return (
            f"ManualStock(ticker={self.ticker!r}, "
            f"name={self.name!r}, close_price={self.close_price})"
        )


@dataclass
class Stock:
    """用 @dataclass 编写的 Stock 类。

    @dataclass 会自动帮你生成：
    - __init__(self, ticker, name, close_price, prev_close=0.0, shares=100)
    - __repr__(self)  -> 打印清晰可读的对象表示
    - __eq__(self, other) -> 支持两个 Stock 对象直接用 == 比较
    """

    ticker: str
    name: str
    close_price: float
    prev_close: float = 0.0
    shares: int = 100

    @property
    def market_value(self) -> float:
        """持仓市值 = 收盘价 * 持仓股数。"""
        # TODO: 计算持仓市值并 round(..., 2)
        return round(self.close_price * self.shares, 2)

    def pct_change(self) -> float:
        """计算今日涨跌幅（百分比，保留 2 位小数）。若 prev_close <= 0 返回 0.0。"""
        # TODO: 涨跌幅公式：(close_price - prev_close) / prev_close * 100
        if self.prev_close <= 0:
            return 0.0
        return round((self.close_price - self.prev_close) / self.prev_close * 100, 2)
    def daily_pnl(self) -> float:
        """计算每日盈亏 = (close_price - prev_close) * shares"""
        if self.prev_close <= 0:
            return 0.0
        return round((self.close_price - self.prev_close) * self.shares, 2)

# ============================================================
# 自检与主入口
# ============================================================
def self_test() -> None:
    # 1. 测试函数参数（默认参数 & 关键字参数）
    assert calc_position_value(10.0) == 1000.3, "默认 100 股 + 万三佣金应为 1000.3"
    assert calc_position_value(10.0, shares=200, commission_rate=0.0) == 2000.0

    # 2. 测试作用域
    local_r, global_r = demo_scope(0.001)
    assert local_r == 0.001 and global_r == 0.0003

    # 3. 测试 @dataclass Stock 类与 __repr__
    s = Stock(ticker="600519", name="贵州茅台", close_price=1550.0, prev_close=1500.0, shares=100)
    assert "Stock(" in repr(s) and "600519" in repr(s), f"__repr__ 输出异常: {s!r}"
    assert s.market_value == 155000.0, f"市值计算错误: {s.market_value}"
    assert s.pct_change() == 3.33, f"涨跌幅计算错误: {s.pct_change()}"

    print("✅ [技术] 函数/作用域/@dataclass Stock 类 自检全部通过！")


def main() -> None:
    parser = argparse.ArgumentParser(description="W2D1 技术：函数/模块/OOP 与 dataclass Stock 类")
    parser.add_argument("--self-test", action="store_true", help="运行自检断言")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    m_stock = ManualStock("000001", "平安银行", 11.50)
    d_stock = Stock(ticker="600519", name="贵州茅台", close_price=1550.0, prev_close=1500.0)

    print("1. 手写 __repr__ 效果:", m_stock)
    print("2. @dataclass 自动 __repr__ 效果:", d_stock)
    print(f"3. {d_stock.name} 1手持仓市值: {d_stock.market_value} 元，今日涨跌幅: {d_stock.pct_change()}%")
    print(f"4. 买入含佣金总成本: {calc_position_value(d_stock.close_price, shares=d_stock.shares)} 元")


if __name__ == "__main__":
    main()
