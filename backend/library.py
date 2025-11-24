from seats import Seat
from students import Student
import random

class Library:
    def __init__(self) -> None:
        self.initialize_seats()
        self.initialize_students()

    def initialize_seats(self,
                         lamp_probability: float = 0.3,
                         socket_probability: float = 0.4) -> None: 
        self.seats = []  # 座位列表
        self.lamp_probability = lamp_probability  # 台灯概率
        self.socket_probability = socket_probability  # 插座概率
                                                                                                      
        for x in range(50):                                                                                                                      
            for y in range(50):                                                                                                                  
                # 随机决定座位是否有台灯和插座
                has_lamp = random.random() < self.lamp_probability
                has_socket = random.random() < self.socket_probability
                seat = Seat(x, y, lamp=has_lamp, socket=has_socket)
                self.seats.append(seat)

    def initialize_students(self,
                            early:float = 0.2,
                            late:float = 0.4,
                            kind:float = 0.5,
                            prefer_lamp = 0.2,
                            prefer_window = 0.3
                            ) -> None:
        pass