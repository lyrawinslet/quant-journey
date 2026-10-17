# 本地开发硬约束 (v1.0)

1. **路径铁律**：当前为 Windows Git Bash 环境。代码中所有文件路径必须使用 `pathlib.Path` 或正斜杠 `/`，严禁出现反斜杠 `\`。
2. **数据契约**：默认测试数据包含且仅包含三列：`trade_date` (日期字符串), `ticker` (标的代码), `close_price` (收盘价浮点数)。严禁自己编造 `price`、`date` 等其他列名。
3. **画图验收标准**：
   - 必须显式设置中文字体为 `SimHei`，并配置 `axes.unicode_minus = False`。
   - 折线图主色固定使用深海蓝 `#1f4e78`，均值线使用琥珀橙 `#ed7d31`（虚线）。
   - 严禁调用 `plt.show()` 弹窗阻塞程序，必须直接保存至当前目录的 `output/test_plot.png`（若 `output` 文件夹不存在需在代码中自动创建），分辨率 `dpi=300`。
4. **代码风格**：核心逻辑必须封装为带类型注解（Type Hints）的函数，并在 `if __name__ == "__main__":` 中生成 20 条模拟数据跑通全流程，最后打印一行 `[SUCCESS] 图表已生成至 output/test_plot.png`。