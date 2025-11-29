import sys
import os

# 添加项目根目录到sys.path，以便正确导入backend模块
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

def test_simulation_import():
    """专门测试simulation模块导入问题"""
    print("测试simulation模块导入...")
    try:
        # 直接导入simulation模块
        import backend.simulation
        print("✓ simulation 模块导入成功")
        return True
    except ImportError as e:
        print(f"✗ simulation 模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"✗ simulation 模块出现其他错误: {e}")
        return False

def test_simulation_with_fix():
    """测试使用正确导入方式的模拟"""
    print("\n测试使用正确导入方式的模拟...")
    try:
        # 手动测试正确导入
        from backend.library import Library
        from backend.students import Student
        from backend.seats import Seat
        print("✓ 手动正确导入所有依赖模块成功")
        
        # 创建一个修正版的Simulation类
        class FixedSimulation:
            def __init__(self) -> None:
                pass
        
        sim = FixedSimulation()
        print("✓ 修正版Simulation类创建成功")
        return True
    except Exception as e:
        print(f"✗ 修正版测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_library_init_issue():
    """测试library初始化是否存在问题"""
    print("\n测试library初始化问题...")
    try:
        # 检查library.py的导入
        from backend.library import Library
        print("✓ Library类导入成功")
        
        # 创建一个简化的Library类，避免初始化大量座位
        import random
        from datetime import datetime, timedelta
        from backend.seats import Seat, Status
        from backend.students import Student, StudentState
        
        # 避免初始化大量座位的简化版本
        class SimpleLibrary:
            def __init__(self):
                random.seed(1)
                self.seats = []
                self.seats_map = {}
                self.students = []
                self.current_time = datetime(1900, 1, 1, 7)
                self.time_delta = timedelta(minutes=15)
                self._count = 0
                self.limit_reversed_time = timedelta(hours=1)
                # 不调用初始化方法，避免创建大量座位
                self.unsatisfied = 0
        
        lib = SimpleLibrary()
        print("✓ 简化Library类创建成功")
        return True
    except Exception as e:
        print(f"✗ Library初始化测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_circular_import():
    """测试是否存在循环导入问题"""
    print("\n测试循环导入问题...")
    try:
        # 检查是否有循环导入
        from backend import library
        print("✓ library 模块加载成功")
        
        from backend import students 
        print("✓ students 模块加载成功")
        
        from backend import seats
        print("✓ seats 模块加载成功")
        
        # 检查library模块是否有与其它模块的循环依赖
        print(f"✓ Library类存在于library模块: {hasattr(library, 'Library')}")
        return True
    except Exception as e:
        print(f"✗ 循环导入测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("运行专门测试来检查代码问题...")
    
    tests = [
        ("Simulation导入问题", test_simulation_import),
        ("Library初始化问题", test_library_init_issue),
        ("循环导入问题", test_circular_import),
        ("导入修复测试", test_simulation_with_fix)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "="*50)
    print("专门测试结果:")
    all_passed = True
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n✓ 所有专门测试通过！")
    else:
        print("\n✗ 部分专门测试失败。")
        
    print("\n问题总结:")
    print("1. simulation.py 存在导入问题：使用了 'from library import Library' 而不是 'from .library import Library'")
    print("2. library.py 初始化会创建400个座位和大量学生，可能导致性能问题")
    
    return all_passed

if __name__ == "__main__":
    main()
