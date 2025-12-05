"""
data_analysis.py
分析模拟数据，整合相同座位数但不同学生数的模拟结果
"""
import json
import os
import re
from typing import Dict, List, Tuple
from config import simulations_base_path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd

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


def analyze_library_dynamic_capacity(data: List[Dict]) -> Dict:
    """
    分析图书馆最大动态容量相关指标
    返回一个包含多个关键指标的字典
    """
    if len(data) <= 1:  # 跳过配置信息
        return {'dynamic_capacity_ratio': 0.0, 'peak_pressure_score': 0.0, 'utilization_efficiency': 0.0}
    
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
    
    if not occupancy_rates:
        return {'dynamic_capacity_ratio': 0.0, 'peak_pressure_score': 0.0, 'utilization_efficiency': 0.0}
    
    # 动态容量比：在座位紧张时（高占用）的不满增长情况
    high_occupancy_unsatisfied_growth = 0
    high_occupancy_periods = 0
    
    for i in range(1, len(occupancy_rates)):
        if occupancy_rates[i-1] >= 80:  # 高占用期间
            high_occupancy_periods += 1
            if unsatisfied_values[i] > unsatisfied_values[i-1]:
                high_occupancy_unsatisfied_growth += (unsatisfied_values[i] - unsatisfied_values[i-1])
    
    # 动态容量比：在高占用期间不满增长越少，动态容量越大
    if high_occupancy_periods > 0:
        avg_growth_during_high_occupancy = high_occupancy_unsatisfied_growth / high_occupancy_periods
        # 取反向指标：增长越少，容量比越高
        dynamic_capacity_ratio = max(0, 1.0 - min(1.0, avg_growth_during_high_occupancy / 2.0))
    else:
        dynamic_capacity_ratio = sum(occupancy_rates) / len(occupancy_rates) / 100.0  # 使用平均占用率作为基础
    
    # 压力分数：综合考虑高占用和不满增长
    peak_pressure_score = min(1.0, (sum(1 for rate in occupancy_rates if rate >= 90) / len(occupancy_rates) * 0.6 + 
                                   len([i for i in range(1, len(unsatisfied_values)) if unsatisfied_values[i] > unsatisfied_values[i-1]]) / len(unsatisfied_values) * 0.4))
    
    # 利用率效率：考虑座位使用效率
    avg_occupancy = sum(occupancy_rates) / len(occupancy_rates) / 100.0
    max_unsatisfied = max(unsatisfied_values) if unsatisfied_values else 0
    utilization_efficiency = max(0, avg_occupancy - (max_unsatisfied / 50.0))  # 惩罚高不满数
    
    return {
        'dynamic_capacity_ratio': dynamic_capacity_ratio,
        'peak_pressure_score': peak_pressure_score,
        'utilization_efficiency': max(0, utilization_efficiency)
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
        print(f"警告: 找不到座位数为 {seat_count} 的模拟数据文件夹: {simulations_folder}")
        return {}
    
    # 获取该文件夹中的所有JSON文件
    json_files = [f for f in os.listdir(simulations_folder) if f.endswith('.json')]
    
    if not json_files:
        print(f"警告: 座位数为 {seat_count} 的文件夹中没有JSON文件")
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
            
            # 计算改进的占用率指标
            occupancy_metric = analyze_seat_occupancy_rate(data)
            
            # 计算图书馆动态容量相关指标
            capacity_metrics = analyze_library_dynamic_capacity(data)
            
            # 计算高占座率时间比例
            high_reversed_ratio = analyze_seat_reversed_rate(data)
            
            # 获取最终不满意数和被清理数
            final_unsatisfied, final_cleared = get_final_unsatisfied_and_cleared(data)
            
            # 存储结果
            analysis_results['occupancy_rates'].append(occupancy_metric)
            analysis_results['reversed_rates'].append(high_reversed_ratio)
            analysis_results['final_unsatisfied'].append(final_unsatisfied)
            analysis_results['final_cleared'].append(final_cleared)
            analysis_results['student_counts'].append(student_count)
            analysis_results['file_names'].append(file_name)
            analysis_results['dynamic_capacity_ratios'].append(capacity_metrics['dynamic_capacity_ratio'])
            analysis_results['peak_pressure_scores'].append(capacity_metrics['peak_pressure_score'])
            analysis_results['utilization_efficiencies'].append(capacity_metrics['utilization_efficiency'])
            
        except Exception as e:
            print(f"处理文件 {file_name} 时出错: {e}")
            continue
    
    # 按学生数量排序
    sorted_indices = sorted(range(len(analysis_results['student_counts'])), 
                           key=lambda i: analysis_results['student_counts'][i])
    
    for key in analysis_results.keys():
        analysis_results[key] = [analysis_results[key][i] for i in sorted_indices]
    
    return analysis_results

def plot_analysis(seat_count: int, analysis_results: Dict, save_path: str = None): # type: ignore
    """
    绘制分析结果 - 合并图像，以超容量比为x轴，包含图书馆最大动态容量相关指标
    """
    if not analysis_results or not analysis_results['student_counts']:
        print(f"没有数据可以绘制分析图表 (座位数: {seat_count})")
        return
    
    # 设置中文字体支持
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    # 提取数据
    student_counts = analysis_results['student_counts']
    occupancy_rates = analysis_results['occupancy_rates']  # 新的综合指标
    reversed_rates = analysis_results.get('reversed_rates', [0]*len(student_counts))  # 如果没有占座率数据，则使用0
    final_unsatisfied = analysis_results['final_unsatisfied']
    final_cleared = analysis_results['final_cleared']
    dynamic_capacity_ratios = analysis_results.get('dynamic_capacity_ratios', [0]*len(student_counts))
    peak_pressure_scores = analysis_results.get('peak_pressure_scores', [0]*len(student_counts))
    utilization_efficiencies = analysis_results.get('utilization_efficiencies', [0]*len(student_counts))
    
    # 计算学生总数超过图书馆静态容量比（以座位数为基准）
    over_capacity_ratios = [max(0, (students - seat_count) / seat_count) for students in student_counts]
    
    # 创建图表 - 3行1列，展示更多与动态容量相关的信息
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 18))
    
    # 设置总标题
    min_students = min(student_counts) if student_counts else 0
    max_students = max(student_counts) if student_counts else 0
    fig.suptitle(f'座位数 {seat_count} 模拟数据分析\n学生数范围: {min_students} - {max_students}', 
                fontsize=16, y=0.98)
    
    # 第一个子图：综合占用指标和占座率 vs 超容量比
    ax1_twin = ax1.twinx()  # 创建第二个y轴
    
    # 绘制综合占用指标 - 以超容量比为x轴
    line1 = ax1.plot(over_capacity_ratios, occupancy_rates, marker='o', color='#4A90A4', 
                     linewidth=2, markersize=8, label='综合占用指标(座位不足影响更大)')
    # 绘制高占座率 - 以超容量比为x轴
    line2 = ax1_twin.plot(over_capacity_ratios, reversed_rates, marker='s', color='#F5A623', 
                          linewidth=2, markersize=8, label='高占座率时间比例')
    
    ax1.set_title('综合占用指标和占座率 vs 学生总数超过图书馆静态容量比', fontsize=14)
    ax1.set_xlabel('学生总数超过图书馆静态容量比 (超容量比)')
    ax1.set_ylabel('综合占用指标', color='#4A90A4')
    ax1_twin.set_ylabel('高占座率时间比例', color='#F5A623')
    
    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.set_ylim(0, 1)
    ax1_twin.set_ylim(0, 1)
    
    # 第二个子图：最终不满意数和被清理数 vs 超容量比
    line3 = ax2.plot(over_capacity_ratios, final_unsatisfied, marker='^', color='#D0021B', 
                     linewidth=2, markersize=8, label='最终不满意数')
    line4 = ax2.plot(over_capacity_ratios, final_cleared, marker='d', color='#90144B', 
                     linewidth=2, markersize=8, label='最终被清理数')
    
    ax2.set_title('最终不满意数和被清理数 vs 学生总数超过图书馆静态容量比', fontsize=14)
    ax2.set_xlabel('学生总数超过图书馆静态容量比 (超容量比)')
    ax2.set_ylabel('数量')
    ax2.legend(loc='upper left')
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    # 第三个子图：图书馆最大动态容量相关指标
    line5 = ax3.plot(over_capacity_ratios, dynamic_capacity_ratios, marker='o', color='#50E3C2', 
                     linewidth=2, markersize=8, label='动态容量比(座位紧张时不满增长的反向指标)')
    line6 = ax3.plot(over_capacity_ratios, peak_pressure_scores, marker='s', color='#BD10E0', 
                     linewidth=2, markersize=8, label='峰值压力分数(高占用+不满增长)')
    line7 = ax3.plot(over_capacity_ratios, utilization_efficiencies, marker='^', color='#B8E986', 
                     linewidth=2, markersize=8, label='利用率效率(考虑座位使用效率)')
    
    ax3.set_title('图书馆最大动态容量相关指标 vs 学生总数超过图书馆静态容量比', fontsize=14)
    ax3.set_xlabel('学生总数超过图书馆静态容量比 (超容量比)')
    ax3.set_ylabel('指标值')
    ax3.legend(loc='upper left')
    ax3.grid(True, linestyle='--', alpha=0.6)
    
    # 调整子图间距，避免重叠
    plt.tight_layout(pad=3.0)
    
    # 保存或显示图表
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"分析图表已保存到: {save_path}")
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

