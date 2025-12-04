"""
simulation.py
模拟主类，协调整个模拟过程
提供交互式命令行界面，支持参数调整和状态查看
"""
from .library import Library
from datetime import datetime, timedelta
from .json_manager import JsonManager
from config import simulation_file_path,test_simulation_path
import os
class Simulation:
    """
    模拟主类，协调图书馆、学生和座位系统
    提供交互式命令行界面，支持 step, status, seats, time, quit, help 命令
    """
    def __init__(self,name:str,row=20, column=20, num_students=200, humanities_rate=0.3, science_rate=0.3,simulation_type="simulation"):
        """
        初始化模拟系统

        Args:
            row (int): 座位网格的行数，默认20
            column (int): 座位网格的列数，默认20
            num_students (int): 学生数量，默认200
            humanities_rate (float): 文科生比例，默认0.3
            science_rate (float): 理科生比例，默认0.3
        """
        self.library = Library()
        # 使用新的初始化方法，支持自定义座位数量
        self.library.initialize_seats(row, column)
        self.library.initialize_students(num_students, humanities_rate, science_rate)
        
        # 设置默认的占座时间限制为1小时
        self.library.set_limit_reversed_time(timedelta(hours=1))
        scale = str(row)+"*"+str(column)+f"->{num_students}"
        stru:list[dict] = [{"test_name":name,"test_scale":scale,"seat_info":self.library.output_seats_info()}]
        path = simulation_file_path if simulation_type=="simulation"else test_simulation_path
        self.jm = JsonManager(os.path.join(path,f"{name}.json"),stru)

    def run(self, run_all = True):
        """
        运行模拟系统
        提供交互式命令行界面，用户可以控制模拟过程
        """
        print("图书馆座位占用行为模拟系统已启动")
        print("输入 'help' 查看可用命令")
        print("当前图书馆座位信息为：")
        self.library.visualize_seats_infomation()
        if run_all:
            while f"{self.library.current_time.strftime('%H:%M')}" != "00:00":
                self.step()
                self.jm.save_json()
            return
            
        while True:
            try:
                command = input(f"[{self.library.current_time.strftime('%H:%M')}] > ").strip().lower()
                
                if command == "step":
                    self.step()
                elif command == "status":
                    self.show_status()
                elif command == "seats":
                    self.show_seats()
                elif command == "time":
                    self.show_time()
                elif command.startswith("set_limit"):
                    self.set_limit_time(command)
                elif command == "quit" or command == "exit":
                    print("退出模拟系统")
                    self.jm.save_json()
                    break
                elif command == "help":
                    self.show_help()
                elif command == "run all":
                    while f"{self.library.current_time.strftime('%H:%M')}" != "00:00":
                        self.step()
                        self.jm.save_json()
                    break
                else:
                    print("未知命令，输入 'help' 查看可用命令")
                    
            except KeyboardInterrupt:
                print("\n程序被用户中断")
                break
            except Exception as e:
                print(f"发生错误: {e}")

    def step(self):
        """
        执行单步模拟
        更新图书馆系统状态，包括时间推进、座位和学生状态更新
        """
        self.library.update()
        total_seats = len(self.library.seats)
        taken_seats = self.library.count_taken_seats()
        reversed_seats = self.library.count_reversed_seats()

        current_state = {"time":self.library.current_time.strftime('%H:%M'),
                         "seats_taken_state":self.library.output_seats_taken_state(),
                         "unstisfied_num":self.library.unsatisfied,
                         "cleared_seats":self.library.count_cleared_seat,
                         "reversed_seats":reversed_seats,
                         "taken_rate":f" {taken_seats} ({taken_seats/total_seats*100:.1f}%)"}
        self.jm.data.append(current_state) # type: ignore

    def show_status(self):
        """
        显示当前模拟状态
        包括座位占用率、占座情况、不满意学生数等统计信息
        """
        total_seats = len(self.library.seats)
        taken_seats = self.library.count_taken_seats()
        reversed_seats = self.library.count_reversed_seats()
        unsatisfied_count = self.library.count_unsatisfied()
        
        print(f"当前时间: {self.library.current_time.strftime('%H:%M')}")
        print(f"总座位数: {total_seats}")
        print(f"被占用座位数: {taken_seats} ({taken_seats/total_seats*100:.1f}%)")
        print(f"占座/标记座位数: {reversed_seats}")
        print(f"不满意学生数: {unsatisfied_count}")

    def show_seats(self):
        """
        显示座位网格状态
        使用符号表示不同座位状态：V空闲，T占用，R占座，S标记
        """
        self.library.visualize_seats_taken_state()

    def show_time(self):
        """
        显示当前模拟时间
        """
        print(f"当前模拟时间: {self.library.current_time.strftime('%Y-%m-%d %H:%M')}")

    def set_limit_time(self, command):
        """
        设置占座时间限制
        格式: set_limit HH:MM

        Args:
            command (str): 完整命令字符串
        """
        try:
            time_part = command.split(' ', 1)[1]
            # 验证时间格式
            hour, minute = time_part.split(':')
            hour = int(hour)
            minute = int(minute)
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                self.library.set_limit_reversed_time(time_part)
                print(f"占座时间限制已设置为 {time_part}")
            else:
                print("时间格式错误：小时应为0-23，分钟应为0-59")
        except (ValueError, IndexError):
            print("时间格式错误：请使用 HH:MM 格式，例如 set_limit 01:30")

    def show_help(self):
        """
        显示帮助信息
        列出所有可用命令及其功能说明
        """
        print("可用命令:")
        print("  step     - 执行单步模拟")
        print("  status   - 显示当前模拟状态")
        print("  seats    - 显示座位网格状态")
        print("  time     - 显示当前模拟时间")
        print("  set_limit HH:MM - 设置占座时间限制")
        print("  quit/exit - 退出模拟并保存")
        print("  help     - 显示此帮助信息")