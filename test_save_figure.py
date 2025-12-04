from backend.plot import plot_simulation,save_figure

# 测试save_figure函数
json_file_path = f"simulation_data/simulations/9-18.json"
plot_simulation(json_file_path)
save_figure(json_file_path)
print("图像已保存到对应的文件夹中！")