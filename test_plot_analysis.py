from backend.plot import plot_analysis

# 测试分析功能通过plot.py调用
print("开始测试通过plot.py调用分析功能...")

# 对9个座位的数据进行分析，指定学生数范围
plot_analysis(9, min_students=9, max_students=19)

print("分析完成！")