from backend.simulation import Simulation
from backend.plot import save_figure
from config import simulations_base_path
import os
import glob

def get_next_simulation_number(seats: int, students: int) -> int:
    """自动检测下一个可用的模拟序号"""
    seat_folder_name = f"{seats}_seats_simulations"
    path = os.path.join(simulations_base_path, seat_folder_name)
    
    # 确保目录存在
    os.makedirs(path, exist_ok=True)
    
    # 查找所有匹配的文件
    pattern = os.path.join(path, f"{students}-*.json")
    matching_files = glob.glob(pattern)
    
    if not matching_files:
        return 1  # 如果没有匹配的文件，从1开始
    
    # 提取模拟序号并找到最大值
    simulation_numbers = []
    for file_path in matching_files:
        filename = os.path.basename(file_path)
        try:
            # 提取 "students-num.json" 中的 num 部分
            num_part = filename.split('-')[1].split('.')[0]
            simulation_numbers.append(int(num_part))
        except (IndexError, ValueError):
            continue  # 如果解析失败，跳过该文件
    
    if not simulation_numbers:
        return 1  # 如果无法解析任何文件名，从1开始
    
    return max(simulation_numbers) + 1  # 返回最大序号+1

# 测试自动检测模拟次数功能
print("测试自动检测模拟次数功能...")

# 使用学生数15进行测试
seats = 9
students = 15

simulation_number = get_next_simulation_number(seats, students)
print(f"检测到这是第 {simulation_number} 次针对 {students} 个学生的模拟")

# 如果需要实际运行模拟，取消下面的注释
# print("运行模拟...")
# sim = Simulation(row=3, column=3, num_students=students, simulation_number=simulation_number) 
# sim.run(run_all=True)
# save_figure(seats=seats, students=students, simulation_number=simulation_number, show_plot=False)
# print("完成")