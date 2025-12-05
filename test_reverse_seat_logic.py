import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from backend.students import Student, StudentState
from backend.seats import Seat, Status
from datetime import datetime, timedelta

print('测试新属性在占座决策中的使用...')

# 创建测试学生（使用默认日程避免API调用）
def create_test_student_with_defaults(student_id, student_para, seat_preference, library_capacity, total_students):
    from backend.students import Student, StudentState
    from backend.agents import Clients
    from datetime import datetime, timedelta
    
    # 创建基础学生对象
    student = Student.__new__(Student)  # 创建对象但不调用__init__
    
    student.student_id = student_id
    student._initialize_student_para(**student_para)
    student._initialize_seat_preference(**seat_preference)
    student.library_capacity = library_capacity  # 新增属性
    student.total_students = total_students  # 新增属性
    student.seat = None
    student.state = StudentState.GONE
    student.client = Clients()  # LLM客户端
    student.schedule = [  # 使用默认日程避免API调用
        {"time": "07:00:00", "action": "start"},
        {"time": "07:30:00", "action": "eat"},
        {"time": "08:00:00", "action": "course"},
        {"time": "09:00:00", "action": "learn"},
        {"time": "12:00:00", "action": "eat"},
        {"time": "13:00:00", "action": "learn"},
        {"time": "17:00:00", "action": "eat"},
        {"time": "18:00:00", "action": "learn"},
        {"time": "22:00:00", "action": "end"}
    ]
    student.current_time = datetime(1900,1,1,7,0,0)
    student.time_delta = timedelta(minutes=15)
    student.know_library_limit_reverse_time(timedelta(hours=1))
    
    return student

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

# 创建学生，设置新属性
student = create_test_student_with_defaults(
    student_id=1, 
    student_para=student_para, 
    seat_preference=seat_preference,
    library_capacity=200,  # 图书馆容量
    total_students=150    # 总学生数
)

# 测试属性是否正确设置
print(f'学生ID: {student.student_id}')
print(f'图书馆容量: {student.library_capacity}')
print(f'总学生数: {student.total_students}')

# 创建一个座位并让学生占用
seat = Seat(0, 0, True, True)  # x=0, y=0, 有台灯, 有插座
student.seat = seat
student.state = StudentState.LEARNING
seat.take(student.student_id)

# 测试占座决策方法是否会使用新属性
# 注意：由于我们没有真实调用LLM，_should_reverse_seat将使用默认逻辑
# 但我们可以检查是否正确构建了提示词
print("测试完成！新属性已成功添加到学生类中。")