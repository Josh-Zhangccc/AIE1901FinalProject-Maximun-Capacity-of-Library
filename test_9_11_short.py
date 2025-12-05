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

# 测试9座11人的模拟
print("开始测试9座11人模拟...")

# 自动检测模拟次数
seats = 9
students = 11
simulation_number = get_next_simulation_number(seats, students)
print(f"这是第 {simulation_number} 次针对 {students} 个学生的模拟")

try:
    print("创建Simulation对象...")
    sim = Simulation(row=3, column=3, num_students=students, simulation_number=simulation_number)
    print("Simulation对象创建成功")
    
    # 只运行一小段时间来测试是否会出现LLM解析错误
    print("运行单步模拟来测试LLM交互...")
    sim.step()  # 执行单步
    print("单步模拟成功完成，LLM交互正常")
    
    # 保存数据
    sim.jm.save_json()
    print("数据保存成功")
    
except Exception as e:
    print(f"模拟过程中出现错误: {e}")
    import traceback
    traceback.print_exc()
    
print("\n测试完成")