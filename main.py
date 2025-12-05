from backend.simulation import Simulation
from backend.plot import save_figure
from config import simulations_base_path
import os
import glob
current_dir = os.path.dirname(os.path.abspath(__file__))
    # 将工作目录设置为脚本所在目录
os.chdir(current_dir)

print(f"现在工作目录是：{os.getcwd()}")

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


def main(n):
    """主函数，启动图书馆座位模拟"""
    print("启动图书馆座位占用行为模拟系统...")
    # 创建模拟实例并运行
    # 使用较小的规模进行演示
    print("本次模拟类型为：simulation（仅支持simulation类型）")
    row = 3  # 默认行数
    column = 3  # 默认列数
    num_students = n
    #int(input("请输入学生数量（默认19）：") or 19)  # 获取学生数
    
    # 自动计算模拟次数
    total_seats = row * column
    simulation_number = get_next_simulation_number(total_seats, num_students)
    print(f"检测到这是第 {simulation_number} 次针对 {num_students} 个学生的模拟")
    
    sim = Simulation(row=row, column=column, num_students=num_students, simulation_number=simulation_number) 
    sim.run(run_all=True)
    # 根据座椅数量确定保存路径
    seat_folder_name = f"{total_seats}_seats_simulations"
    path = os.path.join(simulations_base_path, seat_folder_name)
    file_name = f"{num_students}-{simulation_number}.json"
    file_path = os.path.join(path, file_name)
    # 使用新的save_figure接口
    save_figure(seats=total_seats, students=num_students, simulation_number=simulation_number)
    print(f"模拟数据已保存到 {file_path}")
    print(f"图像已保存到对应的文件夹中")
if __name__ == "__main__":
    main(15)