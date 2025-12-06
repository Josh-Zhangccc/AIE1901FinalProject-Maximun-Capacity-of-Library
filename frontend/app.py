from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory

import os

import sys

import json

from threading import Thread

import time

import subprocess

import multiprocessing as mp

import pandas as pd

import matplotlib.pyplot as plt

import io

import base64

from datetime import datetime, timedelta

# 添加项目根目录到Python路径

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, PROJECT_ROOT)

from backend.simulation import Simulation
from backend.library import Library
from backend.students import Student
from backend.plot import save_figure

def get_next_simulation_number(total_seats, total_students):
    """获取下一个可用的模拟编号，用于自动确定simulation_number"""
    seat_folder_name = f"{total_seats}_seats_simulations"
    seat_simulation_path = os.path.join(SIMULATIONS_PATH, seat_folder_name)
    
    if not os.path.exists(seat_simulation_path):
        return 1
    
    # 查找当前学生数的模拟文件
    existing_simulations = []
    for file in os.listdir(seat_simulation_path):
        if file.endswith('.json') and file.startswith(f"{total_students}-"):
            try:
                # 从文件名 "X-Y.json" 中提取 Y 部分
                sim_number = int(file.split('-')[1].split('.')[0])
                existing_simulations.append(sim_number)
            except (ValueError, IndexError):
                continue  # 跳过无法解析的文件名
    
    if not existing_simulations:
        return 1

    # 返回最大编号+1
    return max(existing_simulations) + 1

app = Flask(__name__)

# 配置路径
SIMULATION_DATA_PATH = os.path.join(PROJECT_ROOT, 'simulation_data')
FIGURES_PATH = os.path.join(SIMULATION_DATA_PATH, 'figures')
SIMULATIONS_PATH = os.path.join(SIMULATION_DATA_PATH, 'simulations')

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/start_simulation')
def start_simulation():
    """开始模拟页面"""
    return render_template('start_simulation.html')

@app.route('/repeat_simulation')
def repeat_simulation():
    """Repeat simulation page"""
    return render_template('repeat_simulation.html')

@app.route('/view_plots')
def view_plots():
    """View plots page"""
    return render_template('view_plots.html')

@app.route('/simulation_records')
def simulation_records():
    """Simulation records page"""
    return render_template('simulation_records.html')

