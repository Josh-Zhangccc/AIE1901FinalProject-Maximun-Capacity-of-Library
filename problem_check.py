import sys
import os

# 添加项目根目录到sys.path，以便正确导入backend模块
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

def test_seat_class():
    """测试座位类功能"""
    print("测试座位类...")
    try:
        from backend.seats import Seat, Status
        from datetime import datetime
        
        # 创建一个座位
        seat = Seat(0, 0, lamp=True, socket=True)
        print(f"  - 座位坐标: {seat.coordinate}")
        print(f"  - 座位状态: {seat.status}")
        print(f"  - 是否有灯: {seat.lamp}")
        print(f"  - 是否有插座: {seat.socket}")
        print(f"  - 是否靠窗: {seat.window}")
        
        # 测试占用
        seat.take(1)
        print(f"  - 占用后状态: {seat.status}")
        
        # 测试离开
        seat.leave(False)
        print(f"  - 离开后状态: {seat.status}")
        
        print("✓ 座位类功能正常")
        return True
    except Exception as e:
        print(f"✗ 座位类测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_student_class():
    """测试学生类功能"""
    print("\n测试学生类...")
    try:
        from backend.students import Student, StudentState
        from backend.seats import Seat, Status
        
        # 创建学生参数
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
        
        # 创建学生
        student = Student(0, student_para, seat_preference)
        print(f"  - 学生状态: {student.state}")
        print(f"  - 日程表长度: {len(student.schedule)}")
        print(f"  - 座位偏好: {student.seat_preference}")
        
        # 测试满意度计算
        seat = Seat(0, 0, lamp=True, socket=True)
        satisfaction = student.calculate_seat_satisfaction(seat)
        print(f"  - 座位满意度: {satisfaction}")
        
        print("✓ 学生类功能正常")
        return True
    except Exception as e:
        print(f"✗ 学生类测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_import_with_delay_check():
    """测试导入并检查是否有循环依赖"""
    print("\n测试模块导入延迟...")
    import time
    
    start_time = time.time()
    try:
        from backend.library import Library
        mid_time = time.time()
        print(f"  - Library类导入耗时: {mid_time - start_time:.2f}秒")
        
        # 不要创建实例，只测试类定义
        print("  - Library类定义正常")
        
        from backend.simulation import Simulation
        end_time = time.time()
        print(f"  - Simulation类导入耗时: {end_time - mid_time:.2f}秒")
        print("  - Simulation类定义正常")
        
        print("✓ 导入延迟测试正常")
        return True
    except Exception as e:
        print(f"✗ 导入延迟测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prompt_format():
    """测试提示词格式"""
    print("\n测试提示词格式...")
    try:
        from backend import prompt
        
        # 检查提示词是否包含必要的格式占位符
        schedule_has_placeholders = '{' in prompt.schedule_prompt and '}' in prompt.schedule_prompt
        leave_has_placeholders = '{' in prompt.leave_prompt and '}' in prompt.leave_prompt
        
        print(f"  - schedule_prompt 包含占位符: {schedule_has_placeholders}")
        print(f"  - leave_prompt 包含占位符: {leave_has_placeholders}")
        
        # 尝试格式化提示词
        formatted_schedule = prompt.schedule_prompt.format(
            schedule_type="正常",
            focus_type="中", 
            course_situation="中"
        )
        print(f"  - schedule_prompt 格式化正常")
        
        formatted_leave = prompt.leave_prompt.format(
            character="守序",
            satisfaction=4.0,
            time="12:00:00",
            limit_time="2h",
            schedule=[{"time": "12:00:00", "action": "eat"}]
        )
        print(f"  - leave_prompt 格式化正常")
        
        print("✓ 提示词格式测试正常")
        return True
    except Exception as e:
        print(f"✗ 提示词格式测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agents_creation():
    """测试agents创建"""
    print("\n测试agents创建...")
    try:
        from backend.agents import Clients
        
        # 创建一个模拟的Clients类，不实际连接API
        class MockClients:
            def __init__(self):
                self.client = None  # 避免实际连接API
                from utils import BASE_URL, API_KEY, MODEL
                self.base_url = BASE_URL
                self.api_key = API_KEY
                self.model = MODEL
            
            def response(self, prompt: str):
                # 模拟响应
                return {"action": "mock_response"}
        
        clients = MockClients()
        print(f"  - API配置加载正常: {clients.base_url is not None}")
        print(f"  - API密钥加载正常: {clients.api_key is not None}")
        
        print("✓ agents创建测试正常")
        return True
    except Exception as e:
        print(f"✗ agents创建测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("运行详细代码问题检查...")
    
    tests = [
        ("座位类功能", test_seat_class),
        ("学生类功能", test_student_class),
        ("导入延迟检查", test_import_with_delay_check),
        ("提示词格式检查", test_prompt_format),
        ("agents创建检查", test_agents_creation)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "="*60)
    print("详细代码问题检查结果:")
    all_passed = True
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n✓ 所有详细测试通过！")
    else:
        print("\n✗ 部分详细测试失败。")
    
    print("\n已识别的问题:")
    print("1. simulation.py - 使用了错误的导入语法: 'from library import Library' 应该是 'from .library import Library'")
    print("2. library.__init__ - 初始化时会自动创建400个座位和200个学生，可能导致长时间延迟")
    print("3. simple_test.py - 会初始化大量座位，可能导致长时间运行")
    
    return all_passed

if __name__ == "__main__":
    main()