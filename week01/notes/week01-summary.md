# 第 1 周（W1）周复盘与 W2 计划

## 本周完成了什么
1. **环境与工程流**：搭好 Python 环境、VS Code 与 Git，跑通了「本地写代码 -> VS Code 源代码管理面板 Stage/Commit/Push -> GitHub 同步」闭环。
2. **命令行与基础语法**：
   - 完成 `hello_stock.py`（掌握 `argparse` 命令行参数解析、固定随机种子 `random.Random(seed)`、以及 `with open` 文件写入）。
   - 手敲完成 20 行命令行番茄钟 `pomodoro.py` 与 `basics_practice.py` 自检。
3. **调试能力突破**：掌握 VS Code 断点（F9 / 行号左侧红点）、条件断点、Watch 表达式监视与 Debug Console 实时求值。
4. **GitHub 门面建设**：补齐仓库 Description、Topics、MIT License，并开启首个 Issue。

## 本周踩坑与收获
- **坑 1**：写了代码没生成文件 / 改了没生效 -> 学会拆解「参数接收 -> 列表收集 -> 写入文件」三步逻辑，并养成 `Ctrl+S` 保存习惯。
- **坑 2**：按 F5 调试没停在断点 -> 发现没传默认参数导致程序提前 `return`，理解了程序执行流与 `Terminal` / `Debug Console` 的区别。

## 下周（W2：函数 / OOP / 模块化）3 件要紧事 Todo
- [ ] **Todo 1（模块化重构）**：把 `hello_stock.py` 拆分成独立的 `quote.py`（数据逻辑）与 `cli.py`（命令行入口）。
- [ ] **Todo 2（面向对象 OOP）**：用 `class` 写出第一个 `MiniBacktest` 最小回测账户骨架（管理现金、持仓、买卖记录）。
- [ ] **Todo 3（异常处理与读写）**：支持把回测交易记录导出为 CSV 文件，并加上异常保护。
