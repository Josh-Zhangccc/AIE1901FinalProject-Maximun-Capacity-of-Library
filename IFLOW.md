# AIE1901 期末考试模拟项目

## 项目概述

这是一个基于Python的图书馆座位占用行为模拟系统，旨在研究学生占座行为与图书馆管理措施对空间利用率和图书馆最大动态容量之间的关系。项目使用DeepSeek的LLM API来模拟学生行为，包含后端Python代码。

项目核心功能：
- 模拟图书馆环境（20x20网格，400个座位）
- 模拟学生基于个人作息、课程表和座位偏好的行为
- 管理座位状态（空闲、占用、占座、标记清理）
- 基于时间限制清理违规占座
- 支持模拟数据的保存与复现功能
- 提供参数调节功能

## 项目结构

```
AIE1901_FinalExamSimulation/
├── backend/                 # 后端代码
│   ├── __init__.py         # 包初始化文件
│   ├── agents.py           # LLM客户端，用于与DeepSeek API交互
│   ├── library.py          # 图书馆类，管理座位和学生初始化
│   ├── prompt.py           # 各种LLM提示词模板
│   ├── seats.py            # 座位类，管理座位状态和属性
│   ├── simulation.py       # 模拟主类，协调整个模拟过程
│   ├── students.py         # 学生类，模拟学生行为
│   └── test/               # 测试目录
│       ├── __init__.py     # 包初始化文件
│       ├── test_interactions.py # 座位、学生和图书馆交互测试
│       ├── test_prompt.py  # 提示词功能测试
│       ├── test_seats.py   # 座位类单元测试
│       └── test_students.py # 学生类单元测试
├── config.py               # 配置文件
├── IFLOW.md                # 项目说明文档
├── main.py                 # 主程序入口
├── seat_simulation_env.yml # Conda环境配置文件
├── simple_test.py          # 简单测试脚本
├── simple_check.py         # 简单检查脚本
├── specific_test.py        # 特定功能测试脚本
├── comprehensive_test.py   # 综合测试脚本
├── problem_check.py        # 问题检查脚本
├── test_seats_fixed.py     # 修复后的座位测试
├── start.py                # Python启动脚本
├── start-app.bat           # Windows批处理启动脚本
├── utils.py                # 工具函数，包含API配置
├── code_issue_report.md    # 代码问题报告文档
└── 要求.txt               # 项目需求文档
```

## 技术栈

- **后端**: Python 3.13.9
- **LLM API**: DeepSeek (通过OpenAI包调用)
- **依赖管理**: Conda
- **Web框架**: Flask (包含Flask-CORS用于跨域)
- **测试框架**: unittest, pytest
- **HTTP Client**: OpenAI Python Package

## 核心组件

### 座位系统 (seats.py)
- 座位状态：空闲(vacant)、占用(taken)、占座(reverse)、标记清理(signed) - 使用Status枚举
- 座位属性：坐标(x, y)、是否有台灯(lamp)、插座(socket)、是否靠窗(window)
- 功能：占用、离开(完全/占座)、标记占座、清理超时占座、时间更新、满意度计算、拥挤参数计算
- 实现了完整的单元测试，确保状态转换逻辑正确
- 时间更新步长为30分钟

### 学生系统 (students.py)
- 使用LLM客户端模拟学生行为
- 学生属性：个人性格(守序/利己)、作息偏好(早鸟/正常/夜猫子)、专注度、课程情况、座位偏好
- 行为逻辑：选择座位、状态改变(离开/回座)、是否占座
- 包含状态枚举(SLEEP, LEARNING, AWAY, GONE) - 使用StudentState枚举
- 支持创建不同专业(文科/理科/工科)和不同学习程度(勤奋/中等/懒惰)的学生
- 根据座位满意度和图书馆规则决定占座行为
- 通过LLM生成动态日程表
- 时间更新步长为30分钟

### LLM客户端 (agents.py)
- 基于DeepSeek API的客户端实现
- 使用OpenAI Python包与DeepSeek API交互
- 使用预设提示词与LLM交互
- 支持JSON格式响应解析
- 包含错误处理和JSON解析功能

