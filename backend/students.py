"""Students.py
本文件实现学生类class Student
"""
from agents import Clients
from enum import Enum
from datetime import datetime, timedelta

class StudentState(Enum):
    """学生状态枚举"""
    NOT_IN_LIB = 1  # 不在图书馆
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
    def __init__(self, student_id, character="守序", schedule_type="正常", focus_type="中", course_situation="中"):
        self.student_id = student_id  # 学生唯一标识
        self.character = character  # 个人性格：守序/利己
        self.schedule_type = schedule_type  # 作息类型：早鸟/正常/夜猫子
        self.focus_type = focus_type  # 专注类型：高/中/低
        self.course_situation = course_situation  # 课程情况：多/中/少
        self.seat_preference = {
            "lamp": 0.3,      # 对台灯的偏好
            "socket": 0.6,    # 对插座的偏好
            "space": 0.1      # 对空间充裕的偏好
        }
        self.schedule = []  # 学生日程表，由LLM生成
        self.current_schedule_index = 0  # 当前日程索引
        self.state = StudentState.NOT_IN_LIB  # 当前状态
        self.assigned_seat = None  # 分配的座位
        self.client = Clients()  # LLM客户端
        self.generate_schedule()  # 初始化时生成日程表

    def generate_schedule(self):
        """使用LLM生成学生日程表"""
        from prompt import schedule_prompt
        formatted_prompt = schedule_prompt.format(
            schedule_type=self.schedule_type,
            focus_type=self.focus_type,
            course_situation=self.course_situation
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

    def get_current_action(self, current_time_str):
        """根据当前时间获取应该执行的动作"""
        # 找到当前时间对应的动作
        for i in range(len(self.schedule) - 1, -1, -1):
            schedule_time = self.schedule[i]["time"]
            if schedule_time <= current_time_str:
                return self.schedule[i]["action"]
        return "end"  # 默认为结束状态

    def calculate_seat_satisfaction(self, seat):
        """计算座位满意度(1-5分)"""
        satisfaction = 1  # 基础分
        if seat.lamp:
            satisfaction += self.seat_preference["lamp"] * 4  # lamp最高加4分
        if seat.socket:
            satisfaction += self.seat_preference["socket"] * 4  # socket最高加4分

        # 计算周围空间满意度（检查周围座位被占用情况）
        # 这里简化为假设我们知道图书馆布局，暂时只考虑座位本身属性
        return min(5, round(satisfaction))

    def should_leave_seat(self, current_time_str, library_limit_time, seat=None):
        """判断离开时是否占座"""
        if seat is None:
            return False  # 没有座位时不需要判断占座

        satisfaction = self.calculate_seat_satisfaction(seat) if seat else 1

        from prompt import leave_prompt
        formatted_prompt = leave_prompt.format(
            character=self.character,
            satisfaction=satisfaction,
            time=current_time_str,
            limit_time=f"{library_limit_time}h",
            schedule=self.schedule
        )
        response = self.client.response(formatted_prompt)

        if isinstance(response, dict) and "action" in response:
            action = response["action"]
            return action == "reverse"  # reverse表示占座
        else:
            # 如果LLM响应格式不正确，使用默认逻辑
            # 满意度高且性格守序的学生倾向于占座
            return satisfaction >= 3 and self.character == "守序"

    def update_state(self, current_time_str, library_limit_time, available_seats=None):
        """更新学生状态"""
        current_action = self.get_current_action(current_time_str)

        if current_action == "end":
            # 一天结束，离开图书馆
            if self.assigned_seat:
                should_reverse = self.should_leave_seat(current_time_str, library_limit_time, self.assigned_seat)
                if should_reverse:
                    self.state = StudentState.AWAY
                else:
                    self.state = StudentState.GONE
            else:
                self.state = StudentState.NOT_IN_LIB

        elif current_action == "start" or current_action == "learn":
            # 需要学习，应在图书馆
            if self.state == StudentState.NOT_IN_LIB or self.state == StudentState.GONE:
                # 寻找座位
                if available_seats:
                    seat = self.find_best_seat(available_seats)
                    if seat:
                        seat.take(self.student_id)
                        self.assigned_seat = seat
                        self.state = StudentState.LEARNING
            elif self.state == StudentState.AWAY:
                # 回到占座的座位
                if self.assigned_seat and self.assigned_seat.status.name == 'reverse':
                    self.assigned_seat.take(self.student_id)
                    self.state = StudentState.LEARNING

        elif current_action == "eat" or current_action == "course" or current_action == "rest":
            # 需要离开座位
            if self.assigned_seat:
                should_reverse = self.should_leave_seat(current_time_str, library_limit_time, self.assigned_seat)
                if should_reverse:
                    self.assigned_seat.leave(reverse=False)  # 暂时离开但占座
                    self.state = StudentState.AWAY
                else:
                    self.assigned_seat.leave(reverse=True)  # 完全离开
                    self.assigned_seat = None
                    self.state = StudentState.NOT_IN_LIB
            else:
                # 没有座位，状态保持不变
                self.state = StudentState.NOT_IN_LIB

    def find_best_seat(self, available_seats):
        """根据偏好寻找最佳座位"""
        if not available_seats:
            return None

        best_seat = None
        best_satisfaction = -1

        for seat in available_seats:
            if seat.status.name == 'vacant':  # 只考虑空闲座位
                satisfaction = self.calculate_seat_satisfaction(seat)
                if satisfaction > best_satisfaction:
                    best_satisfaction = satisfaction
                    best_seat = seat

        return best_seat

    def get_state_description(self):
        """获取状态描述"""
        state_descriptions = {
            StudentState.NOT_IN_LIB: "不在图书馆",
            StudentState.LEARNING: "在图书馆学习",
            StudentState.AWAY: "暂时离开但占座",
            StudentState.GONE: "完全离开图书馆"
        }
        return state_descriptions.get(self.state, "未知状态")

    def reset_for_new_day(self):
        """重置为新一天的初始状态"""
        self.state = StudentState.NOT_IN_LIB
        self.assigned_seat = None
        self.current_schedule_index = 0
        self.generate_schedule()  # 生成新一天的日程
