"""Students.py
本文件实现学生类class Student
学生是图书馆模拟系统中的智能体，根据个人属性、座位偏好和日程安排
做出占用座位、离开座位、占座等决策
"""
from .agents import Clients
from enum import Enum
from datetime import datetime, timedelta
from .seats import Seat,Status

class StudentState(Enum):
    """学生状态枚举
    定义学生在图书馆系统中的各种状态
    """
    SLEEP = 1       # 休眠状态，不进行任何行为，不在图书馆
    LEARNING = 2    # 在图书馆学习状态，占用座位
    AWAY = 3        # 暂时离开但占座状态，座位被保留
    GONE = 4        # 完全离开状态，未占用任何座位

class Student:
    """
    学生类，模拟图书馆中学生的行为
    功能：
        1.自身状态感知（在座/占座/离开），座位信息等
        2.个人喜好（LLM）
        3.行为判断逻辑：
            1.选择座位
            2.状态改变
    """
    def __init__(self,student_id,student_para:dict,seat_preference:dict) -> None:
        """
        初始化学生对象

        Args:
            student_id: 学生唯一标识符
            student_para (dict): 学生基本属性参数
                - character: 个人性格（守序/利己）
                - schedule_type: 作息类型（早鸟/正常/夜猫子）
                - focus_type: 专注程度（高/中/低）
                - course_situation: 课程情况（多/中/少）
            seat_preference (dict): 座位偏好参数
                - lamp: 对台灯的偏好程度（0.0-1.0）
                - socket: 对插座的偏好程度（0.0-1.0）
                - space: 对空间充裕的偏好程度（0.0-1.0）
        """
        self.student_id = student_id  # 学生唯一标识符
        self._initialize_student_para(**student_para)  # 初始化学生基本属性
        self._initialize_seat_preference(**seat_preference)  # 初始化座位偏好
        self.seat = None  # 当前占用的座位对象，无座位时为None
        self.state = StudentState.SLEEP  # 当前状态，默认为休眠状态
        self.client = Clients()  # LLM客户端，用于智能决策
        self.schedule = []  # 学生日程表，由LLM生成
        self.generate_schedule()  # 初始化时生成日程表
        self.current_time = datetime(1900,1,1,7,0,0)  # 当前时间，从7:00:00开始
        self.time_delta = timedelta(minutes=30)  # 时间更新步长，与座位时间同步
        self.know_library_limit_reverse_time(timedelta(hours=1))  # 了解图书馆占座时间限制
    
    def _initialize_seat_preference(self,lamp:float,socket:float,space:float):
        """
        初始化座位偏好参数

        Args:
            lamp (float): 对台灯的偏好程度（0.0-1.0）
            socket (float): 对插座的偏好程度（0.0-1.0）
            space (float): 对空间充裕的偏好程度（0.0-1.0）
        """
        self.seat_preference = {
            "lamp": lamp,      # 对台灯的偏好
            "socket": socket,    # 对插座的偏好
            "space": space      # 对空间充裕的偏好
        }

    def _initialize_student_para(self,character="守序", schedule_type="正常", focus_type="中", course_situation="中"):
        """
        初始化学生基本属性参数

        Args:
            character (str): 个人性格（守序/利己）
            schedule_type (str): 作息类型（早鸟/正常/夜猫子）
            focus_type (str): 专注程度（高/中/低）
            course_situation (str): 课程情况（多/中/少）
        """
        self.student_para = {"character":character,
                             "schedule_type":schedule_type,
                             "focus_type":focus_type,
                             "course_situation":course_situation}

    def generate_schedule(self):
        """
        使用LLM生成学生日程表
        根据学生的个人属性生成一天的学习、生活安排
        日程表包含时间点和对应的行为动作
        """
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
        """
        设置学生了解的图书馆占座时间限制

        Args:
            limit_reverse_time (timedelta): 图书馆允许的最长占座时间
        """
        self.limit_reverse_time = limit_reverse_time

    def get_current_action(self):
        """
        根据当前时间获取应该执行的动作
        遍历日程表找到当前时间对应的行为动作

        Returns:
            str: 当前时间对应的行为动作（start, learn, eat, course, rest, end等）
        """
        # 找到当前时间对应的动作，返回最近的时间点的动作
        for i in range(len(self.schedule) - 1, -1, -1):
            schedule_time = self.schedule[i]["time"]
            schedule_time = datetime.strptime(schedule_time,"%H:%M:%S")
            if schedule_time <= self.current_time:
                return self.schedule[i]["action"]
        return "end"  # 默认为结束状态

    def calculate_seat_satisfaction(self,seat=None):
        """
        计算座位满意度(1-5分)
        根据座位属性和个人偏好计算学生对座位的满意度

        Args:
            seat (Seat): 要评估的座位，如果为None则评估当前座位

        Returns:
            float: 座位满意度分数，分数越高表示越满意
        """
        self.satisfaction = 1  # 基础满意度为1
        if seat is None:
            if self.seat is not None:
                seat = self.seat  # 如果没有指定座位，评估当前座位
            else:
                return self.satisfaction
        # 根据座位属性和个人偏好计算满意度
        if seat.lamp:  # 有台灯增加满意度
            self.satisfaction += 3 * self.seat_preference["lamp"]
        if seat.socket:  # 有插座增加满意度
            self.satisfaction += 3 * self.seat_preference["socket"]
        if seat.window:  # 靠窗座位增加满意度
            self.satisfaction += 1
            # 考虑周围拥挤程度对满意度的影响
            self.satisfaction += 3*(1-seat.crowded_para)*self.seat_preference["space"]
        return self.satisfaction

    def _should_reverse_seat(self) -> bool: 
        """
        使用LLM判断离开时是否占座
        根据当前满意度、个人性格、图书馆规则等因素智能决策

        Returns:
            bool: True表示占座离开，False表示完全离开
        """
        if self.seat is None:
            return False  # 没有座位时不需要判断占座

        self.calculate_seat_satisfaction()  # 计算当前座位满意度
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
        """
        占用座位
        更新学生状态和座位状态，建立学生与座位的关联

        Args:
            seat (Seat): 要占用的座位对象
        """
        self.state = StudentState.LEARNING  # 更新学生状态为学习状态
        self.seat = seat  # 记录当前占用的座位
        self.seat.take(self.student_id)  # 通知座位被占用
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
        """
        离开座位
        根据智能决策决定是完全离开还是占座离开
        """
        if self.state == StudentState.LEARNING:  # 只有学习状态下才可离开
            boolean = self._should_reverse_seat()  # 智能决策是否占座
            self.seat.leave(boolean)  # type: ignore # 通知座位离开
            if boolean:  # 根据决策更新学生状态
                self.state = StudentState.AWAY  # 占座离开，状态为暂时离开
            else:
                self.state = StudentState.GONE  # 完全离开，状态为完全离开

    def update(self):
        """
        更新学生时间
        每次系统时间步进时调用，保持学生时间与系统同步
        """
        self.current_time += self.time_delta

    def choose_seat(self,seats:list[Seat]) -> bool:
        """
        选择座位的主函数
        根据当前状态决定如何处理座位选择

        Args:
            seats (list[Seat]): 可选的座位列表

        Returns:
            bool: 是否成功选择到座位
        """
        if self.state == StudentState.LEARNING:
            return True  # 已在学习状态，无需选择
        elif self.state == StudentState.AWAY:
            # 暂时离开状态，先尝试回到原座位
            if self.seat and (self.seat.status == Status.reverse or self.seat.status == Status.signed):
                self.seat.back()  # 尝试回到原座位
                return True
            else:
                whether_take_seat = self.choose(seats)  # 否则选择新座位
        elif self.state == StudentState.GONE:
            whether_take_seat = self.choose(seats)  # 完全离开状态，选择新座位
        return whether_take_seat

    def choose(self,seats:list[Seat]):
        """
        从可选座位中选择最满意的座位

        Args:
            seats (list[Seat]): 可选的座位列表

        Returns:
            bool: 是否成功选择到座位
        """
        grade = 1  # 最低满意度
        chosen_seat = None  # 选择的座位
        for seat in seats:
            if seat.status == Status.vacant:  # 只考虑空闲座位
                next_grade = self.calculate_seat_satisfaction(seat)  # 计算满意度
                if next_grade >= grade:  # 选择满意度最高的座位
                    grade = next_grade
                    chosen_seat = seat
        if isinstance(chosen_seat, Seat):  # 如果找到合适的座位
            self.take_seat(chosen_seat)  # 占用座位
            return True
        return False  # 没有找到合适的座位

    # 以下为工厂方法，用于创建不同类型的学生
    @classmethod
    def create_humanities_diligent_student(cls, student_id):
        """创建勤奋的文科生"""
        student_para = {
            "character": "守序",  # 性格守序，遵守规则
            "schedule_type": "正常",  # 正常作息
            "focus_type": "高",  # 专注度高
            "course_situation": "多"  # 课程多
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
            "character": "守序",  # 性格守序
            "schedule_type": "正常",  # 正常作息
            "focus_type": "中",  # 专注度中等
            "course_situation": "中"  # 课程中等
        }
        seat_preference = {
            "lamp": 0.5,  # 中等对台灯需求
            "socket": 0.5,  # 中等对插座需求
            "space": 0.5   # 中等对空间需求
        }
        return cls(student_id, student_para, seat_preference)
    
    @classmethod
    def create_humanities_lazy_student(cls, student_id):
        """创建懒惰的文科生"""
        student_para = {
            "character": "利己",  # 性格利己
            "schedule_type": "晚",  # 晚间作息
            "focus_type": "低",  # 专注度低
            "course_situation": "少"  # 课程少
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
            "character": "守序",  # 性格守序
            "schedule_type": "早",  # 早起作息
            "focus_type": "高",  # 专注度高
            "course_situation": "多"  # 课程多
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
            "character": "守序",  # 性格守序
            "schedule_type": "正常",  # 正常作息
            "focus_type": "中",  # 专注度中等
            "course_situation": "中"  # 课程中等
        }
        seat_preference = {
            "lamp": 0.6,  # 中等对台灯需求
            "socket": 0.6,  # 中等对插座需求
            "space": 0.5   # 中等对空间需求
        }
        return cls(student_id, student_para, seat_preference)
    
    @classmethod
    def create_science_lazy_student(cls, student_id):
        """创建懒惰的理科生"""
        student_para = {
            "character": "利己",  # 性格利己
            "schedule_type": "晚",  # 晚间作息
            "focus_type": "低",  # 专注度低
            "course_situation": "少"  # 课程少
        }
        seat_preference = {
            "lamp": 0.4,  # 中等对台灯需求
            "socket": 0.7,    # 可能需要设备充电
            "space": 0.3      # 对空间要求不高
        }
        return cls(student_id, student_para, seat_preference)
    
    @classmethod
    def create_engineering_diligent_student(cls, student_id):
        """创建勤奋的工科生"""
        student_para = {
            "character": "守序",  # 性格守序
            "schedule_type": "早",  # 早起作息
            "focus_type": "高",  # 专注度高
            "course_situation": "多"  # 课程多
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
            "character": "守序",  # 性格守序
            "schedule_type": "正常",  # 正常作息
            "focus_type": "中",  # 专注度中等
            "course_situation": "中"  # 课程中等
        }
        seat_preference = {
            "lamp": 0.7,  # 较高对台灯需求
            "socket": 0.7,  # 较高对插座需求
            "space": 0.6   # 较高对空间需求
        }
        return cls(student_id, student_para, seat_preference)
    
    @classmethod
    def create_engineering_lazy_student(cls, student_id):
        """创建懒惰的工科生"""
        student_para = {
            "character": "利己",  # 性格利己
            "schedule_type": "晚",  # 晚间作息
            "focus_type": "低",  # 专注度低
            "course_situation": "少"  # 课程少
        }
        seat_preference = {
            "lamp": 0.5,  # 中等对台灯需求
            "socket": 0.8,    # 仍需给设备充电
            "space": 0.4      # 对空间要求不高
        }
        return cls(student_id, student_para, seat_preference)