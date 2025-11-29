"""
simulation.py
模拟主类，协调整个模拟过程
提供交互式命令行界面，支持参数调整和状态查看
"""
from .library import Library
from datetime import datetime, timedelta


class Simulation:
    """
    模拟主类，协调图书馆、学生和座位系统
    提供交互式命令行界面，支持 step, status, seats, time, quit, help 命令
    """
    def __init__(self, row=20, column=20, num_students=200, humanities_rate=0.3, science_rate=0.3):
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

    def run(self):
        """
        运行模拟系统
        提供交互式命令行界面，用户可以控制模拟过程
        """
        print("图书馆座位占用行为模拟系统已启动")
        print("输入 'help' 查看可用命令")
        
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
                    break
                elif command == "help":
                    self.show_help()
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
        使用符号表示不同座位状态：V空闲，O占用，R占座，S标记
        """
        # 确定网格大小
        max_x = max(seat.coordinate[0] for seat in self.library.seats) + 1
        max_y = max(seat.coordinate[1] for seat in self.library.seats) + 1
        
        # 创建二维网格表示座位状态
        grid = [['V' for _ in range(max_y)] for _ in range(max_x)]
        
        for seat in self.library.seats:
            x, y = seat.coordinate
            if 0 <= x < max_x and 0 <= y < max_y:  # 确保坐标在范围内
                if seat.status.name == 'vacant':
                    grid[x][y] = 'V'
                elif seat.status.name == 'taken':
                    grid[x][y] = 'O'
                elif seat.status.name == 'reverse':
                    grid[x][y] = 'R'
                elif seat.status.name == 'signed':
                    grid[x][y] = 'S'
        
        # 打印网格
        print(f"座位状态图 (V:空闲, O:占用, R:占座, S:标记) - {max_x}x{max_y}网格")
        for row in grid:
            print(''.join(row))

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
        print("  quit/exit - 退出模拟")
        print("  help     - 显示此帮助信息")

if __name__ == "__main__":
    # 创建模拟实例并运行
    # 使用较小的规模进行演示
    sim = Simulation(row=5, column=5, num_students=10)
    sim.run()