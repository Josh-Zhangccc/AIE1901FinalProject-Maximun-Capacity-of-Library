# AIE1901 Final Project: Maximun Capacity of Library

## 图书馆最大容量研究 - 基于LLM的座位占用行为模拟系统

### 项目概述

这是一个基于Python的图书馆座位占用行为模拟系统，旨在研究学生占座行为与图书馆管理措施对空间利用率和图书馆最大动态容量之间的关系。项目使用DeepSeek的LLM API来模拟学生行为，包含完整的后端代码和数据可视化功能。

项目核心功能：
- 模拟图书馆环境（支持自定义网格大小，默认3x3网格，9个座位作为演示，可扩展到更大规模）
- 模拟学生基于个人作息、课程表和座位偏好的行为
- 管理座位状态（空闲、占用、占座、标记清理）
- 基于时间限制清理违规占座
- 支持模拟数据的保存与复现功能
- 提供参数调节功能和交互式命令行界面
- 实现模拟数据的可视化分析功能
- 自动分析图书馆最大动态容量相关指标

### 项目结构

```
AIE1901_FinalExamSimulation/
├── backend/                 # 后端代码
│   ├── __init__.py         # 包初始化文件
│   ├── agents.py           # LLM客户端，用于与DeepSeek API交互
│   ├── data_analysis.py    # 数据分析模块，分析图书馆最大动态容量相关指标
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
├── IFLOW.md               # 项目说明文档
├── main.py                # 主程序入口
├── plot_9_15_2.py         # 数据可视化脚本
├── plot_9_15.py           # 数据可视化脚本
├── problem_check.py       # 问题检查脚本
├── README.md              # 项目说明文档
├── rename_json_files.py   # JSON文件重命名脚本
├── requirements.txt       # 项目依赖包列表
├── seat_simulation_env.yml # Conda环境配置文件
├── test_9_11_short.py     # 测试脚本
├── test_9_11_simulation.py # 测试脚本
├── test_9_11.py          # 测试脚本
├── test_agents_retry.py   # 测试脚本
├── test_analysis.py       # 测试脚本
├── test_auto_simulation_number.py # 测试脚本
├── test_new_save_figure.py # 测试脚本
├── test_new_simulation.py # 测试脚本
├── test_plot_analysis.py  # 测试脚本
├── test_save_figure.py    # 测试脚本
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
- **数据可视化**: 自动生成整合图像，展示模拟结果的关键指标
- **自动编号系统**: 根据学生数量自动生成模拟编号，便于数据管理
- **自动分析系统**: 根据座位数自动分析相关指标并生成分析图表
- **数据整合功能**: 将相同参数的多次实验整合到一张图像中

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

Project core features:
- Simulate library environment (supports custom grid sizes, defaults to 3x3 grid with 9 seats for demonstration, extensible to larger scales)
- Simulate student behaviors based on personal schedules, timetables, and seat preferences
- Manage seat states (vacant, occupied, reserved, marked for cleanup)
- Clean up违规 seat reservations based on time limits
- Support simulation data saving and reproduction functions
- Provide parameter adjustment and interactive command-line interface
- Implement simulation data visualization analysis functions
- Automatically analyze library maximum dynamic capacity related indicators

### Project Structure

```
AIE1901_FinalExamSimulation/
├── backend/                 # Backend code
│   ├── __init__.py         # Package initialization file
│   ├── agents.py           # LLM client for DeepSeek API interaction
│   ├── data_analysis.py    # Data analysis module, analyzing library maximum dynamic capacity related indicators
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
├── IFLOW.md               # Project documentation
├── main.py                # Main program entry point
├── plot_9_15_2.py         # Data visualization script
├── plot_9_15.py           # Data visualization script
├── problem_check.py       # Problem checking script
├── README.md              # Project documentation
├── rename_json_files.py   # JSON file renaming script
├── requirements.txt       # Project dependency list
├── seat_simulation_env.yml # Conda environment configuration file
├── test_9_11_short.py     # Test script
├── test_9_11_simulation.py # Test script
├── test_9_11.py          # Test script
├── test_agents_retry.py   # Test script
├── test_analysis.py       # Test script
├── test_auto_simulation_number.py # Test script
├── test_new_save_figure.py # Test script
├── test_new_simulation.py # Test script
├── test_plot_analysis.py  # Test script
├── test_save_figure.py    # Test script
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
- **Data Visualization**: Automatically generate integrated charts showing key simulation indicators
- **Auto Numbering System**: Automatically generate simulation numbers based on student count for easy data management
- **Auto Analysis System**: Automatically analyze relevant indicators by seat count and generate analysis charts
- **Data Integration Feature**: Integrate multiple experiments with the same parameters into one chart

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