@app.route('/api/seat_counts')
def get_seat_counts():
    """Get seat counts list (folder names)"""
    try:
        seat_counts = []

        if os.path.exists(SIMULATIONS_PATH):
            for seat_dir in os.listdir(SIMULATIONS_PATH):
                seat_dir_path = os.path.join(SIMULATIONS_PATH, seat_dir)
                if os.path.isdir(seat_dir_path) and seat_dir.endswith('_seats_simulations'):
                    seat_count = seat_dir.replace('_seats_simulations', '')
                    seat_counts.append({
                        'value': seat_dir,  # 完整的文件夹名
                        'label': f"{seat_count} seats",  # 显示标签
                        'seat_count': int(seat_count) if seat_count.isdigit() else 0
                    })

        # 按座位数排序
        seat_counts.sort(key=lambda x: x['seat_count'])
        return jsonify(seat_counts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/student_files/<seat_folder>')
def get_student_files(seat_folder):
    """Get student files list under specified seat count folder"""
    try:
        student_files = []

        seat_path = os.path.join(SIMULATIONS_PATH, seat_folder)
        if os.path.exists(seat_path) and os.path.isdir(seat_path):
            for file in os.listdir(seat_path):
                if file.endswith('.json'):
                    # 从文件名提取学生数，例如 "15-3.json" -> 15
                    student_count = file.split('-')[0] if '-' in file else 'unknown'
                    student_files.append({
                        'path': os.path.join(seat_folder, file),  # 相对于SIMULATIONS_PATH的路径
                        'name': file,
                        'student_count': int(student_count) if student_count.isdigit() else 0
                    })

        # 按学生数排序
        student_files.sort(key=lambda x: x['student_count'])
        return jsonify(student_files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/simulation_records')
def get_simulation_records():
    """Get simulation records data (maintain backward compatibility)"""
    try:
        records = []

        if os.path.exists(SIMULATIONS_PATH):
            for seat_dir in os.listdir(SIMULATIONS_PATH):
                seat_dir_path = os.path.join(SIMULATIONS_PATH, seat_dir)
                if os.path.isdir(seat_dir_path):
                    for file in os.listdir(seat_dir_path):
                        if file.endswith('.json'):
                            records.append({
                                'path': os.path.join(seat_dir, file),  # 相对于SIMULATIONS_PATH的路径
                                'name': file,
                                'seat_count': seat_dir.replace('_seats_simulations', '') if seat_dir.endswith('_seats_simulations') else 'unknown'
                            })

        return jsonify(records)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plots')
def get_plots():
    """Get plot data"""
    try:
        plots = []

        if os.path.exists(FIGURES_PATH):
            for root, dirs, files in os.walk(FIGURES_PATH):
                for file in files:
                    if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        # 返回相对于figures目录的路径
                        rel_path = os.path.relpath(os.path.join(root, file), FIGURES_PATH)
                        # 确保路径使用正斜杠（在Windows上）
                        rel_path = rel_path.replace('\\', '/')
                        plots.append({
                            'path': rel_path,
                            'name': file
                        })

        return jsonify(plots)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to serve simulation data files
@app.route('/simulation_data/figures/<path:filename>')
def serve_simulation_figures(filename):
    """Serve simulation figure files"""
    return send_from_directory(FIGURES_PATH, filename)

# Route to serve simulation data JSON files
@app.route('/simulation_data/simulations/<path:filepath>')
def serve_simulation_data(filepath):
    """Serve simulation data JSON files"""
    # Join the path components to get the full path
    full_path = os.path.join(SIMULATIONS_PATH, filepath)
    directory = os.path.dirname(full_path)
    filename = os.path.basename(full_path)
    return send_from_directory(directory, filename)


def run_single_simulation(params, result_queue, simulation_id):
    """运行单个模拟的函数，用于多进程"""
    try:
        # 创建模拟参数
        rows, cols = params['rows'], params['cols']
        total_students = params['total_students']
        cleaning_time = params['cleaning_time']
        
        # Create library and students
        library = Library()
        library.initialize_seats(rows, cols)
        library.set_limit_reversed_time(timedelta(minutes=cleaning_time))
        
        # 计算各专业学生数量
        humanities_count = int(total_students * params['humanities_ratio'] / 100)
        science_count = int(total_students * params['science_ratio'] / 100)
        engineering_count = total_students - humanities_count - science_count  # Remaining as Engineering
        
        # 创建学生 - 使用图书馆容量和总学生数参数
        students = []
        for i in range(humanities_count):
            if i < humanities_count // 3:
                students.append(Student.create_humanities_diligent_student(i, library_capacity=rows*cols, total_students=total_students))
            elif i < 2 * humanities_count // 3:
                students.append(Student.create_humanities_medium_student(i, library_capacity=rows*cols, total_students=total_students))
            else:
                students.append(Student.create_humanities_lazy_student(i, library_capacity=rows*cols, total_students=total_students))

        for i in range(science_count):
            if i < science_count // 3:
                students.append(Student.create_science_diligent_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))
            elif i < 2 * science_count // 3:
                students.append(Student.create_science_medium_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))
            else:
                students.append(Student.create_science_lazy_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))

        for i in range(engineering_count):
            if i < engineering_count // 3:
                students.append(Student.create_engineering_diligent_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))
            elif i < 2 * engineering_count // 3:
                students.append(Student.create_engineering_medium_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))
            else:
                students.append(Student.create_engineering_lazy_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))

        # 将学生添加到图书馆
        library.students = students
        library._count = total_students  # Set student counter

        # 确定模拟编号
        simulation_number = get_next_simulation_number(rows * cols, total_students)
        # 运行模拟
        simulation = Simulation(row=rows, column=cols, num_students=total_students, humanities_rate=humanities_count/total_students if total_students > 0 else 0, science_rate=science_count/total_students if total_students > 0 else 0, simulation_number=simulation_number)
        simulation.library = library  # 替换模拟中的图书馆实例
        simulation.run(run_all=True)

        # 保存结果到对应的座位数目录
        total_seats = rows * cols
        seat_folder_name = f"{total_seats}_seats_simulations"
        seat_simulation_path = os.path.join(SIMULATIONS_PATH, seat_folder_name)
        os.makedirs(seat_simulation_path, exist_ok=True)

        filename = f"{total_students}-{simulation.simulation_number}.json"
        filepath = os.path.join(seat_simulation_path, filename)

        # 保存模拟数据
        simulation.save_to_json(filepath)  # Use Simulation's save_to_json method to save data

        result_queue.put({
            'id': simulation_id,
            'status': 'completed',
            'filepath': filepath,
            'message': f'Simulation {simulation_id} completed successfully'
        })

    except Exception as e:
        result_queue.put({
            'id': simulation_id,
            'status': 'error',
            'error': str(e),
            'message': f'Simulation {simulation_id} failed: {str(e)}'
        })

