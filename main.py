from backend.simulation import Simulation
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
    # 将工作目录设置为脚本所在目录
os.chdir(current_dir)

print(f"现在工作目录是：{os.getcwd()}")

def main():
    """主函数，启动图书馆座位模拟"""
    print("启动图书馆座位占用行为模拟系统...")
    # 创建模拟实例并运行
    # 使用较小的规模进行演示
    simulation_type = input("本次模拟类型为：")
    if not simulation_type:
        simulation_type = "simulation"
    name = input("命名本次模拟为：")
    sim = Simulation(name, row=3, column=3, num_students=10, simulation_type=simulation_type) 
    sim.run()

if __name__ == "__main__":
    main()