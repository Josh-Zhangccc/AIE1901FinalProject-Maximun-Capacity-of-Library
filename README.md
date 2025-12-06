# AIE1901 Final Project: Maximum Capacity of Library

## Library Maximum Capacity Research - LLM-based Seat Occupancy Behavior Simulation System

### Project Overview

This is a Python-based library seat occupancy behavior simulation system designed to study the relationship between student seat-reserving behaviors, library management measures, space utilization, and the library's maximum dynamic capacity. The project uses the DeepSeek LLM API to simulate student behaviors and includes complete backend code, modern frontend interface, and data visualization functionality.

Core project features:
- Simulate library environment (supports custom grid sizes, defaults to 3x3 grid with 9 seats for demonstration, extensible to larger scales)
- Simulate student behaviors based on personal schedules, timetables, and seat preferences
- Manage seat states (vacant, occupied, reserved, marked for cleanup)
- Clean up rule-violating seat reservations based on time limits
- Support simulation data saving and reproduction functions
- Provide parameter adjustment and interactive command-line interface
- Implement simulation data visualization analysis functions
- Automatically analyze library maximum dynamic capacity related indicators
- **New**: Modern Flask frontend interface, supporting multi-language and multi-process acceleration
- **New**: Range simulation and repeat simulation functionality

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
├── frontend/                # Frontend code (new)
│   ├── app.py              # Flask application main file
│   ├── static/             # Static resources
│   │   ├── css/
│   │   │   └── style.css   # Style file
│   │   ├── js/
│   │   │   ├── main.js     # Main JavaScript logic
│   │   │   ├── start_simulation.js    # Start simulation page logic
│   │   │   ├── repeat_simulation.js   # Repeat simulation page logic
│   │   │   ├── view_plots.js          # View plots page logic
│   │   │   └── simulation_records.js  # Simulation records page logic
│   │   └── images/
│   │       └── placeholder_plot.svg   # Placeholder image
│   └── templates/          # HTML templates
│       ├── index.html      # Homepage
│       ├── start_simulation.html      # Start simulation page
│       ├── repeat_simulation.html     # Repeat simulation page
│       ├── view_plots.html            # View plots page
│       └── simulation_records.html    # Simulation records page
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
├── test_analysis.py       # Test script
├── test_auto_simulation_number.py # Test script
├── fix_format.py          # Format fix script
├── fix_function_def.py    # Function definition fix script
├── simple_fix2.py         # Simple fix script
└── 要求.txt              # Project requirements document
```

### Tech Stack

- **Backend**: Python 3.13.9
- **Frontend**: Flask 3.1.2, Bootstrap 5, JavaScript
- **LLM API**: DeepSeek (via OpenAI package)
- **Dependency Management**: Conda/pip
- **HTTP Client**: OpenAI Python Package
- **Data Visualization**: matplotlib, pandas
- **Multi-process**: multiprocessing
- **Other Libraries**: datetime, enum, random, etc.

### Installation and Running

#### Environment Setup

Use Conda to create the specified environment:
```bash
conda env create -f seat_simulation_env.yml
```

The environment includes necessary Python packages such as Flask, Flask-CORS, OpenAI, httpx, pydantic, matplotlib, pandas, etc.

Activate the conda environment:
```bash
conda activate seat-simulation
```

#### Running the Application

1. **Direct Run Main Program**
   The main program (main.py) by default runs an automated simulation series, from 9 students to 18 students, with 3 repetitions for each student count, using a 3x3 grid (9 seats) for simulation.
   ```bash
   python main.py
   ```

2. **Modify Main Program Parameters**
   You can modify parameters in main.py to customize the simulation:
   - `row` and `column`: Define the library seat grid size
   - Numbers in `range(3)`: Define the number of repeated experiments for each student count
   - `range(9,19,1)`: Define the student count range (from 9 to 18, increment by 1)

3. **Start Frontend Interface**
   The project also provides a modern frontend interface built with Flask, offering an intuitive user interface to control and monitor the simulation process:

   1. Ensure project dependencies are installed:
      ```bash
      pip install -r requirements.txt
      ```

   2. Enter the frontend directory and start the application:
      ```bash
      cd frontend
      python app.py
      ```

   3. Access http://localhost:5000 to view the application

   The frontend interface includes the following features:
   - **Homepage**: Provides four main function entries: start simulation, repeat simulation, draw/view plots, and simulation records
   - **Start simulation**: Allows users to set various parameters (grid size, number of students, major ratios, cleaning time, etc.) for simulation
   - **Repeat simulation**: Repeats simulation based on existing simulation records
   - **Draw/View plots**: Generates and views visualization charts of simulation results
   - **Simulation records**: View and manage all simulation records
   - **Multi-language support**: Supports both Chinese and English interface switching
   - **Multi-process acceleration**: Uses multiprocessing for parallel simulation

4. **Command Line Simulation** (Advanced)
   You can also modify the main.py file to create an interactive command-line interface for running simulations:

   ```python
   from backend.simulation import Simulation

   # Create simulation instance
   sim = Simulation(row=3, column=3, num_students=15, simulation_number=1)
   sim.run(run_all=False)  # run_all=False launches interactive command-line interface
   ```

   Interactive command-line supports the following commands:
   - `step`: Execute next simulation step
   - `status`: Display current simulation status
   - `seats`: Show seat occupancy situation
   - `time`: Show current simulation time
   - `set_limit [minutes]`: Set seat reservation time limit (in minutes)
   - `quit`: Exit simulation
   - `help`: Show help information

### API Configuration

The project uses DeepSeek's LLM API to simulate student behaviors. API configuration information (BASE_URL, API_KEY, MODEL) should be stored in the `utils.py` file (this file is currently missing and needs to be created), including:
- `BASE_URL`: API base URL
- `API_KEY`: API key
- `MODEL`: Model name used

**Note**: The project code references the `utils.py` file to get API configuration, but this file appears to be missing. You need to create a `utils.py` file in the project root and add the necessary API configuration.

Example `utils.py`:
```python
BASE_URL = "https://api.deepseek.com"
API_KEY = "your-api-key-here"
MODEL = "deepseek-chat"
```

### Simulation Analysis

#### Simulation Data Storage

##### Data Storage Structure
- Simulation data is classified and stored in the `simulation_data/simulations/` directory based on total number of seats
- Each seat count corresponds to a subdirectory in the format `{total_seats}_seats_simulations`
- Each simulation data is named in the format `{students}-{simulation_number}.json`
- Example: `15-1.json` represents the 1st simulation with 15 students

#### Visualization Charts

##### Basic Simulation Charts
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

##### Analysis Charts
Analysis charts are generated by the `plot_analysis` function in `data_analysis.py` and contain three subplots:

**Figure 1: Comprehensive Occupancy Indicator and Seat Reservation Rate vs Ratio of Student Count to Library Static Capacity**
- X-axis: Over-capacity ratio - (total number of students - total number of seats) / total number of seats
- Left Y-axis: Comprehensive occupancy indicator - reflects the difficulty of students finding seats under seat tightness
- Right Y-axis: High seat reservation time ratio - time ratio where reserved seats exceed 30% of total seats

**Figure 2: Final Unsatisfied Count and Cleared Seats vs Ratio of Student Count to Library Static Capacity**
- Shows the change in final unsatisfied student count and cleared reserved seats as the over-capacity ratio increases

**Figure 3: Library Maximum Dynamic Capacity Related Indicators vs Ratio of Student Count to Library Static Capacity**
- Contains key indicators such as dynamic capacity ratio, peak pressure score, and utilization efficiency

### Key Metrics and Calculation Methods

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

---

## 图书馆最大容量研究 - 基于LLM的座位占用行为模拟系统

### 项目概述

这是一个基于Python的图书馆座位占用行为模拟系统，旨在研究学生占座行为与图书馆管理措施对空间利用率和图书馆最大动态容量之间的关系。项目使用DeepSeek的LLM API来模拟学生行为，包含完整的后端代码、现代化前端界面和数据可视化功能。

项目核心功能：
- 模拟图书馆环境（支持自定义网格大小，默认3x3网格，9个座位作为演示，可扩展到更大规模）
- 模拟学生基于个人作息、课程表和座位偏好的行为
- 管理座位状态（空闲、占用、占座、标记清理）
- 基于时间限制清理违规占座
- 支持模拟数据的保存与复现功能
- 提供参数调节功能和交互式命令行界面
- 实现模拟数据的可视化分析功能
- 自动分析图书馆最大动态容量相关指标
- **新增**: 现代化Flask前端界面，支持多语言、多进程加速
- **新增**: 范围模拟和重复模拟功能

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
├── frontend/                # 前端代码（新增）
│   ├── app.py              # Flask应用主文件
│   ├── static/             # 静态资源
│   │   ├── css/
│   │   │   └── style.css   # 样式文件
│   │   ├── js/
│   │   │   ├── main.js     # 主要JavaScript逻辑
│   │   │   ├── start_simulation.js    # 开始模拟页面逻辑
│   │   │   ├── repeat_simulation.js   # 重复模拟页面逻辑
│   │   │   ├── view_plots.js          # 查看图像页面逻辑
│   │   │   └── simulation_records.js  # 模拟记录页面逻辑
│   │   └── images/
│   │       └── placeholder_plot.svg   # 占位图像
│   └── templates/          # HTML模板
│       ├── index.html      # 首页
│       ├── start_simulation.html      # 开始模拟页面
│       ├── repeat_simulation.html     # 重复模拟页面
│       ├── view_plots.html            # 查看图像页面
│       └── simulation_records.html    # 模拟记录页面
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
├── test_analysis.py       # 测试脚本
├── test_auto_simulation_number.py # 测试脚本
├── fix_format.py          # 格式修复脚本
├── fix_function_def.py    # 函数定义修复脚本
├── simple_fix2.py         # 简单修复脚本
└── 要求.txt              # 项目需求文档
```

