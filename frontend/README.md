# 图书馆座位模拟系统前端

这是一个现代化的前端界面，用于图书馆座位占用行为模拟系统。前端使用Flask构建，提供直观的用户界面来控制和监控模拟过程。

## 功能特性

- **首页**：提供开始模拟、重复模拟、绘制/查看图像、模拟记录四个主要功能入口
- **开始模拟**：允许用户设置各种参数（网格大小、学生数量、专业比例、清理时间等）进行模拟
- **重复模拟**：基于现有模拟记录重复运行模拟
- **绘制/查看图像**：生成和查看模拟结果的可视化图表
- **模拟记录**：查看和管理所有模拟记录
- **多语言支持**：支持中英文界面切换
- **多进程加速**：使用multiprocessing实现并行模拟

## 安装和运行

1. 确保已安装项目依赖：
   ```
   pip install -r requirements.txt
   ```

2. 进入frontend目录并启动应用：
   ```
   cd frontend
   python app.py
   ```

3. 访问 http://localhost:5000 查看应用

## 前端文件结构

```
frontend/
├── app.py                 # Flask应用主文件
├── static/                # 静态资源
│   ├── css/
│   │   └── style.css      # 样式文件
│   ├── js/
│   │   ├── main.js        # 主要JavaScript逻辑
│   │   ├── start_simulation.js    # 开始模拟页面逻辑
│   │   ├── repeat_simulation.js   # 重复模拟页面逻辑
│   │   ├── view_plots.js          # 查看图像页面逻辑
│   │   └── simulation_records.js  # 模拟记录页面逻辑
│   └── images/
└── templates/             # HTML模板
    ├── index.html         # 首页
    ├── start_simulation.html      # 开始模拟页面
    ├── repeat_simulation.html     # 重复模拟页面
    ├── view_plots.html            # 查看图像页面
    └── simulation_records.html    # 模拟记录页面
```

## 使用说明

### 开始模拟页面
- 设置网格大小（行数和列数）
- 调整文、理、工学生比例（总和为100%）
- 设置清理占座时间
- 选择学生数量或范围模拟参数
- 可选择使用多进程加速模拟

### 重复模拟页面
- 从现有模拟记录中选择一个
- 设置重复次数
- 控制模拟的开始、暂停和停止

### 绘制/查看图像页面
- 从模拟数据生成可视化图表
- 查看已生成的图表

### 模拟记录页面
- 查看完整的模拟文件结构
- 浏览最近的模拟记录
- 执行加载、查看、删除等操作

## 技术栈

- **前端框架**：Flask
- **前端模板**：Jinja2
- **UI框架**：Bootstrap 5
- **图标**：Feather Icons
- **多进程**：multiprocessing
- **可视化**：matplotlib

## API端点

- `GET /` - 首页
- `POST /api/start_simulation` - 开始模拟
- `POST /api/start_range_simulation` - 开始范围模拟
- `POST /api/generate_plots` - 生成图像
- `GET /api/simulation_records` - 获取模拟记录
- `GET /api/plots` - 获取图像文件
- `GET /simulation_data/figures/<filename>` - 提供图像文件

## 注意事项

- 确保后端模块（backend）在Python路径中
- 模拟数据保存在 `simulation_data/simulations/` 目录
- 图像文件保存在 `simulation_data/figures/` 目录
- 应用默认运行在端口5000