from .seats import Seat,Status
from .students import Student,StudentState
import random
from datetime import datetime, timedelta
random.seed(1)

#Seat含有的属性：lamp,socket,x,y
#Students含有的属性：lamp:float,socket:float,space:float///character="守序", schedule_type="正常", focus_type="中", course_situation="中"
class Library:
    """
    图书馆类，管理座位和学生系统，协调整个模拟过程
    负责座位初始化、学生初始化、占座管理、时间推进等功能
    """
    def __init__(self) -> None:
        """
        初始化图书馆对象
        创建20x20网格的座位系统和学生群体，并设置初始时间和参数
        """
        self.seats:list[Seat] = []  # 存储所有座位对象的列表
        self.seats_map:dict[tuple[int,int],Seat] = {}  # 座位坐标到座位对象的映射，用于快速查找
        self.students:list[Student] = []  # 存储所有学生对象的列表
        self.current_time = datetime(1900,1,1,7)  # 当前模拟时间，从早上7点开始
        self.time_delta = timedelta(minutes=15)  # 时间更新步长，图书馆时间更新为15分钟
        self._count = 0  # 学生ID计数器，确保每个学生有唯一ID
        self.limit_reversed_time = timedelta(hours=1)  # 占座时间限制，超过此时间的占座将被清理
        self.unsatisfied = 0  # 不满意计数器，记录因没有座位而无法学习的学生数

    @staticmethod
    def _random_assign(random_num:int):
        """
        生成指定数量的随机数列表
        用于随机分配座位属性（台灯、插座）和学生类型

        Args:
            random_num (int): 需要生成的随机数数量

        Returns:
            list: 包含指定数量随机数的列表，每个数在0-1之间
        """
        random_nums = [random.random() for _ in range(random_num)] #@list
        return random_nums

    def initialize_seats(self,row:int,column:int,lamp_rate:float=0.5,socket_rate:float=0.5):
        """
        初始化座位系统，在20x20网格中创建400个座位
        随机分配台灯和插座属性，边缘座位自动为靠窗座位

        Args:
            lamp_rate (float): 座位有台灯的概率，默认为0.5
            socket_rate (float): 座位有插座的概率，默认为0.5
        """
        self.rows = row
        self.columns = column
        self.seats.clear()  # 清空现有座位列表
        # 生成400个随机数用于决定是否分配台灯和插座
        lamp_list = [lamp>=lamp_rate for lamp in self._random_assign(row*column)]  # 生成400个随机值
        socket_list = [socket>=socket_rate for socket in self._random_assign(row*column)]
        # 遍历20x20网格，创建每个座位
        idx = 0
        for x in range(row):
            for y in range(column):
                # 根据随机数决定是否分配台灯和插座
                self.seats.append(Seat(x,y,lamp_list[idx],socket_list[idx]))
                idx += 1
        # 构建座位坐标到座位对象的映射，便于后续查找
        for seat in self.seats:
            self.seats_map[seat.coordinate] = seat

    def visualize_seats_taken_state(self):
        print("\n","="*self.rows*4)
        print("   ",end =" ")
        for row in range(self.rows):
            print(row,end = "  "if len(str(row))==1 else" ")
        for column in range(self.columns):
            print("\n",column,end="  "if len(str(column))==1 else " ")
            for row in range(self.rows):
                seat = self.seats_map.get((row,column),Seat(-1,-1))
                taken_state = seat.status
                print(taken_state.value,end="  ")

    def visualize_seats_infomation(self):
        print("\n","="*self.rows*4)
        print("   ",end =" ")
        for row in range(self.rows):
            print(row,end = "  "if len(str(row))==1 else" ")
        for column in range(self.columns):
            print("\n",column,end="  "if len(str(column))==1 else " ")
            for row in range(self.rows):
                seat = self.seats_map.get((row,column),Seat(-1,-1))
                output = "N"
                lamp = seat.lamp
                socket = seat.socket
                if lamp and socket: #both true
                    output = "B"
                elif lamp and not socket:   #lamp
                    output = "L"
                elif not lamp and socket: 
                    output = "S"
                print(output,end="  ")

    def _init_students_with_different_major(self,students_number:int,type:str):
        """
        根据专业类型初始化指定数量的学生
        根据随机数将学生分为勤奋、中等、懒惰三种类型

        Args:
            students_number (int): 要创建的学生数量
            type (str): 专业类型（'humanities', 'science', 'engineering'）
        """
        # 记录初始学生数量
        initial_student_count = len(self.students)
        initial_count = self._count

        # 生成随机数列表，用于分配学生类型
        _list = self._random_assign(students_number)
        # 根据随机数范围将学生分为三类：勤奋（>=0.7）、中等（0.3-0.7）、懒惰（<=0.3）
        diligent_list = [i>=0.7 for i in _list]
        medium_list = [0.3<i<0.7 for i in _list]
        lazy_list = [i<=0.3 for i in _list]

        # 根据专业类型创建对应专业及能力的学生
        # 使用全局计数器来确保ID连续，而不是使用过滤后的索引
        match type:
            case 'humanities':  # 文科专业
                for idx, is_diligent in enumerate(diligent_list):
                    if is_diligent:
                        new_student = Student.create_humanities_diligent_student(self._count)
                        self.students.append(new_student)
                        self._count += 1
                
                # 创建中等程度的文科生（0.3<随机数<0.7的）
                for idx, is_medium in enumerate(medium_list):
                    if is_medium:
                        new_student = Student.create_humanities_medium_student(self._count)
                        self.students.append(new_student)
                        self._count += 1
                
                # 创建懒惰的文科生（随机数<=0.3的）
                for idx, is_lazy in enumerate(lazy_list):
                    if is_lazy:
                        new_student = Student.create_humanities_lazy_student(self._count)
                        self.students.append(new_student)
                        self._count += 1

            case 'science':  # 理科专业
                for idx, is_diligent in enumerate(diligent_list):
                    if is_diligent:
                        new_student = Student.create_science_diligent_student(self._count)
                        self.students.append(new_student)
                        self._count += 1
                
                for idx, is_medium in enumerate(medium_list):
                    if is_medium:
                        new_student = Student.create_science_medium_student(self._count)
                        self.students.append(new_student)
                        self._count += 1
                
                for idx, is_lazy in enumerate(lazy_list):
                    if is_lazy:
                        new_student = Student.create_science_lazy_student(self._count)
                        self.students.append(new_student)
                        self._count += 1

            case 'engineering':  # 工科专业
                for idx, is_diligent in enumerate(diligent_list):
                    if is_diligent:
                        new_student = Student.create_engineering_diligent_student(self._count)
                        self.students.append(new_student)
                        self._count += 1
                
                for idx, is_medium in enumerate(medium_list):
                    if is_medium:
                        new_student = Student.create_engineering_medium_student(self._count)
                        self.students.append(new_student)
                        self._count += 1
                
                for idx, is_lazy in enumerate(lazy_list):
                    if is_lazy:
                        new_student = Student.create_engineering_lazy_student(self._count)
                        self.students.append(new_student)
                        self._count += 1

        # 如果没有创建任何学生（可能由于随机分配导致），创建一个默认类型的学生
        # 但只在students_number > 0时才这样做
        if students_number > 0 and len(self.students) == initial_student_count:
            # 根据专业类型创建一个默认中等类型的学生
            match type:
                case 'humanities':
                    new_student = Student.create_humanities_medium_student(self._count)
                case 'science':
                    new_student = Student.create_science_medium_student(self._count)
                case 'engineering':
                    new_student = Student.create_engineering_medium_student(self._count)
                case _:
                    new_student = Student.create_engineering_medium_student(self._count)  # 默认情况
            self.students.append(new_student)
            self._count += 1

    def initialize_students(self,num:int=200,humanities:float=0.3,science:float=0.3):
        """
        初始化学生系统，创建指定数量和比例的学生

        Args:
            num (int): 总学生数量，默认为200
            humanities (float): 文科生比例，默认为0.3
            science (float): 理科生比例，默认为0.3
        """
        self.students.clear()  # 清空现有学生列表
        # 根据比例计算各专业学生数量
        humanities = int((num * humanities))
        science = int(num * science)
        engineering = num - humanities - science  # 工科生数量为剩余数量
        # 按专业分别初始化学生
        for population,subject in zip([humanities,science,engineering],["humanities","science","engineering"]):
            self._init_students_with_different_major(population,subject)

    def set_limit_reversed_time(self,time):
        """
        设置占座时间限制
        可以接受timedelta对象或"HH:MM"格式的字符串

        Args:
            time: 时间限制，可以是timedelta对象或"HH:MM"格式的字符串
        """
        if isinstance(time,timedelta):
            self.limit_reversed_time = time  # 直接设置timedelta对象
        elif isinstance(time,str):
            time_list = time.split(":")  # 分割时间字符串
            hour = int(time_list[0])  # 解析小时
            minute = int(time_list[1])  # 解析分钟
            self.limit_reversed_time = timedelta(hours=hour,minutes=minute)  # 创建timedelta对象
        else:
            raise TypeError  # 如果不是以上两种类型，抛出类型错误
        for student in self.students:
            student.know_library_limit_reverse_time(self.limit_reversed_time)



    def update(self):
        """
        更新图书馆系统状态
        推进时间，更新座位和学生状态，处理学生行为
        这是模拟系统的核心更新函数
        """
        self.clear_seat()
        self.current_time+=self.time_delta  # 推进系统时间
        # 更新所有学生状态和行为
        for student in self.students:
            student.update()  # 更新学生时间
            self.next_step_of_each_student(student)  # 处理学生下一步行为
        # 更新所有座位的状态和拥挤参数
        for seat in self.seats:
            seat.update()  # 更新座位时间
            self.calculate_each_seat_crowded_para()  # 计算座位拥挤参数
        self.sign_seat()
        

    def sign_seat(self):
        """
        标记违规占座
        检查所有占座状态的座位，将其标记为违规状态
        图书馆管理员定期检查时调用此方法
        """
        for seat in self.seats:
            seat.sign()

    def clear_seat(self):
        """
        清理超时占座
        清理超过时间限制的违规占座座位
        根据座位占用时间与系统时间限制比较来决定是否清理
        """
        for seat in self.seats:
            if seat.status == Status.signed:  # 只清理已被标记的座位
                # 计算座位占用时间是否超过限制
                if seat.taken_time - datetime(1900,1,1,7) > self.limit_reversed_time:
                    seat.clear()  # 清理该座位

    def get_unsatisfied(self):
        """
        增加不满意计数
        当学生无法找到座位时调用此方法
        用于统计图书馆管理效果
        """
        self.unsatisfied += 1

    def count_unsatisfied(self):
        """
        获取不满意计数

        Returns:
            int: 不满意的学生总数
        """
        return self.unsatisfied

    def output_seat_info(self):
        """
        输出座位信息
        返回包含所有座位详细信息的字典
        用于数据记录和可视化
        """
        seats_dic = {}
        for seat in self.seats:
            seats_dic[seat.coordinate] = {"lamp":seat.lamp,
                                          "socket":seat.socket,
                                          "window":seat.window,
                                          "status":seat.status}

    def next_step_of_each_student(self,student:Student):
        """
        处理单个学生的下一步行为
        根据学生当前时间对应的动作执行相应行为

        Args:
            student (Student): 需要处理行为的学生对象
        """
        action = student.get_current_action()  # 获取学生当前应执行的动作
        print(student.student_id)
        print(student.state,action)
        match action:
            case "start":  # 开始一天的活动
                # 当学生处于SLEEP状态且时间到达start时间点时，需要转换状态以便开始选座
                if student.state == StudentState.SLEEP:
                    student.state = StudentState.GONE  # 转换为GONE状态，这样学生就可以选座了
                    print(f"学生{student.student_id}苏醒了")
            case "learn":  # 学习动作
                if student.state != StudentState.LEARNING:  # 如果学生不在学习状态
                    take_seat = student.choose_seat(self.seats)  # 尝试选择座位
                    if not take_seat:  # 如果没有选到座位
                        self.get_unsatisfied()  # 增加不满意计数
                        print(f"学生{student.student_id}因为没有选到座位而心生不满")
            case "end":  # 结束一天的活动
                student.state = StudentState.SLEEP  # 学生进入休眠状态
                print(f"学生{student.student_id}的一天结束了")
            case "away":  # 临时离开
                # 学生离开座位，根据智能决策决定是否占座
                if student.state == StudentState.LEARNING:
                    student.leave_seat()  # 学生离开座位，根据智能决策决定是否占座
                    print(f"学生{student.student_id}离开了座位")
            case _:  # 其他动作（如吃饭、上课等）
                # 为其他动作提供更灵活的处理
                self._handle_other_actions(student, action)

    def _handle_other_actions(self, student: Student, action: str):
        """
        处理学生的其他动作

        Args:
            student (Student): 学生对象
            action (str): 学生的动作
        """
        # 对于各种非学习动作，学生需要暂时离开座位
        # 离开座位时，会根据学生的性格和满意度智能决定是否占座
        if student.state == StudentState.LEARNING:
            student.leave_seat()
            print(f"学生{student.student_id}离开了座位")
        elif student.state == StudentState.AWAY:
            # 如果已经在暂时离开状态，检查是否需要返回
            if student.seat and (student.seat.status in [Status.vacant, Status.taken]):
                # 如果原座位已空出或被占用，需要学生重新选择座位
                student.state = StudentState.GONE
                print(f"学生{student.student_id}的座位被清理了")

    def count_taken_seats(self):
        """
        统计被占用的座位数量
        计算当前正在被学生使用的座位数

        Returns:
            int: 被占用的座位数量
        """
        count = 0
        for seat in self.seats:
            if seat.status != Status.vacant:  # 统计非空闲状态的座位
                count += 1
        return count
    

    def count_reversed_seats(self):
        """
        统计占座和标记的座位数量
        计算当前被占座或已标记的座位数

        Returns:
            int: 占座和标记的座位数量
        """
        count = 0
        for seat in self.seats:
            if seat.status == Status.reverse or seat.status == Status.signed:  # 统计占座和标记状态的座位
                count += 1
        return count

    def calculate_each_seat_crowded_para(self):
        """
        计算每个座位的拥挤参数
        考虑周围座位的占用情况和窗户因素，影响学生对座位的满意度
        使用8个方向的邻近座位进行计算
        """
        # 8个方向：左上、上、右上、左、右、左下、下、右下
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0), (1, 1)]
        
        for seat in self.seats:
            x,y = seat.coordinate  # 获取座位坐标
            crowded_para = 0  # 初始化拥挤参数
            len_around_seat = 0  # 邻近座位总数
            # 遍历8个方向的邻近座位
            for dx,dy in directions:
                nx = x + dx  # 邻近座位x坐标
                ny = y + dy  # 邻近座位y坐标
                around_seat = self.seats_map.get((nx,ny),None)  # 获取邻近座位对象
                if around_seat:  # 如果邻近位置有座位
                    len_around_seat += 1  # 邻近座位数加1
                    if around_seat.status != Status.vacant:  # 如果邻近座位被占用
                        crowded_para += 1  # 拥挤参数加1
                    if around_seat.window:  # 如果邻近是窗户
                        crowded_para -= 0.5  # 窗户减少拥挤感
            # 计算平均拥度
            crowded_para =crowded_para/len_around_seat if len_around_seat>0 else 0
            seat.set_crowded_para(crowded_para)  # 设置座位的拥挤参数

    def output_seats_info(self):
        dic = {}
        for coordinate,seat in self.seats_map.items():
            output = "N"
            lamp = seat.lamp
            socket = seat.socket
            if lamp and socket: #both true
                output = "B"
            elif lamp and not socket:   #lamp
                output = "L"
            elif not lamp and socket: 
                output = "S"
            x,y = coordinate
            dic[f"{x},{y}"] = output
        return dic
    
    def output_seats_taken_state(self):
        dic = {}
        for coordinate,seat in self.seats_map.items():
            output = seat.status.value
            x,y = coordinate
            dic[f"{x},{y}"] = output
        return dic