# AIE1901 期末考试模拟项目 - 图书馆最大容量研究

## 项目概述

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

## 项目结构

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
├── test_9_11_short.py     # 测试脚本
├── test_9_11_simulation.py # 测试脚本
├── test_9_11.py          # 测试脚本
├── test_agents_retry.py   # 测试脚本
├── test_analysis.py       # 测试脚本
├── test_auto_simulation_number.py # 测试脚本
├── test_library_new_attributes.py # 测试脚本（新增）
├── test_library_without_api.py # 测试脚本（新增）
├── test_new_attributes.py # 测试脚本（新增）
├── test_new_save_figure.py # 测试脚本（新增）
├── test_new_simulation.py # 测试脚本（新增）
├── test_plot_analysis.py  # 测试脚本（新增）
├── test_reverse_seat_logic.py # 测试脚本（新增）
├── test_save_figure.py    # 测试脚本
├── utils.py               # 工具函数，包含API配置
└── 要求.txt              # 项目需求文档
```

## 技术栈

- **后端**: Python 3.13.9
- **前端**: Flask 3.1.2, Bootstrap 5, JavaScript
- **LLM API**: DeepSeek (通过OpenAI包调用)
- **依赖管理**: Conda/pip
- **HTTP Client**: OpenAI Python Package
- **数据可视化**: matplotlib, pandas
- **多进程**: multiprocessing
- **其他库**: datetime, enum, random等标准库

## 核心组件

### JSON管理器 (json_manager.py)
- 提供JsonManager类，实现JSON文件的初始化和基本的结构创建、读写操作
- 支持多种文件格式检测（JSON、Pickle、Gzip压缩的JSON）
- 用于模拟数据的保存与复现功能

### 配置管理器 (config.py)
- 定义模拟数据文件的存储路径
- 提供统一的路径管理，便于项目维护

### 座位系统 (seats.py)
- 座位状态：空闲(vacant)、占用(taken)、占座(reverse)、标记清理(signed) - 使用Status枚举
- 座位属性：坐标(x, y)、是否有台灯(lamp)、插座(socket)、是否靠窗(window)
- 功能：占用、离开(完全/占座)、标记占座、清理超时占座、时间更新、满意度计算、拥挤参数计算
- 实现了完整的单元测试，确保状态转换逻辑正确
- 时间更新步长为15分钟（与图书馆系统同步）

### 学生系统 (students.py)
- 使用LLM客户端模拟学生行为
- 学生属性：个人性格(守序/利己)、作息偏好(早鸟/正常/晚)、专注度(高/中/低)、课程情况(多/中/少)、座位偏好
- 行为逻辑：选择座位、状态改变(离开/回座)、是否占座
- 包含状态枚举(SLEEP, LEARNING, AWAY, GONE) - 使用StudentState枚举
- 支持创建不同专业(文科/理科/工科)和不同学习程度(勤奋/中等/懒惰)的学生
- 根据座位满意度和图书馆规则决定占座行为
- 通过LLM生成动态日程表
- 时间更新步长为15分钟（与图书馆系统同步）
- 提供工厂方法批量创建不同类型学生，包括：
  - 勤奋学生：高专注度、高规则性
  - 中等学生：平衡各项指标
  - 懒惰学生：低专注度、低规则性
  - 按专业分类：文科、理科、工科学生各有不同的座位偏好

### LLM客户端 (agents.py)
- 基于DeepSeek API的客户端实现
- 使用OpenAI Python包与DeepSeek API交互
- 使用预设提示词与LLM交互
- 支持JSON格式响应解析
- 包含错误处理和JSON解析功能

### 图书馆系统 (library.py)
- 支持自定义网格大小的座位初始化（演示时使用3x3网格，可扩展至更大规模）
- 随机分配台灯、插座属性，边缘座位自动为靠窗座位
- 管理学生初始化，支持不同专业(人文、科学、工程)和学习程度(勤奋、中等、懒惰)的学生
- 实现座位清理机制(标记占座、清理超时占座)
- 计算座位拥挤参数，统计图书馆利用率
- 时间更新步长为15分钟
- 包含清理超时占座逻辑和标记机制
- 支持动态设置占座时间限制
- 提供座位状态可视化功能
- 实现座位拥挤参数计算，考虑周围座位占用情况

### 数据可视化系统 (plot.py)
- 提供数据解析功能，从JSON模拟数据中提取时间序列
- 实现三张核心图表的绘制：
  1. 座位占有率和占座数量随时间变化图
  2. 不满意数及清理座位数随时间变化图
- 支持中文标签显示
- 包含复杂的拥挤度计算算法，考虑了实际用户体验
- 实现多次实验数据的整合显示功能
- 提供测试脚本test_plot.py用于验证功能

### 数据分析系统 (data_analysis.py)
- 提供图书馆最大动态容量相关指标分析
- 计算综合占用指标，重点考虑座位不足（不满增长）的情况
- 实现动态容量比、峰值压力分数、利用率效率等关键指标分析
- 支持相同参数多次实验的平均处理
- 生成综合分析图表，展示学生数量与图书馆容量关系

### 模拟框架 (simulation.py)
- 协调图书馆、学生和座位系统
- 管理模拟时间流
- 提供交互式命令行界面，支持 step, status, seats, time, set_limit, quit, help 命令
- 支持自定义模拟参数（网格大小、学生数量、专业比例等）
- 实现了实时的模拟状态查看和参数调整功能
- 集成JSON管理器，实现模拟数据的自动保存

### 前端系统 (frontend/)
- **Flask应用** (app.py): 提供REST API和页面路由
- **模板系统** (templates/): Jinja2模板引擎，提供用户界面
- **静态资源** (static/): CSS、JavaScript、图像资源
- **功能模块**:
  - 首页: 提供开始模拟、重复模拟、绘制/查看图像、模拟记录四个主要功能入口
  - 开始模拟: 允许用户设置各种参数（网格大小、学生数量、专业比例、清理时间等）进行模拟
  - 重复模拟: 基于现有模拟记录重复运行模拟
  - 绘制/查看图像: 生成和查看模拟结果的可视化图表
  - 模拟记录: 查看和管理所有模拟记录
- **多语言支持**: 支持中英文界面切换
- **多进程加速**: 使用multiprocessing实现并行模拟

## 环境配置

使用Conda创建指定环境：
```bash
conda env create -f seat_simulation_env.yml
```

环境包含必要的Python包，如Flask、Flask-CORS、OpenAI、httpx、pydantic、matplotlib、pandas等。

## API配置

在`utils.py`中配置DeepSeek API：
- `BASE_URL`: https://api.deepseek.com
- `API_KEY`: sk-cf8230f3e78a4cedadf7f7ab158f5441
- `MODEL`: deepseek-chat

## 运行方式

### 方式1：直接运行主程序
主程序（main.py）默认会运行一个自动化的模拟系列，从9个学生到18个学生，每种学生数量重复3次，使用3x3网格（9个座位）进行模拟。
```bash
python main.py
```

### 方式2：修改主程序参数
您可以修改main.py中的参数来自定义模拟：
- `row` 和 `column`：定义图书馆座位网格大小
- `range(3)` 中的数字：定义每种学生数量的重复实验次数
- `range(9,19,1)`：定义学生数量范围（从9到18，每次递增1）

### 方式3：通过命令行界面运行
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

### 方式4：使用独立的模拟脚本
您也可以直接使用backend.simulation模块创建模拟：
```python
from backend.simulation import Simulation