@app.route('/api/start_simulation', methods=['POST'])
def start_simulation_api():
    """Start simulation API"""
    try:
        data = request.json
        use_multiprocessing = data.get('useMultiprocessing', False)
        
        if use_multiprocessing:
            # Use multiprocessing to run simulation
            result_queue = mp.Queue()
            
            # 准备参数
            params = {
                'rows': data['rows'],
                'cols': data['cols'],
                'total_students': data['totalStudents'],
                'humanities_ratio': data['humanitiesRatio'],
                'science_ratio': data['scienceRatio'],
                'engineering_ratio': data['engineeringRatio'],
                'cleaning_time': data['cleaningTime']
            }
            
            # Create and start process
            process = mp.Process(target=run_single_simulation, args=(params, result_queue, 1))
            process.start()
            process.join()  # 等待进程完成
            
            # Get result
            result = result_queue.get()
            if result['status'] == 'error':
                return jsonify({'status': 'error', 'message': result['error']})
        else:
            # Run simulation in single thread
            rows = data['rows']
            cols = data['cols']
            total_students = data['totalStudents']
            cleaning_time = data['cleaningTime']
            humanities_ratio = data['humanitiesRatio']
            science_ratio = data['scienceRatio']
            engineering_ratio = data['engineeringRatio']

            # Create library and students
            library = Library()
            library.initialize_seats(rows, cols)
            library.set_limit_reversed_time(timedelta(minutes=cleaning_time))
            
            # 计算各专业学生数量
            humanities_count = int(total_students * humanities_ratio / 100)
            science_count = int(total_students * science_ratio / 100)
            engineering_count = total_students - humanities_count - science_count  # Remaining as Engineering

            # 创建学生
            students = []
            for i in range(humanities_count):
                if i < humanities_count // 3:
                    students.append(Student.create_humanities_diligent_student(i, library_capacity=rows*cols, total_students=total_students))
                elif i < 2 * humanities_count // 3:
                    students.append(Student.create_humanities_medium_student(i, library_capacity=rows*cols, total_students=total_students))
                else:
                    students.append(Student.create_humanities_lazy_student(i, library_capacity=rows*cols, total_students=total_students))

            for i in range(science_count):
                if i < science_count // 3:
                    students.append(Student.create_science_diligent_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))
                elif i < 2 * science_count // 3:
                    students.append(Student.create_science_medium_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))
                else:
                    students.append(Student.create_science_lazy_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))

            for i in range(engineering_count):
                if i < engineering_count // 3:
                    students.append(Student.create_engineering_diligent_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))
                elif i < 2 * engineering_count // 3:
                    students.append(Student.create_engineering_medium_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))
                else:
                    students.append(Student.create_engineering_lazy_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))

            # 将学生添加到图书馆
            library.students = students
            library._count = total_students  # Set student counter

            # 确定模拟编号
            simulation_number = get_next_simulation_number(rows * cols, total_students)
            # 运行模拟
            simulation = Simulation(row=rows, column=cols, num_students=total_students, humanities_rate=humanities_count/total_students, science_rate=science_count/total_students, simulation_number=simulation_number)
            simulation.library = library  # 替换模拟中的图书馆实例
            simulation.run(run_all=True)

            # 保存结果到对应的座位数目录
            total_seats = rows * cols
            seat_folder_name = f"{total_seats}_seats_simulations"
            seat_simulation_path = os.path.join(SIMULATIONS_PATH, seat_folder_name)
            os.makedirs(seat_simulation_path, exist_ok=True)

            filename = f"{total_students}-{simulation.simulation_number}.json"
            filepath = os.path.join(seat_simulation_path, filename)

            # 保存模拟数据
            simulation.save_to_json(filepath)  # Use Simulation's save_to_json method to save data

        return jsonify({'status': 'success', 'message': 'Simulation completed successfully'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def run_range_simulation(params, result_queue):
    """Run range simulation function, for multiprocessing"""
    try:
        min_students = params['min_students']
        max_students = params['max_students']
        step = params['student_step']
        repeat_count = params['repeat_count']
        rows = params['rows']
        cols = params['cols']
        cleaning_time = params['cleaning_time']
        humanities_ratio = params['humanities_ratio']
        science_ratio = params['science_ratio']
        engineering_ratio = params['engineering_ratio']

        results = []

        for total_students in range(min_students, max_students + 1, step):
            for run in range(repeat_count):
                # Use the next available simulation number for each run
                simulation_number = get_next_simulation_number(rows * cols, total_students)
                
                # Create library and students
                library = Library()
                library.initialize_seats(rows, cols)
                library.set_limit_reversed_time(timedelta(minutes=cleaning_time))
                
                # 计算各专业学生数量
                humanities_count = int(total_students * humanities_ratio / 100)
                science_count = int(total_students * science_ratio / 100)
                engineering_count = total_students - humanities_count - science_count  # Remaining as Engineering
                
                # 创建学生
                students = []
                for i in range(humanities_count):
                    if i < humanities_count // 3:
                        students.append(Student.create_humanities_diligent_student(i, library_capacity=rows*cols, total_students=total_students))
                    elif i < 2 * humanities_count // 3:
                        students.append(Student.create_humanities_medium_student(i, library_capacity=rows*cols, total_students=total_students))
                    else:
                        students.append(Student.create_humanities_lazy_student(i, library_capacity=rows*cols, total_students=total_students))

                for i in range(science_count):
                    if i < science_count // 3:
                        students.append(Student.create_science_diligent_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))
                    elif i < 2 * science_count // 3:
                        students.append(Student.create_science_medium_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))
                    else:
                        students.append(Student.create_science_lazy_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))

                for i in range(engineering_count):
                    if i < engineering_count // 3:
                        students.append(Student.create_engineering_diligent_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))
                    elif i < 2 * engineering_count // 3:
                        students.append(Student.create_engineering_medium_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))
                    else:
                        students.append(Student.create_engineering_lazy_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))

                # 将学生添加到图书馆
                library.students = students
                library._count = total_students  # Set student counter
                
                # 运行模拟
                simulation = Simulation(row=rows, column=cols, num_students=total_students, humanities_rate=humanities_count/total_students if total_students > 0 else 0, science_rate=science_count/total_students if total_students > 0 else 0, simulation_number=simulation_number)
                simulation.library = library  # 替换模拟中的图书馆实例
                simulation.run(run_all=True)

                # 保存结果到对应的座位数目录
                total_seats = rows * cols
                seat_folder_name = f"{total_seats}_seats_simulations"
                seat_simulation_path = os.path.join(SIMULATIONS_PATH, seat_folder_name)
                os.makedirs(seat_simulation_path, exist_ok=True)

                filename = f"{total_students}-{simulation.simulation_number}.json"
                filepath = os.path.join(seat_simulation_path, filename)

                # 保存模拟数据
                simulation.save_to_json(filepath)  # Use Simulation's save_to_json method to save data

                results.append({
                    'student_count': total_students,
                    'simulation_number': simulation.simulation_number,
                    'filepath': filepath,
                    'status': 'completed'
                })

        result_queue.put({
            'status': 'completed',
            'results': results,
            'message': f'Range simulation completed successfully'
        })

    except Exception as e:
        result_queue.put({
            'status': 'error',
            'error': str(e),
            'message': f'Range simulation failed: {str(e)}'
        })

