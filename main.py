from backend.simulation import Simulation

def main():
    """主函数，启动图书馆座位模拟"""
    print("启动图书馆座位占用行为模拟系统...")
    # 创建模拟实例并运行
    # 使用较小的规模进行演示
    sim = Simulation(row=5, column=4, num_students=2)  # 5x4网格，共20个座位
    sim.run()

if __name__ == "__main__":
    main()