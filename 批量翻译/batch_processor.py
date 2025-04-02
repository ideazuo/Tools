import os
from gemini_integration import GeminiIntegration

def read_system_instructions(file_path):
    """读取系统指令文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def process_files(api_key, system_instructions, input_dir, output_dir):
    """
    批量处理目录中的文件
    :param api_key: Gemini API密钥
    :param system_instructions: 系统指令内容
    :param input_dir: 输入目录路径
    :param output_dir: 输出目录路径
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化Gemini客户端
    gemini = GeminiIntegration(api_key)
    
    # 获取输入目录中的所有文件
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    
    for filename in files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"processed_{filename}")
        
        # 读取输入文件内容
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 组合系统指令和文件内容作为提示
        prompt = f"{system_instructions}\n\n{content}"
        
        # 调用Gemini处理
        response = gemini.generate_text(prompt)
        
        # 保存结果
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response)
        
        print(f"已处理文件: {filename} -> {output_path}")

if __name__ == "__main__":
    # 示例用法
    api_key = "AIzaSyDS9TuQCWE-r3SwWrE_SvMxYJASBFHIwW0"  # 替换为你的API密钥
    system_instructions_file = "system_instructions.txt"  # 系统指令文件路径
    input_directory = "input"  # 输入目录路径
    output_directory = "output"  # 输出目录路径
    
    # 读取系统指令
    instructions = read_system_instructions(system_instructions_file)
    
    # 开始批量处理
    process_files(api_key, instructions, input_directory, output_directory)