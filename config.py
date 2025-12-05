import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# 基础路径
simulation_data_path = os.path.join(current_dir, 'simulation_data')
simulations_base_path = os.path.join(simulation_data_path, 'simulations')

# 测试模拟路径（保留但不再使用）
test_simulation_path = os.path.join(simulation_data_path, 'test')