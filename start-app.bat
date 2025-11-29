@echo off
REM Windows批处理脚本，用于启动图书馆座位模拟系统
echo 启动图书馆座位占用行为模拟系统...

REM 激活conda环境并运行Python程序
call conda activate seat-simulation
if errorlevel 1 (
    echo 错误：无法激活 seat-simulation 环境，请确保已创建该环境
    pause
    exit /b 1
)

echo 运行模拟程序...
python main.py

REM 如果出现错误，暂停以便查看错误信息
if errorlevel 1 (
    echo 程序运行出错，请检查错误信息
    pause
)

REM 程序正常结束时也暂停一下，让用户看到结果
echo 模拟程序已结束
pause