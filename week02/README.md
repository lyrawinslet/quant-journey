# 第 2 周（W2）：函数 / 模块 / OOP / pandas 与可视化进阶

目标：掌握函数与面向对象（`@dataclass` / `class`）、异常处理与 `logging`、`requests` 接口抓取、pandas 基础与对齐运算，以及 `matplotlib` / `plotly` 可视化。

| 天 | 主题 | 产出 |
|---|---|---|
| D1 | 函数/作用域/`@dataclass` 写 `Stock` 类 + pandas `Series/DataFrame/loc/iloc` + AkShare 抓日线画图 + `Ctrl+Shift+P` 10 命令 | `stock_oop.py`、`pandas_intro.py`、`akshare_plot.py`、`day01-2026-10-19.md` |
| D2 | 异常处理 + `logging` + `argparse` + 把图存进 `assets/` 并嵌进 `README` + `Ctrl+P` / `Ctrl+Shift+O` / `F12` | `cli_logging.py`、`assets/maotai_close.png` |
| D3 | `requests` 抓公开汇率接口 + pandas `reindex/drop/算术对齐/apply/排序排名` + `matplotlib` vs `plotly` 对比 + 多光标快捷键 | `w2d3_practice.py`、`sample_quotes.csv`、`day02-03-2026-10-21.md` |

## 本周运行与自检命令

```bash
# W2D1：函数/作用域/dataclass Stock 类 & pandas 入门 & AkShare 画图
python week02/scripts/stock_oop.py --self-test
python week02/scripts/pandas_intro.py --self-test
python week02/scripts/akshare_plot.py

# W2D2：异常处理 + logging + 导出 assets/ 图表
python week02/scripts/cli_logging.py --self-test
python week02/scripts/cli_logging.py --ticker 600519

# W2D3：requests 汇率接口 + pandas 5 大操作 + matplotlib/plotly 双图对比
python week02/scripts/w2d3_practice.py --self-test
python week02/scripts/w2d3_practice.py
```