### 图书馆系统 (library.py)
- 初始化20x20网格中的座位
- 随机分配台灯、插座属性，边缘座位自动为靠窗座位
- 管理学生初始化，支持不同专业(人文、科学、工程)和学习程度(勤奋、中等、懒惰)的学生
- 实现座位清理机制(标记占座、清理超时占座)
- 计算座位拥挤参数，统计图书馆利用率
- 时间更新步长为15分钟
- 包含清理超时占座逻辑和标记机制

### 模拟框架 (simulation.py)
- 协调图书馆、学生和座位系统
- 管理模拟时间流
- 提供交互式命令行界面，支持 step, status, seats, time, quit, help 命令
- 实现了实时的模拟状态查看和参数调整功能

## 环境配置

使用Conda创建指定环境：
```bash
conda env create -f seat_simulation_env.yml
```

环境包含必要的Python包，如Flask、Flask-CORS、OpenAI、httpx等。

## API配置

在`utils.py`中配置DeepSeek API：
- `BASE_URL`: https://api.deepseek.com
- `API_KEY`: sk-cf8230f3e78a4cedadf7f7ab158f5441
- `MODEL`: deepseek-chat

### 运行方式

当前运行方式：
```bash
# 激活conda环境
conda activate seat-simulation

# 运行主程序
python main.py
```

或者使用Windows批处理文件：
```bash
start-app.bat
```

## 测试

项目包含单元测试，位于`backend/test/`目录下：
- `test_seats.py`: 座位类的完整单元测试，覆盖所有状态转换场景
- `test_prompt.py`: 提示词功能测试
- `test_students.py`: 学生类的完整单元测试，覆盖学生行为的各种场景
- `test_interactions.py`: 座位、学生和图书馆之间交互的综合测试
  - 测试学生与座位的基本交互
  - 测试占座行为
  - 测试图书馆的占座标记和清理系统
  - 测试基于学生日程的交互
  - 测试座位舒适度和拥挤度计算
  - 测试图书馆座位计数功能

运行测试：
```bash
python -m pytest backend/test/
# 或
python backend/test/test_seats.py
python backend/test/test_students.py
python backend/test/test_interactions.py
```

## 模拟特性

- **时间系统**: 模拟一天(7:00-24:00)，图书馆时间更新步长为15分钟，学生时间更新步长为30分钟
- **学生行为**: 基于课程表、作息和占座度的智能决策
- **数据记录**: 记录每次更新的数据以支持模拟复现 (计划中)
- **参数调节**: 用户可调节学生数量、座位偏好、检查清理时间等参数 (计划中)
- **座位初始化**: 20x20网格中的座位，随机分配台灯、插座属性，边缘座位为靠窗座位
- **座位状态管理**: 包括占用时间跟踪和状态转换
- **学生类型**: 支持3种专业(人文、科学、工程)和3种学习程度(勤奋、中等、懒惰)的学生，共9种不同类型的学生
- **交互测试**: 包含综合交互测试，验证系统各组件间的协作关系
- **交互式命令行界面**: 支持实时查看模拟状态、座位概览和调整时间限制

## 提示词系统 (prompt.py)

包含两个主要的LLM提示词模板：
- `schedule_prompt`: 根据学生特征生成日程表
- `leave_prompt`: 根据学生性格和满意度判断是否占座

## 前端功能（计划中）

- 中英文语言选择
- 创建新模拟/复现旧模拟
- 滑块调节学生数量、座位偏好、检查和清理时间
- 图书馆座位可视化显示
- 模拟数据可视化图表，支持多种可隐藏的图表

## 项目状态

目前项目架构已建立，包含完整的座位管理系统、学生系统、LLM客户端和提示词系统。测试用例已实现，特别是座位系统、学生系统和交互测试覆盖了各种场景。图书馆系统已实现基本功能，包括座位初始化、学生初始化和管理功能。

**待完善部分：**
- 前端界面需要开发
- 模拟数据记录与复现功能需要实现
- 完整的模拟流程需要实现
- 模拟结果可视化功能需要实现