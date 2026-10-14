"""W1 基础语法练习：数据类型 / 条件 / 循环 / dict / set / 函数。

自己先写一遍，再运行 `python basics_practice.py --self-test` 检查；
每道题都留了 TODO，把它改成你自己的写法。
"""
import argparse


# 1. 变量与类型：把字符串转成数字并做格式化输出
def bmi(weight_kg: float, height_m: float) -> str:
    """返回形如 'BMI=22.5（正常）' 的字符串。"""
    value = weight_kg / height_m ** 2
    if value < 18.5:
        label = "偏瘦"
    elif value < 24:
        label = "正常"
    elif value < 28:
        label = "偏胖"
    else:
        label = "肥胖"
    return f"BMI={value:.1f}（{label}）"


# 2. 循环 + dict：统计词频
def word_count(text: str) -> dict:
    """把句子拆成词并统计出现次数（忽略大小写）。"""
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


# 3. set：找出两只股票池的差异
def diff_codes(a: list, b: list) -> dict:
    sa, sb = set(a), set(b)
    return {"只在A": sorted(sa - sb), "只在B": sorted(sb - sa), "都有": sorted(sa & sb)}


# 4. 循环 + 累积：算复利
def compound(principal: float, rate: float, years: int) -> float:
    """按年复利，返回期末金额。"""
    total = principal
    for _ in range(years):
        total *= (1 + rate)
    return round(total, 2)


# 5. 列表推导式：筛出涨幅大于阈值的标的
def strong_stocks(changes: dict, threshold: float = 3.0) -> list:
    return [code for code, chg in changes.items() if chg > threshold]


def self_test() -> None:
    assert bmi(70, 1.75) == "BMI=22.9（正常）", bmi(70, 1.75)
    assert word_count("a b A") == {"a": 2, "b": 1}
    assert diff_codes(["600519", "000001"], ["000001"])["只在A"] == ["600519"]
    assert compound(10000, 0.1, 2) == 12100.0
    assert strong_stocks({"A": 4.2, "B": 1.0}) == ["A"]
    print("✅ 5 道题全部通过，可以提交了")


def main() -> None:
    parser = argparse.ArgumentParser(description="W1 基础语法练习")
    parser.add_argument("--self-test", action="store_true", help="运行 5 道题的自检")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    print(bmi(70, 1.75))
    print(word_count("量化的路上 每天 提交 每天 进步"))
    print(diff_codes(["600519", "000001"], ["000001", "300750"]))
    print(compound(10000, 0.10, 5))
    print(strong_stocks({"600519": 4.2, "000001": -1.5, "300750": 3.1}))


if __name__ == "__main__":
    main()