## 模拟分析说明

### 模拟数据存储

#### 数据存储结构
- 模拟数据根据座位总数分类存储在 `simulation_data/simulations/` 目录下
- 每个座位数对应一个子目录，格式为 `{total_seats}_seats_simulations`
- 每次模拟的数据以 `{students}-{simulation_number}.json` 格式命名
- 例如：`15-1.json` 表示15个学生的第1次模拟

#### JSON数据格式
- 每个JSON文件包含两部分数据：
  1. 初始配置信息：包含测试名称、规模、座位信息等
  2. 时间序列数据：按时间步长记录模拟过程中的各项指标

#### 时间序列记录内容
- `time`: 记录当前模拟时间（HH:MM格式）
- `seats_taken_state`: 座位占用状态矩阵
- `unstisfied_num`: 不满意学生数量
- `cleared_seats`: 已清理的违规占座数量
- `reversed_seats`: 当前占座数量
- `taken_rate`: 座位占用率（格式："数量 (百分比%)"）

### 可视化图表说明

#### 基础模拟图表
基础模拟图表由 `plot.py` 中的 `plot_combined_simulation` 函数生成，包含两个子图：

**图1: 座位占有率和占座数量随时间变化**
- 左Y轴：座位占有率（%）- 显示实际座位被占用的比例
- 右Y轴：占座数量 - 显示违反图书馆规则的占座行为数量
- 当进行多次重复实验时，图表会显示：
  - 次要数据：单次实验（淡色虚线）
  - 主要数据：平均值（实线，正常颜色和线宽）

**图2: 不满意数及清理座位数随时间变化**
- 显示学生因找不到座位而产生不满的情况
- 显示图书馆系统自动清理违规占座的情况
- 当进行多次重复实验时，同样会显示平均值和单次实验数据

#### 分析图表
分析图表由 `data_analysis.py` 中的 `plot_analysis` 函数生成，包含三个子图：

**图1: 综合占用指标和占座率 vs 学生总数超过图书馆静态容量比**
- X轴：超容量比 - (学生总数 - 座位总数) / 座位总数
- 左Y轴：综合占用指标 - 反映在座位紧张情况下学生找座难易程度
- 右Y轴：高占座率时间比例 - 占座数超过座位总数30%的时间占比

**图2: 最终不满意数和被清理数 vs 学生总数超过图书馆静态容量比**
- 显示随着超容量比增加，最终的不满意学生数和被清理占座数的变化

**图3: 图书馆最大动态容量相关指标 vs 学生总数超过图书馆静态容量比**
- 包含动态容量比、峰值压力分数、利用率效率等关键指标

### 指标含义与计算方式

#### 综合占用指标
- **含义**: 重点考虑座位不足（不满增长）的情况，衡量座位紧张程度的综合指标
- **计算方式**: 
  - 计算不满数增长情况，特别是在高占用率（≥70%）情况下的不满增长加倍计算
  - 使用归一化方法，使座位不足情况影响更大
  - 组合指标：不满增长权重70%，高占用率权重30%

#### 动态容量比
- **含义**: 衡量在高占用期间不满增长情况的反向指标，反映图书馆在高压力下的处理能力
- **计算方式**: 
  - 统计高占用期间（≥80%）的不满增长情况
  - 取反向指标：增长越少，容量比越高
  - 动态容量比 = max(0, 1.0 - min(1.0, avg_growth_during_high_occupancy / 2.0))

#### 峰值压力分数
- **含义**: 综合考虑高占用和不满增长的图书馆压力指标
- **计算方式**: 
  - 峰值压力分数 = (高占用时间占比 * 0.6 + 不满增长时间占比 * 0.4)
  - 其中高占用定义为占用率≥90%

#### 利用率效率
- **含义**: 考虑座位使用效率的指标，惩罚高不满数
- **计算方式**: 
  - 平均占用率 - (最大不满数 / 50.0)
  - 利用率效率 = max(0, avg_occupancy - (max_unsatisfied / 50.0))

#### 高占座率时间比例
- **含义**: 衡量占座行为严重程度的指标
- **计算方式**: 
  - 高占座率定义为占座数≥总座位数的30%
  - 高占座率时间占比 = 高占座率时间段数 / 总时间段数

---

## Simulation Analysis Instructions

### Simulation Data Storage

