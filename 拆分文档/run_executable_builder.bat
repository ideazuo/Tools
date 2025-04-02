@echo off
echo 正在启动构建过程...
python build_executable.py
if %ERRORLEVEL% NEQ 0 (
    echo 构建失败，请确保已安装Python并且可以从命令行运行python命令。
    pause
) 