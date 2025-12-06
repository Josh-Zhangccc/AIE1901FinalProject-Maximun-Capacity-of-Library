"""
data_analysis.py
分析模拟数据，整合相同座位数但不同学生数的模拟结果
"""
import json
import os
import re
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
from typing import Dict, List, Tuple
from config import simulations_base_path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd

# Configure font settings for proper character display on Windows
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']  # Use fonts that support English characters properly
plt.rcParams['axes.unicode_minus'] = False  # Used to properly display minus signs

def analyze_seat_occupancy_rate(data: List[Dict]) -> float:
    """
    计算有利于判断图书馆最大动态容量的指标
    重点考虑座位不足（不满增长）的情况，使这种情形对结果影响更大
    """
    if len(data) <= 1:  # 跳过配置信息
        return 0.0
    
    # 提取占用率数据和不满数
    occupancy_rates = []
    unsatisfied_values = []
    
    for item in data[1:]:  # 跳过第一个配置项
        taken_rate_str = item.get('taken_rate', ' 0 (0.0%)')
        match = re.search(r'\(([\d.]+)%\)', taken_rate_str)
        if match:
            rate = float(match.group(1))
            occupancy_rates.append(rate)
        else:
            occupancy_rates.append(0.0)
        
        unsatisfied = item.get('unstisfied_num', 0)
        unsatisfied_values.append(unsatisfied)
    
    if not occupancy_rates or len(occupancy_rates) < 2:
        return 0.0
    
    # 计算不满数的增长情况（座位不足的指标）
    increasing_unsatisfied_count = 0
    total_increases = 0
    max_unsatisfied = max(unsatisfied_values) if unsatisfied_values else 0
    
    for i in range(1, len(unsatisfied_values)):
        if unsatisfied_values[i] > unsatisfied_values[i-1]:
            total_increases += unsatisfied_values[i] - unsatisfied_values[i-1]
            # 如果在高占用率（>=70%）情况下不满数增加，加倍计算
            if occupancy_rates[i-1] >= 70:
                increasing_unsatisfied_count += 2 * (unsatisfied_values[i] - unsatisfied_values[i-1])
            else:
                increasing_unsatisfied_count += (unsatisfied_values[i] - unsatisfied_values[i-1])
    
    # 计算高占用率时间（座位紧张的指标）
    high_occupancy_threshold = 85.0  # 提高阈值以更准确反映座位紧张
    high_occupancy_count = sum(1 for rate in occupancy_rates if rate >= high_occupancy_threshold)
    
    # 综合指标：不满增长作为主要指标，高占用率作为辅助指标
    # 使用归一化方法，使座位不足情况影响更大
    normalized_unsatisfied_impact = min(1.0, total_increases / 20.0)  # 假设20是较大的不满增长值
    normalized_occupancy_ratio = high_occupancy_count / len(occupancy_rates)
    
    # 组合指标，不满增长权重更高 (70%)，高占用率权重较低 (30%)
    combined_metric = 0.7 * normalized_unsatisfied_impact + 0.3 * normalized_occupancy_ratio
    
    return min(1.0, combined_metric)


def analyze_seat_occupancy_rate(data: List[Dict]) -> float:
    """
    计算改进的综合占用指标
    高座位占用时间比例（座位占用率大于80%的时间比例）
    归一化处理：超过80%的时间占总时间的比例
    """
    if len(data) <= 1:  # 跳过配置信息
        return 0.0
    
    occupancy_rates = []
    
    for item in data[1:]:  # 跳过第一个配置项
        taken_rate_str = item.get('taken_rate', ' 0 (0.0%)')
        match = re.search(r'\(([\d.]+)%\)', taken_rate_str)
        if match:
            rate = float(match.group(1))
            occupancy_rates.append(rate)
        else:
            occupancy_rates.append(0.0)
    
    if not occupancy_rates:
        return 0.0
    
    # 计算座位占用率大于80%的时间比例
    high_occupancy_count = sum(1 for rate in occupancy_rates if rate > 80)
    total_time_points = len(occupancy_rates)
    
    high_occupancy_ratio = high_occupancy_ratio = high_occupancy_count / total_time_points if total_time_points > 0 else 0.0
    
    # 归一化：如果超过80%的时间大于7点到23:59（即15小时）的一半（7.5小时），则数值为1
    # 从7:00到23:59共有16*4 + 3*4 + 1 = 64 + 12 + 1 = 77个15分钟时间段（约等于19.25小时）
    # 实际上7:00到23:59是16小时59分钟 = 16*4 + 3*4 + 1*4/4 = 64 + 12 + 1 = 77个15分钟时间段
    # 一天总共有24*4 = 96个15分钟时间段
    # 但实际模拟时间是从7:00到23:59，共16*4 + 3*4 + 1 = 77个时间段
    # 7.5小时 = 7.5*4 = 30个15分钟时间段
    
    # 实际上模拟从7:00到00:00（即24:00），即17小时 = 17*4 = 68个15分钟时间段
    # 考虑到0点可能代表第二天的开始，我们使用17小时 = 68个时间段
    # 7.5小时 = 30个时间段
    # 但更简单的方法是：如果占用率超过80%的时间比例 > 0.5，则为1
    
    # 基于实际数据的时间长度进行归一化
    time_threshold = 0.5  # 可以调整这个阈值
    
    normalized_value = min(1.0, high_occupancy_ratio / time_threshold) if time_threshold > 0 else 0.0
    return normalized_value


