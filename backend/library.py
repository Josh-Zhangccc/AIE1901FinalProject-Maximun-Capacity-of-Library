from seats import Seat
from students import Student,StudentState
import random
from datetime import datetime, timedelta
random.seed(1)

#Seat含有的属性：lamp,socket,x,y
#Students含有的属性：lamp:float,socket:float,space:float///character="守序", schedule_type="正常", focus_type="中", course_situation="中"
class Library:
    def __init__(self) -> None:
        self.seats = []
        self.students = []
        self.current_time = datetime(1900,1,1,7)
        self.time_delta = timedelta(minutes=15)
        self._count = 0
    @staticmethod
    def _random_assign(random_num:int):
        random_nums = [random.random() for _ in range(random_num)] #@list
        return random_nums

    def initialize_seats(self,lamp_rate:float=0.5,socket_rate:float=0.5):
        lamp_list = [lamp>=lamp_rate for lamp in self._random_assign(20)]
        socket_list = [socket>=socket_rate for socket in self._random_assign(20)]
        for x in range(20):
            for y in range(20):
                for lamp,socket in zip(lamp_list,socket_list):
                    self.seats.append(Seat(x,y,lamp,socket))
    
    def _init_students_with_different_major(self,students_number:int,type:str):
        _list = self._random_assign(students_number)
        diligent_list = [i>=0.7 for i in _list]
        medium_list = [0.3<i<0.5 for i in _list]
        lazy_list = [i<=0.3 for i in _list]

        match type:
            case 'humanities':
                for i in diligent_list:
                     new_students = [Student.create_humanities_diligent_student(self._count + idx)  # idx 是过滤后的索引，避免 count 断层
                                    for idx, i in enumerate(diligent_list)if i
                                    ]
                self.students.extend(new_students)
                self._count += len(new_students)
                for i in medium_list:
                    new_students = [Student.create_humanities_medium_student(self._count + idx)  
                                    for idx, i in enumerate(diligent_list)if i]  
                self.students.extend(new_students)
                self._count += len(new_students)
                for i in lazy_list:
                    new_students = [Student.create_humanities_lazy_student(self._count + idx)  
                                    for idx, i in enumerate(diligent_list)if i]  
                self.students.extend(new_students)
                self._count += len(new_students)




    def initialize_students(self,num:int=200,humanities:float=0.3,science:float=0.3):
        humanities = int((num * humanities))
        science = int(num * science)
        engineering = num - humanities - science
        

    def update(self):
        pass

    def sign_seat(self):
        pass

    def clear_seat(self):
        pass

    def count_unsatisfied(self):
        pass

    def output_seat_info(self):
        pass

    def next_step_of_each_student(self):
        pass

    def count_taken_seats(self):
        pass

    def count_reversed_seats(self):
        pass

    def calculate_each_seat_crowded_para(self):
        pass