### 技术栈

- **后端**: Python 3.13.9
- **前端**: Flask 3.1.2, Bootstrap 5, JavaScript
- **LLM API**: DeepSeek (通过OpenAI包调用)
- **依赖管理**: Conda/pip
- **HTTP Client**: OpenAI Python Package
- **数据可视化**: matplotlib, pandas
- **多进程**: multiprocessing
- **其他库**: datetime, enum, random等标准库

### 安装与运行

#### 环境配置

使用Conda创建指定环境：
```bash
conda env create -f seat_simulation_env.yml
```

环境包含必要的Python包，如Flask、Flask-CORS、OpenAI、httpx、pydantic、matplotlib、pandas等。

激活conda环境：
```bash
conda activate seat-simulation
```

#### 运行应用

1. **直接运行主程序**
   主程序（main.py）默认会运行一个自动化的模拟系列，从9个学生到18个学生，每种学生数量重复3次，使用3x3网格（9个座位）进行模拟。
   ```bash
   python main.py
   ```

2. **修改主程序参数**
   您可以修改main.py中的参数来自定义模拟：
   - `row` 和 `column`：定义图书馆座位网格大小
   - `range(3)` 中的数字：定义每种学生数量的重复实验次数
   - `range(9,19,1)`：定义学生数量范围（从9到18，每次递增1）

