from backend.students import Student

# 测试创建学生对象，传入预定义的日程避免API调用
print('测试创建学生对象...')
default_schedule = [
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

student = Student(1, 
                  {'character': '守序', 'schedule_type': '正常', 'focus_type': '中', 'course_situation': '中'}, 
                  {'lamp': 0.5, 'socket': 0.5, 'space': 0.5}, 
                  schedule=default_schedule,
                  library_capacity=100, 
                  total_students=50)

print('学生创建成功！')
print(f'student_id: {student.student_id}')
print(f'library_capacity: {student.library_capacity}')
print(f'total_students: {student.total_students}')
print(f'schedule: {student.schedule[0:2]}...')  # 只打印前两项