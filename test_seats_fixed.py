import unittest
import sys
import os
# 添加项目根目录到sys.path，以便正确导入backend模块
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

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
        # 初始占用时间为1900年1月1日7点
        self.assertEqual(self.seat.taken_time.hour, 7)
        self.assertEqual(self.seat.taken_time.minute, 0)

    def test_take_seat(self):
        """测试占用座位"""
        self.seat.take(5)  # 学生5占用座位
        self.assertEqual(self.seat.status, Status.taken)
        self.assertEqual(self.seat.owner, 5)

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
        self.seat.leave(reverse=False)  # 完全离开
        self.assertEqual(self.seat.status, Status.vacant)
        self.assertIsNone(self.seat.owner)

    def test_leave_and_reserve(self):
        """测试离开但占座"""
        self.seat.take(5)
        self.seat.leave(reverse=True)  # 占座离开
        self.assertEqual(self.seat.status, Status.reverse)
        self.assertEqual(self.seat.owner, 5)

    def test_sign_reserved_seat(self):
        """测试标记占座"""
        self.seat.take(5)
        self.seat.leave(reverse=True)  # 占座
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
        self.seat.leave(reverse=True)  # 占座
        self.seat.sign()  # 标记占座
        self.seat.clear()  # 清理
        self.assertEqual(self.seat.status, Status.vacant)
        self.assertIsNone(self.seat.owner)

    def test_taken_hours(self):
        """测试taken_hours方法"""
        self.seat.taken_time = self.seat.taken_time.replace(hour=9, minute=30)
        hours = self.seat.taken_hours()
        self.assertEqual(hours, 9.5)

    def test_update_time(self):
        """测试更新时间"""
        original_hour = self.seat.taken_time.hour
        original_minute = self.seat.taken_time.minute
        self.seat.update()
        # 验证时间是否更新了30分钟
        expected_minute = (original_minute + 30) % 60
        expected_hour = original_hour + (original_minute + 30) // 60
        self.assertEqual(self.seat.taken_time.hour, expected_hour)
        self.assertEqual(self.seat.taken_time.minute, expected_minute)

if __name__ == '__main__':
    unittest.main()