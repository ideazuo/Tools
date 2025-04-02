import os
import subprocess
import sys

def install_pyinstaller():
    """安装PyInstaller（如果尚未安装）"""
    try:
        import PyInstaller
        print("PyInstaller已安装")
    except ImportError:
        print("正在安装PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller安装完成")

def build_executable():
    """构建可执行文件"""
    print("正在构建可执行文件...")
    
    # 确保脚本路径正确
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chapter_splitter.py")
    if not os.path.exists(script_path):
        print(f"错误：找不到源文件 {script_path}")
        return False
        
    # 构建命令
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "章节分割工具",
        "--icon", "NONE",  # 可以替换为你的.ico文件
        script_path
    ]
    
    # 运行PyInstaller
    try:
        subprocess.check_call(cmd)
        print("构建成功！")
        
        # 显示输出文件位置
        dist_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist"))
        print(f"可执行文件已保存到: {dist_dir}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

if __name__ == "__main__":
    # 安装依赖
    install_pyinstaller()
    
    # 构建可执行文件
    success = build_executable()
    
    # 保持窗口打开
    if success:
        input("\n构建完成！按回车键退出...")
    else:
        input("\n构建失败！按回车键退出...") 