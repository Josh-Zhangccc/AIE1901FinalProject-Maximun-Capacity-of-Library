from enum import Enum
from datetime import datetime,timedelta

class Status(Enum):
    """座位状态枚举"""
    vacant  = 1  # 空闲
    taken   = 2  # 已占用
    reverse = 3  # 已占座（暂时离开）
    signed  = 4  # 标记清理（违规占座）

class Seat:
    """座位类，用于管理图书馆座位的状态和属性"""
    
    def __init__(self,x:int,y:int,
                 lamp:bool=False,
                 socket:bool=False) -> None:
        """
        初始化座位对象
        
        Args:
            x (int): 座位的x坐标
            y (int): 座位的y坐标
            lamp (bool): 座位是否有台灯，默认为False
            socket (bool): 座位是否有插座，默认为False
        """
        self.coordinate = (x,y)  # 座位坐标
        self.lamp = lamp          # 是否有台灯
        self.socket = socket      # 是否有插座
        self.status = Status.vacant  # 座位状态
        self.owner = None         # 座位当前使用者（学生索引）
        self.taken_time = datetime(1900,1,1,7,0,0)  # 座位被占用的时间
        self.window = False
        if x*y == 0 or x == 20 or y == 20:
            self.window  = True         #是否有窗户

        self.crowded_para = 0           #拥挤参数
        self.time_delta = timedelta(minutes=30)

    def taken_hours(self):
        """
        将占用时间格式化为小时数（包含分钟的小数部分）
        
        Returns:
            float: 以小时为单位的占用时间
        """
        return self.taken_time.hour + self.taken_time.minute/60
    
    def update(self):
        """
        更新座位占用时间
        """
        if self.taken_hours() != 0:
            self.taken_time += self.time_delta
            
    def take(self,student_index):
        """
        学生占用座位
        
        Args:
            student_index: 学生索引，表示占用座位的学生
        """
        if self.status == Status.vacant:
            self.status = Status.taken
            self.owner = student_index

    def leave(self,reverse:bool):
        """
        学生离开座位
        
        Args:
            reverse (bool): 
                - False: 学生完全离开（释放座位）
                - True: 学生暂时离开但占座（座位状态改为reverse）
        """
        if self.owner:
            if not reverse:
                # 学生完全离开，座位变为空闲
                self.status = Status.vacant
                self.owner = None
            else:
                # 学生暂时离开但占座
                self.status = Status.reverse

    def back(self):
        '''
        占座的学生回到座位
        '''
        if self.status == Status.reverse:
            self.status = Status.taken

    def sign(self):
        """
        标记违规占座
        将暂时离开但占座的状态改为标记清理状态
        """
        if self.status == Status.reverse:
            self.status = Status.signed

    def clear(self):
        """
        清理超时的违规占座
        """
        if self.status == Status.signed :
            self.status = Status.vacant
            self.owner = None

    def set_crowded_para(self,num):
        self.crowded_para = num