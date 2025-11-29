from backend.simulation import Simulation

# 创建模拟实例并运行几步
print("启动图书馆座位占用行为模拟系统...")
sim = Simulation(row=5, column=4, num_students=10)  # 5x4网格，共20个座位

print("执行几步模拟...")
for i in range(20):
    sim.step()
    print(f"Step {i+1} completed at time: {sim.library.current_time.strftime('%H:%M')}")
    seats_taken = sim.library.count_taken_seats()
    if seats_taken > 0:
        print(f"  发现座位被占用! 当前被占用座位数: {seats_taken}")
        break

print("显示最终状态...")
sim.show_status()
print("显示最终座位状态...")
sim.show_seats()

print("测试完成！")