# 创建一个3x3网格，15个学生的模拟，保存为第1次实验
sim = Simulation(row=3, column=3, num_students=15, simulation_number=1)
sim.run(run_all=True)  # run_all=True 会自动运行完整模拟
```

### 方式5：启动前端界面
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

## 测试

项目包含多种测试，位于`backend/test/`目录下：
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
- `problem_check.py`: 项目问题检查脚本，包含多项测试
- `test_plot.py`: 可视化功能测试脚本
- **新增测试**:
  - `test_library_new_attributes.py`: 测试图书馆新属性
  - `test_library_without_api.py`: 测试无API调用的图书馆功能
  - `test_new_attributes.py`: 测试新学生属性
  - `test_new_save_figure.py`: 测试新图像保存功能
  - `test_new_simulation.py`: 测试新模拟功能
  - `test_plot_analysis.py`: 测试绘图分析功能
  - `test_reverse_seat_logic.py`: 测试占座逻辑
  - `test_agents_retry.py`: 测试代理重试机制
  - `test_analysis.py`: 测试分析功能
  - `test_auto_simulation_number.py`: 测试自动模拟编号功能

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

## 模拟特性

- **时间系统**: 模拟一天(7:00-23:59)，图书馆时间更新步长为15分钟，学生时间更新步长也为15分钟
- **学生行为**: 基于课程表、作息和满意度的智能决策
- **参数调节**: 用户可调节网格大小、学生数量、专业比例、座位偏好、检查清理时间等参数
- **数据可视化**: 自动生成整合图像，展示模拟结果的关键指标
- **自动编号系统**: 根据学生数量自动生成模拟编号，便于数据管理
- **自动分析系统**: 根据座位数自动分析相关指标并生成分析图表
- **数据整合功能**: 将相同参数的多次实验整合到一张图像中
- **多进程支持**: 支持并行模拟以提高性能
- **前端界面**: 提供直观的Web界面进行模拟控制和数据查看

## 提示词系统 (prompt.py)

包含两个主要的LLM提示词模板：
- `schedule_prompt`: 根据学生特征生成日程表，包含start、learn、eat、course、rest、end六种行为
- `leave_prompt`: 根据学生性格和满意度判断是否占座，包含action和reason字段

## 项目状态

目前项目架构已建立，包含完整的座位管理系统、学生系统、LLM客户端和提示词系统。测试用例已实现，特别是座位系统、学生系统和交互测试覆盖了各种场景。图书馆系统已实现基本功能，包括座位初始化、学生初始化和管理功能。模拟框架提供了交互式命令行界面，支持参数调节和实时监控。JSON管理器实现了模拟数据的保存与复现功能。新增了数据可视化功能和数据分析功能，可以生成分析图表并评估图书馆最大动态容量相关指标。

**已完成部分：**
- 核心模拟系统
- 座位状态管理
- 学生行为模拟
- LLM集成
- 交互式界面
- 测试系统
- 模拟数据保存功能
- 数据可视化功能
- 图书馆最大动态容量分析系统
- 自动编号和整合显示功能
- **新增**: 现代化Flask前端界面
- **新增**: 多进程并行模拟支持
- **新增**: 范围模拟和重复模拟功能

**待完善部分：**
- 完整的模拟流程优化
- 性能优化（如解决Library初始化时可能导致的长时间延迟问题）

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