import json
import matplotlib.pyplot as plt
import pandas as pd
import re
from datetime import datetime
import matplotlib.dates as mdates

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
    
    # 创建图形
    fig, axes = plt.subplots(3, 1, figsize=(16, 18))
    
    # 设置总标题，包含测试名称、规模和座位/学生数量信息
    if student_count > 0:
        suptitle_text = f' {test_name} | 规模: {test_scale}\n座位总数: {seat_count}, 学生总数: {student_count}'
    else:
        suptitle_text = f'{test_name} | 规模: {test_scale}\n座位总数: {seat_count}'
    
    fig.suptitle(suptitle_text, fontsize=16, y=0.98)
    
    # 第一张图：座位占有率和占座率
    ax1 = axes[0]
    ax1_twin = ax1.twinx()  # 创建第二个y轴用于显示占座数量
    
    # 绘制座位占有率百分比
    line1 = ax1.plot(time_objects, data['taken_rate_percentages'], label='座位占有率', marker='o', color='blue', linewidth=2)
    # 绘制占座数量
    line2 = ax1_twin.plot(time_objects, data['reversed_seats'], label='占座数量', marker='s', color='red', linewidth=2)
    
    ax1.set_title('图1: 座位占有率和占座数量随时间变化', fontsize=14, pad=20)
    ax1.set_xlabel('时间', fontsize=12)
    ax1.set_ylabel('座位占有率 (%)', color='blue', fontsize=12)
    ax1_twin.set_ylabel('占座数量', color='red', fontsize=12)
    
    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # 设置x轴格式
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")
    
    # 第二张图：不满意数及其增长数和清理座位数及其增长数
    ax2 = axes[1]
    
    # 绘制不满意数和清理座位数（左y轴）
    line3 = ax2.plot(time_objects, data['unsatisfied_nums'], label='不满意数', marker='o', color='orange', linewidth=2)
    line4 = ax2.plot(time_objects, data['cleared_seats'], label='清理座位数', marker='s', color='green', linewidth=2)
    
    # 创建第二个y轴用于显示增长数
    ax2_twin = ax2.twinx()
    line5 = ax2_twin.plot(time_objects, data['unsatisfied_growth'], label='不满意数增长', marker='^', color='purple', linewidth=2)
    line6 = ax2_twin.plot(time_objects, data['cleared_seats_growth'], label='清理座位数增长', marker='v', color='brown', linewidth=2)
    
    ax2.set_title('图2: 不满意数及清理座位数随时间变化', fontsize=14, pad=20)
    ax2.set_xlabel('时间', fontsize=12)
    ax2.set_ylabel('累积数量', color='black', fontsize=12)
    ax2_twin.set_ylabel('增长数量', color='black', fontsize=12)
    
    # 合并图例
    lines3, labels3 = ax2.get_legend_handles_labels()
    lines5, labels5 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines3 + lines5, labels3 + labels5, loc='upper left', fontsize=10)
    
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    # 设置x轴格式
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax2.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")
    
    # 第三张图：图书馆中座位的拥挤程度和归一化座位占有率
    ax3 = axes[2]
    
    # 计算拥挤程度（根据周围座位占用情况估算）
    # 这里使用一个更精确的方法：拥挤度 = 占有率的平方根（表示随着占有率增加，拥挤度递增）
    if data['taken_rate_percentages']:
        # 使用更合理的拥挤度计算方法，考虑了图书馆的实际体验
        # 当座位占用率达到一定阈值（如70%）时，拥挤感会显著增加
        complex_crowdedness = []
        for p in data['taken_rate_percentages']:
            if p <= 30:
                crowdedness = p / 100  # 低占用率时拥挤感线性增长
            elif p <= 70:
                crowdedness = 0.3 + (p - 30) * 0.7 / 40  # 中等占用率时拥挤感加速增长
            else:
                crowdedness = 0.9 + (p - 70) * 0.1 / 30  # 高占用率时拥挤感接近上限
            complex_crowdedness.append(min(1.0, crowdedness))
    else:
        complex_crowdedness = []
    
    # 归一化座位占有率（0-1之间）
    max_rate = max(data['taken_rate_percentages']) if data['taken_rate_percentages'] else 1
    normalized_taken_rate = [rate/max_rate if max_rate > 0 else 0 for rate in data['taken_rate_percentages']]
    
    ax3.plot(time_objects, complex_crowdedness, label='拥挤程度（估算）', marker='o', color='green', linewidth=2)
    ax3.plot(time_objects, normalized_taken_rate, label='归一化座位占有率', marker='d', color='red', linewidth=2)
    
    ax3.set_title('图3: 图书馆座位拥挤程度与归一化占有率', fontsize=14, pad=20)
    ax3.set_xlabel('时间', fontsize=12)
    ax3.set_ylabel('程度/归一化值', fontsize=12)
    ax3.legend(loc='upper left', fontsize=10)
    ax3.grid(True, linestyle='--', alpha=0.6)
    
    # 设置x轴格式
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax3.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.setp(ax3.get_xticklabels(), rotation=45, ha="right")
    
    # 调整子图间距，避免标题重叠
    plt.subplots_adjust(top=0.93, hspace=0.4)
    
    plt.show()