@app.route('/api/repeat_simulation', methods=['POST'])
def repeat_simulation_api():
    """Repeat simulation API"""
    try:
        data = request.json
        use_multiprocessing = data.get('useMultiprocessing', False)
        
        if use_multiprocessing:
            # Use multiprocessing to run simulation
            result_queue = mp.Queue()
            
            # Prepare parameters
            params = {
                'min_students': data['minStudents'],
                'max_students': data['maxStudents'],
                'student_step': data.get('studentStep', 1),  # 默认步长为1
                'repeat_count': data['repeatCount'],
                'rows': data['rows'],
                'cols': data['cols'],
                'cleaning_time': data['cleaningTime'],
                'humanities_ratio': data['humanitiesRatio'],
                'science_ratio': data['scienceRatio'],
                'engineering_ratio': data['engineeringRatio']
            }
            
            # Create and start process
            process = mp.Process(target=run_range_simulation, args=(params, result_queue))
            process.start()
            process.join()  # Wait for process to complete
            
            # Get result
            result = result_queue.get()
            if result['status'] == 'error':
                return jsonify({'status': 'error', 'message': result['error']})
        else:
            # Run simulation in single thread
            min_students = data['minStudents']
            max_students = data['maxStudents']
            student_step = data.get('studentStep', 1)  # 默认步长为1
            repeat_count = data['repeatCount']
            rows = data['rows']
            cols = data['cols']
            cleaning_time = data['cleaningTime']
            humanities_ratio = data['humanitiesRatio']
            science_ratio = data['scienceRatio']
            engineering_ratio = data['engineeringRatio']

            results = []
            for total_students in range(min_students, max_students + 1, student_step):
                for run in range(repeat_count):
                    # Use the next available simulation number for each run
                    simulation_number = get_next_simulation_number(rows * cols, total_students)
                    
                    # Create library and students
                    library = Library()
                    library.initialize_seats(rows, cols)
                    library.set_limit_reversed_time(timedelta(minutes=cleaning_time))
                    
                    # 计算各专业学生数量
                    humanities_count = int(total_students * humanities_ratio / 100)
                    science_count = int(total_students * science_ratio / 100)
                    engineering_count = total_students - humanities_count - science_count  # Remaining as Engineering
                    
                    # 创建学生
                    students = []
                    for i in range(humanities_count):
                        if i < humanities_count // 3:
                            students.append(Student.create_humanities_diligent_student(i, library_capacity=rows*cols, total_students=total_students))
                        elif i < 2 * humanities_count // 3:
                            students.append(Student.create_humanities_medium_student(i, library_capacity=rows*cols, total_students=total_students))
                        else:
                            students.append(Student.create_humanities_lazy_student(i, library_capacity=rows*cols, total_students=total_students))

                    for i in range(science_count):
                        if i < science_count // 3:
                            students.append(Student.create_science_diligent_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))
                        elif i < 2 * science_count // 3:
                            students.append(Student.create_science_medium_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))
                        else:
                            students.append(Student.create_science_lazy_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))

                    for i in range(engineering_count):
                        if i < engineering_count // 3:
                            students.append(Student.create_engineering_diligent_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))
                        elif i < 2 * engineering_count // 3:
                            students.append(Student.create_engineering_medium_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))
                        else:
                            students.append(Student.create_engineering_lazy_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))

                    # 将学生添加到图书馆
                    library.students = students
                    library._count = total_students  # Set student counter
                    
                    # 运行模拟
                    simulation = Simulation(row=rows, column=cols, num_students=total_students, humanities_rate=humanities_count/total_students if total_students > 0 else 0, science_rate=science_count/total_students if total_students > 0 else 0, simulation_number=simulation_number)
                    simulation.library = library  # 替换模拟中的图书馆实例
                    simulation.run(run_all=True)

                    # 保存结果到对应的座位数目录
                    total_seats = rows * cols
                    seat_folder_name = f"{total_seats}_seats_simulations"
                    seat_simulation_path = os.path.join(SIMULATIONS_PATH, seat_folder_name)
                    os.makedirs(seat_simulation_path, exist_ok=True)

                    filename = f"{total_students}-{simulation.simulation_number}.json"
                    filepath = os.path.join(seat_simulation_path, filename)

                    # 保存模拟数据
                    simulation.save_to_json(filepath)  # Use Simulation's save_to_json method to save data

                    results.append({
                        'student_count': total_students,
                        'simulation_number': simulation.simulation_number,
                        'filepath': filepath,
                        'status': 'completed'
                    })

        return jsonify({'status': 'success', 'message': 'Range simulation completed successfully', 'results': results})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/start_range_simulation', methods=['POST'])
