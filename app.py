from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime
from backend.simulation import Simulation

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 全局模拟实例
simulation = None

# 存储模拟数据的目录
DATA_DIR = "simulation_data"
os.makedirs(DATA_DIR, exist_ok=True)

@app.route('/')
def index():
    """提供前端页面"""
    return send_file('frontend.html')

@app.route('/api/start', methods=['POST'])
def start_simulation():
    """启动新模拟"""
    global simulation
    
    # 获取前端发送的参数
    data = request.json
    row = data.get('row', 20)
    column = data.get('column', 20)
    num_students = data.get('num_students', 200)
    humanities_rate = data.get('humanities_rate', 0.3)
    science_rate = data.get('science_rate', 0.3)
    
    # 创建新的模拟实例
    simulation = Simulation(row=row, column=column, num_students=num_students, 
                           humanities_rate=humanities_rate, science_rate=science_rate)
    
    # 执行一步模拟以获取初始状态
    simulation.step()
    
    return jsonify({
        "status": "success",
        "message": "Simulation started successfully",
        "current_time": simulation.library.current_time.strftime('%H:%M')
    })

@app.route('/api/step', methods=['POST'])
def step_simulation():
    """执行一步模拟"""
    global simulation
    
    if simulation is None:
        return jsonify({"status": "error", "message": "No simulation running"}), 400
    
    # 执行一步模拟
    simulation.step()
    
    # 获取当前状态
    status_data = get_current_status()
    return jsonify(status_data)

@app.route('/api/status', methods=['GET'])
def get_status():
    """获取当前模拟状态"""
    global simulation
    
    if simulation is None:
        return jsonify({"status": "error", "message": "No simulation running"}), 400
    
    status_data = get_current_status()
    return jsonify(status_data)

@app.route('/api/seats', methods=['GET'])
def get_seats():
    """获取座位状态"""
    global simulation
    
    if simulation is None:
        return jsonify({"status": "error", "message": "No simulation running"}), 400
    
    seats_data = []
    for seat in simulation.library.seats:
        seat_info = {
            "id": seat.coordinate[0] * 20 + seat.coordinate[1],  # 将坐标转换为ID
            "x": seat.coordinate[0],
            "y": seat.coordinate[1],
            "status": seat.status.name,
            "lamp": seat.lamp,
            "socket": seat.socket,
            "window": seat.window,
            "taken_time": seat.taken_time.strftime('%H:%M:%S') if seat.taken_time.year > 1900 else None
        }
        seats_data.append(seat_info)
    
    return jsonify({
        "seats": seats_data,
        "total_seats": len(seats_data)
    })

@app.route('/api/control', methods=['POST'])
def control_simulation():
    """控制模拟（暂停、重置等）"""
    global simulation
    
    data = request.json
    action = data.get('action')
    
    if action == 'pause':
        # 暂停功能在当前实现中不需要特殊处理
        return jsonify({"status": "success", "message": "Simulation paused"})
    elif action == 'reset':
        # 重置模拟
        simulation = None
        return jsonify({"status": "success", "message": "Simulation reset"})
    else:
        return jsonify({"status": "error", "message": "Invalid action"}), 400

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计数据"""
    global simulation
    
    if simulation is None:
        return jsonify({"status": "error", "message": "No simulation running"}), 400
    
    total_seats = len(simulation.library.seats)
    taken_seats = simulation.library.count_taken_seats()
    reversed_seats = simulation.library.count_reversed_seats()
    unsatisfied_count = simulation.library.count_unsatisfied()
    
    occupancy_rate = (taken_seats / total_seats * 100) if total_seats > 0 else 0
    reverse_rate = (reversed_seats / total_seats * 100) if total_seats > 0 else 0
    unsatisfied_rate = (unsatisfied_count / 100 * 100) if 100 > 0 else 0  # 假设有100个学生
    
    return jsonify({
        "total_seats": total_seats,
        "taken_seats": taken_seats,
        "reversed_seats": reversed_seats,
        "unsatisfied_count": unsatisfied_count,
        "occupancy_rate": round(occupancy_rate, 2),
        "reverse_rate": round(reverse_rate, 2),
        "unsatisfied_rate": round(unsatisfied_rate, 2),
        "current_time": simulation.library.current_time.strftime('%H:%M')
    })

@app.route('/api/set_limit', methods=['POST'])
def set_limit():
    """设置占座时间限制"""
    global simulation
    
    if simulation is None:
        return jsonify({"status": "error", "message": "No simulation running"}), 400
    
    data = request.json
    time_limit = data.get('time_limit')
    
    # 解析时间限制格式 HH:MM
    try:
        hours, minutes = map(int, time_limit.split(':'))
        from datetime import timedelta
        time_delta = timedelta(hours=hours, minutes=minutes)
        simulation.library.set_limit_reversed_time(time_delta)
        
        return jsonify({
            "status": "success", 
            "message": f"Time limit set to {time_limit}",
            "time_limit": time_limit
        })
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid time format. Use HH:MM"}), 400

def get_current_status():
    """获取当前模拟的完整状态"""
    if simulation is None:
        return {"status": "error", "message": "No simulation running"}
    
    total_seats = len(simulation.library.seats)
    taken_seats = simulation.library.count_taken_seats()
    reversed_seats = simulation.library.count_reversed_seats()
    unsatisfied_count = simulation.library.count_unsatisfied()
    
    occupancy_rate = (taken_seats / total_seats * 100) if total_seats > 0 else 0
    reverse_rate = (reversed_seats / total_seats * 100) if total_seats > 0 else 0
    unsatisfied_rate = (unsatisfied_count / max(len(simulation.library.students), 1) * 100)
    
    return {
        "current_time": simulation.library.current_time.strftime('%H:%M'),
        "total_seats": total_seats,
        "taken_seats": taken_seats,
        "reversed_seats": reversed_seats,
        "unsatisfied_count": unsatisfied_count,
        "occupancy_rate": round(occupancy_rate, 2),
        "reverse_rate": round(reverse_rate, 2),
        "unsatisfied_rate": round(unsatisfied_rate, 2),
        "status": "running"
    }

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)