def calculate_peak_pressure_score(data: List[Dict]) -> float:
    """
    峰值压力分数：由高座位占用时的不满数增长决定
    选取高占用时间段，取不满增长值的最大值，不需要归一化
    """
    if len(data) <= 1:  # 跳过配置信息
        return 0.0
    
    occupancy_rates = []
    unsatisfied_values = []
    
    for item in data[1:]:  # 跳过第一个配置项
        taken_rate_str = item.get('taken_rate', ' 0 (0.0%)')
        match = re.search(r'\(([\d.]+)%\)', taken_rate_str)
        if match:
            rate = float(match.group(1))
            occupancy_rates.append(rate)
        else:
            occupancy_rates.append(0.0)
        
        unsatisfied = item.get('unstisfied_num', 0)
        unsatisfied_values.append(unsatisfied)
    
    if not occupancy_rates or len(occupancy_rates) < 2:
        return 0.0
    
    # 计算不满数的增长值
    unsatisfied_growths = []
    for i in range(1, len(unsatisfied_values)):
        growth = unsatisfied_values[i] - unsatisfied_values[i-1]
        if growth > 0 and occupancy_rates[i-1] >= 80:  # 只在高占用期间计算增长
            unsatisfied_growths.append(growth)
    
    # 返回高占用期间不满增长的最大值
    peak_pressure_score = max(unsatisfied_growths) if unsatisfied_growths else 0.0
    return peak_pressure_score


def analyze_library_dynamic_capacity(data: List[Dict], student_count: int = 0) -> Dict:
    """
    分析图书馆最大动态容量相关指标
    返回一个包含多个关键指标的字典
    """
    # 计算峰值压力分数
    peak_pressure_score = calculate_peak_pressure_score(data)
    
    # 动态容量比：基于峰值压力，使用学生数进行归一化
    # 峰值压力越小，动态容量越大
    if student_count > 0:
        normalized_pressure = peak_pressure_score / student_count
        dynamic_capacity_ratio = max(0, 1.0 - normalized_pressure)
    else:
        # 如果没有学生数，默认使用之前的参考值
        dynamic_capacity_ratio = max(0, 1.0 - min(1.0, peak_pressure_score / 10.0))
    
    return {
        'dynamic_capacity_ratio': dynamic_capacity_ratio,
        'peak_pressure_score': peak_pressure_score,
        'utilization_efficiency': 0.0  # 为了保持兼容性，但这个值不再使用
    }

def analyze_seat_reversed_rate(data: List[Dict]) -> float:
    """
    计算占座率高的时间占总时间的比例
    """
    if len(data) <= 1:  # 跳过配置信息
        return 0.0
    
    # 提取占座数据
    reversed_seats_count = []
    total_seats = 0
    
    for item in data[1:]:  # 跳过第一个配置项
        # 首先确定总座位数 - 从第一个数据项获取
        if total_seats == 0:
            taken_rate_str = item.get('taken_rate', ' 0 (0.0%)')
            match = re.search(r'(\d+) \([\d.]+%\)', taken_rate_str)
            if match:
                # 这里我们需要从座位信息中获取总座位数
                # 从配置中获取更准确的座位数
                config = data[0] if data else {}
                seat_info = config.get('seat_info', {})
                total_seats = len(seat_info)
        
        reversed_count = item.get('reversed_seats', 0)
        reversed_seats_count.append(reversed_count)
    
    if not reversed_seats_count or total_seats == 0:
        return 0.0
    
    # 计算占座率高的时间（占座数 >= 总座位数的30%）
    high_reversed_threshold = total_seats * 0.3  # 占座数超过座位总数30%时为高占座率
    high_reversed_count = sum(1 for count in reversed_seats_count if count >= high_reversed_threshold)
    
    # 返回高占座率时间占比
    return high_reversed_count / len(reversed_seats_count) if reversed_seats_count else 0.0