3. **启动前端界面**
   项目还提供了现代化的前端界面，使用Flask构建，提供直观的用户界面来控制和监控模拟过程：

   1. 确保已安装项目依赖：
      ```bash
      pip install -r requirements.txt
      ```

   2. 进入frontend目录并启动应用：
      ```bash
      cd frontend
      python app.py
      ```

   3. 访问 http://localhost:5000 查看应用

   前端界面包含以下功能：
   - **首页**：提供开始模拟、重复模拟、绘制/查看图像、模拟记录四个主要功能入口
   - **开始模拟**：允许用户设置各种参数（网格大小、学生数量、专业比例、清理时间等）进行模拟
   - **重复模拟**：基于现有模拟记录重复运行模拟
   - **绘制/查看图像**：生成和查看模拟结果的可视化图表
   - **模拟记录**：查看和管理所有模拟记录
   - **多语言支持**：支持中英文界面切换
   - **多进程加速**：使用multiprocessing实现并行模拟

4. **命令行模拟** (高级)
   您也可以修改main.py文件，创建一个交互式的命令行界面来运行模拟：

   ```python
   from backend.simulation import Simulation

   # 创建模拟实例
   sim = Simulation(row=3, column=3, num_students=15, simulation_number=1)
   sim.run(run_all=False)  # run_all=False 会启动交互式命令行界面
   ```

   交互式命令行支持以下命令：
   - `step`: 执行下一步模拟
   - `status`: 显示当前模拟状态
   - `seats`: 显示座位占用情况
   - `time`: 显示当前模拟时间
   - `set_limit [minutes]`: 设置占座时间限制（分钟）
   - `quit`: 退出模拟
   - `help`: 显示帮助信息

### API配置

项目使用DeepSeek的LLM API来模拟学生行为，API配置信息（BASE_URL, API_KEY, MODEL）应存放在`utils.py`文件中（该文件目前缺少，需要创建），包括：
- `BASE_URL`: API基础URL
- `API_KEY`: API密钥
- `MODEL`: 使用的模型名称

**注意**: 项目代码中引用了`utils.py`文件来获取API配置，但该文件似乎缺失。需要在项目根目录创建`utils.py`文件并添加必要的API配置。

`utils.py`示例：
```python
BASE_URL = "https://api.deepseek.com"
API_KEY = "your-api-key-here"
MODEL = "deepseek-chat"
```

### 模拟分析

#### 模拟数据存储

##### 数据存储结构
- 模拟数据根据座位总数分类存储在 `simulation_data/simulations/` 目录下
- 每个座位数对应一个子目录，格式为 `{total_seats}_seats_simulations`
- 每次模拟的数据以 `{students}-{simulation_number}.json` 格式命名
- 例如：`15-1.json` 表示15个学生的第1次模拟

#### 可视化图表

##### 基础模拟图表
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

##### 分析图表
分析图表由 `data_analysis.py` 中的 `plot_analysis` 函数生成，包含三个子图：

**图1: 综合占用指标和占座率 vs 学生总数超过图书馆静态容量比**
- X轴：超容量比 - (学生总数 - 座位总数) / 座位总数
- 左Y轴：综合占用指标 - 反映在座位紧张情况下学生找座难易程度
- 右Y轴：高占座率时间比例 - 占座数超过座位总数30%的时间占比

**图2: 最终不满意数和被清理数 vs 学生总数超过图书馆静态容量比**
- 显示随着超容量比增加，最终的不满意学生数和被清理占座数的变化

**图3: 图书馆最大动态容量相关指标 vs 学生总数超过图书馆静态容量比**
- 包含动态容量比、峰值压力分数、利用率效率等关键指标

### 关键指标与计算方式

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