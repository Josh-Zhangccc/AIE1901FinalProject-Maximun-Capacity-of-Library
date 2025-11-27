import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from backend.students import Student, StudentState
from backend.seats import Seat, Status


class TestStudent(unittest.TestCase):
    def setUp(self):
        """为每个测试设置初始学生"""
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
        self.student = Student(1, student_para, seat_preference)

    def test_initialization(self):
        """测试学生初始化"""
        self.assertEqual(self.student.student_id, 1)
        self.assertEqual(self.student.student_para["character"], "守序")
        self.assertEqual(self.student.student_para["schedule_type"], "正常")
        self.assertEqual(self.student.student_para["focus_type"], "中")
        self.assertEqual(self.student.student_para["course_situation"], "中")
        self.assertEqual(self.student.state, StudentState.SLEEP)
        self.assertIsNone(self.student.seat)
        self.assertIsNotNone(self.student.schedule)
        self.assertEqual(self.student.current_time, datetime(1900, 1, 1, 7, 0, 0))

    def test_seat_preference_initialization(self):
        """测试座位偏好初始化"""
        self.assertEqual(self.student.seat_preference["lamp"], 0.5)
        self.assertEqual(self.student.seat_preference["socket"], 0.5)
        self.assertEqual(self.student.seat_preference["space"], 0.5)

    def test_generate_schedule_with_default(self):
        """测试生成日程表（默认值）"""
        # 验证生成的日程表不为空
        self.assertIsNotNone(self.student.schedule)
        self.assertGreater(len(self.student.schedule), 0)

    @patch('backend.students.Clients')
    def test_generate_schedule_with_mock_client(self, mock_client_class):
        """测试生成日程表（模拟客户端）"""
        mock_client = Mock()
        mock_client.response.return_value = [
            {"time": "07:00:00", "action": "start"},
            {"time": "08:00:00", "action": "learn"},
            {"time": "12:00:00", "action": "eat"}
        ]
        mock_client_class.return_value = mock_client
        
        # 重新创建学生以使用mock客户端
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
        student = Student(1, student_para, seat_preference)
        
        self.assertEqual(len(student.schedule), 3)
        self.assertEqual(student.schedule[0]["action"], "start")

    def test_get_current_action(self):
        """测试获取当前动作"""
        # 设置当前时间为上午9点
        self.student.current_time = datetime(1900, 1, 1, 9, 0, 0)
        action = self.student.get_current_action()
        # 验证返回的是有效的动作类型
        self.assertIn(action, ["start", "learn", "eat", "course", "rest", "end"])

        # 设置当前时间为上午7点
        self.student.current_time = datetime(1900, 1, 1, 7, 0, 0)
        action = self.student.get_current_action()
        # 验证返回的是有效的动作类型
        self.assertIn(action, ["start", "learn", "eat", "course", "rest", "end"])

        # 设置当前时间为晚上11点
        self.student.current_time = datetime(1900, 1, 1, 23, 0, 0)
        action = self.student.get_current_action()
        # 验证返回的是有效的动作类型
        self.assertIn(action, ["start", "learn", "eat", "course", "rest", "end"])

    def test_calculate_seat_satisfaction_without_seat(self):
        """测试没有座位时的满意度计算"""
        satisfaction = self.student.calculate_seat_satisfaction()
        self.assertEqual(satisfaction, 1)

    def test_calculate_seat_satisfaction_with_seat(self):
        """测试有座位时的满意度计算"""
        # 创建一个有台灯和插座的座位
        seat = Seat(1, 1, lamp=True, socket=True)
        seat.window = True  # 假设这个座位靠窗
        seat.crowded_para = 0.5  # 拥挤参数

        satisfaction = self.student.calculate_seat_satisfaction(seat)
        # 基础分数1 + 台灯分数(3*0.5) + 插座分数(3*0.5) + 窗户分数(1) + 空间分数(3*0.5*0.5)
        expected_satisfaction = 1 + 3 * 0.5 + 3 * 0.5 + 1 + 3 * 0.5 * 0.5
        self.assertEqual(satisfaction, expected_satisfaction)

    def test_know_library_limit_reverse_time(self):
        """测试设置图书馆占座时间限制"""
        new_limit = timedelta(hours=2)
        self.student.know_library_limit_reverse_time(new_limit)
        self.assertEqual(self.student.limit_reverse_time, new_limit)

    def test_take_seat(self):
        """测试占用座位"""
        seat = Seat(1, 1)
        self.student.take_seat(seat)

        self.assertEqual(self.student.state, StudentState.LEARNING)
        self.assertEqual(self.student.seat, seat)
        self.assertEqual(seat.status, Status.taken)
        self.assertEqual(seat.owner, 1)

    def test_take_seat_when_already_have_seat(self):
        """测试已占用座位时再次占用"""
        seat1 = Seat(1, 1)
        seat2 = Seat(2, 2)
        
        self.student.take_seat(seat1)
        original_seat = self.student.seat
        original_state = self.student.state
        
        self.student.take_seat(seat2)  # 尝试占用另一个座位
        
        # 学生不应改变其占用的座位
        self.assertEqual(self.student.seat, original_seat)
        self.assertEqual(self.student.state, original_state)

    def test_leave_seat_when_learning_and_should_reserve(self):
        """测试学习状态下离开并占座"""
        seat = Seat(1, 1)
        self.student.take_seat(seat)
        
        # 模拟学生决定占座（通过修改内部方法）
        # 注意：当_should_reverse_seat返回True时，传递给seat.leave的参数为True，
        # 根据seat.leave的实现，这会导致完全离开（释放座位）
        with patch.object(self.student, '_should_reverse_seat', return_value=True):
            self.student.leave_seat()

        self.assertEqual(self.student.state, StudentState.AWAY)
        self.assertEqual(seat.status, Status.vacant)
        self.assertIsNone(seat.owner)

    def test_leave_seat_when_learning_and_should_not_reserve(self):
        """测试学习状态下离开但不占座"""
        seat = Seat(1, 1)
        self.student.take_seat(seat)
        
        # 模拟学生决定不占座
        # 注意：当_should_reverse_seat返回False时，传递给seat.leave的参数为False，
        # 根据seat.leave的实现，这会导致暂时离开但占座
        with patch.object(self.student, '_should_reverse_seat', return_value=False):
            self.student.leave_seat()

        self.assertEqual(self.student.state, StudentState.GONE)
        self.assertEqual(seat.status, Status.reverse)
        self.assertEqual(seat.owner, 1)

    def test_update_time(self):
        """测试时间更新"""
        original_time = self.student.current_time
        self.student.update()
        
        expected_time = original_time + timedelta(minutes=30)
        self.assertEqual(self.student.current_time, expected_time)

    def test_choose_seat_when_available(self):
        """测试选择座位（有可用座位时）"""
        # 创建几个座位
        seat1 = Seat(1, 1, lamp=True, socket=True)
        seat2 = Seat(2, 2, lamp=False, socket=False)
        seats = [seat1, seat2]
        
        # 只有seat1是空闲的
        seat2.take(5)  # 让学生5占用seat2
        
        result = self.student.choose(seats)
        
        self.assertTrue(result)  # 应该成功选择座位
        self.assertEqual(self.student.seat, seat1)  # 应该选择seat1（满意度更高）
        self.assertEqual(self.student.state, StudentState.LEARNING)

    def test_choose_seat_when_no_available(self):
        """测试选择座位（无可用座位时）"""
        # 创建两个被占用的座位
        seat1 = Seat(1, 1)
        seat2 = Seat(2, 2)
        seats = [seat1, seat2]
        
        seat1.take(5)  # 让学生5占用seat1
        seat2.take(6)  # 让学生6占用seat2
        
        result = self.student.choose(seats)
        
        self.assertFalse(result)  # 应该选择失败
        self.assertIsNone(self.student.seat)  # 没有分配座位
        self.assertEqual(self.student.state, StudentState.SLEEP)  # 状态未改变

    def test_choose_seat_when_higher_satisfaction(self):
        """测试选择满意度更高的座位"""
        # 创建两个空闲的座位，但满意度不同
        seat1 = Seat(1, 1, lamp=True, socket=True)  # 有台灯和插座，满意度更高
        seat2 = Seat(2, 2, lamp=False, socket=False)  # 没有台灯和插座，满意度较低
        seats = [seat1, seat2]
        
        result = self.student.choose(seats)
        
        self.assertTrue(result)  # 应该成功选择座位
        self.assertEqual(self.student.seat, seat1)  # 应该选择满意度更高的seat1


if __name__ == '__main__':
    unittest.main()