def start_range_simulation_api():
    """Start range simulation API - for compatibility with frontend"""
    try:
        data = request.json
        use_multiprocessing = data.get('useMultiprocessing', False)
        
        if use_multiprocessing:
            # Use multiprocessing to run simulation
            result_queue = mp.Queue()
            
            # Prepare parameters
            params = {
                'min_students': data['minStudents'],
                'max_students': data['maxStudents'],
                'student_step': data.get('studentStep', 1),  # 默认步长为1
                'repeat_count': data['repeatCount'],
                'rows': data['rows'],
                'cols': data['cols'],
                'cleaning_time': data['cleaningTime'],
                'humanities_ratio': data['humanitiesRatio'],
                'science_ratio': data['scienceRatio'],
                'engineering_ratio': data['engineeringRatio']
            }
            
            # Create and start process
            process = mp.Process(target=run_range_simulation, args=(params, result_queue))
            process.start()
            process.join()  # Wait for process to complete
            
            # Get result
            result = result_queue.get()
            if result['status'] == 'error':
                return jsonify({'status': 'error', 'message': result['error']})
            
            # Format results for frontend
            formatted_results = []
            if 'results' in result:
                for res in result['results']:
                    formatted_results.append({
                        'students': res.get('student_count', 0),
                        'number': res.get('simulation_number', 0),
                        'path': res.get('filepath', ''),
                        'status': res.get('status', 'completed')
                    })
            
            return jsonify({
                'status': 'success', 
                'message': f'Range simulation completed successfully with {len(formatted_results)} runs', 
                'results': formatted_results
            })
        else:
            # Run simulation in single thread
            min_students = data['minStudents']
            max_students = data['maxStudents']
            student_step = data.get('studentStep', 1)  # 默认步长为1
            repeat_count = data['repeatCount']
            rows = data['rows']
            cols = data['cols']
            cleaning_time = data['cleaningTime']
            humanities_ratio = data['humanitiesRatio']
            science_ratio = data['scienceRatio']
            engineering_ratio = data['engineeringRatio']

            results = []
            for total_students in range(min_students, max_students + 1, student_step):
                for run in range(repeat_count):
                    # Use the next available simulation number for each run
                    simulation_number = get_next_simulation_number(rows * cols, total_students)
                    
                    # Create library and students
                    library = Library()
                    library.initialize_seats(rows, cols)
                    library.set_limit_reversed_time(timedelta(minutes=cleaning_time))
                    
                    # 计算各专业学生数量
                    humanities_count = int(total_students * humanities_ratio / 100)
                    science_count = int(total_students * science_ratio / 100)
                    engineering_count = total_students - humanities_count - science_count  # Remaining as Engineering
                    
                    # 创建学生
                    students = []
                    for i in range(humanities_count):
                        if i < humanities_count // 3:
                            students.append(Student.create_humanities_diligent_student(i, library_capacity=rows*cols, total_students=total_students))
                        elif i < 2 * humanities_count // 3:
                            students.append(Student.create_humanities_medium_student(i, library_capacity=rows*cols, total_students=total_students))
                        else:
                            students.append(Student.create_humanities_lazy_student(i, library_capacity=rows*cols, total_students=total_students))

                    for i in range(science_count):
                        if i < science_count // 3:
                            students.append(Student.create_science_diligent_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))
                        elif i < 2 * science_count // 3:
                            students.append(Student.create_science_medium_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))
                        else:
                            students.append(Student.create_science_lazy_student(humanities_count + i, library_capacity=rows*cols, total_students=total_students))

                    for i in range(engineering_count):
                        if i < engineering_count // 3:
                            students.append(Student.create_engineering_diligent_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))
                        elif i < 2 * engineering_count // 3:
                            students.append(Student.create_engineering_medium_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))
                        else:
                            students.append(Student.create_engineering_lazy_student(humanities_count + science_count + i, library_capacity=rows*cols, total_students=total_students))

                    # 将学生添加到图书馆
                    library.students = students
                    library._count = total_students  # Set student counter
                    
                    # 运行模拟
                    simulation = Simulation(row=rows, column=cols, num_students=total_students, humanities_rate=humanities_count/total_students if total_students > 0 else 0, science_rate=science_count/total_students if total_students > 0 else 0, simulation_number=simulation_number)
                    simulation.library = library  # 替换模拟中的图书馆实例
                    simulation.run(run_all=True)

                    # 保存结果到对应的座位数目录
                    total_seats = rows * cols
                    seat_folder_name = f"{total_seats}_seats_simulations"
                    seat_simulation_path = os.path.join(SIMULATIONS_PATH, seat_folder_name)
                    os.makedirs(seat_simulation_path, exist_ok=True)

                    filename = f"{total_students}-{simulation.simulation_number}.json"
                    filepath = os.path.join(seat_simulation_path, filename)

                    # 保存模拟数据
                    simulation.save_to_json(filepath)  # Use Simulation's save_to_json method to save data

                    results.append({
                        'students': total_students,
                        'number': simulation.simulation_number,
                        'path': filepath,
                        'status': 'completed'
                    })

            return jsonify({
                'status': 'success', 
                'message': f'Range simulation completed successfully with {len(results)} runs', 
                'results': results
            })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Add new API endpoint for generating plots
