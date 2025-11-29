import sys
import os

# 添加项目根目录到sys.path，以便正确导入backend模块
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

def test_basic_imports():
    """测试基本导入功能"""
    print("测试基本模块导入...")
    try:
        import backend
        print("✓ backend 包导入成功")
    except Exception as e:
        print(f"✗ backend 包导入失败: {e}")
        return False
    
    try:
        from backend import seats
        print("✓ seats 模块导入成功")
    except Exception as e:
        print(f"✗ seats 模块导入失败: {e}")
        return False
    
    try:
        from backend import students
        print("✓ students 模块导入成功")
    except Exception as e:
        print(f"✗ students 模块导入失败: {e}")
        return False
    
    try:
        from backend import library
        print("✓ library 模块导入成功")
    except Exception as e:
        print(f"✗ library 模块导入失败: {e}")
        return False
    
    try:
        from backend import agents
        print("✓ agents 模块导入成功")
    except Exception as e:
        print(f"✗ agents 模块导入失败: {e}")
        return False
    
    try:
        from backend import prompt
        print("✓ prompt 模块导入成功")
    except Exception as e:
        print(f"✗ prompt 模块导入失败: {e}")
        return False
    
    try:
        from backend import simulation
        print("✓ simulation 模块导入成功")
    except Exception as e:
        print(f"✗ simulation 模块导入失败: {e}")
        return False
    
    return True

def test_seat_creation():
    """测试座位创建"""
    print("\n测试座位创建...")
    try:
        from backend.seats import Seat
        seat = Seat(0, 0)
        print(f"✓ 座位创建成功: {seat.coordinate}, 状态: {seat.status}")
        return True
    except Exception as e:
        print(f"✗ 座位创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_library():
    """测试简单图书馆初始化"""
    print("\n测试简单图书馆初始化...")
    try:
        # 临时创建一个测试版本的图书馆，避免初始化大量座位和学生
        from backend.seats import Seat, Status
        from backend.students import Student, StudentState
        import random
        from datetime import datetime, timedelta
        
        # 创建一个简化的图书馆类，只创建少量座位和学生
        class SimpleLibrary:
            def __init__(self):
                self.seats = []
                self.students = []
                self.current_time = datetime(1900, 1, 1, 7)
                self.time_delta = timedelta(minutes=15)
                self.unsatisfied = 0
                self.initialize_seats_small()
                self.initialize_students_small()
            
            def initialize_seats_small(self):
                # 只创建少量座位测试
                for i in range(5):  # 只创建5个座位
                    self.seats.append(Seat(i, 0, lamp=(i % 2 == 0), socket=(i % 3 == 0)))
            
            def initialize_students_small(self):
                student_para = {
                    "character": "守序",
                    "schedule_type": "正常", 
                    "focus_type": "中", 
                    "course_situation": "中"
                }
                seat_preference = {
                    "lamp": 0.5,
                    "socket": 0.5,
                    "space": 0.5
                }
                
                # 只创建一个学生测试
                from backend.students import Student
                self.students.append(Student(0, student_para, seat_preference))
        
        lib = SimpleLibrary()
        print(f"✓ 简单图书馆初始化成功，座位数: {len(lib.seats)}，学生数: {len(lib.students)}")
        return True
    except Exception as e:
        print(f"✗ 简单图书馆初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("运行简化的测试来检查代码问题...")
    
    tests = [
        ("基本导入", test_basic_imports),
        ("座位创建", test_seat_creation),
        ("简单图书馆", test_simple_library)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "="*40)
    print("测试结果:")
    all_passed = True
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n✓ 基本测试通过！")
    else:
        print("\n✗ 部分基本测试失败。")
    
    return all_passed

if __name__ == "__main__":
    main()