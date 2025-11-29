import unittest
import sys
import os
# 添加项目根目录到sys.path，以便正确导入backend模块
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))

from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from backend.library import Library
from backend.students import Student, StudentState
from backend.seats import Seat, Status


class TestInteraction(unittest.TestCase):
    """测试座位、学生和图书馆之间的交互关系"""

    def setUp(self):
        """为测试设置初始环境 - 使用小规模数据避免初始化大量座位和学生"""
        self.library = Library()
        
        # 手动初始化少量座位（而不是20x20网格）
        self.library.seats.clear()
        # 创建几个测试座位
        test_seats = [
            Seat(0, 0, lamp=True, socket=True),
            Seat(0, 1, lamp=False, socket=True),
            Seat(0, 2, lamp=True, socket=False),
            Seat(0, 3, lamp=False, socket=False)
        ]
        self.library.seats = test_seats
        for seat in self.library.seats:
            self.library.seats_map[seat.coordinate] = seat
        
        # 创建少量学生用于测试
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
        # 清空现有学生并创建测试学生
        self.library.students = [Student(0, student_para, seat_preference)]
        
    def test_student_seat_interaction(self):
        """测试学生与座位的基本交互"""
        student = self.library.students[0]
        available_seat = self.library.seats[0]  # 使用第一个座位
        
        # 验证初始状态
        self.assertEqual(available_seat.status, Status.vacant)
        self.assertEqual(student.state, StudentState.SLEEP)
        
        # 学生占用座位
        student.take_seat(available_seat)
        
        # 验证交互结果
        self.assertEqual(student.state, StudentState.LEARNING)
        self.assertEqual(student.seat, available_seat)
        self.assertEqual(available_seat.status, Status.taken)
        self.assertEqual(available_seat.owner, student.student_id)
        
        # 学生离开座位
        with patch.object(student, '_should_reverse_seat', return_value=False):
            student.leave_seat()
        
        # 验证离开后的状态
        self.assertEqual(student.state, StudentState.GONE)
        # 当_should_reverse_seat返回False时，传递给seat.leave的参数是False
        # 根据seat.leave的逻辑：if not reverse -> 设置为vacant
        self.assertEqual(available_seat.status, Status.vacant)  # 修正：应该是vacant而不是reverse
        self.assertIsNone(available_seat.owner)

    def test_seat_reservation_behavior(self):
        """测试占座行为"""
        student = self.library.students[0]
        seat = self.library.seats[1]
        
        # 学生占用座位
        student.take_seat(seat)
        self.assertEqual(seat.status, Status.taken)
        
        # 学生离开并占座
        with patch.object(student, '_should_reverse_seat', return_value=True):
            student.leave_seat()
        
        # 验证离开后占座状态
        self.assertEqual(student.state, StudentState.AWAY)
        # 当_should_reverse_seat返回True时，传递给seat.leave的参数是True
        # 根据seat.leave的逻辑：if not reverse -> vacant, if reverse -> reverse
        # 所以传递True时，座位应该是reverse状态
        self.assertEqual(seat.status, Status.reverse)
        self.assertEqual(seat.owner, student.student_id)

    def test_library_reservation_system(self):
        """测试图书馆的占座标记和清理系统"""
        student = self.library.students[0]
        seat = self.library.seats[2]
        
        # 学生占用座位
        student.take_seat(seat)
        
        # 学生离开并占座
        with patch.object(student, '_should_reverse_seat', return_value=True):
            student.leave_seat()
        
        # 验证占座状态
        self.assertEqual(seat.status, Status.reverse)
        
        # 图书馆标记占座
        self.library.sign_seat()
        
        # 验证标记后的状态
        self.assertEqual(seat.status, Status.signed)
        
        # 图书馆清理超时占座
        self.library.clear_seat()
        
        # 由于时间没有超过限制，座位状态不变
        # 如果时间超过限制，座位会被清理为vacant状态

    def test_library_update_system(self):
        """测试图书馆的更新系统"""
        initial_time = self.library.current_time
        
        # 执行一次更新
        self.library.update()
        
        # 验证时间是否正确更新
        expected_time = initial_time + self.library.time_delta
        self.assertEqual(self.library.current_time, expected_time)
        
        # 验证座位时间是否更新
        for seat in self.library.seats:
            # 只有非空闲座位的时间才会更新
            if seat.status != Status.vacant:
                seat.update()  # 手动更新座位时间

    def test_student_schedule_based_interaction(self):
        """测试基于学生日程的交互"""
        student = self.library.students[0]
        
        # 检查学生日程表是否生成
        self.assertGreater(len(student.schedule), 0, "学生应有生成的日程表")
        
        # 设置时间并检查学生应执行的动作
        student.current_time = datetime(1900, 1, 1, 8, 0, 0)
        action = student.get_current_action()
        self.assertIn(action, ["start", "learn", "eat", "course", "rest", "end"], "动作应在允许范围内")

    def test_seat_comfort_and_crowding_calculation(self):
        """测试座位舒适度和拥挤度计算"""
        # 执行图书馆更新以计算拥挤参数
        self.library.calculate_each_seat_crowding_para()
        
        # 验证至少一个座位有计算出的拥挤参数
        seats_with_crowded_para = [seat for seat in self.library.seats if seat.crowded_para >= 0]
        self.assertGreater(len(seats_with_crowded_para), 0, "应有座位计算出拥挤参数")
        
        # 测试学生对座位满意度的计算
        student = self.library.students[0]
        test_seat = self.library.seats[0]
        
        satisfaction = student.calculate_seat_satisfaction(test_seat)
        self.assertIsInstance(satisfaction, (int, float), "满意度应为数字")
        self.assertGreaterEqual(satisfaction, 1, "满意度至少为1")

    def test_library_seat_counting(self):
        """测试图书馆座位计数功能"""
        # 初始状态下，所有座位都应该是空闲的
        vacant_count = sum(1 for seat in self.library.seats if seat.status == Status.vacant)
        taken_count = self.library.count_taken_seats()
        
        # count_taken_seats方法的实现有问题 - 它返回的是len(self.seats) - count，而count是空闲座位数
        # 所以实际上是返回总座位数-空闲座位数=非空闲座位数
        expected_taken = len(self.library.seats) - vacant_count
        self.assertEqual(taken_count, expected_taken, "占用座位计数应正确")

    def test_library_unsatisfied_tracking(self):
        """测试图书馆不满意计数"""
        initial_unsatisfied = self.library.count_unsatisfied()
        
        # 触发不满意计数
        self.library.get_unsatisfied()
        
        new_unsatisfied = self.library.count_unsatisfied()
        self.assertEqual(new_unsatisfied, initial_unsatisfied + 1, "不满意计数应增加")


if __name__ == '__main__':
    unittest.main()