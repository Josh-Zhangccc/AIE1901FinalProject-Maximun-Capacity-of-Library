#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完全重构有问题的函数定义部分
"""
def fix_function_definition():
    with open('C:\\Users\\18136\\Desktop\\AIE1901_FinalExamSimulation\\frontend\\app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并修复 repeat_simulation 函数定义部分
    # 找到 @app.route('/repeat_simulation') 到 def repeat_simulation():
    import re
    
    # 定义正确的函数格式
    correct_function = '''@app.route('/repeat_simulation')
def repeat_simulation():
    """Repeat simulation page"""
    return render_template('repeat_simulation.html')
'''

    # 使用正则表达式替换整个函数定义部分
    pattern = r'(@app\.route\\(\'/repeat_simulation\'\)\s*\n\s*\n*def repeat_simulation\\(\\):\s*\n\s*\n*(\s*\"\"\".*?\"\"\"\s*\n\s*\n*)?\s*return render_template\\(.*?\\)\s*\n(\s*return render_template\\(.*?\\)\s*\n)?(\s*\n)*)'
    content = re.sub(pattern, correct_function + '\n\n', content, flags=re.DOTALL)
    
    # 保存修复后的文件
    with open('C:\\Users\\18136\\Desktop\\AIE1901_FinalExamSimulation\\frontend\\app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed function definition in app.py")

if __name__ == "__main__":
    fix_function_definition()