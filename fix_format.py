#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
精确修复repeat_simulation函数定义格式
"""

def fix_function_format():
    # 读取整个文件
    with open('C:\\Users\\18136\\Desktop\\AIE1901_FinalExamSimulation\\frontend\\app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 手动替换函数定义部分，确保格式正确
    # 查找并替换
    old_section = '\n@app.route(\'/repeat_simulation\')\n\ndef repeat_simulation():\n\n    \"\"\"Repeat simulation page\"\"\"\n\n    return render_template(\'/repeat_simulation.html\')\n\n\n'
    new_section = '\n@app.route(\'/repeat_simulation\')\ndef repeat_simulation():\n    \"\"\"Repeat simulation page\"\"\"\n    return render_template(\'/repeat_simulation.html\')\n\n'
    
    if old_section in content:
        content = content.replace(old_section, new_section)
    else:
        # 如果上面的格式不匹配，尝试其他可能的格式
        import re
        # 匹配有额外空行的函数定义
        pattern = r'(@app\\.route\\(\'/repeat_simulation\\'\)\\s*\\n\\s*\\n*(def repeat_simulation\\(\\):\\s*\\n)\\s*\\n*(\\s*\"\"\".*?\"\"\"\\s*\\n)\\s*\\n*(\\s*return render_template\\(.*?\\)\\s*\\n)'
        replacement = r'\1\2    \3    \4\n'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # 保存文件
    with open('C:\\Users\\18136\\Desktop\\AIE1901_FinalExamSimulation\\frontend\\app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed function format in app.py")

if __name__ == "__main__":
    fix_function_format()