def get_final_unsatisfied_and_cleared(data: List[Dict]) -> Tuple[int, int]:
    """
    获取最终的不满意数和被清理数
    """
    if not data or len(data) <= 1:
        return 0, 0
    
    # 获取最后一个数据点的值
    last_data = data[-1]
    unsatisfied = last_data.get('unstisfied_num', 0)
    cleared = last_data.get('cleared_seats', 0)
    
    return unsatisfied, cleared

def get_student_count_from_scale(scale: str) -> int:
    """
    从scale字符串中提取学生数量，例如从"3*3->10"中提取10
    """
    try:
        if '->' in scale:
            return int(scale.split('->')[1])
        return 0
    except:
        return 0

def analyze_simulations_by_seat_count(seat_count: int) -> Dict:
    """
    分析指定座位数的所有模拟数据
    """
    seat_folder_name = f"{seat_count}_seats_simulations"
    simulations_folder = os.path.join(simulations_base_path, seat_folder_name)
    
    if not os.path.exists(simulations_folder):
        print(f"Warning: Cannot find simulation data folder for {seat_count} seats: {simulations_folder}")
        return {}
    
    # 获取该文件夹中的所有JSON文件
    json_files = [f for f in os.listdir(simulations_folder) if f.endswith('.json')]
    
    if not json_files:
        print(f"Warning: No JSON files found in folder for {seat_count} seats")
        return {}
    
    analysis_results = {
        'occupancy_rates': [],
        'reversed_rates': [],
        'final_unsatisfied': [],
        'final_cleared': [],
        'student_counts': [],
        'file_names': [],
        'dynamic_capacity_ratios': [],  # 新增：动态容量比
        'peak_pressure_scores': [],     # 新增：压力分数
        'utilization_efficiencies': []  # 新增：利用率效率
    }
    
    for file_name in json_files:
        file_path = os.path.join(simulations_folder, file_name)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
            if not data or len(data) < 2:
                continue
                
            # 获取初始配置
            config = data[0]
            scale = config.get('test_scale', '0*0->0')
            student_count = get_student_count_from_scale(scale)
            
            # 计算新的综合占用指标（高座位占用时间比例）
            high_occupancy_ratio = analyze_seat_occupancy_rate(data)
            
            # 计算峰值压力分数
            peak_pressure_score = calculate_peak_pressure_score(data)
            
            # 综合占用指标：直接使用高占用时间比例
            occupancy_metric = high_occupancy_ratio
            
            # 计算图书馆动态容量相关指标
            capacity_metrics = analyze_library_dynamic_capacity(data, student_count)
            
            # 计算高占座率时间比例
            high_reversed_ratio = analyze_seat_reversed_rate(data)
            
            # 获取最终不满意数和被清理数
            final_unsatisfied, final_cleared = get_final_unsatisfied_and_cleared(data)
            
            # 存储结果
            analysis_results['occupancy_rates'].append(occupancy_metric)  # 高座位占用时间比例
            analysis_results['reversed_rates'].append(high_reversed_ratio)
            analysis_results['final_unsatisfied'].append(final_unsatisfied)
            analysis_results['final_cleared'].append(final_cleared)
            analysis_results['student_counts'].append(student_count)
            analysis_results['file_names'].append(file_name)
            analysis_results['dynamic_capacity_ratios'].append(capacity_metrics['dynamic_capacity_ratio'])
            analysis_results['peak_pressure_scores'].append(peak_pressure_score)  # 使用直接计算的峰值压力分数
            analysis_results['utilization_efficiencies'].append(0.0)  # 为了保持兼容性，设置为0
            
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")
            continue
    
    # 按学生数量排序
    sorted_indices = sorted(range(len(analysis_results['student_counts'])), 
                           key=lambda i: analysis_results['student_counts'][i])
    
    for key in analysis_results.keys():
        analysis_results[key] = [analysis_results[key][i] for i in sorted_indices]
    
    return analysis_results

