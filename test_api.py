import requests
import json
import os
import sys

# 添加项目根目录到Python路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

def test_api_endpoints():
    """测试API端点是否正常工作"""
    base_url = "http://127.0.0.1:5000"
    
    print("测试API端点...")
    
    # 测试获取座位数量
    try:
        response = requests.get(f"{base_url}/api/seat_counts")
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
        response = requests.get(f"{base_url}/api/plots")
        print(f"\n图像列表API状态: {response.status_code}")
        if response.status_code == 200:
            plots = response.json()
            print(f"找到 {len(plots)} 个图像")
            for plot in plots[:5]:  # 只显示前5个
                print(f"  - {plot['name']}: {plot['path']}")
        else:
            print(f"图像列表API错误: {response.text}")
    except Exception as e:
        print(f"无法连接到图像列表API: {e}")
    
    # 测试学生文件列表（使用第一个找到的座位数）
    if 'seat_counts' in locals() and len(seat_counts) > 0:
        try:
            seat_folder = seat_counts[0]['value']
            response = requests.get(f"{base_url}/api/student_files/{seat_folder}")
            print(f"\n学生文件API状态: {response.status_code}")
            if response.status_code == 200:
                files = response.json()
                print(f"找到 {len(files)} 个学生文件")
                for file in files[:5]:  # 只显示前5个
                    print(f"  - {file['name']}: {file['student_count']} 学生")
            else:
                print(f"学生文件API错误: {response.text}")
        except Exception as e:
            print(f"无法连接到学生文件API: {e}")
    
    print("\nAPI测试完成")

if __name__ == "__main__":
    test_api_endpoints()