"""Students.py
本文件实现学生类class Student
"""
from .agents import Clients
from enum import Enum
from datetime import datetime, timedelta
from .seats import Seat,Status

class StudentState(Enum):
    """学生状态枚举"""
    SLEEP = 1       # 休眠状态，不进行任何行为
    LEARNING = 2    # 在图书馆学习
    AWAY = 3        # 暂时离开但占座
    GONE = 4        # 完全离开（释放座位）

class Student:
    """
    功能：
        1.自身状态感知（在座/占座/离开），座位信息等
        2.个人喜好（LLM）
        3.行为判断逻辑：
            1.选择座位
            2.状态改变
    """
    def __init__(self,student_id,student_para:dict,seat_preference:dict) -> None:
        self.student_id = student_id
        self._initialize_student_para(**student_para)
        self._initialize_seat_preference(**seat_preference)
        self.seat = None
        self.state = StudentState.SLEEP  # 当前状态
        self.client = Clients()
        self.schedule = []  # 学生日程表，由LLM生成
        self.generate_schedule()  # 初始化时生成日程表
        self.current_time = datetime(1900,1,1,7,0,0)
        self.time_delta = timedelta(minutes=30)
        self.know_library_limit_reverse_time(timedelta(hours=1))
    
    def _initialize_seat_preference(self,lamp:float,socket:float,space:float):
        self.seat_preference = {
            "lamp": lamp,      # 对台灯的偏好
            "socket": socket,    # 对插座的偏好
            "space": space      # 对空间充裕的偏好
        }

    def _initialize_student_para(self,character="守序", schedule_type="正常", focus_type="中", course_situation="中"):
        self.student_para = {"character":character,
                             "schedule_type":schedule_type,
                             "focus_type":focus_type,
                             "course_situation":course_situation}

    def generate_schedule(self):
        """使用LLM生成学生日程表"""
        from .prompt import schedule_prompt
        formatted_prompt = schedule_prompt.format(
            schedule_type=self.student_para["schedule_type"],
            focus_type=self.student_para["focus_type"],
            course_situation=self.student_para["course_situation"]
        )
        response = self.client.response(formatted_prompt)
        if isinstance(response, list):
            self.schedule = response
        else:
            # 如果LLM响应格式不正确，使用默认日程
            self.schedule = [
                {"time": "08:00:00", "action": "start"},
                {"time": "08:00:00", "action": "eat"},
                {"time": "09:00:00", "action": "learn"},
                {"time": "12:00:00", "action": "eat"},
                {"time": "13:00:00", "action": "learn"},
                {"time": "17:00:00", "action": "eat"},
                {"time": "18:00:00", "action": "learn"},
                {"time": "22:00:00", "action": "end"}
            ]

    def know_library_limit_reverse_time(self,limit_reverse_time:timedelta):
        self.limit_reverse_time = limit_reverse_time

    def get_current_action(self):
        """根据当前时间获取应该执行的动作"""
        # 找到当前时间对应的动作
        for i in range(len(self.schedule) - 1, -1, -1):
            schedule_time = self.schedule[i]["time"]
            schedule_time = datetime.strptime(schedule_time,"%H:%M:%S")
            if schedule_time <= self.current_time:
                return self.schedule[i]["action"]
        return "end"  # 默认为结束状态

    def calculate_seat_satisfaction(self,seat=None):
        """计算座位满意度(1-5分)"""
        self.satisfaction = 1
        if seat is None:
            if self.seat is not None:
                seat = self.seat
            else:
                return self.satisfaction
        if seat.lamp:
            self.satisfaction += 3 * self.seat_preference["lamp"]
        if seat.socket:
            self.satisfaction += 3 * self.seat_preference["socket"]
        if seat.window:
            self.satisfaction += 1
            self.satisfaction += 3*(1-seat.crowded_para)*self.seat_preference["space"]
        return self.satisfaction

    def _should_reverse_seat(self) -> bool: 
        """判断离开时是否占座"""
        if self.seat is None:
            return False  # 没有座位时不需要判断占座

        self.calculate_seat_satisfaction()
        from .prompt import leave_prompt
        formatted_prompt = leave_prompt.format(
            character=self.student_para["character"],
            satisfaction=self.satisfaction,
            time=str(self.current_time),
            limit_time=f"{self.limit_reverse_time}h",
            schedule=self.schedule
        )
        response = self.client.response(formatted_prompt)

        if isinstance(response, dict) and "action" in response:
            action = response["action"]
            return action == "reverse"  # reverse表示占座
        else:
            # 如果LLM响应格式不正确，使用默认逻辑
            # 满意度高且性格守序的学生倾向于占座
            return self.satisfaction >= 3 and self.student_para["character"] == "守序"
        
    def take_seat(self,seat:Seat):
        self.state = StudentState.LEARNING
        self.seat = seat
        self.seat.take(self.student_id)
        '''情况列举：Student--Seat
            1. 在图书馆（LEARNING）--taken
            2. 不在图书馆：
                2.1. AWAY--reverse/signed/vacant
                2.2. GONE--None
            3. SLEEP--None
            
            核心函数：  take_seat(seat):
                                    LEARNING,self.seat = seat
                        leave_seat():
                                    LEARNING时，bool，->AWAY/GONE
                                    其他： pass
                        choose():
                                    LEARNING:pass
                                    AWAY:
                                        seat--vacant->GONE
                                        seat -> None
                                    GONE:
                                        评分，选
                                        '''
    def leave_seat(self):
        if self.state == StudentState.LEARNING:
            boolen = self._should_reverse_seat()
            self.seat.leave(boolen)  # type: ignore
            if boolen:
                self.state = StudentState.AWAY
            else:
                self.state = StudentState.GONE

    def update(self):
        self.current_time += self.time_delta

    def choose_seat(self,seats:list[Seat]) -> bool:
        if self.state == StudentState.LEARNING:
            return True
        elif self.state == StudentState.AWAY:
            if self.seat and (self.seat.status == Status.reverse or self.seat.status == Status.signed):
                self.seat.back()
                return True
            else:
                whether_take_seat = self.choose(seats)
        elif self.state == StudentState.GONE:
            whether_take_seat = self.choose(seats)
        return whether_take_seat

    def choose(self,seats:list[Seat]):
        grade = 1
        chosen_seat = None
        for seat in seats:
            if seat.status == Status.vacant:
                next_grade = self.calculate_seat_satisfaction(seat)
                if next_grade>=grade:
                    grade = next_grade
                    chosen_seat = seat
        if type(chosen_seat) == Seat:
            self.take_seat(chosen_seat)
            return True
        return False

    
    @classmethod
    def create_humanities_diligent_student(cls, student_id):
        """创建勤奋的文科生"""
        student_para = {
            "character": "守序", 
            "schedule_type": "正常", 
            "focus_type": "高", 
            "course_situation": "多"
        }
        seat_preference = {
            "lamp": 0.7,      # 文科生喜欢光线好的环境阅读
            "socket": 0.4,    # 对插座需求一般
            "space": 0.6      # 需要安静宽松的环境
        }
        return cls(student_id, student_para, seat_preference)
    
    @classmethod
    def create_humanities_medium_student(cls, student_id):
        """创建中等程度的文科生"""
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
        return cls(student_id, student_para, seat_preference)
    
    @classmethod
    def create_humanities_lazy_student(cls, student_id):
        """创建懒惰的文科生"""
        student_para = {
            "character": "利己", 
            "schedule_type": "晚", 
            "focus_type": "低", 
            "course_situation": "少"
        }
        seat_preference = {
            "lamp": 0.3,      # 对光线要求不高
            "socket": 0.6,    # 可能需要给设备充电
            "space": 0.4      # 对环境要求不高
        }
        return cls(student_id, student_para, seat_preference)
    
    @classmethod
    def create_science_diligent_student(cls, student_id):
        """创建勤奋的理科生"""
        student_para = {
            "character": "守序", 
            "schedule_type": "早", 
            "focus_type": "高", 
            "course_situation": "多"
        }
        seat_preference = {
            "lamp": 0.8,      # 理科生需要好的光线来计算和阅读图表
            "socket": 0.7,    # 需要给计算器或笔记本供电
            "space": 0.5      # 需要足够的桌面空间
        }
        return cls(student_id, student_para, seat_preference)
    
    @classmethod
    def create_science_medium_student(cls, student_id):
        """创建中等程度的理科生"""
        student_para = {
            "character": "守序", 
            "schedule_type": "正常", 
            "focus_type": "中", 
            "course_situation": "中"
        }
        seat_preference = {
            "lamp": 0.6,
            "socket": 0.6,
            "space": 0.5
        }
        return cls(student_id, student_para, seat_preference)
    
    @classmethod
    def create_science_lazy_student(cls, student_id):
        """创建懒惰的理科生"""
        student_para = {
            "character": "利己", 
            "schedule_type": "晚", 
            "focus_type": "低", 
            "course_situation": "少"
        }
        seat_preference = {
            "lamp": 0.4,
            "socket": 0.7,    # 可能需要设备充电
            "space": 0.3      # 对空间要求不高
        }
        return cls(student_id, student_para, seat_preference)
    
    @classmethod
    def create_engineering_diligent_student(cls, student_id):
        """创建勤奋的工科生"""
        student_para = {
            "character": "守序", 
            "schedule_type": "早", 
            "focus_type": "高", 
            "course_situation": "多"
        }
        seat_preference = {
            "lamp": 0.9,      # 工科生需要极好的光线进行复杂设计和编程
            "socket": 0.9,    # 需要给电脑、设备供电
            "space": 0.7      # 需要大量桌面空间进行设计和计算
        }
        return cls(student_id, student_para, seat_preference)
    
    @classmethod
    def create_engineering_medium_student(cls, student_id):
        """创建中等程度的工科生"""
        student_para = {
            "character": "守序", 
            "schedule_type": "正常", 
            "focus_type": "中", 
            "course_situation": "中"
        }
        seat_preference = {
            "lamp": 0.7,
            "socket": 0.7,
            "space": 0.6
        }
        return cls(student_id, student_para, seat_preference)
    
    @classmethod
    def create_engineering_lazy_student(cls, student_id):
        """创建懒惰的工科生"""
        student_para = {
            "character": "利己", 
            "schedule_type": "晚", 
            "focus_type": "低", 
            "course_situation": "少"
        }
        seat_preference = {
            "lamp": 0.5,
            "socket": 0.8,    # 仍需给设备充电
            "space": 0.4
        }
        return cls(student_id, student_para, seat_preference)
