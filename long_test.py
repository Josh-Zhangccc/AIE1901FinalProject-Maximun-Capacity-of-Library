from backend.simulation import Simulation

# 创建模拟实例并运行几步
print("启动图书馆座位占用行为模拟系统...")
sim = Simulation(row=5, column=4, num_students=10)  # 5x4网格，共20个座位

print("执行更多步骤观察座位占用情况...")
for i in range(20):
    sim.step()
    print(f"Step {i+1} completed at time: {sim.library.current_time.strftime('%H:%M')}")
    print(f"  被占用座位数: {sim.library.count_taken_seats()}")
    print(f"  不满意学生数: {sim.library.count_unsatisfied()}")
    # 检查前3个学生状态
    learning_students = sum(1 for s in sim.library.students if s.state.name == "LEARNING")
    gone_students = sum(1 for s in sim.library.students if s.state.name == "GONE")
    away_students = sum(1 for s in sim.library.students if s.state.name == "AWAY")
    sleep_students = sum(1 for s in sim.library.students if s.state.name == "SLEEP")
    print(f"  正在学习的学生数: {learning_students}, GONE: {gone_students}, AWAY: {away_students}, SLEEP: {sleep_students}")

print("测试完成！")