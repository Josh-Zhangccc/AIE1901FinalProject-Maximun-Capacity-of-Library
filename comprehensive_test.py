import sys
import os
import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

# 添加项目根目录到sys.path，以便正确导入backend模块
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """测试所有模块是否可以成功导入"""
    print("正在测试模块导入...")
    try:
        from backend import agents, library, prompt, seats, simulation, students
        from backend.seats import Seat, Status
        from backend.students import Student, StudentState
        from backend.library import Library
        from backend.simulation import Simulation
        print("✓ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 模块导入失败: {e}")
        return False

def test_seat_functionality():
    """测试座位系统功能"""
    print("\n正在测试座位系统...")
    try:
        from backend.seats import Seat, Status
        
        # 创建一个座位
        seat = Seat(0, 0, lamp=True, socket=True)
        
        # 测试初始状态
        assert seat.status == Status.vacant
        assert seat.coordinate == (0, 0)
        assert seat.lamp == True
        assert seat.socket == True
        assert seat.window == True  # 因为x=0, y=0在边缘
        print("✓ 座位创建和初始状态正常")
        
        # 测试占用座位
        seat.take(1)
        assert seat.status == Status.taken
        assert seat.owner == 1
        print("✓ 座位占用功能正常")
        
        # 测试离开座位（不占座）
        seat.leave(False)
        assert seat.status == Status.vacant
        assert seat.owner is None
        print("✓ 座位离开功能（不占座）正常")
        
        # 测试占座离开
        seat.take(1)
        seat.leave(True)
        assert seat.status == Status.reverse
        assert seat.owner == 1
        print("✓ 座位占座离开功能正常")
        
        # 测试返回座位
        seat.back()
        assert seat.status == Status.taken
        print("✓ 座位返回功能正常")
        
        # 测试标记占座
        seat.leave(True)
        seat.sign()
        assert seat.status == Status.signed
        print("✓ 座位标记占座功能正常")
        
        # 测试清理占座
        seat.clear()
        assert seat.status == Status.vacant
        assert seat.owner is None
        print("✓ 座位清理功能正常")
        
        return True
    except Exception as e:
        print(f"✗ 座位系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_student_functionality():
    """测试学生系统功能"""
    print("\n正在测试学生系统...")
    try:
        from backend.students import Student, StudentState
        from backend.seats import Seat, Status
        
        # 创建一个学生
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
        
        student = Student(0, student_para, seat_preference)
        
        # 测试初始状态
        assert student.state == StudentState.SLEEP
        assert student.seat is None
        assert len(student.schedule) > 0
        print("✓ 学生创建和初始状态正常")
        
        # 测试座位满意度计算
        seat = Seat(0, 0, lamp=True, socket=True)
        satisfaction = student.calculate_seat_satisfaction(seat)
        assert satisfaction >= 1
        print(f"✓ 座位满意度计算正常，满意度: {satisfaction}")
        
        # 测试占用座位
        student.take_seat(seat)
        assert student.state == StudentState.LEARNING
        assert student.seat == seat
        assert seat.status == Status.taken
        print("✓ 学生占用座位功能正常")
        
        # 测试离开座位（不占座）
        with patch.object(student, '_should_reverse_seat', return_value=False):
            student.leave_seat()
        assert student.state == StudentState.GONE
        assert seat.status == Status.vacant
        print("✓ 学生离开座位功能（不占座）正常")
        
        # 测试占座离开
        student.take_seat(seat)
        with patch.object(student, '_should_reverse_seat', return_value=True):
            student.leave_seat()
        assert student.state == StudentState.AWAY
        assert seat.status == Status.reverse
        print("✓ 学生占座离开功能正常")
        
        # 测试返回座位
        student.choose_seat([seat])
        assert student.state == StudentState.LEARNING
        assert seat.status == Status.taken
        print("✓ 学生返回座位功能正常")
        
        return True
    except Exception as e:
        print(f"✗ 学生系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_library_functionality():
    """测试图书馆系统功能"""
    print("\n正在测试图书馆系统...")
    try:
        from backend.library import Library
        from backend.seats import Seat, Status
        from backend.students import Student, StudentState
        
        # 创建图书馆
        library = Library()
        
        # 测试座位初始化
        assert len(library.seats) == 400  # 20x20网格
        print("✓ 图书馆座位初始化正常")
        
        # 测试学生初始化
        assert len(library.students) > 0
        print(f"✓ 图书馆学生初始化正常，学生数量: {len(library.students)}")
        
        # 测试座位拥挤参数计算
        library.calculate_each_seat_crowded_para()
        # 检查是否有座位的拥挤参数被设置
        seats_with_crowding = [s for s in library.seats if s.crowded_para >= 0]
        assert len(seats_with_crowding) > 0
        print("✓ 图书馆座位拥挤参数计算正常")
        
        # 测试时间更新
        initial_time = library.current_time
        library.update()
        assert library.current_time > initial_time
        print("✓ 图书馆时间更新功能正常")
        
        # 测试占座标记
        library.sign_seat()  # 这应该不会报错，即使没有占座的座位
        print("✓ 图书馆占座标记功能正常")
        
        # 测试占座清理
        library.clear_seat()  # 这应该不会报错，即使没有标记的座位
        print("✓ 图书馆占座清理功能正常")
        
        # 测试计数功能
        taken_count = library.count_taken_seats()
        reversed_count = library.count_reversed_seats()
        print(f"✓ 图书馆座位计数功能正常，占用座位数: {taken_count}, 占座数: {reversed_count}")
        
        return True
    except Exception as e:
        print(f"✗ 图书馆系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prompt_functionality():
    """测试提示词系统功能"""
    print("\n正在测试提示词系统...")
    try:
        from backend import prompt
        
        # 检查提示词是否存在
        assert hasattr(prompt, 'schedule_prompt')
        assert hasattr(prompt, 'leave_prompt')
        assert isinstance(prompt.schedule_prompt, str)
        assert isinstance(prompt.leave_prompt, str)
        
        print("✓ 提示词系统正常")
        return True
    except Exception as e:
        print(f"✗ 提示词系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agents_functionality():
    """测试LLM客户端功能"""
    print("\n正在测试LLM客户端...")
    try:
        from backend.agents import Clients
        
        # 创建客户端实例
        client = Clients()
        
        # 检查客户端属性是否正确初始化
        assert hasattr(client, 'client')
        assert client.client is not None
        
        print("✓ LLM客户端初始化正常")
        return True
    except Exception as e:
        print(f"✗ LLM客户端测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simulation_functionality():
    """测试模拟框架功能"""
    print("\n正在测试模拟框架...")
    try:
        from backend.simulation import Simulation
        
        # 创建模拟实例
        sim = Simulation()
        
        # 检查是否能正常创建
        assert sim is not None
        
        print("✓ 模拟框架初始化正常")
        return True
    except Exception as e:
        print(f"✗ 模拟框架测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有测试"""
    print("开始全面测试图书馆座位模拟系统...")
    
    all_tests = [
        ("模块导入", test_imports),
        ("座位系统", test_seat_functionality),
        ("学生系统", test_student_functionality),
        ("图书馆系统", test_library_functionality),
        ("提示词系统", test_prompt_functionality),
        ("LLM客户端", test_agents_functionality),
        ("模拟框架", test_simulation_functionality)
    ]
    
    results = []
    for test_name, test_func in all_tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "="*50)
    print("测试结果汇总:")
    all_passed = True
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n✓ 所有测试通过！")
    else:
        print("\n✗ 部分测试失败，请查看详细错误信息。")
    
    return all_passed

if __name__ == "__main__":
    main()
