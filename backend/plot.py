import json
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import pandas as pd
import re
from datetime import datetime
import matplotlib.dates as mdates
import os

# Configure font settings for proper character display on Windows
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']  # Use fonts that support English characters properly
plt.rcParams['axes.unicode_minus'] = False  # Used to properly display minus signs

def parse_json_data(json_file_path):
    """
    解析JSON数据文件，提取用于可视化的数据
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取Time序列数据（跳过第一个测试配置信息）
    time_data = []
    taken_rate_nums = []
    taken_rate_percentages = []
    reversed_seats = []
    unsatisfied_nums = []
    cleared_seats = []
    unsatisfied_growth = []
    cleared_seats_growth = []
    
    # 计算增长值的变量
    prev_unsatisfied = 0
    prev_cleared = 0
    
    for item in data[1:]:  # 跳过第一项测试配置信息
        if 'time' in item:
            time_data.append(item['time'])
            
            # 解析taken_rate字段（如" 1 (11.1%)"）提取数字和百分比
            taken_rate_str = item['taken_rate']
            match = re.search(r'(\d+)\s+\(([\d.]+)%\)', taken_rate_str)
            if match:
                taken_count = int(match.group(1))
                taken_percentage = float(match.group(2))
                taken_rate_nums.append(taken_count)
                taken_rate_percentages.append(taken_percentage)
            else:
                taken_rate_nums.append(0)
                taken_rate_percentages.append(0.0)
            
            # 提取占座数
            reversed_seats.append(item.get('reversed_seats', 0))
            
            # 提取Unsatisfied Count和Cleared Seats Count
            unsatisfied_nums.append(item.get('unstisfied_num', 0))
            cleared_seats.append(item.get('cleared_seats', 0))
            
            # 计算增长值
            current_unsatisfied = item.get('unstisfied_num', 0)
            current_cleared = item.get('cleared_seats', 0)
            
            unsatisfied_growth.append(current_unsatisfied - prev_unsatisfied)
            cleared_seats_growth.append(current_cleared - prev_cleared)
            
            prev_unsatisfied = current_unsatisfied
            prev_cleared = current_cleared
    
    return {
        'time_data': time_data,
        'taken_rate_nums': taken_rate_nums,
        'taken_rate_percentages': taken_rate_percentages,
        'reversed_seats': reversed_seats,
        'unsatisfied_nums': unsatisfied_nums,
        'cleared_seats': cleared_seats,
        'unsatisfied_growth': unsatisfied_growth,
        'cleared_seats_growth': cleared_seats_growth
    }
'''
def plot_simulation(json_file_path):
    """
    绘制模拟数据的三张图表
    1. Seat Occupancy Rate和占座率
    2. Unsatisfied Count及其增长数和Cleared Seats Count及其增长数
    3. 图书馆中座位的拥挤程度（还是用library的评分）然后平均归一化与Seat Occupancy Rate
    """
    # 解析数据
    data = parse_json_data(json_file_path)
    
    # 读取初始配置数据以获取座位数和学生数信息
    with open(json_file_path, 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    
    initial_config = full_data[0]  # 获取初始配置信息
    test_name = initial_config.get('test_name', 'Unknown Test')
    test_scale = initial_config.get('test_scale', '未知Scale')
    
    # 获取座位数（从seat_info中计算）
    seat_info = initial_config.get('seat_info', {})
    seat_count = len(seat_info)
    
    # 从test_scale字段中尝试提取学生数信息
    # test_scale格式可能类似"3*3->10"，表示3x3网格，10个学生
    student_count = 0
    if '->' in test_scale:
        try:
            student_count = int(test_scale.split('->')[1])
        except:
            student_count = 0
    
    # 将Time字符串转换为datetime对象以便绘图
    time_objects = [datetime.strptime(t, '%H:%M') for t in data['time_data']]
    
    # 设置x轴范围为7a.m到12p.m (7:00到12:00)
    start_time = datetime.strptime('07:00', '%H:%M')
    end_time = datetime.strptime('23:59', '%H:%M')
    
    # 过滤Time范围内的数据点，只保留7:00到12:00之间的数据
    filtered_data = {
        'time_objects': [],
        'taken_rate_percentages': [],
        'reversed_seats': [],
        'unsatisfied_nums': [],
        'cleared_seats': []
    }
    
    for i, time_obj in enumerate(time_objects):
        if start_time <= time_obj <= end_time:
            filtered_data['time_objects'].append(time_obj)
            filtered_data['taken_rate_percentages'].append(data['taken_rate_percentages'][i])
            filtered_data['reversed_seats'].append(data['reversed_seats'][i])
            filtered_data['unsatisfied_nums'].append(data['unsatisfied_nums'][i])
            filtered_data['cleared_seats'].append(data['cleared_seats'][i])
    
    # 创建图形
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    
    # 设置总标题，包含测试名称、Scale和座位/学生数量信息
    if student_count > 0:
        suptitle_text = f' Scale: {test_scale}\nTotal Seats: {seat_count}, Total Students: {student_count}'
    else:
        suptitle_text = f'Scale: {test_scale}\nTotal Seats: {seat_count}'
    
    fig.suptitle(suptitle_text, fontsize=16, y=0.98)
    
    # 第一张图：Seat Occupancy Rate和占座率
    ax1 = axes[0]
    ax1_twin = ax1.twinx()  # 创建第二个y轴用于显示Seat Reservation Count
    
    # 绘制Seat Occupancy Rate百分比（使用过滤后的数据）
    line1 = ax1.plot(filtered_data['time_objects'], filtered_data['taken_rate_percentages'], label='Seat Occupancy Rate', marker='o', color='#4A90A4', linewidth=2)  # Cold Blue Series
    # 绘制Seat Reservation Count（使用过滤后的数据）
    line2 = ax1_twin.plot(filtered_data['time_objects'], filtered_data['reversed_seats'], label='Seat Reservation Count', marker='s', color='#967E7B', linewidth=2)  # Gray Brown Series
    
    ax1.set_title('图1: Seat Occupancy Rate和Seat Reservation Count随Time变化', fontsize=14, pad=20)
    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('Seat Occupancy Rate (%)', color='#4A90A4', fontsize=12)
    ax1_twin.set_ylabel('Seat Reservation Count', color='#967E7B', fontsize=12)
    
    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # 设置x轴范围
    ax1.set_xlim(start_time, end_time)
    
    # 设置x轴格式
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # One tick per hour
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")
    
    # 第二张图：Unsatisfied Count及其增长数和Cleared Seats Count及其增长数
    ax2 = axes[1]
    
    # 绘制Unsatisfied Count和Cleared Seats Count（左y轴）（使用过滤后的数据）
    line3 = ax2.plot(filtered_data['time_objects'], filtered_data['unsatisfied_nums'], label='Unsatisfied Count', marker='o', color='#7F9D9F', linewidth=2)  # Gray Green Series
    line4 = ax2.plot(filtered_data['time_objects'], filtered_data['cleared_seats'], label='Cleared Seats Count', marker='s', color='#6C6C6C', linewidth=2)  # Gray Series
    
    # 创建第二个y轴用于显示增长数
    
    ax2.set_title('图2: Unsatisfied Count及Cleared Seats Count随Time变化', fontsize=14, pad=20)
    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('Cumulative Count', color='black', fontsize=12)
    
    # 合并图例
    lines3, labels3 = ax2.get_legend_handles_labels()
    ax2.legend(lines3, labels3, loc='upper left', fontsize=10)
    
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    # 设置x轴范围
    ax1.set_xlim(start_time, end_time)
    ax2.set_xlim(start_time, end_time)
    
    # 设置x轴格式
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax2.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # One tick per hour
    plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")
    
    # 调整子图间距，避免标题重叠
    plt.subplots_adjust(hspace=0.4)
    
    plt.show()
'''

def save_figure(seats: int, students: int, simulation_number: int = 1, show_plot: bool = True):
    """
    根据标准化参数保存图像 - 将相同参数的实验整合到一张图像中
    :param seats: 座位数量
    :param students: 学生数量
    :param simulation_number: 模拟次数（默认为1）
    :param show_plot: 是否显示图表（默认为True）
    """
    import os
    from config import simulations_base_path
    import json
    import glob
    import re

    # 构建JSON文件路径
    seat_folder_name = f"{seats}_seats_simulations"
    path = os.path.join(simulations_base_path, seat_folder_name)
    
    # 检查路径是否存在
    if not os.path.exists(path):
        print(f"错误：找不到座位数为 {seats} 的模拟数据文件夹 {path}")
        return False

    # 查找所有相同学生数的模拟文件
    all_json_files = glob.glob(os.path.join(path, f"{students}-*.json"))
    
    if not all_json_files:
        print(f"错误：在路径 {path} 中找不到学生数为 {students} 的JSON文件")
        return False

    # 按模拟次数排序
    def extract_simulation_number(file_path):
        match = re.search(rf"{students}-(\d+)\.json", os.path.basename(file_path))
        return int(match.group(1)) if match else 0

    all_json_files.sort(key=extract_simulation_number)
    
    # 设置保存路径
    save_path = os.path.join('simulation_data', 'figures')

    # 创建以座位数命名的文件夹（使用下划线代替冒号以兼容Windows）
    seat_folder = f"seats_{seats}"
    full_save_path = os.path.join(save_path, seat_folder)
    os.makedirs(full_save_path, exist_ok=True)

    # 生成图像文件名（整合形式：students_XX.png）
    image_filename = f"students_{students}.png"

    # 完整的保存路径
    image_path = os.path.join(full_save_path, image_filename)

    # 生成整合图像
    plot_combined_simulation(all_json_files, image_path)

    if show_plot:
        plt.show()
    else:
        plt.close()
    
    # 自动plot所有未plot的实验并更新平均实验图像
    update_average_analysis(seats)
    
    return True


def plot_combined_simulation(json_files, save_path=None):
    """
    将相同参数的多次实验整合到一张图像中
    :param json_files: 相同参数的JSON文件列表
    :param save_path: 保存路径
    """
    import json
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime
    import re
    import os

    # 解析所有JSON文件的数据
    all_data = []
    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        parsed = parse_json_data(file_path)  # 复用现有的解析函数
        all_data.append(parsed)
    
    # 只取前3次重复实验（如果有多于3次的话）
    if len(all_data) > 3:
        all_data = all_data[:3]
    
    # Set English label support
    plt.rcParams['axes.unicode_minus'] = False  # Used to properly display minus signs

    # 创建图形
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    
    # 读取第一个文件获取配置信息
    with open(json_files[0], 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    initial_config = full_data[0]  # 获取初始配置信息
    test_scale = initial_config.get('test_scale', '未知Scale')
    
    # 获取座位数（从seat_info中计算）
    seat_info = initial_config.get('seat_info', {})
    seat_count = len(seat_info)
    
    # 从test_scale字段中尝试提取学生数信息
    student_count = 0
    if '->' in test_scale:
        try:
            student_count = int(test_scale.split('->')[1])
        except:
            student_count = 0

    # 设置总标题
    if student_count > 0:
        suptitle_text = f' Scale: {test_scale}\nTotal Seats: {seat_count}, Total Students: {student_count}'
    else:
        suptitle_text = f'Scale: {test_scale}\nTotal Seats: {seat_count}'
    
    fig.suptitle(suptitle_text, fontsize=16, y=0.98)
    
    # 设置x轴范围
    start_time = datetime.strptime('07:00', '%H:%M')
    end_time = datetime.strptime('23:59', '%H:%M')
    
    # 如果有多次实验，先计算平均值
    avg_taken_rate_percentages = None
    avg_reversed_seats = None
    avg_unsatisfied_nums = None
    avg_cleared_seats = None

    if len(all_data) > 1:
        # 计算平均值
        num_points = min(len(data['taken_rate_percentages']) for data in all_data)
        avg_taken_rate_percentages = [sum(data['taken_rate_percentages'][i] for data in all_data if i < len(data['taken_rate_percentages'])) / len(all_data) for i in range(num_points)]
        avg_reversed_seats = [sum(data['reversed_seats'][i] for data in all_data if i < len(data['reversed_seats'])) / len(all_data) for i in range(num_points)]
        avg_unsatisfied_nums = [sum(data['unsatisfied_nums'][i] for data in all_data if i < len(data['unsatisfied_nums'])) / len(all_data) for i in range(num_points)]
        avg_cleared_seats = [sum(data['cleared_seats'][i] for data in all_data if i < len(data['cleared_seats'])) / len(all_data) for i in range(num_points)]

    # 第一张图：Seat Occupancy Rate和占座率
    ax1 = axes[0]
    ax1_twin = ax1.twinx()  # 创建第二个y轴用于显示Seat Reservation Count

    # 绘制次要数据（淡颜色，虚线）- 只绘制前3次实验
    for i, data in enumerate(all_data[:3]):  # 只取前3次
        if i == 0 and len(all_data) == 1:
            # 如果只有1次实验，不绘制次要数据
            continue
            
        # 获取Time数据
        time_objects = [datetime.strptime(t, '%H:%M') for t in data['time_data']]
        # 过滤Time范围内的数据点
        filtered_times = []
        filtered_taken_rates = []
        filtered_reversed_seats = []
        for j, time_obj in enumerate(time_objects):
            if start_time <= time_obj <= end_time and j < len(data['taken_rate_percentages']):
                filtered_times.append(time_obj)
                filtered_taken_rates.append(data['taken_rate_percentages'][j])
                filtered_reversed_seats.append(data['reversed_seats'][j])
        
        # 绘制次要数据（淡色、虚线）
        ax1.plot(filtered_times, filtered_taken_rates, linestyle='--', color='#4A90A4', alpha=0.4, linewidth=1.5)
        ax1_twin.plot(filtered_times, filtered_reversed_seats, linestyle='--', color='#967E7B', alpha=0.4, linewidth=1.5)

    # 绘制平均值（主要数据，实线，正常颜色和线宽）
    if avg_taken_rate_percentages and avg_reversed_seats:
        # 获取Time数据（使用第一个数据的Time轴作为参考）
        time_objects = [datetime.strptime(t, '%H:%M') for t in all_data[0]['time_data']]
        # 过滤Time范围内的数据点
        filtered_times = []
        filtered_avg_taken_rates = []
        filtered_avg_reversed_seats = []
        for j, time_obj in enumerate(time_objects):
            if start_time <= time_obj <= end_time and j < len(avg_taken_rate_percentages):
                filtered_times.append(time_obj)
                filtered_avg_taken_rates.append(avg_taken_rate_percentages[j])
                filtered_avg_reversed_seats.append(avg_reversed_seats[j])
        
        # 绘制平均值（主要曲线）
        ax1.plot(filtered_times, filtered_avg_taken_rates, label='平均Seat Occupancy Rate', marker='o', color='#4A90A4', linewidth=2)
        ax1_twin.plot(filtered_times, filtered_avg_reversed_seats, label='平均Seat Reservation Count', marker='s', color='#967E7B', linewidth=2)
    elif len(all_data) == 1:
        # 如果只有1次实验，绘制这次实验的曲线作为主要曲线
        data = all_data[0]
        time_objects = [datetime.strptime(t, '%H:%M') for t in data['time_data']]
        # 过滤Time范围内的数据点
        filtered_times = []
        filtered_taken_rates = []
        filtered_reversed_seats = []
        for j, time_obj in enumerate(time_objects):
            if start_time <= time_obj <= end_time and j < len(data['taken_rate_percentages']):
                filtered_times.append(time_obj)
                filtered_taken_rates.append(data['taken_rate_percentages'][j])
                filtered_reversed_seats.append(data['reversed_seats'][j])
        
        # 绘制单次实验的曲线
        ax1.plot(filtered_times, filtered_taken_rates, label='Seat Occupancy Rate', marker='o', color='#4A90A4', linewidth=2)
        ax1_twin.plot(filtered_times, filtered_reversed_seats, label='Seat Reservation Count', marker='s', color='#967E7B', linewidth=2)

    ax1.set_title('图1: Seat Occupancy Rate和Seat Reservation Count随Time变化', fontsize=14, pad=20)
    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('Seat Occupancy Rate (%)', color='#4A90A4', fontsize=12)
    ax1_twin.set_ylabel('Seat Reservation Count', color='#967E7B', fontsize=12)

    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

    ax1.grid(True, linestyle='--', alpha=0.6)

    # 设置x轴范围
    ax1.set_xlim(start_time, end_time)

    # 设置x轴格式
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # One tick per hour
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")

    # 第二张图：Unsatisfied Count及Cleared Seats Count随Time变化
    ax2 = axes[1]

    # 绘制次要数据（淡颜色，虚线）- 只绘制前3次实验
    for i, data in enumerate(all_data[:3]):  # 只取前3次
        if i == 0 and len(all_data) == 1:
            # 如果只有1次实验，不绘制次要数据
            continue

        # 获取Time数据
        time_objects = [datetime.strptime(t, '%H:%M') for t in data['time_data']]
        # 过滤Time范围内的数据点
        filtered_times = []
        filtered_unsatisfied_nums = []
        filtered_cleared_seats = []
        for j, time_obj in enumerate(time_objects):
            if start_time <= time_obj <= end_time and j < len(data['unsatisfied_nums']):
                filtered_times.append(time_obj)
                filtered_unsatisfied_nums.append(data['unsatisfied_nums'][j])
                filtered_cleared_seats.append(data['cleared_seats'][j])

        # 绘制次要数据（淡色、虚线）
        ax2.plot(filtered_times, filtered_unsatisfied_nums, linestyle='--', color='#7F9D9F', alpha=0.4, linewidth=1.5)
        ax2.plot(filtered_times, filtered_cleared_seats, linestyle='--', color='#6C6C6C', alpha=0.4, linewidth=1.5)

    # 绘制平均值（主要数据，实线，正常颜色和线宽）
    if avg_unsatisfied_nums and avg_cleared_seats:
        # 获取Time数据（使用第一个数据的Time轴作为参考）
        time_objects = [datetime.strptime(t, '%H:%M') for t in all_data[0]['time_data']]
        # 过滤Time范围内的数据点
        filtered_times = []
        filtered_avg_unsatisfied_nums = []
        filtered_avg_cleared_seats = []
        for j, time_obj in enumerate(time_objects):
            if start_time <= time_obj <= end_time and j < len(avg_unsatisfied_nums):
                filtered_times.append(time_obj)
                filtered_avg_unsatisfied_nums.append(avg_unsatisfied_nums[j])
                filtered_avg_cleared_seats.append(avg_cleared_seats[j])

        # 绘制平均值（主要曲线）
        ax2.plot(filtered_times, filtered_avg_unsatisfied_nums, label='平均Unsatisfied Count', marker='o', color='#7F9D9F', linewidth=2)
        ax2.plot(filtered_times, filtered_avg_cleared_seats, label='平均Cleared Seats Count', marker='s', color='#6C6C6C', linewidth=2)
    elif len(all_data) == 1:
        # 如果只有1次实验，绘制这次实验的曲线作为主要曲线
        data = all_data[0]
        time_objects = [datetime.strptime(t, '%H:%M') for t in data['time_data']]
        # 过滤Time范围内的数据点
        filtered_times = []
        filtered_unsatisfied_nums = []
        filtered_cleared_seats = []
        for j, time_obj in enumerate(time_objects):
            if start_time <= time_obj <= end_time and j < len(data['unsatisfied_nums']):
                filtered_times.append(time_obj)
                filtered_unsatisfied_nums.append(data['unsatisfied_nums'][j])
                filtered_cleared_seats.append(data['cleared_seats'][j])

        # 绘制单次实验的曲线
        ax2.plot(filtered_times, filtered_unsatisfied_nums, label='Unsatisfied Count', marker='o', color='#7F9D9F', linewidth=2)
        ax2.plot(filtered_times, filtered_cleared_seats, label='Cleared Seats Count', marker='s', color='#6C6C6C', linewidth=2)

    ax2.set_title('图2: Unsatisfied Count及Cleared Seats Count随Time变化', fontsize=14, pad=20)
    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('Cumulative Count', color='black', fontsize=12)

    # 合并图例
    lines3, labels3 = ax2.get_legend_handles_labels()
    ax2.legend(lines3, labels3, loc='upper left', fontsize=10)

    ax2.grid(True, linestyle='--', alpha=0.6)

    # 设置x轴范围
    ax1.set_xlim(start_time, end_time)
    ax2.set_xlim(start_time, end_time)

    # 设置x轴格式
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax2.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # One tick per hour
    plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")

    # 调整子图间距，避免标题重叠
    plt.subplots_adjust(hspace=0.4)
    
    # 保存图像
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"整合图像已保存到: {save_path}")
    else:
        plt.show()


def auto_plot_remaining_simulations(seats: int, students: int):
    """
    自动绘制所有未绘制的模拟实验（整合形式）
    """
    import os
    from config import simulations_base_path
    import glob

    # 查找所有属于相同学生数的模拟文件
    seat_folder_name = f"{seats}_seats_simulations"
    path = os.path.join(simulations_base_path, seat_folder_name)
    
    if not os.path.exists(path):
        return

    # 查找所有匹配的JSON文件
    json_files = glob.glob(os.path.join(path, f"{students}-*.json"))
    
    if not json_files:
        return

    # 检查整合图像是否已存在
    save_path = os.path.join('simulation_data', 'figures', f"seats_{seats}")
    image_filename = f"students_{students}.png"  # 整合形式
    image_path = os.path.join(save_path, image_filename)
    
    if not os.path.exists(image_path):
        # 生成整合图像
        plot_combined_simulation(json_files, image_path)
        print(f"已自动生成整合图像: {image_path}")


def update_average_analysis(seats: int):
    """
    更新平均分析图像
    """
    from .data_analysis import run_analysis
    run_analysis(seats)


def plot_analysis(seat_count: int, min_students: int = None, max_students: int = None, output_dir: str = None):
    """
    调用数据分析模块绘制整合分析图
    :param seat_count: 座位数量
    :param min_students: 最小学生数
    :param max_students: 最大学生数
    :param output_dir: 输出目录
    """
    from .data_analysis import run_analysis
    results = run_analysis(seat_count, min_students, max_students, output_dir)
    return results


def plot_simulation(json_file_path, save_to_path=None):
    """
    绘制模拟数据的三张图表
    1. Seat Occupancy Rate和占座率
    2. Unsatisfied Count及其增长数和Cleared Seats Count及其增长数
    3. 图书馆中座位的拥挤程度（还是用library的评分）然后平均归一化与Seat Occupancy Rate
    """
    # 解析数据
    data = parse_json_data(json_file_path)
    
    # 读取初始配置数据以获取座位数和学生数信息
    with open(json_file_path, 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    
    initial_config = full_data[0]  # 获取初始配置信息
    test_name = initial_config.get('test_name', 'Unknown Test')
    test_scale = initial_config.get('test_scale', '未知Scale')
    
    # 获取座位数（从seat_info中计算）
    seat_info = initial_config.get('seat_info', {})
    seat_count = len(seat_info)
    
    # 从test_scale字段中尝试提取学生数信息
    # test_scale格式可能类似"3*3->10"，表示3x3网格，10个学生
    student_count = 0
    if '->' in test_scale:
        try:
            student_count = int(test_scale.split('->')[1])
        except:
            student_count = 0
    
    # 将Time字符串转换为datetime对象以便绘图
    time_objects = [datetime.strptime(t, '%H:%M') for t in data['time_data']]
    
    # 设置x轴范围为7a.m到12p.m (7:00到12:00)
    start_time = datetime.strptime('07:00', '%H:%M')
    end_time = datetime.strptime('23:59', '%H:%M')
    
    # 过滤Time范围内的数据点，只保留7:00到12:00之间的数据
    filtered_data = {
        'time_objects': [],
        'taken_rate_percentages': [],
        'reversed_seats': [],
        'unsatisfied_nums': [],
        'cleared_seats': []
    }
    
    for i, time_obj in enumerate(time_objects):
        if start_time <= time_obj <= end_time:
            filtered_data['time_objects'].append(time_obj)
            filtered_data['taken_rate_percentages'].append(data['taken_rate_percentages'][i])
            filtered_data['reversed_seats'].append(data['reversed_seats'][i])
            filtered_data['unsatisfied_nums'].append(data['unsatisfied_nums'][i])
            filtered_data['cleared_seats'].append(data['cleared_seats'][i])
    
    # 创建图形
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    
    # 设置总标题，包含测试名称、Scale和座位/学生数量信息
    if student_count > 0:
        suptitle_text = f' Scale: {test_scale}\nTotal Seats: {seat_count}, Total Students: {student_count}'
    else:
        suptitle_text = f'Scale: {test_scale}\nTotal Seats: {seat_count}'
    
    fig.suptitle(suptitle_text, fontsize=16, y=0.98)
    
    # 第一张图：Seat Occupancy Rate和占座率
    ax1 = axes[0]
    ax1_twin = ax1.twinx()  # 创建第二个y轴用于显示Seat Reservation Count
    
    # 绘制Seat Occupancy Rate百分比（使用过滤后的数据）
    line1 = ax1.plot(filtered_data['time_objects'], filtered_data['taken_rate_percentages'], label='Seat Occupancy Rate', marker='o', color='#4A90A4', linewidth=2)  # Cold Blue Series
    # 绘制Seat Reservation Count（使用过滤后的数据）
    line2 = ax1_twin.plot(filtered_data['time_objects'], filtered_data['reversed_seats'], label='Seat Reservation Count', marker='s', color='#967E7B', linewidth=2)  # Gray Brown Series
    
    ax1.set_title('图1: Seat Occupancy Rate和Seat Reservation Count随Time变化', fontsize=14, pad=20)
    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('Seat Occupancy Rate (%)', color='#4A90A4', fontsize=12)
    ax1_twin.set_ylabel('Seat Reservation Count', color='#967E7B', fontsize=12)
    
    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # 设置x轴范围
    ax1.set_xlim(start_time, end_time)
    
    # 设置x轴格式
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # One tick per hour
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")
    
    # 第二张图：Unsatisfied Count及其增长数和Cleared Seats Count及其增长数
    ax2 = axes[1]
    
    # 绘制Unsatisfied Count和Cleared Seats Count（左y轴）（使用过滤后的数据）
    line3 = ax2.plot(filtered_data['time_objects'], filtered_data['unsatisfied_nums'], label='Unsatisfied Count', marker='o', color='#7F9D9F', linewidth=2)  # Gray Green Series
    line4 = ax2.plot(filtered_data['time_objects'], filtered_data['cleared_seats'], label='Cleared Seats Count', marker='s', color='#6C6C6C', linewidth=2)  # Gray Series
    
    # 创建第二个y轴用于显示增长数
    
    ax2.set_title('图2: Unsatisfied Count及Cleared Seats Count随Time变化', fontsize=14, pad=20)
    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('Cumulative Count', color='black', fontsize=12)
    
    # 合并图例
    lines3, labels3 = ax2.get_legend_handles_labels()
    ax2.legend(lines3, labels3, loc='upper left', fontsize=10)
    
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    # 设置x轴范围
    ax1.set_xlim(start_time, end_time)
    ax2.set_xlim(start_time, end_time)
    
    # 设置x轴格式
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax2.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # One tick per hour
    plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")
    
    # 调整子图间距，避免标题重叠
    plt.subplots_adjust(hspace=0.4)
    
    # 如果提供了保存路径，则保存图像
    if save_to_path:
        plt.savefig(save_to_path, dpi=300, bbox_inches='tight')
        plt.close()  # 关闭图形以节省内存
    else:
        plt.show()