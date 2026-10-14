# 第 1 周（W1）：环境 + Python 基础语法

目标：装好环境，能写出并跑起来第一个命令行工具，学会用 Git 提交。

| 天 | 主题 | 产出 |
|---|---|---|
| D1 | 装 Miniconda + VS Code + Git，建 conda 环境 | 环境可用截图 |
| D2 | 数据类型、字符串、list/tuple、条件判断 | 5 个类型转换练习 |
| D3 | 循环、dict/set；把代码整理进仓库 + 写 README | `hello_stock.py`、`basics_practice.py`、README |
| D4 | Git 全流程（add/commit/push/branch）+ VS Code 面板 | 5 次提交记录 |
| D5 | 第一个 CLI：argparse 参数解析 | `hello_stock.py --list` |
| D6 | 整理 `scripts/` + 打首个 tag | `v0.1.0` |

## 本周要掌握的命令

```bash
python week01/scripts/hello_stock.py 600519
python week01/scripts/basics_practice.py --self-test

git add -A
git commit -m "feat(week01): 完成 hello_stock.py"
git push
```

## 自检（能全部做到就算过关）

- [ ] 新终端里能激活 `quant` 环境并运行脚本
- [ ] 不看教程能写出函数、循环、dict 统计词频
- [ ] 能用 VS Code 的源代码管理面板完成一次提交（不碰命令行）
- [ ] 本周至少 5 次提交，README 有运行说明
