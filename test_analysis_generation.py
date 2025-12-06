import os
import sys

# 添加项目根目录到Python路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from backend.data_analysis import run_analysis

def test_analysis_generation():
    """测试特定参数的分析图像生成"""
    print("测试分析图像生成 (seats=9, min_students=9, max_students=18)...")
    
    try:
        # 测试生成9-9-18的分析图像
        result = run_analysis(seat_count=9, min_students=9, max_students=18, output_dir=None)
        print(f"分析图像生成结果: {'成功' if result is not None else '失败'}")
        
        if result:
            print("分析图像已生成成功")
        else:
            print("分析图像生成失败或没有数据")
            
    except Exception as e:
        print(f"分析图像生成出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_analysis_generation()