def plot_analysis(seat_count: int, analysis_results: Dict, save_path: str = None): # type: ignore
    """
    绘制分析结果 - 按照新要求的三个图表
    1. 综合占用指标：高座位占用时间比例 + 峰值压力分数
    2. 最大不满数和动态容量比
    3. 最大清理数和峰值最大占座率
    """
    if not analysis_results or not analysis_results['student_counts']:
        print(f"No data available to plot analysis chart (Seat count: {seat_count})")
        return
    
    # Set English label support
    plt.rcParams['axes.unicode_minus'] = False  # Used to properly display minus signs
    
    # Extract data
    student_counts = analysis_results['student_counts']
    occupancy_rates = analysis_results['occupancy_rates']  # High seat occupancy time ratio
    final_unsatisfied = analysis_results['final_unsatisfied']
    final_cleared = analysis_results['final_cleared']
    reversed_rates = analysis_results.get('reversed_rates', [0]*len(student_counts))  # High reservation rate time ratio
    dynamic_capacity_ratios = analysis_results.get('dynamic_capacity_ratios', [0]*len(student_counts))
    peak_pressure_scores = analysis_results.get('peak_pressure_scores', [0]*len(student_counts))
    
    # Calculate the ratio of total student count exceeding library static capacity (based on seat count)
    over_capacity_ratios = [max(0, (students - seat_count) / seat_count) for students in student_counts]
    
    # Create chart - 3 rows, 1 column
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 18))
    
    # Set main title
    min_students = min(student_counts) if student_counts else 0
    max_students = max(student_counts) if student_counts else 0
    fig.suptitle(f'Analysis of Simulations with {seat_count} Seats\nStudent Count Range: {min_students} - {max_students}', 
                fontsize=16, y=0.98)
    
    # First subplot: Comprehensive occupancy index (high occupancy ratio + peak pressure score)
    ax1_twin = ax1.twinx()  # Create second y-axis
    
    # Plot high seat occupancy time ratio - with over-capacity ratio as x-axis
    line1 = ax1.plot(over_capacity_ratios, occupancy_rates, marker='o', color='#4A90A4', 
                     linewidth=2, markersize=8, label='High Seat Occupancy Time Ratio (>80%)')
    # Plot peak pressure score - with over-capacity ratio as x-axis
    line2 = ax1_twin.plot(over_capacity_ratios, peak_pressure_scores, marker='s', color='#F5A623', 
                          linewidth=2, markersize=8, label='Peak Pressure Score')
    
    ax1.set_title('High Seat Occupancy Time Ratio and Peak Pressure Score vs Over-Capacity Ratio', fontsize=14)
    ax1.set_xlabel('Ratio of Total Students Exceeding Library Static Capacity (Over-Capacity Ratio)')
    ax1.set_ylabel('High Seat Occupancy Time Ratio', color='#4A90A4')
    ax1_twin.set_ylabel('Peak Pressure Score', color='#F5A623')
    
    # Merge legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + lines2, loc='upper left')
    
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.set_ylim(0, 1)
    ax1_twin.set_ylim(0, max(peak_pressure_scores) if peak_pressure_scores else 1)
    
    # Second subplot: Maximum unsatisfied count and dynamic capacity ratio
    ax2_twin = ax2.twinx()  # Create second y-axis
    
    line3 = ax2.plot(over_capacity_ratios, final_unsatisfied, marker='^', color='#D0021B', 
                     linewidth=2, markersize=8, label='Max Unsatisfied Count')
    line4 = ax2_twin.plot(over_capacity_ratios, dynamic_capacity_ratios, marker='o', color='#50E3C2', 
                          linewidth=2, markersize=8, label='Dynamic Capacity Ratio')
    
    ax2.set_title('Max Unsatisfied Count and Dynamic Capacity Ratio vs Over-Capacity Ratio', fontsize=14)
    ax2.set_xlabel('Ratio of Total Students Exceeding Library Static Capacity (Over-Capacity Ratio)')
    ax2.set_ylabel('Max Unsatisfied Count', color='#D0021B')
    ax2_twin.set_ylabel('Dynamic Capacity Ratio', color='#50E3C2')
    
    # Merge legends
    lines3, labels3 = ax2.get_legend_handles_labels()
    lines4, labels4 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines3 + lines4, labels3 + lines4, loc='upper left')
    
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2_twin.set_ylim(0, 1)
    
    # Third subplot: Maximum cleared count and peak maximum reservation rate
    ax3_twin = ax3.twinx()  # Create second y-axis
    
    line5 = ax3.plot(over_capacity_ratios, final_cleared, marker='d', color='#90144B', 
                     linewidth=2, markersize=8, label='Max Cleared Count')
    line6 = ax3_twin.plot(over_capacity_ratios, reversed_rates, marker='s', color='#F5A623', 
                          linewidth=2, markersize=8, label='Peak Maximum Reservation Rate')
    
    ax3.set_title('Max Cleared Count and Peak Maximum Reservation Rate vs Over-Capacity Ratio', fontsize=14)
    ax3.set_xlabel('Ratio of Total Students Exceeding Library Static Capacity (Over-Capacity Ratio)')
    ax3.set_ylabel('Max Cleared Count', color='#90144B')
    ax3_twin.set_ylabel('Peak Maximum Reservation Rate', color='#F5A623')
    
    # Merge legends
    lines5, labels5 = ax3.get_legend_handles_labels()
    lines6, labels6 = ax3_twin.get_legend_handles_labels()
    ax3.legend(lines5 + lines6, labels5 + labels6, loc='upper left')
    
    ax3.grid(True, linestyle='--', alpha=0.6)
    
    # Adjust subplot spacing to avoid overlap
    plt.tight_layout(pad=3.0)
    
    # Save or display chart
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Analysis chart saved to: {save_path}")
    else:
        plt.show()

