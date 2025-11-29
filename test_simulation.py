from backend.simulation import Simulation

# 创建模拟实例并运行几步
print("启动图书馆座位占用行为模拟系统...")
sim = Simulation(row=5, column=4, num_students=10)  # 5x4网格，共20个座位

print("执行几步模拟...")
for i in range(3):
    sim.step()
    print(f"Step {i+1} completed at time: {sim.library.current_time}")

print("显示当前状态...")
sim.show_status()

print("显示座位状态...")
sim.show_seats()

print("测试完成！")