from backend.plot import save_figure
import os

# 测试新的save_figure函数接口
print("测试新的save_figure函数接口...")

# 使用现有数据测试
seats = 9
students = 14  # 使用现有的数据
simulation_number = 1

# 检查JSON文件是否存在
from config import simulations_base_path
seat_folder_name = f"{seats}_seats_simulations"
json_file_path = os.path.join(simulations_base_path, seat_folder_name, f"{students}-{simulation_number}.json")

if os.path.exists(json_file_path):
    print(f"找到JSON文件: {json_file_path}")
    # 调用新的save_figure接口
    save_figure(seats=seats, students=students, simulation_number=simulation_number, show_plot=False)
    print("图像已生成")
else:
    print(f"JSON文件不存在: {json_file_path}")
    # 检查9_seats_simulations目录中的文件
    folder_path = os.path.join(simulations_base_path, seat_folder_name)
    if os.path.exists(folder_path):
        print(f"\n{folder_path} 文件夹中的文件:")
        for file in os.listdir(folder_path):
            if file.endswith('.json'):
                print(f"  - {file}")