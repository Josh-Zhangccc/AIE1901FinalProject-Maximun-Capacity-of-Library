from seats import Seat,Status
from students import Student,StudentState
import random
from datetime import datetime, timedelta
random.seed(1)

#Seat含有的属性：lamp,socket,x,y
#Students含有的属性：lamp:float,socket:float,space:float///character="守序", schedule_type="正常", focus_type="中", course_situation="中"
class Library:
    def __init__(self) -> None:
        self.seats:list[Seat] = []
        self.seats_map = {}
        self.students:list[Student] = []
        self.current_time = datetime(1900,1,1,7)
        self.time_delta = timedelta(minutes=15)
        self._count = 0
        self.limit_reversed_time = timedelta(hours=1)
        self.initialize_seats()
        self.initialize_students()
        self.unsatisfied = 0

    @staticmethod
    def _random_assign(random_num:int):
        random_nums = [random.random() for _ in range(random_num)] #@list
        return random_nums

    def initialize_seats(self,lamp_rate:float=0.5,socket_rate:float=0.5):
        self.seats.clear()
        lamp_list = [lamp>=lamp_rate for lamp in self._random_assign(20)]
        socket_list = [socket>=socket_rate for socket in self._random_assign(20)]
        for x in range(20):
            for y in range(20):
                for lamp,socket in zip(lamp_list,socket_list):
                    self.seats.append(Seat(x,y,lamp,socket))
        for seat in self.seats:
            self.seats_map[seat.coordinate] = seat

    def _init_students_with_different_major(self,students_number:int,type:str):
        _list = self._random_assign(students_number)
        diligent_list = [i>=0.7 for i in _list]
        medium_list = [0.3<i<0.7 for i in _list]
        lazy_list = [i<=0.3 for i in _list]

        match type:
            case 'humanities':
                new_students = [Student.create_humanities_diligent_student(self._count + idx)  # idx 是过滤后的索引，避免 count 断层
                               for idx, is_diligent in enumerate(diligent_list) if is_diligent
                               ]
                self.students.extend(new_students)
                self._count += len(new_students)
                
                new_students = [Student.create_humanities_medium_student(self._count + idx)  
                               for idx, is_medium in enumerate(medium_list) if is_medium]  
                self.students.extend(new_students)
                self._count += len(new_students)
                
                new_students = [Student.create_humanities_lazy_student(self._count + idx)  
                               for idx, is_lazy in enumerate(lazy_list) if is_lazy]  
                self.students.extend(new_students)
                self._count += len(new_students)

            case 'science':
                new_students = [Student.create_science_diligent_student(self._count + idx)
                               for idx, is_diligent in enumerate(diligent_list) if is_diligent
                               ]
                self.students.extend(new_students)
                self._count += len(new_students)
                
                new_students = [Student.create_science_medium_student(self._count + idx)  
                               for idx, is_medium in enumerate(medium_list) if is_medium]  
                self.students.extend(new_students)
                self._count += len(new_students)
                
                new_students = [Student.create_science_lazy_student(self._count + idx)  
                               for idx, is_lazy in enumerate(lazy_list) if is_lazy]  
                self.students.extend(new_students)
                self._count += len(new_students)

            case 'engineering':
                new_students = [Student.create_engineering_diligent_student(self._count + idx)
                               for idx, is_diligent in enumerate(diligent_list) if is_diligent
                               ]
                self.students.extend(new_students)
                self._count += len(new_students)
                
                new_students = [Student.create_engineering_medium_student(self._count + idx)  
                               for idx, is_medium in enumerate(medium_list) if is_medium]  
                self.students.extend(new_students)
                self._count += len(new_students)
                
                new_students = [Student.create_engineering_lazy_student(self._count + idx)  
                               for idx, is_lazy in enumerate(lazy_list) if is_lazy]  
                self.students.extend(new_students)
                self._count += len(new_students)

    def initialize_students(self,num:int=200,humanities:float=0.3,science:float=0.3):
        self.students.clear()
        humanities = int((num * humanities))
        science = int(num * science)
        engineering = num - humanities - science
        for population,subject in zip([humanities,science,engineering],["humanities","science","engineering"]):
            self._init_students_with_different_major(population,subject)

    def set_limit_reversed_time(self,time):
        if isinstance(time,timedelta):
            self.limit_reversed_time = time
        if isinstance(time,str):
            time_list = time.split(":")
            hour = eval(time_list[0])
            minute = eval(time_list[1])
            self.limit_reversed_time = timedelta(hours=hour,minutes=minute)
        raise TypeError


    def update(self):
        self.current_time+=self.time_delta
        for seat in self.seats:
            seat.update()
            self.calculate_each_seat_crowded_para()
        for student in self.students:
            student.update
            self.next_step_of_each_student(student)

    def sign_seat(self):
        for seat in self.seats:
            if seat.status == Status.reverse:
                seat.sign()

    def clear_seat(self):
        for seat in self.seats:
            if seat.status == Status.signed:
                if seat.taken_time - datetime(1900,1,1,7) >= self.limit_reversed_time:
                    seat.clear()

    def get_unsatisfied(self):
        self.unsatisfied += 1

    def count_unsatisfied(self):
        return self.unsatisfied

    def output_seat_info(self):
        seats_dic = {}
        for seat in self.seats:
            seats_dic[seat.coordinate] = {"lamp":seat.lamp,
                                          "socket":seat.socket,
                                          "window":seat.window,
                                          "status":seat.status}

    def next_step_of_each_student(self,student:Student):
        action = student.get_current_action()
        match action:
            case "start":
                pass
            case "learn":
                if student.state != StudentState.LEARNING:
                    take_seat = student.choose_seat(self.seats)
                    if not take_seat:
                        self.get_unsatisfied()
            case "end":
                student.state = StudentState.SLEEP
            case _:
                student.leave_seat()


    def count_taken_seats(self):
        count = 0
        for seat in self.seats:
            if seat.status != Status.vacant:
                count += 1
        return len(self.seats) - count
    

    def count_reversed_seats(self):
        count = 0
        for seat in self.seats:
            if seat.status == Status.reverse or seat.status == Status.signed:
                count += 1
        return count

    def calculate_each_seat_crowded_para(self):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0), (1, 1)]
        
        for seat in self.seats:
            x,y = seat.coordinate
            crowded_para = 0
            len_around_seat = 0
            for dx,dy in directions:
                nx = x + dx
                ny = y + dy
                around_seat = self.seats_map.get((nx,ny),None)
                if around_seat:
                    len_around_seat += 1
                    if around_seat.status != Status.vacant:
                        crowded_para += 1
                    if around_seat.window:
                        crowded_para -= 0.5
            crowded_para /= len_around_seat
            seat.set_crowded_para(crowded_para)
