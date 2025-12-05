import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from backend.library import Library
from backend.students import Student

print('测试创建图书馆和学生对象（不调用LLM API）...')

# 创建一个自定义的测试学生，使用默认日程避免API调用
def create_test_student_with_defaults(student_id, student_para, seat_preference, library_capacity, total_students):
    from backend.students import Student, StudentState
    from backend.agents import Clients
    from datetime import datetime, timedelta
    from backend.seats import Status
    
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

# 创建图书馆
lib = Library()
lib.initialize_seats(3, 3)

# 创建测试学生，使用默认日程避免API调用
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

# 创建几个测试学生
for i in range(9):
    student = create_test_student_with_defaults(
        student_id=i, 
        student_para=student_para, 
        seat_preference=seat_preference,
        library_capacity=len(lib.seats),  # 使用座位总数作为容量
        total_students=9  # 总学生数
    )
    lib.students.append(student)
    lib._count += 1

print('图书馆和学生创建成功！')
print('座位数量:', len(lib.seats))
print('学生数量:', len(lib.students))
if lib.students:
    print('第一个学生的library_capacity:', lib.students[0].library_capacity)
    print('第一个学生的total_students:', lib.students[0].total_students)

print("测试完成！")