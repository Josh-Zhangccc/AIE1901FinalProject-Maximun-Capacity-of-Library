from backend.plot import save_figure
import os

# 检查文件是否存在
json_file_path = r"simulation_data\\simulations\\9_seats_simulations\\9-15.json"

if os.path.exists(json_file_path):
    print(f"找到文件: {json_file_path}")
    # 尝试保存图像
    save_figure(json_file_path, show_plot=True)
    print("图像已生成!")
else:
    print(f"文件不存在: {json_file_path}")
    # 列出9_seats_simulations文件夹中的所有文件
    folder_path = r"simulation_data\\simulations\\9_seats_simulations"
    if os.path.exists(folder_path):
        print(f"\n{folder_path} 文件夹中的文件:")
        for file in os.listdir(folder_path):
            if file.endswith('.json'):
                print(f"  - {file}")
    else:
        print(f"文件夹 {folder_path} 也不存在")