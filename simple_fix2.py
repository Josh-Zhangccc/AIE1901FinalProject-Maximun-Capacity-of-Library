#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单直接地修复函数格式
"""
def simple_fix():
    with open('C:\\Users\\18136\\Desktop\\AIE1901_FinalExamSimulation\\frontend\\app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换所有不正确的repeat_simulation函数定义为正确的格式
    import re
    
    # 定义一个函数来修复函数定义格式
    def replace_func(match):
        return "\n@app.route('/repeat_simulation')\n" + \
               "def repeat_simulation():\n" + \
               '    """Repeat simulation page"""\n' + \
               "    return render_template('repeat_simulation.html')\n\n"
    
    # 匹配从@app.route('/repeat_simulation')开始到return语句结束的整个块
    pattern = r'\n@app\.route\\(\'/repeat_simulation\'\)\s*\n\s*\n*def repeat_simulation\\(\\):\s*\n\s*\n*\s*""".*?"""\s*\n\s*\n*\s*return render_template\\(.*?\\)\s*\n\s*\n*'
    content = re.sub(pattern, replace_func, content, flags=re.DOTALL)
    
    # 保存修复后的内容
    with open('C:\\Users\\18136\\Desktop\\AIE1901_FinalExamSimulation\\frontend\\app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed function format in app.py")

if __name__ == "__main__":
    simple_fix()