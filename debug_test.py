from backend.simulation import Simulation

# 创建模拟实例并运行几步
print("启动图书馆座位占用行为模拟系统...")
sim = Simulation(row=5, column=4, num_students=10)  # 5x4网格，共20个座位

print("初始时间:", sim.library.current_time)
print("前3个学生的初始时间:", [s.current_time for s in sim.library.students[:3]])
print("前3个学生的初始状态:", [s.state.name for s in sim.library.students[:3]])

print("\n执行几步模拟...")
for i in range(5):
    sim.step()
    print(f"Step {i+1} completed at time: {sim.library.current_time}")
    print(f"  被占用座位数: {sim.library.count_taken_seats()}")
    print(f"  不满意学生数: {sim.library.count_unsatisfied()}")
    # 检查前3个学生状态
    learning_students = sum(1 for s in sim.library.students if s.state.name == "LEARNING")
    print(f"  正在学习的学生数: {learning_students}")

print("\n执行更多步骤...")
for i in range(10):
    sim.step()
    if i % 3 == 0:  # 每3步输出一次
        print(f"Step {i+6} completed at time: {sim.library.current_time}")
        print(f"  被占用座位数: {sim.library.count_taken_seats()}")
        print(f"  不满意学生数: {sim.library.count_unsatisfied()}")
        learning_students = sum(1 for s in sim.library.students if s.state.name == "LEARNING")
        print(f"  正在学习的学生数: {learning_students}")

print("测试完成！")