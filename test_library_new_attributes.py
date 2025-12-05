from backend.library import Library
from backend.students import Student

print('测试创建图书馆和学生对象...')
lib = Library()
lib.initialize_seats(3, 3)
lib.initialize_students(9)
print('图书馆和学生创建成功！')
print('座位数量:', len(lib.seats))
print('学生数量:', len(lib.students))
if lib.students:
    print('第一个学生的library_capacity:', lib.students[0].library_capacity)
    print('第一个学生的total_students:', lib.students[0].total_students)
    
print("测试完成！")