@app.route('/api/generate_plots', methods=['POST'])
def generate_plots_api():
    """Generate plots from simulation data"""
    try:
        data = request.json
        seat_count = data['seat_count']
        plot_type = data['plot_type']
        
        if plot_type == 'student':
            # Generate student simulation plot
            student_count = data['student_count']
            from backend.plot import save_figure
            success = save_figure(seats=seat_count, students=student_count, show_plot=False)
            if success:
                # Determine expected path
                seat_folder = f"seats_{seat_count}"
                image_filename = f"students_{student_count}.png"
                expected_path = os.path.join(seat_folder, image_filename)
                return jsonify({
                    'status': 'success',
                    'message': f'Student plot for {student_count} students with {seat_count} seats generated successfully',
                    'expected_path': expected_path
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': f'Failed to generate student plot for {student_count} students with {seat_count} seats'
                })
        elif plot_type == 'analysis':
            # Generate analysis plot
            min_students = data['min_students']
            max_students = data['max_students']
            from backend.data_analysis import run_analysis
            results = run_analysis(seat_count, min_students, max_students)
            if results is not None:
                # Determine expected path
                seat_folder = f"seats_{seat_count}"
                file_name = f"analysis({seat_count}-{min_students}-{max_students}).png"
                expected_path = os.path.join(seat_folder, file_name)
                return jsonify({
                    'status': 'success',
                    'message': f'Analysis plot for {seat_count} seats, students {min_students}-{max_students} generated successfully',
                    'expected_path': expected_path
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': f'Failed to generate analysis plot for {seat_count} seats, students {min_students}-{max_students}'
                })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid plot type. Use "student" or "analysis".'
            })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Add new API endpoint for batch plot generation
