# AIE1901 期末考试模拟项目

## 项目概述

这是一个基于Python的图书馆座位占用行为模拟系统，旨在研究学生占座行为与图书馆管理措施对空间利用率和图书馆最大动态容量之间的关系。项目使用DeepSeek的LLM API来模拟学生行为，包含后端Python代码和前端HTML界面。

项目核心功能：
- 模拟图书馆环境（当前网格大小20x20，实际座位数量根据可用座位决定）
- 模拟学生基于个人作息、课程表和座位偏好的行为
- 管理座位状态（空闲、占用、占座、标记清理）
- 基于时间限制清理违规占座
- 支持模拟数据的保存与复现功能
- 提供前端界面进行参数调节和结果可视化

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
│       ├── test_prompt.py  # 提示词功能测试
│       ├── test_seats.py   # 座位类单元测试
│       └── test_students.py # 学生类单元测试
├── config.py               # 配置文件（当前为空）
├── main.py                 # 主程序入口
├── start.py                # 启动脚本（当前为空，需要实现Windows命令行脚本）
├── utils.py                # 工具函数，包含API配置
├── seat_simulation_env.yml # Conda环境配置文件
└── 要求.txt               # 项目需求文档
```

## 技术栈

- **后端**: Python 3.13.9
- **LLM API**: DeepSeek (通过OpenAI包调用)
- **Web框架**: Flask
- **依赖管理**: Conda
- **前端**: HTML, JavaScript (计划中)
- **测试框架**: unittest

## 核心组件

### 座位系统 (seats.py)
- 座位状态：空闲(vacant)、占用(taken)、占座(reverse)、标记清理(signed)
- 座位属性：坐标(x, y)、是否有台灯(lamp)、插座(socket)、是否靠窗(window)
- 功能：占用、离开(完全/占座)、标记占座、清理超时占座、时间更新、满意度计算
- 实现了完整的单元测试，确保状态转换逻辑正确

### 学生系统 (students.py)
- 使用LLM客户端模拟学生行为
- 学生属性：个人性格(守序/利己)、作息偏好(早鸟/正常/夜猫子)、专注度、课程情况、座位偏好
- 行为逻辑：选择座位、状态改变(离开/回座)、是否占座
- 包含状态枚举(SLEEP, LEARNING, AWAY, GONE)和动态日程表生成
- 根据座位满意度和图书馆规则决定占座行为
- 时间更新步长为30分钟

### LLM客户端 (agents.py)
- 基于DeepSeek API的客户端实现
- 使用预设提示词与LLM交互
- 支持JSON格式响应解析
- 包含错误处理和JSON解析功能

### 图书馆系统 (library.py)
- 初始化网格中的座位
- 随机分配台灯、插座、靠窗属性
- 管理学生初始化
- **注意**: 当前library.py文件的实现尚不完整，只包含基本方法框架

### 模拟框架 (simulation.py)
- 协调图书馆、学生和座位系统
- 管理模拟时间流(30分钟为一个时间步)
- **注意**: 当前simulation.py文件的实现尚不完整，只包含基本方法框架

## 环境配置

使用Conda创建指定环境：
```bash
conda env create -f seat_simulation_env.yml
```

环境包含必要的Python包，如Flask、OpenAI、httpx等。

## API配置

在`utils.py`中配置DeepSeek API：
- `BASE_URL`: https://api.deepseek.com
- `API_KEY`: sk-cf8230f3e78a4cedadf7f7ab158f5441
- `MODEL`: deepseek-chat

## 运行方式

项目需要实现一个Windows命令行脚本"start-app"来直接运行后端Python程序。后端使用Flask框架提供API，前端使用HTML实现。

当前运行方式：
```bash
# 激活conda环境
conda activate seat-simulation

# 运行主程序
python main.py
```

## 测试

项目包含单元测试，位于`backend/test/`目录下：
- `test_seats.py`: 座位类的完整单元测试，覆盖所有状态转换场景
- `test_prompt.py`: 提示词功能测试
- `test_students.py`: 学生类的完整单元测试，覆盖学生行为的各种场景
  - 测试学生初始化、日程表生成
  - 测试座位选择、占用和离开逻辑
  - 测试占座决策逻辑
  - 测试时间更新和状态转换

运行测试：
```bash
python -m pytest backend/test/
# 或
python backend/test/test_seats.py
python backend/test/test_students.py
```

## 模拟特性

- **时间系统**: 模拟一天(7:00-24:00)，每30分钟更新一次
- **学生行为**: 基于课程表、作息和占座度的智能决策
- **数据记录**: 记录每次更新的数据以支持模拟复现
- **参数调节**: 用户可调节学生数量、座位偏好、检查清理时间等参数
- **座位初始化**: 网格中的座位，随机分配台灯、插座、靠窗属性
- **座位状态管理**: 包括占用时间跟踪和状态转换

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

目前项目架构已建立，包含完整的座位管理系统、LLM客户端和提示词系统。测试用例已实现，特别是座位系统和学生系统的单元测试覆盖了各种场景。需要进一步完善模拟逻辑、学生行为模拟和前端界面。start.py启动脚本仍需实现Windows命令行脚本功能。模拟时间更新步长为30分钟，而非需求文档中提到的15分钟。

**待完善部分：**
- library.py 和 simulation.py 需要完整的实现
- start.py 启动脚本需要创建
- 前端界面需要开发
- 数据记录和复现功能需要实现
- main.py 需要实现完整的模拟流程