#### Data Storage Structure
- Simulation data is classified and stored in the `simulation_data/simulations/` directory based on total number of seats
- Each seat count corresponds to a subdirectory in the format `{total_seats}_seats_simulations`
- Each simulation data is named in the format `{students}-{simulation_number}.json`
- Example: `15-1.json` represents the 1st simulation with 15 students

#### JSON Data Format
- Each JSON file contains two parts of data:
  1. Initial configuration information: including test name, scale, seat information, etc.
  2. Time series data: recording various indicators during the simulation process by time steps

#### Time Series Recording Content
- `time`: Records current simulation time (HH:MM format)
- `seats_taken_state`: Seat occupancy status matrix
- `unstisfied_num`: Number of unsatisfied students
- `cleared_seats`: Number of cleared rule-violating reserved seats
- `reversed_seats`: Current number of reserved seats
- `taken_rate`: Seat occupancy rate (format: "count (percentage%)")


### Visualization Charts Instructions

#### Basic Simulation Charts
Basic simulation charts are generated by the `plot_combined_simulation` function in `plot.py` and contain two subplots:

**Figure 1: Seat Occupancy Rate and Reserved Seat Count Over Time**
- Left Y-axis: Seat occupancy rate (%) - shows the actual proportion of seats occupied
- Right Y-axis: Reserved seat count - shows the number of rule-violating seat reservation behaviors
- When conducting multiple repeated experiments, the chart displays:
  - Secondary data: Single experiments (light-colored dashed lines)
  - Primary data: Average values (solid lines, normal color and line width)

**Figure 2: Number of Unsatisfied Students and Cleared Seats Over Time**
- Shows the situation where students become unsatisfied due to inability to find seats
- Shows the automatic clearing of rule-violating reserved seats by the library system
- For multiple repeated experiments, average values and single experiment data are displayed

#### Analysis Charts
Analysis charts are generated by the `plot_analysis` function in `data_analysis.py` and contain three subplots:

**Figure 1: Comprehensive Occupancy Indicator and Seat Reservation Rate vs Ratio of Student Count to Library Static Capacity**
- X-axis: Over-capacity ratio - (total number of students - total number of seats) / total number of seats
- Left Y-axis: Comprehensive occupancy indicator - reflects the difficulty of students finding seats under seat tightness
- Right Y-axis: High seat reservation time ratio - time ratio where reserved seats exceed 30% of total seats

**Figure 2: Final Unsatisfied Count and Cleared Seats vs Ratio of Student Count to Library Static Capacity**
- Shows the change in final unsatisfied student count and cleared reserved seats as the over-capacity ratio increases

**Figure 3: Library Maximum Dynamic Capacity Related Indicators vs Ratio of Student Count to Library Static Capacity**
- Contains key indicators such as dynamic capacity ratio, peak pressure score, and utilization efficiency

### Indicator Meanings and Calculation Methods

#### Comprehensive Occupancy Indicator
- **Meaning**: Focuses on the situation of seat insufficiency (increase in dissatisfaction), measuring the comprehensive indicator of seat tightness
- **Calculation Method**:
  - Calculate the increase in dissatisfaction, especially doubling the dissatisfaction increase under high occupancy (≥70%)
  - Use normalization method to make seat insufficiency situations have greater impact
  - Combined indicator: dissatisfaction growth weight 70%, high occupancy weight 30%

#### Dynamic Capacity Ratio
- **Meaning**: Reverse indicator measuring the increase in dissatisfaction during high occupancy periods, reflecting the library's processing capability under high pressure
- **Calculation Method**:
  - Count dissatisfaction increase during high occupancy periods (≥80%)
  - Take reverse indicator: the less the growth, the higher the capacity ratio
  - Dynamic capacity ratio = max(0, 1.0 - min(1.0, avg_growth_during_high_occupancy / 2.0))

#### Peak Pressure Score
- **Meaning**: Library pressure indicator combining high occupancy and dissatisfaction growth
- **Calculation Method**:
  - Peak pressure score = (high occupancy time ratio * 0.6 + dissatisfaction growth time ratio * 0.4)
  - High occupancy is defined as occupancy rate ≥ 90%

#### Utilization Efficiency
- **Meaning**: Indicator considering seat utilization efficiency, penalizing high dissatisfaction numbers
- **Calculation Method**:
  - Average occupancy rate - (maximum dissatisfaction / 50.0)
  - Utilization efficiency = max(0, avg_occupancy - (max_unsatisfied / 50.0))

#### High Seat Reservation Time Ratio
- **Meaning**: Indicator measuring the severity of seat reservation behavior
- **Calculation Method**:
  - High seat reservation defined as reserved seat count ≥ 30% of total seats
  - High seat reservation time ratio = high seat reservation time periods / total time periods