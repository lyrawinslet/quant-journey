# quant-journey

> 零基础文科生转量化的**练习代码仓库**：每天写的东西都往这里放，一天一次提交。
> 配套的 39 周计划表与作品集在 [Quant-Learning-Path](https://github.com/lyrawinslet/Quant-Learning-Path)。

## 这是什么

- 第 1-9 周的**基础练习代码**（Python 语法、NumPy、pandas、指标计算）
- 每周一个 `weekNN/` 目录：`scripts/`（可运行代码）+ `notes/`（当天笔记）
- 目的只有一个：**让每天的产出看得见**。代码丑没关系，能跑、有记录就算数。

## 快速开始

```bash
git clone https://github.com/lyrawinslet/quant-journey.git
cd quant-journey
python week01/scripts/hello_stock.py 600519        # 第 1 周的第一个小工具（纯标准库，无需依赖）
```

想跑 pandas 版本（第 4 周起）：

```bash
pip install -r requirements.txt
```

## 目录结构

```
quant-journey/
├─ week01/
│  ├─ scripts/
│  │  ├─ hello_stock.py        # argparse 命令行工具：输入代码打印问候 + 随机行情
│  │  └─ basics_practice.py    # 数据类型/循环/dict 练习（带 --self-test 自检）
│  └─ notes/
│     └─ day03-2026-10-14.md   # 当天笔记：做了什么 / 卡在哪 / 明天第一件事
├─ requirements.txt
└─ .gitignore
```

## 学习进度

| 周 | 主题 | 产出 | 状态 |
|---|---|---|---|
| W1 | 环境搭建 + Python 基础语法 | `hello_stock.py`、`basics_practice.py` | ✅ 已完成 |
| W2 | 函数 / OOP / 文件读写 | MiniBacktest 骨架 | ⏳ 进行中 |
| W3 | NumPy 向量化 + 指标盲写 | `indicators.py` | ⏳ |
| W4 | pandas 清洗与分组 | `clean_pipeline.py` | ⏳ |

## 第 1 周学到了什么

- 装好 Miniconda + VS Code + Git，建了 `quant` 环境
- 变量/类型/字符串格式化、`if/elif/else`、`for/while`、`list/tuple/dict/set`
- 第一个 CLI 工具：`argparse` 解析参数、`random` 造数据、函数拆分
- Git 基本流程：`add / commit / push`，用 VS Code 源代码管理面板也能提交

## 每天怎么提交

```bash
git add -A
git commit -m "feat(week01): W1D3 hello_stock.py 支持 --list 列出示例股票"
git push
```

提交信息格式：`feat/fix/docs/test(范围): 干了什么`。

## 免责声明

仅用于学习与研究；代码里的行情数据是**随机生成的假数据**，不构成任何投资建议。
