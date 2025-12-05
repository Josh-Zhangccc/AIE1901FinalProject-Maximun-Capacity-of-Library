from backend.simulation import Simulation
from backend.plot import save_figure
from config import simulations_base_path
import os

# 模拟运行一次
print("测试新的模拟功能...")

# 使用较小的规模进行演示
row = 3  # 默认行数
column = 3  # 默认列数
num_students = 15  # 学生数
simulation_number = 1  # 模拟次数

sim = Simulation(row=row, column=column, num_students=num_students, simulation_number=simulation_number) 
sim.run(run_all=True)

# 使用新的save_figure接口
total_seats = row * column
save_figure(seats=total_seats, students=num_students, simulation_number=simulation_number, show_plot=False)

print(f"模拟数据已保存，座位数: {total_seats}, 学生数: {num_students}, 模拟次数: {simulation_number}")
print("图像已保存到对应的文件夹中")