@app.route('/api/generate_batch_plots', methods=['POST'])
def generate_batch_plots_api():
    """Generate batch plots: both analysis and all student plots in range"""
    try:
        data = request.json
        seat_count = data['seat_count']
        min_students = data['min_students']
        max_students = data['max_students']
        generate_analysis = data.get('generate_analysis', True)
        generate_student_plots = data.get('generate_student_plots', True)
        
        results = []
        
        # Generate analysis plot if requested
        if generate_analysis:
            from backend.data_analysis import run_analysis
            analysis_results = run_analysis(seat_count, min_students, max_students)
            if analysis_results is not None:
                seat_folder = f"seats_{seat_count}"
                file_name = f"analysis({seat_count}-{min_students}-{max_students}).png"
                expected_path = os.path.join(seat_folder, file_name)
                results.append({
                    'type': 'analysis',
                    'path': expected_path,
                    'status': 'success',
                    'message': f'Analysis plot for {seat_count} seats, students {min_students}-{max_students} generated'
                })
            else:
                results.append({
                    'type': 'analysis',
                    'status': 'error',
                    'message': f'Failed to generate analysis plot for {seat_count} seats, students {min_students}-{max_students}'
                })
        
        # Generate student plots if requested
        if generate_student_plots:
            from backend.plot import save_figure
            student_results = []
            for student_count in range(min_students, max_students + 1):
                success = save_figure(seats=seat_count, students=student_count, show_plot=False)
                if success:
                    seat_folder = f"seats_{seat_count}"
                    image_filename = f"students_{student_count}.png"
                    expected_path = os.path.join(seat_folder, image_filename)
                    student_results.append({
                        'type': 'student',
                        'student_count': student_count,
                        'path': expected_path,
                        'status': 'success',
                        'message': f'Student plot for {student_count} students with {seat_count} seats generated'
                    })
                else:
                    student_results.append({
                        'type': 'student',
                        'student_count': student_count,
                        'status': 'error',
                        'message': f'Failed to generate student plot for {student_count} students with {seat_count} seats'
                    })
            results.extend(student_results)
        
        return jsonify({
            'status': 'success',
            'message': f'Batch generation completed for seat count {seat_count}, students {min_students}-{max_students}',
            'results': results
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Add new API endpoint for checking existing plots
@app.route('/api/check_existing_plots', methods=['POST'])
def check_existing_plots_api():
    """Check for existing plots based on parameters"""
    try:
        data = request.json
        seat_count = data['seat_count']
        min_students = data.get('min_students')
        max_students = data.get('max_students')
        check_analysis = data.get('check_analysis', True)
        check_student_plots = data.get('check_student_plots', True)
        filter_by_seat_count = data.get('filter_by_seat_count', True)
        
        # Get all available plots
        all_plots = []
        if os.path.exists(FIGURES_PATH):
            for root, dirs, files in os.walk(FIGURES_PATH):
                for file in files:
                    if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        # Return relative to figures directory path
                        rel_path = os.path.relpath(os.path.join(root, file), FIGURES_PATH)
                        # Ensure path uses forward slashes (on Windows)
                        rel_path = rel_path.replace('\\', '/')
                        all_plots.append({
                            'path': rel_path,
                            'name': file
                        })
        
        # Filter plots based on seat count and student range
        analysis_plots = []
        student_plots = []
        
        seat_folder = f"seats_{seat_count}"
        
        for plot in all_plots:
            # Check if plot belongs to the specified seat count
            if filter_by_seat_count and not plot['path'].startswith(f"{seat_folder}/"):
                continue
            
            # Check if it's an analysis plot
            if 'analysis' in plot['name'] and check_analysis:
                # Check if it matches the seat count and student range
                if f"({seat_count}-" in plot['name']:
                    if min_students is not None and max_students is not None:
                        # Extract student range from analysis plot name like "analysis(9-9-19).png"
                        import re
                        match = re.search(rf"analysis\({seat_count}-(\d+)-(\d+)\)", plot['name'])
                        if match:
                            plot_min, plot_max = int(match.group(1)), int(match.group(2))
                            if plot_min >= min_students and plot_max <= max_students:
                                analysis_plots.append(plot)
                        else:
                            # If regex doesn't match, check if it contains the seat count anyway
                            analysis_plots.append(plot)
                    else:
                        analysis_plots.append(plot)
            # Check if it's a student plot
            elif 'students_' in plot['name'] and check_student_plots:
                # Check if it matches the seat count
                if plot['path'].startswith(f"{seat_folder}/"):
                    if min_students is not None and max_students is not None:
                        # Extract student count from student plot name like "students_15.png"
                        import re
                        match = re.search(r"students_(\d+)\.png", plot['name'])
                        if match:
                            student_count = int(match.group(1))
                            if min_students <= student_count <= max_students:
                                student_plots.append(plot)
                        else:
                            # If regex doesn't match, check if it contains the seat count anyway
                            student_plots.append(plot)
                    else:
                        student_plots.append(plot)
        
        # Create summary
        summary = {
            'analysis_count': len(analysis_plots),
            'student_count': len(student_plots),
            'total_count': len(analysis_plots) + len(student_plots)
        }
        
        return jsonify({
            'status': 'success',
            'results': {
                'analysis_plots': analysis_plots,
                'student_plots': student_plots
            },
            'summary': summary,
            'message': f'Found {summary["total_count"]} plots for seat count {seat_count}'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)