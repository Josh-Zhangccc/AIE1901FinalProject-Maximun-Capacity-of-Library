from enum import Enum
from datetime import datetime,timedelta

class Status(Enum):
    """座位状态枚举
    定义座位在图书馆系统中的各种状态
    """
    vacant  = "V"  # 空闲 - 座位未被占用
    taken   = "T"  # 已占用 - 座位被学生占用学习
    reverse = "R"  # 已占座（暂时离开） - 学生暂时离开但保留座位
    signed  = "S" # 标记清理（违规占座） - 座位被系统标记为违规占座

class Seat:
    """座位类，用于管理图书馆座位的状态和属性
    座位是图书馆模拟系统的基本单元，具有坐标位置、设施属性和状态管理功能
    """
    
    def __init__(self,x:int,y:int,
                 lamp:bool=False,
                 socket:bool=False) -> None:
        """
        初始化座位对象

        Args:
            x (int): 座位的x坐标，范围0-19对应20x20网格
            y (int): 座位的y坐标，范围0-19对应20x20网格
            lamp (bool): 座位是否有台灯，影响学生满意度，默认为False
            socket (bool): 座位是否有插座，影响学生满意度，默认为False
        """
        self.coordinate = (x,y)  # 座位坐标，用于在20x20网格中唯一标识座位
        self.lamp = lamp          # 是否有台灯，影响学生满意度
        self.socket = socket      # 是否有插座，影响学生满意度
        self.status = Status.vacant  # 座位状态，初始为空闲
        self.owner = None         # 座位当前使用者ID（学生索引），无使用者时为None
        self.taken_time = datetime(1900,1,1,7)  # 座位被占用的时间，用于计算占座时长
        self.window = False       # 是否靠窗，边缘座位自动为靠窗座位，影响学生满意度
        # 判断是否为靠窗座位：x或y为0表示左边缘或上边缘，x或y为19表示右边缘或下边缘
        if x == 0 or y == 0 or x == 19 or y == 19:
            self.window  = True

        self.crowded_para = 0           # 拥挤参数，表示周围座位的占用情况，影响学生满意度
        self.time_delta = timedelta(minutes=15)  # 时间更新步长，与学生时间更新同步

    def taken_hours(self):
        """
        将占用时间格式化为小时数（包含分钟的小数部分）
        用于计算座位占用时长，判断是否超过图书馆占座时间限制

        Returns:
            float: 以小时为单位的占用时间，格式为小时.分钟/60
        """
        return self.taken_time.hour + self.taken_time.minute/60
    
    def update(self):
        """
        更新座位占用时间
        每次模拟时间步进时调用，仅对非空闲座位更新占用时间
        用于跟踪占座时长，以便后续判断是否超时
        """
        if self.status == Status.signed:  # 只有被占用的座位才更新时间
            self.taken_time += self.time_delta
            
    def take(self,student_index):
        """
        学生占用座位
        将座位状态从未占用变为已占用，并记录使用者ID

        Args:
            student_index: 学生唯一标识符，表示占用座位的学生ID
        """
        if self.status == Status.vacant:  # 只有空闲座位才能被占用
            self.status = Status.taken
            self.owner = student_index

    def leave(self,reverse:bool):
        """
        学生离开座位
        根据参数决定是完全释放座位还是暂时占座离开

        Args:
            reverse (bool): 离开类型
                - False: 学生完全离开（释放座位），座位变为空闲状态
                - True: 学生暂时离开但占座（座位状态改为reverse），保留座位使用权
        """
        if self.status == Status.taken:  # 确保座位有使用者才允许离开操作
            if not reverse:
                print('Seat接收到',False,'预期行为：学生完全离开，座位变为空闲，清除使用者信息')
                # 学生完全离开，座位变为空闲，清除使用者信息
                self.status = Status.vacant
                self.owner = None
            else:
                print('Seat接收到',True,'预期行为：学生暂时离开但占座，座位状态改为占座状态，保留使用者信息')
                # 学生暂时离开但占座，座位状态改为占座状态，保留使用者信息
                self.status = Status.reverse

    def back(self):
        '''
        占座的学生回到座位
        当暂时离开但占座的学生返回时，将座位状态从占座改为已占用
        '''
        if self.status == Status.reverse:  # 只有占座状态的学生才能返回
            self.status = Status.taken

    def sign(self):
        """
        标记违规占座
        将暂时离开但占座的状态改为标记清理状态
        图书馆管理系统发现超时占座时调用此方法
        """
        if self.status == Status.reverse:  # 只能标记占座状态的座位
            self.status = Status.signed

    def clear(self):
        """
        清理超时的违规占座
        将标记清理状态的座位重置为空闲状态，释放占用
        图书馆管理系统清理超时占座时调用此方法
        """
        if self.status == Status.signed:  # 只清理被标记的座位
            self.status = Status.vacant
            self.owner = None

    def set_crowded_para(self,num):
        """
        设置座位拥挤参数
        用于计算座位周围环境的拥挤程度，影响学生对座位的满意度

        Args:
            num (float): 拥挤参数值，范围0-1，0表示周围完全空旷，1表示周围完全拥挤
        """
        self.crowded_para = num