def run_analysis(seat_count: int, output_dir: str = None):
    """
    运行完整分析流程
    """
    print(f"开始分析座位数为 {seat_count} 的模拟数据...")
    
    # 执行分析
    results = analyze_simulations_by_seat_count(seat_count)
    
    if not results or not results['student_counts']:
        print(f"没有找到座位数为 {seat_count} 的有效模拟数据")
        return
    
    print(f"找到 {len(results['student_counts'])} 个模拟数据文件进行分析")
    
    # 对相同学生数的模拟进行平均处理
    results = average_similar_simulations(results)
    
    # 确定输出目录
    if output_dir is None:
        output_dir = os.path.join('simulation_data', 'figures')
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成文件名 (按照要求的格式: analysis(seats-min-max))
    min_students = min(results['student_counts']) if results['student_counts'] else 0
    max_students = max(results['student_counts']) if results['student_counts'] else 0
    file_name = f"analysis({seat_count}-{min_students}-{max_students}).png"
    save_path = os.path.join(output_dir, f"seats_{seat_count}", file_name)
    
    # 创建座位数子目录
    seat_dir = os.path.join(output_dir, f"seats_{seat_count}")
    os.makedirs(seat_dir, exist_ok=True)
    
    # 绘制并保存图表
    plot_analysis(seat_count, results, save_path)
    
    # 打印统计摘要
    print("\n分析结果摘要:")
    print(f"座位数: {seat_count}")
    print(f"学生数范围: {min_students} - {max_students}")
    print(f"处理后的模拟文件数: {len(results['student_counts'])}")
    print(f"平均综合占用指标: {sum(results['occupancy_rates'])/len(results['occupancy_rates']):.3f}")
    print(f"平均高占座率时间比例: {sum(results['reversed_rates'])/len(results['reversed_rates']):.3f}")
    print(f"平均最终不满意数: {sum(results['final_unsatisfied'])/len(results['final_unsatisfied']):.1f}")
    print(f"平均最终被清理数: {sum(results['final_cleared'])/len(results['final_cleared']):.1f}")
    print(f"平均动态容量比: {sum(results['dynamic_capacity_ratios'])/len(results['dynamic_capacity_ratios']):.3f}")
    print(f"平均峰值压力分数: {sum(results['peak_pressure_scores'])/len(results['peak_pressure_scores']):.3f}")
    print(f"平均利用率效率: {sum(results['utilization_efficiencies'])/len(results['utilization_efficiencies']):.3f}")
    
    return results