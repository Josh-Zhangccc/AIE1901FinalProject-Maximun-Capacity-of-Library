import json
import matplotlib.pyplot as plt
import pandas as pd
import re
from datetime import datetime
import matplotlib.dates as mdates
import os

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def parse_json_data(json_file_path):
    """
    解析JSON数据文件，提取用于可视化的数据
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取时间序列数据（跳过第一个测试配置信息）
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
            
            # 提取不满意数和清理座位数
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
    1. 座位占有率和占座率
    2. 不满意数及其增长数和清理座位数及其增长数
    3. 图书馆中座位的拥挤程度（还是用library的评分）然后平均归一化与座位占有率
    """
    # 解析数据
    data = parse_json_data(json_file_path)
    
    # 读取初始配置数据以获取座位数和学生数信息
    with open(json_file_path, 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    
    initial_config = full_data[0]  # 获取初始配置信息
    test_name = initial_config.get('test_name', '未知测试')
    test_scale = initial_config.get('test_scale', '未知规模')
    
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
    
    # 将时间字符串转换为datetime对象以便绘图
    time_objects = [datetime.strptime(t, '%H:%M') for t in data['time_data']]
    
    # 设置x轴范围为7a.m到12p.m (7:00到12:00)
    start_time = datetime.strptime('07:00', '%H:%M')
    end_time = datetime.strptime('23:59', '%H:%M')
    
    # 过滤时间范围内的数据点，只保留7:00到12:00之间的数据
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
    
    # 设置总标题，包含测试名称、规模和座位/学生数量信息
    if student_count > 0:
        suptitle_text = f' 规模: {test_scale}\n座位总数: {seat_count}, 学生总数: {student_count}'
    else:
        suptitle_text = f'规模: {test_scale}\n座位总数: {seat_count}'
    
    fig.suptitle(suptitle_text, fontsize=16, y=0.98)
    
    # 第一张图：座位占有率和占座率
    ax1 = axes[0]
    ax1_twin = ax1.twinx()  # 创建第二个y轴用于显示占座数量
    
    # 绘制座位占有率百分比（使用过滤后的数据）
    line1 = ax1.plot(filtered_data['time_objects'], filtered_data['taken_rate_percentages'], label='座位占有率', marker='o', color='#4A90A4', linewidth=2)  # 冷蓝色系
    # 绘制占座数量（使用过滤后的数据）
    line2 = ax1_twin.plot(filtered_data['time_objects'], filtered_data['reversed_seats'], label='占座数量', marker='s', color='#967E7B', linewidth=2)  # 灰褐色系
    
    ax1.set_title('图1: 座位占有率和占座数量随时间变化', fontsize=14, pad=20)
    ax1.set_xlabel('时间', fontsize=12)
    ax1.set_ylabel('座位占有率 (%)', color='#4A90A4', fontsize=12)
    ax1_twin.set_ylabel('占座数量', color='#967E7B', fontsize=12)
    
    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # 设置x轴范围
    ax1.set_xlim(start_time, end_time)
    
    # 设置x轴格式
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # 每小时一个刻度
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")
    
    # 第二张图：不满意数及其增长数和清理座位数及其增长数
    ax2 = axes[1]
    
    # 绘制不满意数和清理座位数（左y轴）（使用过滤后的数据）
    line3 = ax2.plot(filtered_data['time_objects'], filtered_data['unsatisfied_nums'], label='不满意数', marker='o', color='#7F9D9F', linewidth=2)  # 灰绿色系
    line4 = ax2.plot(filtered_data['time_objects'], filtered_data['cleared_seats'], label='清理座位数', marker='s', color='#6C6C6C', linewidth=2)  # 灰色系
    
    # 创建第二个y轴用于显示增长数
    
    ax2.set_title('图2: 不满意数及清理座位数随时间变化', fontsize=14, pad=20)
    ax2.set_xlabel('时间', fontsize=12)
    ax2.set_ylabel('累积数量', color='black', fontsize=12)
    
    # 合并图例
    lines3, labels3 = ax2.get_legend_handles_labels()
    ax2.legend(lines3, labels3, loc='upper left', fontsize=10)
    
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    # 设置x轴范围
    ax1.set_xlim(start_time, end_time)
    ax2.set_xlim(start_time, end_time)
    
    # 设置x轴格式
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax2.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # 每小时一个刻度
    plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")
    
    # 调整子图间距，避免标题重叠
    plt.subplots_adjust(hspace=0.4)
    
    plt.show()
'''

def save_figure(json_file_path, save_path=None, show_plot=True):
    """
    根据JSON文件中的座位数和学生数信息创建文件夹并保存图像
    :param json_file_path: JSON数据文件路径
    :param save_path: 保存路径（可选，默认为simulation_data/figures）
    :param show_plot: 是否显示图表（默认为True）
    """
    # 读取JSON文件获取座位数和学生数信息
    with open(json_file_path, 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    
    initial_config = full_data[0]  # 获取初始配置信息
    test_scale = initial_config.get('test_scale', '未知规模')
    
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

    # 设置默认保存路径
    if save_path is None:
        save_path = os.path.join('simulation_data', 'figures')

    # 创建以座位数命名的文件夹（使用下划线代替冒号以兼容Windows）
    seat_folder = f"seats_{seat_count}"
    full_save_path = os.path.join(save_path, seat_folder)
    os.makedirs(full_save_path, exist_ok=True)

    # 生成图像文件名（包含学生数信息，使用下划线代替冒号以兼容Windows）
    if student_count > 0:
        image_filename = f"students_{student_count}.png"
    else:
        image_filename = "visualization.png"  # 默认文件名

    # 完整的保存路径
    image_path = os.path.join(full_save_path, image_filename)

    # 生成并保存图像
    plot_simulation(json_file_path, save_to_path=image_path)

    if show_plot:
        plt.show()
    else:
        plt.close()


def plot_simulation(json_file_path, save_to_path=None):
    """
    绘制模拟数据的三张图表
    1. 座位占有率和占座率
    2. 不满意数及其增长数和清理座位数及其增长数
    3. 图书馆中座位的拥挤程度（还是用library的评分）然后平均归一化与座位占有率
    """
    # 解析数据
    data = parse_json_data(json_file_path)
    
    # 读取初始配置数据以获取座位数和学生数信息
    with open(json_file_path, 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    
    initial_config = full_data[0]  # 获取初始配置信息
    test_name = initial_config.get('test_name', '未知测试')
    test_scale = initial_config.get('test_scale', '未知规模')
    
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
    
    # 将时间字符串转换为datetime对象以便绘图
    time_objects = [datetime.strptime(t, '%H:%M') for t in data['time_data']]
    
    # 设置x轴范围为7a.m到12p.m (7:00到12:00)
    start_time = datetime.strptime('07:00', '%H:%M')
    end_time = datetime.strptime('23:59', '%H:%M')
    
    # 过滤时间范围内的数据点，只保留7:00到12:00之间的数据
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
    
    # 设置总标题，包含测试名称、规模和座位/学生数量信息
    if student_count > 0:
        suptitle_text = f' 规模: {test_scale}\n座位总数: {seat_count}, 学生总数: {student_count}'
    else:
        suptitle_text = f'规模: {test_scale}\n座位总数: {seat_count}'
    
    fig.suptitle(suptitle_text, fontsize=16, y=0.98)
    
    # 第一张图：座位占有率和占座率
    ax1 = axes[0]
    ax1_twin = ax1.twinx()  # 创建第二个y轴用于显示占座数量
    
    # 绘制座位占有率百分比（使用过滤后的数据）
    line1 = ax1.plot(filtered_data['time_objects'], filtered_data['taken_rate_percentages'], label='座位占有率', marker='o', color='#4A90A4', linewidth=2)  # 冷蓝色系
    # 绘制占座数量（使用过滤后的数据）
    line2 = ax1_twin.plot(filtered_data['time_objects'], filtered_data['reversed_seats'], label='占座数量', marker='s', color='#967E7B', linewidth=2)  # 灰褐色系
    
    ax1.set_title('图1: 座位占有率和占座数量随时间变化', fontsize=14, pad=20)
    ax1.set_xlabel('时间', fontsize=12)
    ax1.set_ylabel('座位占有率 (%)', color='#4A90A4', fontsize=12)
    ax1_twin.set_ylabel('占座数量', color='#967E7B', fontsize=12)
    
    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # 设置x轴范围
    ax1.set_xlim(start_time, end_time)
    
    # 设置x轴格式
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # 每小时一个刻度
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")
    
    # 第二张图：不满意数及其增长数和清理座位数及其增长数
    ax2 = axes[1]
    
    # 绘制不满意数和清理座位数（左y轴）（使用过滤后的数据）
    line3 = ax2.plot(filtered_data['time_objects'], filtered_data['unsatisfied_nums'], label='不满意数', marker='o', color='#7F9D9F', linewidth=2)  # 灰绿色系
    line4 = ax2.plot(filtered_data['time_objects'], filtered_data['cleared_seats'], label='清理座位数', marker='s', color='#6C6C6C', linewidth=2)  # 灰色系
    
    # 创建第二个y轴用于显示增长数
    
    ax2.set_title('图2: 不满意数及清理座位数随时间变化', fontsize=14, pad=20)
    ax2.set_xlabel('时间', fontsize=12)
    ax2.set_ylabel('累积数量', color='black', fontsize=12)
    
    # 合并图例
    lines3, labels3 = ax2.get_legend_handles_labels()
    ax2.legend(lines3, labels3, loc='upper left', fontsize=10)
    
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    # 设置x轴范围
    ax1.set_xlim(start_time, end_time)
    ax2.set_xlim(start_time, end_time)
    
    # 设置x轴格式
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax2.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # 每小时一个刻度
    plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")
    
    # 调整子图间距，避免标题重叠
    plt.subplots_adjust(hspace=0.4)
    
    # 如果提供了保存路径，则保存图像
    if save_to_path:
        plt.savefig(save_to_path, dpi=300, bbox_inches='tight')
        plt.close()  # 关闭图形以节省内存
    else:
        plt.show()