def average_similar_simulations(results: Dict) -> Dict:
    """
    对相同学生数的模拟进行平均处理，整合重复情况
    """
    if not results or not results['student_counts']:
        return results
    
    # 创建字典，以学生数为键，收集所有相同学生数的模拟结果
    student_data = {}
    for i, student_count in enumerate(results['student_counts']):
        if student_count not in student_data:
            student_data[student_count] = {
                'occupancy_rates': [],
                'reversed_rates': [],
                'final_unsatisfied': [],
                'final_cleared': [],
                'dynamic_capacity_ratios': [],
                'peak_pressure_scores': [],
                'utilization_efficiencies': [],
                'file_names': []
            }
        
        student_data[student_count]['occupancy_rates'].append(results['occupancy_rates'][i])
        student_data[student_count]['reversed_rates'].append(results['reversed_rates'][i])
        student_data[student_count]['final_unsatisfied'].append(results['final_unsatisfied'][i])
        student_data[student_count]['final_cleared'].append(results['final_cleared'][i])
        student_data[student_count]['dynamic_capacity_ratios'].append(results['dynamic_capacity_ratios'][i] if 'dynamic_capacity_ratios' in results else 0)
        student_data[student_count]['peak_pressure_scores'].append(results['peak_pressure_scores'][i] if 'peak_pressure_scores' in results else 0)
        student_data[student_count]['utilization_efficiencies'].append(results['utilization_efficiencies'][i] if 'utilization_efficiencies' in results else 0)
        student_data[student_count]['file_names'].append(results['file_names'][i])
    
    # 计算每个学生数的平均值
    new_results = {
        'occupancy_rates': [],
        'reversed_rates': [],
        'final_unsatisfied': [],
        'final_cleared': [],
        'student_counts': [],
        'file_names': [],
        'dynamic_capacity_ratios': [],
        'peak_pressure_scores': [],
        'utilization_efficiencies': []
    }
    
    for student_count, data in student_data.items():
        new_results['student_counts'].append(student_count)
        new_results['occupancy_rates'].append(sum(data['occupancy_rates']) / len(data['occupancy_rates']))
        new_results['reversed_rates'].append(sum(data['reversed_rates']) / len(data['reversed_rates']))
        new_results['final_unsatisfied'].append(sum(data['final_unsatisfied']) / len(data['final_unsatisfied']))
        new_results['final_cleared'].append(sum(data['final_cleared']) / len(data['final_cleared']))
        new_results['dynamic_capacity_ratios'].append(sum(data['dynamic_capacity_ratios']) / len(data['dynamic_capacity_ratios']))
        new_results['peak_pressure_scores'].append(sum(data['peak_pressure_scores']) / len(data['peak_pressure_scores']))
        new_results['utilization_efficiencies'].append(sum(data['utilization_efficiencies']) / len(data['utilization_efficiencies']))
        # 使用所有相关文件名的组合
        new_results['file_names'].append(', '.join(data['file_names']))
    
    # 按学生数量排序
    sorted_indices = sorted(range(len(new_results['student_counts'])), 
                           key=lambda i: new_results['student_counts'][i])
    
    for key in new_results.keys():
        new_results[key] = [new_results[key][i] for i in sorted_indices]
    
    return new_results

