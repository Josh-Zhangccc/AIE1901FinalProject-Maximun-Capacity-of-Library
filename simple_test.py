import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

from backend.library import Library

# 创建图书馆实例并测试座位初始化
library = Library()
print("正在初始化座位...")
library.initialize_seats(lamp_rate=0.5, socket_rate=0.5)
print(f"初始化后座位总数: {len(library.seats)}")
print("如果数量过多，说明存在循环逻辑错误")