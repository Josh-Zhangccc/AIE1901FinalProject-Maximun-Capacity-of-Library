import os
import json
import re
from collections import defaultdict

# 分析并重命名9_seats_simulations文件夹中的JSON文件
simulations_folder = "simulation_data/simulations/9_seats_simulations"

# 读取所有JSON文件并提取学生数
student_data = defaultdict(list)  # {student_count: [file_list]}

for filename in os.listdir(simulations_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(simulations_folder, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if data and len(data) > 0:
                    config = data[0]  # 获取初始配置信息
                    test_scale = config.get('test_scale', '未知规模')
                    
                    # 从test_scale字段中提取学生数，格式为"3*3->XX"
                    if '->' in test_scale:
                        student_count = int(test_scale.split('->')[1])
                        student_data[student_count].append((filename, file_path))
                    else:
                        print(f"无法从 {filename} 中提取学生数: {test_scale}")
                        
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")

# 按学生数和原始文件名排序，为每个学生数分配模拟次数
renamed_files = []
for student_count in sorted(student_data.keys()):
    # 按原始文件名排序，确保重命名的一致性
    files = sorted(student_data[student_count], key=lambda x: x[0])
    
    for idx, (original_filename, file_path) in enumerate(files, 1):
        new_filename = f"{student_count}-{idx}.json"
        new_file_path = os.path.join(simulations_folder, new_filename)
        
        # 如果新文件名与原文件名不同，则进行重命名
        if original_filename != new_filename:
            print(f"重命名: {original_filename} -> {new_filename}")
            os.rename(file_path, new_file_path)
            renamed_files.append((original_filename, new_filename))
        else:
            print(f"文件已符合标准格式: {original_filename}")

print(f"\n总共重命名了 {len(renamed_files)} 个文件")