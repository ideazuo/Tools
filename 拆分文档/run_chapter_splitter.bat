@echo off
echo 正在启动章节分割工具...
python chapter_splitter.py
if %ERRORLEVEL% NEQ 0 (
    echo 运行失败，请确保已安装Python并且可以从命令行运行python命令。
    echo 如果已安装Python但无法启动，请尝试使用build_executable.py构建可执行文件。
    pause
) 