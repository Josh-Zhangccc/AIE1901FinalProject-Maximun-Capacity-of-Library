from backend.simulation import Simulation

# 创建模拟实例并运行几步
print("启动图书馆座位占用行为模拟系统...")
sim = Simulation(row=5, column=4, num_students=10)  # 5x4网格，共20个座位

print(f"初始时间: {sim.library.current_time}, 座位总数: {len(sim.library.seats)}")
print(f"学生总数: {len(sim.library.students)}")

# 运行几步模拟
for i in range(10):
    sim.step()
    seats_taken = sim.library.count_taken_seats()
    unsatisfied = sim.library.count_unsatisfied()
    print(f"Step {i+1}: 时间 {sim.library.current_time.strftime('%H:%M')}, 占用座位: {seats_taken}, 不满学生: {unsatisfied}")

print("\n最终状态:")
sim.show_status()
print("\n最终座位状态:")
sim.show_seats()
print("测试完成！")