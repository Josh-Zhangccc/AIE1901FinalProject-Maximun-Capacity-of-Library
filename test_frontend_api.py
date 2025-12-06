import os
import sys
import json
import threading
import time
from flask import Flask

# 添加项目根目录到Python路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from frontend.app import app

def run_flask_app():
    """在后台运行Flask应用"""
    app.run(debug=False, host='127.0.0.1', port=5000)

def test_frontend_api():
    """测试前端API端点"""
    print("启动Flask应用...")
    
    # 在后台线程启动Flask应用
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    
    # 等待服务器启动
    time.sleep(3)
    
    import requests
    
    print("开始测试API端点...")
    
    # 测试获取座位数量
    try:
        response = requests.get("http://127.0.0.1:5000/api/seat_counts", timeout=10)
        print(f"座位数量API状态: {response.status_code}")
        if response.status_code == 200:
            seat_counts = response.json()
            print(f"找到 {len(seat_counts)} 个座位数选项")
            for seat in seat_counts:
                print(f"  - {seat['label']}: {seat['value']}")
        else:
            print(f"座位数量API错误: {response.text}")
    except Exception as e:
        print(f"无法连接到座位数量API: {e}")
    
    # 测试获取图像
    try:
        response = requests.get("http://127.0.0.1:5000/api/plots", timeout=10)
        print(f"\n图像列表API状态: {response.status_code}")
        if response.status_code == 200:
            plots = response.json()
            print(f"找到 {len(plots)} 个图像")
            for plot in plots[:10]:  # 只显示前10个
                print(f"  - {plot['name']}: {plot['path']}")
        else:
            print(f"图像列表API错误: {response.text}")
    except Exception as e:
        print(f"无法连接到图像列表API: {e}")
    
    # 测试学生文件列表（使用第一个找到的座位数）
    try:
        # 先获取座位数
        response = requests.get("http://127.0.0.1:5000/api/seat_counts", timeout=10)
        if response.status_code == 200:
            seat_counts = response.json()
            if seat_counts:
                seat_folder = seat_counts[0]['value']
                response = requests.get(f"http://127.0.0.1:5000/api/student_files/{seat_folder}", timeout=10)
                print(f"\n学生文件API状态: {response.status_code}")
                if response.status_code == 200:
                    files = response.json()
                    print(f"找到 {len(files)} 个学生文件")
                    for file in files[:5]:  # 只显示前5个
                        print(f"  - {file['name']}: {file['student_count']} 学生")
                else:
                    print(f"学生文件API错误: {response.text}")
            else:
                print("没有找到任何座位数")
        else:
            print("无法获取座位数列表")
    except Exception as e:
        print(f"无法连接到学生文件API: {e}")
    
    # 测试图像生成API
    try:
        print("\n测试图像生成API...")
        # 测试学生图像生成
        payload = {
            "seat_count": 9,
            "student_count": 10,
            "plot_type": "student"
        }
        response = requests.post("http://127.0.0.1:5000/api/generate_plots", 
                                json=payload, timeout=30)  # 增加超时时间
        print(f"学生图像生成API状态: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  结果: {result.get('message', '无消息')}")
        else:
            print(f"  学生图像生成API错误: {response.text}")
    except Exception as e:
        print(f"无法连接到学生图像生成API: {e}")
    
    try:
        # 测试分析图像生成
        payload = {
            "seat_count": 9,
            "min_students": 9,
            "max_students": 19,
            "plot_type": "analysis"
        }
        response = requests.post("http://127.0.0.1:5000/api/generate_plots", 
                                json=payload, timeout=60)  # 更长的超时时间
        print(f"分析图像生成API状态: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  结果: {result.get('message', '无消息')}")
        else:
            print(f"  分析图像生成API错误: {response.text}")
    except Exception as e:
        print(f"无法连接到分析图像生成API: {e}")
    
    print("\nAPI测试完成")
    
    # 让应用运行一段时间以便测试
    time.sleep(2)

if __name__ == "__main__":
    test_frontend_api()