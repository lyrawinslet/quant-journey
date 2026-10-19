# 第 2 周（W2）：函数 / 模块 / OOP / pandas 与 AkShare 初体验

目标：掌握函数与面向对象（`@dataclass` / `class`）、模块化拆分、pandas 基础索引切片，以及用 AkShare 抓取真实日线并画图。

| 天 | 主题 | 产出 |
|---|---|---|
| D1 | 函数/作用域/`@dataclass` 写 `Stock` 类 + pandas `Series/DataFrame/loc/iloc` + AkShare 抓日线画图 + `Ctrl+Shift+P` 10 命令 | `stock_oop.py`、`pandas_intro.py`、`akshare_plot.py`、`day01-2026-10-19.md` |

## 今日（W2D1）运行与自检命令

```bash
# 1. 技术：函数/作用域/dataclass Stock 类自检
python week02/scripts/stock_oop.py --self-test

# 2. 数理：pandas Series/DataFrame/loc/iloc 自检
python week02/scripts/pandas_intro.py --self-test

# 3. 实战：AkShare 抓 1 只股票日线 + matplotlib 画收盘价
python week02/scripts/akshare_plot.py
```
