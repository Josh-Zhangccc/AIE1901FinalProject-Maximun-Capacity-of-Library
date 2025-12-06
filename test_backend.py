import os
import sys
import json

# 添加项目根目录到Python路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from backend.plot import save_figure
from backend.data_analysis import run_analysis

def test_backend_functions():
    """测试后端绘图功能"""
    print("正在测试后端绘图功能...")
    
    # 测试save_figure函数
    print("\n1. 测试save_figure函数...")
    try:
        success = save_figure(seats=9, students=10, simulation_number=1, show_plot=False)
        print(f"   save_figure执行结果: {'成功' if success else '失败'}")
    except Exception as e:
        print(f"   save_figure执行出错: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试run_analysis函数
    print("\n2. 测试run_analysis函数...")
    try:
        results = run_analysis(9, 9, 19)  # 座位数9，学生范围9-19
        print(f"   run_analysis执行结果: {'成功' if results is not None else '失败'}")
    except Exception as e:
        print(f"   run_analysis执行出错: {e}")
        import traceback
        traceback.print_exc()
    
    # 检查生成的图像文件
    print("\n3. 检查生成的图像文件...")
    figure_dir = os.path.join(PROJECT_ROOT, "simulation_data", "figures", "seats_9")
    if os.path.exists(figure_dir):
        files = os.listdir(figure_dir)
        print(f"   seats_9文件夹中有 {len(files)} 个图像文件:")
        for file in files[:10]:  # 只显示前10个
            print(f"     - {file}")
    else:
        print("   未找到图像输出目录")
    
    print("\n后端功能测试完成")

if __name__ == "__main__":
    test_backend_functions()