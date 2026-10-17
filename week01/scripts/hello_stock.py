"""W1 第一个命令行小工具：输入股票代码，打印问候 + 一段随机行情。

纯标准库实现，装好 Python 就能跑（第 1 周还没必要引入第三方依赖）：
    python hello_stock.py 600519
    python hello_stock.py 600519 000001 --count 2
    python hello_stock.py --list
"""
import argparse
import random

STOCKS = {
    "600519": ("贵州茅台", 1520.0),
    "000001": ("平安银行", 11.4),
    "300750": ("宁德时代", 245.0),
    "510300": ("沪深300ETF", 4.12),
    "159915": ("创业板ETF", 2.18),
}


def fake_quote(code: str, seed=None) -> dict:
    """生成一条假的行情记录（用代码做随机种子，保证同一代码结果稳定）。"""
    name, base = STOCKS.get(code, ("未知标的", 100.0))
    rng = random.Random(seed if seed is not None else code)
    chg = rng.uniform(-0.05, 0.05)
    return {
        "code": code,
        "name": name,
        "close": round(base * (1 + chg), 2),
        "change_pct": round(chg * 100, 2),
    }


def show(quote: dict) -> str:
    """把一条行情格式化成一行文本。"""
    return (f"{quote['code']}  {quote['name']:<8} "
            f"收盘 {quote['close']:>9.2f}  涨跌 {quote['change_pct']:+.2f}%")


def main() -> None:
    parser = argparse.ArgumentParser(description="输入股票代码，打印问候 + 随机行情")
    parser.add_argument("codes", nargs="*", default=["600519", "000001"], help="股票代码，可多个")
    parser.add_argument("--list", action="store_true", help="列出内置示例股票")
    parser.add_argument("--count", type=int, default=1, help="每个代码打印几条")
    parser.add_argument("--save",default="",help="把行情保存到指定文件名")
    args = parser.parse_args()

    if args.list or not args.codes:
        print("内置示例股票：")
        for code, (name, base) in STOCKS.items():
            print(f"  {code}  {name:<10} 参考价 {base}")
        if not args.codes:
            return

    print("你好，这是你的第一个量化小工具。今天也要提交一次代码 :)")
    lines=[]
    for code in args.codes:
        for i in range(args.count):
            line=show(fake_quote(code,seed=f"{code}-{i}"))
            print("  " + line)
            lines.append(line)
    if args.save:
        with open(args.save,"w",encoding="utf-8")as f:
            f.write("\n".join(lines)+"\n")
        print(f"行情已成功写入文件:{args.save}")

if __name__ == "__main__":
    main()
