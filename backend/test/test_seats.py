import unittest
from datetime import timedelta
from backend.seats import Seat, Status

class TestSeat(unittest.TestCase):
    def setUp(self):
        """为每个测试设置初始座位"""
        self.seat = Seat(1, 1, lamp=True, socket=True)

    def test_initial_state(self):
        """测试座位初始状态"""
        self.assertEqual(self.seat.coordinate, (1, 1))
        self.assertTrue(self.seat.lamp)
        self.assertTrue(self.seat.socket)
        self.assertEqual(self.seat.status, Status.vacant)
        self.assertIsNone(self.seat.owner)
        # 初始占用时间为2025年11月24日7点
        self.assertEqual(self.seat.taken_time.hour, 7)
        self.assertEqual(self.seat.taken_time.minute, 0)

    def test_take_seat(self):
        """测试占用座位"""
        result = self.seat.take(5)  # 学生5占用座位
        self.assertEqual(self.seat.status, Status.taken)
        self.assertEqual(self.seat.owner, 5)
        # 这个方法没有返回值，所以不检查result

    def test_take_occupied_seat(self):
        """测试尝试占用已被占用的座位"""
        self.seat.take(5)
        original_status = self.seat.status
        original_owner = self.seat.owner
        self.seat.take(6)  # 学生6尝试占用
        # 应该没有变化
        self.assertEqual(self.seat.status, original_status)
        self.assertEqual(self.seat.owner, original_owner)

    def test_leave_completely(self):
        """测试完全离开座位"""
        self.seat.take(5)
        self.seat.leave(reverse=True)
        self.assertEqual(self.seat.status, Status.vacant)
        self.assertIsNone(self.seat.owner)

    def test_leave_and_reserve(self):
        """测试离开但占座"""
        self.seat.take(5)
        self.seat.leave(reverse=False)
        self.assertEqual(self.seat.status, Status.reverse)
        self.assertEqual(self.seat.owner, 5)

    def test_sign_reserved_seat(self):
        """测试标记占座"""
        self.seat.take(5)
        self.seat.leave(reverse=False)  # 先占座
        self.seat.sign()
        self.assertEqual(self.seat.status, Status.signed)

    def test_sign_taken_seat(self):
        """测试尝试标记未占座的座位"""
        self.seat.take(5)
        original_status = self.seat.status
        self.seat.sign()
        # 应该没有变化
        self.assertEqual(self.seat.status, original_status)

    def test_clear_timeout_seat(self):
        """测试清理超时占座"""
        self.seat.take(5)
        self.seat.leave(reverse=False)  # 占座
        self.seat.sign()  # 标记占座
        # 模拟时间超过限制
        self.seat.taken_time = self.seat.taken_time.replace(hour=5)  # 设置为5小时前
        self.seat.clear(2.0)  # 2小时限制
        self.assertEqual(self.seat.status, Status.vacant)
        # 根据代码实现，清理占座后owner被设置为None
        self.assertIsNone(self.seat.owner)

    def test_clear_non_timeout_seat(self):
        """测试不清理未超时占座"""
        self.seat.take(5)
        self.seat.leave(reverse=False)  # 占座
        self.seat.sign()  # 标记占座
        # 将时间改为3点，这样taken_hours()返回3.0，小于limit_time 7.0
        self.seat.taken_time = self.seat.taken_time.replace(hour=3)
        self.seat.clear(7.0)  # 限制是7小时，但当前时间只有3小时，所以不会清理
        # 状态不应该改变
        self.assertEqual(self.seat.status, Status.signed)
        self.assertEqual(self.seat.owner, 5)

    def test_taken_hours(self):
        """测试taken_hours方法"""
        self.seat.taken_time = self.seat.taken_time.replace(hour=9, minute=30)
        hours = self.seat.taken_hours()
        self.assertEqual(hours, 9.5)

    def test_update_time(self):
        """测试更新时间"""
        original_hour = self.seat.taken_time.hour
        original_minute = self.seat.taken_time.minute
        self.seat.update(timedelta(minutes=30))
        self.assertEqual(self.seat.taken_time.hour, original_hour)
        self.assertEqual(self.seat.taken_time.minute, original_minute + 30)

    def test_update_time_with_hour_change(self):
        """测试更新时间跨小时"""
        self.seat.taken_time = self.seat.taken_time.replace(hour=9, minute=45)
        self.seat.update(timedelta(minutes=30))
        self.assertEqual(self.seat.taken_time.hour, 10)
        self.assertEqual(self.seat.taken_time.minute, 15)

if __name__ == '__main__':
    unittest.main()