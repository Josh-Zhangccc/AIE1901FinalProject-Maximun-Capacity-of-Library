@echo off
REM Windows批处理脚本，用于启动图书馆座位模拟系统（前后端）
echo 启动图书馆座位占用行为模拟系统...

REM 激活conda环境
call conda activate seat-simulation
if errorlevel 1 (
    echo 错误：无法激活 seat-simulation 环境，请确保已创建该环境
    pause
    exit /b 1
)

echo 启动Flask后端服务...
echo 请在浏览器中访问 http://127.0.0.1:5000 来使用前端界面
start http://127.0.0.1:5000
python app.py

REM 如果出现错误，暂停以便查看错误信息
if errorlevel 1 (
    echo 程序运行出错，请检查错误信息
    pause
)

REM 程序正常结束时也暂停一下，让用户看到结果
echo 模拟程序已结束
pause