def run_analysis(seat_count: int, min_students: int = None, max_students: int = None, output_dir: str = None):
    """
    运行完整分析流程
    :param seat_count: 座位数量
    :param min_students: 最小学生数
    :param max_students: 最大学生数
    :param output_dir: 输出目录
    """
    print(f"Starting analysis of simulation data for {seat_count} seats...")
    
    # 执行分析
    results = analyze_simulations_by_seat_count(seat_count)
    
    if not results or not results['student_counts']:
        print(f"No valid simulation data found for {seat_count} seats")
        return None
    
    print(f"Found {len(results['student_counts'])} simulation data files for analysis")
    
    # 根据指定范围过滤数据
    if min_students is not None or max_students is not None:
        filtered_results = {
            'occupancy_rates': [],
            'reversed_rates': [],
            'final_unsatisfied': [],
            'final_cleared': [],
            'student_counts': [],
            'file_names': [],
            'dynamic_capacity_ratios': [],
            'peak_pressure_scores': [],
            'utilization_efficiencies': []
        }
        
        for i, student_count in enumerate(results['student_counts']):
            if (min_students is None or student_count >= min_students) and \
               (max_students is None or student_count <= max_students):
                for key in filtered_results.keys():
                    filtered_results[key].append(results[key][i])
        
        results = filtered_results
        print(f"After filtering by range {min_students}-{max_students}, {len(results['student_counts'])} data points remain")
    
    if not results['student_counts']:
        print(f"No valid simulation data in specified range {min_students}-{max_students}")
        return None
    
    # 对相同学生数的模拟进行平均处理
    results = average_similar_simulations(results)
    
    # 确定输出目录
    if output_dir is None:
        output_dir = os.path.join('simulation_data', 'figures')
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成文件名 (按照要求的格式: analysis(seats-min-max))
    if results['student_counts']:  # 确保列表非空
        min_result = min(results['student_counts']) if results['student_counts'] else 0
        max_result = max(results['student_counts']) if results['student_counts'] else 0
        file_name = f"analysis({seat_count}-{min_result}-{max_result}).png"
        save_path = os.path.join(output_dir, f"seats_{seat_count}", file_name)
        
        # 创建座位数子目录
        seat_dir = os.path.join(output_dir, f"seats_{seat_count}")
        os.makedirs(seat_dir, exist_ok=True)
        
        # 绘制并保存图表
        plot_analysis(seat_count, results, save_path)
    else:
        print("No valid data to generate analysis chart")
        return None
    
    # 打印统计摘要
    print("\nAnalysis Result Summary:")
    print(f"Seat Count: {seat_count}")
    print(f"Student Count Range: {min_result} - {max_result}")
    print(f"Number of processed simulation files: {len(results['student_counts'])}")
    print(f"Average Comprehensive Occupancy Index: {sum(results['occupancy_rates'])/len(results['occupancy_rates']):.3f}" if results['occupancy_rates'] else "Average Comprehensive Occupancy Index: 0")
    print(f"Average High Reservation Rate Time Ratio: {sum(results['reversed_rates'])/len(results['reversed_rates']):.3f}" if results['reversed_rates'] else "Average High Reservation Rate Time Ratio: 0")
    print(f"Average Final Unsatisfied Count: {sum(results['final_unsatisfied'])/len(results['final_unsatisfied']):.1f}" if results['final_unsatisfied'] else "Average Final Unsatisfied Count: 0")
    print(f"Average Final Cleared Count: {sum(results['final_cleared'])/len(results['final_cleared']):.1f}" if results['final_cleared'] else "Average Final Cleared Count: 0")
    print(f"Average Dynamic Capacity Ratio: {sum(results['dynamic_capacity_ratios'])/len(results['dynamic_capacity_ratios']):.3f}" if results['dynamic_capacity_ratios'] else "Average Dynamic Capacity Ratio: 0")
    print(f"Average Peak Pressure Score: {sum(results['peak_pressure_scores'])/len(results['peak_pressure_scores']):.3f}" if results['peak_pressure_scores'] else "Average Peak Pressure Score: 0")
    print(f"Average Utilization Efficiency: {sum(results['utilization_efficiencies'])/len(results['utilization_efficiencies']):.3f}" if results['utilization_efficiencies'] else "Average Utilization Efficiency: 0")
    
    return results