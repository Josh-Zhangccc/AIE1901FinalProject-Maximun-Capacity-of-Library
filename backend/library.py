from seats import Seat
from students import Student
import random

class Library:
    def __init__(self, populations:int = 180, lamp_probability: float = 0.3, socket_probability: float = 0.4) -> None:
        """
        初始化图书馆对象
        
        Args:
            populations (int): 学生总数，默认180
            lamp_probability (float): 座位有台灯的概率，默认0.3
            socket_probability (float): 座位有插座的概率，默认0.4
        """
        self.seats = []  # 座位列表
        self.populations = populations  # 学生总数
        self.lamp_probability = lamp_probability  # 台灯概率
        self.socket_probability = socket_probability  # 插座概率
        
        # 创建2500个座位（50x50网格）
        for x in range(50):
            for y in range(50):
                # 随机决定座位是否有台灯和插座
                has_lamp = random.random() < self.lamp_probability
                has_socket = random.random() < self.socket_probability
                seat = Seat(x, y, lamp=has_lamp, socket=has_socket)
                self.seats.append(seat)