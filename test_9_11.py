from backend.plot import plot_simulation
import json

# 直接显示9-11.json的图表
json_file_path = "simulation_data/simulations/9-11.json"

# 读取JSON文件并打印测试名称，确认文件内容
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f"测试名称: {data[0]['test_name']}")
    print(f"测试规模: {data[0]['test_scale']}")

# 显示图表
plot_simulation(json_file_path, save_to_path=None)  # 直接显示，不保存