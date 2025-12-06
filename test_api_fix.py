import os
import sys
import threading
import time
import json

# 添加项目根目录到Python路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

def test_api_endpoints():
    """测试API端点功能，不实际启动服务器"""
    print("测试API端点功能...")
    
    # 直接测试后端函数
    from backend.plot import save_figure
    from backend.data_analysis import run_analysis
    
    print("\n1. 测试图像生成功能...")
    try:
        # 测试学生图像生成
        result = save_figure(seats=9, students=10, simulation_number=1, show_plot=False)
        print(f"   学生图像生成结果: {'成功' if result else '失败'}")
    except Exception as e:
        print(f"   学生图像生成错误: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        # 测试分析图像生成
        result = run_analysis(9, 9, 19)
        print(f"   分析图像生成结果: {'成功' if result is not None else '失败'}")
    except Exception as e:
        print(f"   分析图像生成错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nAPI功能测试完成")

if __name__ == "__main__":
    test_api_endpoints()
