# AIE1901 Final Project: Maximun Capacity of Library

## 图书馆最大容量研究 - 基于LLM的座位占用行为模拟系统

### 项目概述

这是一个基于Python的图书馆座位占用行为模拟系统，旨在研究学生占座行为与图书馆管理措施对空间利用率和图书馆最大动态容量之间的关系。项目使用DeepSeek的LLM API来模拟学生行为，包含完整的后端代码和数据可视化功能。

### 核心功能

- 模拟图书馆环境（支持自定义网格大小，默认3x3网格，9个座位作为演示，可扩展到更大规模）
- 模拟学生基于个人作息、课程表和座位偏好的行为
- 管理座位状态（空闲、占用、占座、标记清理）
- 基于时间限制清理违规占座
- 支持模拟数据的保存与复现功能
- 提供参数调节功能和交互式命令行界面
- 实现模拟数据的可视化分析功能

### 项目结构

```
AIE1901_FinalExamSimulation/
├── backend/                 # 后端代码
│   ├── __init__.py         # 包初始化文件
│   ├── agents.py           # LLM客户端，用于与DeepSeek API交互
│   ├── json_manager.py     # JSON文件管理器，用于模拟数据的保存和读取
│   ├── library.py          # 图书馆类，管理座位和学生初始化
│   ├── plot.py             # 数据可视化模块，生成模拟数据图表
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
├── simulation_data/        # 模拟数据存储目录
│   ├── figures/            # 存储可视化图表
│   ├── simulations/        # 存储模拟数据的JSON文件
│   └── test/              # 存储测试模拟数据
├── config.py              # 项目配置文件，包含路径配置
├── main.py                # 主程序入口
├── problem_check.py       # 问题检查脚本
├── seat_simulation_env.yml # Conda环境配置文件
├── test_plot.py           # 可视化功能测试脚本
├── utils.py               # 工具函数，包含API配置
└── 要求.txt              # 项目需求文档
```

### 技术栈

- **后端**: Python 3.13.9
- **LLM API**: DeepSeek (通过OpenAI包调用)
- **依赖管理**: Conda
- **HTTP Client**: OpenAI Python Package
- **数据可视化**: matplotlib, pandas
- **其他库**: datetime, enum, random等标准库

### 安装与运行

1. 克隆项目到本地
2. 使用Conda创建指定环境：
   ```bash
   conda env create -f seat_simulation_env.yml
   ```
3. 激活conda环境：
   ```bash
   conda activate seat-simulation
   ```
4. 运行主程序：
   ```bash
   python main.py
   ```

### 项目特性

- **时间系统**: 模拟一天(7:00-24:00)，图书馆时间更新步长为15分钟
- **学生行为**: 基于课程表、作息和满意度的智能决策
- **参数调节**: 用户可调节网格大小、学生数量、专业比例、座位偏好、检查清理时间等参数
- **数据可视化**: 自动生成三张分析图表，展示模拟结果的关键指标

### API配置

项目中的API密钥已经配置在`utils.py`文件中，但为了安全起见，该文件已被添加到.gitignore中，不会上传到GitHub。

### 测试

运行测试：
```bash
python -m pytest backend/test/
# 或运行特定测试
python backend/test/test_seats.py
python backend/test/test_students.py
python backend/test/test_interactions.py
python problem_check.py  # 根目录的问题检查脚本
python test_plot.py      # 可视化功能测试
```

---

## Library Maximum Capacity Research - LLM-based Seat Occupancy Behavior Simulation System

### Project Overview

This is a Python-based library seat occupancy behavior simulation system designed to study the relationship between student seat-reserving behaviors, library management measures, space utilization, and the library's maximum dynamic capacity. The project uses the DeepSeek LLM API to simulate student behaviors and includes complete backend code and data visualization functionality.

### Core Features

- Simulate library environment (supports custom grid sizes, defaults to 3x3 grid with 9 seats for demonstration, extensible to larger scales)
- Simulate student behaviors based on personal schedules, timetables, and seat preferences
- Manage seat states (vacant, occupied, reserved, marked for cleanup)
- Clean up违规 seat reservations based on time limits
- Support simulation data saving and reproduction functions
- Provide parameter adjustment and interactive command-line interface
- Implement simulation data visualization analysis functions

### Project Structure

```
AIE1901_FinalExamSimulation/
├── backend/                 # Backend code
│   ├── __init__.py         # Package initialization file
│   ├── agents.py           # LLM client for DeepSeek API interaction
│   ├── json_manager.py     # JSON manager for simulation data saving and retrieval
│   ├── library.py          # Library class, managing seat and student initialization
│   ├── plot.py             # Data visualization module, generating simulation data charts
│   ├── prompt.py           # Various LLM prompt templates
│   ├── seats.py            # Seat class, managing seat status and attributes
│   ├── simulation.py       # Simulation main class, coordinating the entire process
│   ├── students.py         # Student class, simulating student behavior
│   └── test/               # Test directory
│       ├── __init__.py     # Package initialization file
│       ├── test_interactions.py # Seat, student and library interaction tests
│       ├── test_prompt.py  # Prompt function tests
│       ├── test_seats.py   # Seat class unit tests
│       └── test_students.py # Student class unit tests
├── simulation_data/        # Simulation data storage directory
│   ├── figures/            # Store visualization charts
│   ├── simulations/        # Store simulation data in JSON files
│   └── test/              # Store test simulation data
├── config.py              # Project configuration file, containing path configuration
├── main.py                # Main program entry point
├── problem_check.py       # Problem checking script
├── seat_simulation_env.yml # Conda environment configuration file
├── test_plot.py           # Visualization function test script
├── utils.py               # Utility functions, containing API configuration
└── 要求.txt              # Project requirements document
```

### Tech Stack

- **Backend**: Python 3.13.9
- **LLM API**: DeepSeek (via OpenAI package)
- **Dependency Management**: Conda
- **HTTP Client**: OpenAI Python Package
- **Data Visualization**: matplotlib, pandas
- **Other Libraries**: datetime, enum, random, etc.

### Installation and Running

1. Clone the project to your local machine
2. Use Conda to create the specified environment:
   ```bash
   conda env create -f seat_simulation_env.yml
   ```
3. Activate the conda environment:
   ```bash
   conda activate seat-simulation
   ```
4. Run the main program:
   ```bash
   python main.py
   ```

### Project Features

- **Time System**: Simulate a day (7:00-24:00), with 15-minute library time increments
- **Student Behavior**: Intelligent decision-making based on timetables, schedules, and satisfaction
- **Parameter Adjustment**: Users can adjust grid size, number of students, major ratios, seat preferences, check and cleanup times
- **Data Visualization**: Automatically generate three analytical charts showing key simulation results

### API Configuration

The API key in the project is configured in the `utils.py` file, but for security reasons, this file has been added to .gitignore and will not be uploaded to GitHub.

### Testing

Run tests:
```bash
python -m pytest backend/test/
# Or run specific tests
python backend/test/test_seats.py
python backend/test/test_students.py
python backend/test/test_interactions.py
python problem_check.py  # Root directory problem check script
python test_plot.py      # Visualization function test
```