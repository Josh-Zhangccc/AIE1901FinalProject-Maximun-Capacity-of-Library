from backend.plot import plot_simulation
import json
import os

# 直接显示9-11.json的图表
# 检查新路径是否存在，如果不存在则使用旧路径
new_json_file_path = "simulation_data/simulations/9_seats_simulations/9-11.json"
old_json_file_path = "simulation_data/simulations/9-11.json"

if os.path.exists(new_json_file_path):
    json_file_path = new_json_file_path
elif os.path.exists(old_json_file_path):
    json_file_path = old_json_file_path
else:
    print(f"找不到文件: {new_json_file_path} 或 {old_json_file_path}")
    exit(1)

# 读取JSON文件并打印测试名称，确认文件内容
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f"测试名称: {data[0]['test_name']}")
    print(f"测试规模: {data[0]['test_scale']}")

# 显示图表
plot_simulation(json_file_path, save_to_path=None)  # 直接显示，不保存