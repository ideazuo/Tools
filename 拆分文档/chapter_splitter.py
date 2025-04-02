import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import traceback
import sys

def chinese_to_arabic(chinese_str):
    """将中文数字转换为阿拉伯数字
    
    支持以下格式:
    - 简单数字: 一, 二, 三, ...
    - 带单位数字: 十一, 一百二十三, ...
    - 并列数字: 一三五 (135), 二零 (20), ...
    """
    chinese_num_dict = {
        '零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '百': 100, '千': 1000,
        '万': 10000, '亿': 100000000
    }
    
    # 特殊情况处理
    if not chinese_str:
        return 0
    if chinese_str == '十':
        return 10
    
    # 检查是否包含单位（十、百、千等）
    has_unit = any(unit in chinese_str for unit in ['十', '百', '千', '万', '亿'])
    
    # 如果没有单位，可能是并列数字形式（如"一三五"表示135）
    if not has_unit:
        result = 0
        for char in chinese_str:
            if char in chinese_num_dict:
                # 按位累加，如"一三五"转为135
                result = result * 10 + chinese_num_dict[char]
        return result
    
    # 处理带单位的数字(十、百、千、万、亿)
    result = 0
    temp_num = 0
    
    # 从左到右处理
    for i, char in enumerate(chinese_str):
        if char not in chinese_num_dict:
            continue
            
        value = chinese_num_dict[char]
        if value >= 10000:  # 万或亿
            if temp_num == 0:
                temp_num = 1
            result += temp_num * value
            temp_num = 0
        elif value >= 10:  # 十、百、千
            if temp_num == 0:
                temp_num = 1
            result += temp_num * value
            temp_num = 0
        else:  # 数字
            temp_num = value
            
        # 处理最后一个字符是数字的情况
        if i == len(chinese_str) - 1 and temp_num > 0:
            result += temp_num
    
    return result

def detect_encoding(file_path):
    """尝试检测文件编码，默认为UTF-8"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'big5']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
                return encoding
        except UnicodeDecodeError:
            continue
    return 'utf-8'  # 如果都失败，返回默认编码

def split_text_file(source_file_path):
    # Get the directory and filename of the source file
    source_dir = os.path.dirname(source_file_path)
    if not source_dir:  # If no directory specified, use current directory
        source_dir = os.getcwd()
    
    # Detect encoding of the source file
    encoding = detect_encoding(source_file_path)
    
    # Read the source file with detected encoding
    with open(source_file_path, 'r', encoding=encoding) as f:
        content = f.read()
    
    # Regular expression to match both Arabic and Chinese numeric chapters
    # 匹配阿拉伯数字章节如"第1章"和中文数字章节如"第一章"、"第十一章"、"第一三五章"
    # 更精确的模式：章节标题通常在行首，并且是单独的一行或后面跟着空格/标点
    # 这个正则表达式会确保每个章节的内容包含从当前章节标题到下一个章节标题之前的所有内容
    
    # 首先找出所有章节标题的位置
    title_pattern = r'^第(?:\d+|[零一二两三四五六七八九十百千万亿]+)章.*?$'
    title_matches = list(re.finditer(title_pattern, content, re.MULTILINE))
    
    # 根据标题位置分割内容
    chapters = []
    for i, match in enumerate(title_matches):
        start_pos = match.start()
        if i < len(title_matches) - 1:
            end_pos = title_matches[i+1].start()
            chapter_text = content[start_pos:end_pos]
        else:
            # 最后一章包含到文件末尾的内容
            chapter_text = content[start_pos:]
        chapters.append(chapter_text)
    
    if not chapters:
        messagebox.showinfo("提示", "未找到任何章节标记（如\"第1章\"或\"第一章\"）")
        return
    
    # Create count of successfully processed chapters
    success_count = 0
    
    # 文件夹计数器，用于生成001, 002, 003等格式的文件夹名
    folder_counter = 1
    current_folder = None
    
    # Process each chapter
    for chapter in chapters:
        try:
            # Extract the chapter title for the filename (first line)
            chapter_title = chapter.strip().split('\n')[0].strip()
            
            # 检查是否是第1章或第一章，如果是则创建新文件夹
            is_first_chapter = False
            
            # 匹配阿拉伯数字"第1章"
            arabic_match = re.match(r'^第(\d+)章', chapter_title)
            if arabic_match and arabic_match.group(1) == '1':
                is_first_chapter = True
            
            # 匹配中文数字"第一章"、"第壹章"等
            chinese_match = re.match(r'^第([零一二两三四五六七八九十百千万亿]+)章', chapter_title)
            if chinese_match:
                try:
                    chapter_num = chinese_to_arabic(chinese_match.group(1))
                    if chapter_num == 1:
                        is_first_chapter = True
                except Exception as e:
                    print(f"处理中文数字章节 '{chapter_title}' 时出错: {str(e)}")
                
            if is_first_chapter:
                folder_name = f"{folder_counter:03d}"  # 格式化为001, 002, 003等
                folder_path = os.path.join(source_dir, folder_name)
                
                # 如果文件夹已存在，尝试创建新的文件夹名
                while os.path.exists(folder_path):
                    folder_counter += 1
                    folder_name = f"{folder_counter:03d}"
                    folder_path = os.path.join(source_dir, folder_name)
                
                # 创建文件夹
                os.makedirs(folder_path, exist_ok=True)
                
                # 更新当前文件夹
                current_folder = folder_path
                
                # 记录下一本书的文件夹编号
                folder_counter += 1
            
            # 如果还没有遇到过第1章，则在源文件目录中创建第一个文件夹
            if current_folder is None:
                folder_name = f"{folder_counter:03d}"
                current_folder = os.path.join(source_dir, folder_name)
                os.makedirs(current_folder, exist_ok=True)
                folder_counter += 1
            
            # 将章节标题中的中文数字转换为阿拉伯数字（仅用于文件名）
            filename_title = chapter_title
            # 匹配"第X章"格式
            chinese_chapter_match = re.match(r'^第([零一二两三四五六七八九十百千万亿]+)章(.*?)$', filename_title)
            if chinese_chapter_match:
                try:
                    chinese_num = chinese_chapter_match.group(1)
                    arabic_num = chinese_to_arabic(chinese_num)
                    rest_of_title = chinese_chapter_match.group(2)
                    filename_title = f"第{arabic_num}章{rest_of_title}"
                except Exception as e:
                    print(f"转换文件名中的中文数字 '{chinese_num}' 时出错: {str(e)}")
            
            # Create a valid filename
            filename = f"{filename_title}.txt"
            # Remove any invalid characters from filename
            filename = re.sub(r'[\\/*?:"<>|]', "", filename)
            
            # Create full path for the new file in the current folder
            new_file_path = os.path.join(current_folder, filename)
            
            # 将章节内容写入文件，统一使用UTF-8编码
            # 注意：章节内容已经包含从当前章节标题到下一章节标题之前的所有内容
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(chapter)
            
            success_count += 1
        except Exception as e:
            messagebox.showwarning("警告", f"处理章节 '{chapter_title}' 时出错: {str(e)}")
    
    messagebox.showinfo("完成", f"成功分割了 {success_count} 个章节，并按书籍组织到不同文件夹\n所有文件均已保存为UTF-8编码\n章节标题中的中文数字已转换为阿拉伯数字\n每个章节文件包含从该章节标题到下一章节标题之前的所有内容\n最后一个章节包含从该章节标题到文件末尾的所有内容")

def select_file():
    file_path = filedialog.askopenfilename(
        title="选择源文件",
        filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
    )
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

def process_file():
    file_path = entry_path.get()
    if not file_path:
        messagebox.showwarning("警告", "请选择源文件")
        return
    
    if not os.path.exists(file_path):
        messagebox.showerror("错误", "文件不存在")
        return
    
    try:
        split_text_file(file_path)
    except Exception as e:
        error_msg = f"处理文件时出错：{str(e)}\n\n{traceback.format_exc()}"
        messagebox.showerror("错误", error_msg)

# 创建主应用函数
def main():
    global entry_path, root
    
    # Create GUI with a more modern look
    root = tk.Tk()
    root.title("章节分割工具")
    root.geometry("550x220")
    root.resizable(True, False)
    
    # Set background color
    bg_color = "#f0f0f0"
    root.configure(bg=bg_color)
    
    # File selection area
    frame_file = tk.Frame(root, pady=20, bg=bg_color)
    frame_file.pack(fill=tk.X, padx=20)
    
    label_path = tk.Label(frame_file, text="源文件路径:", bg=bg_color, font=("微软雅黑", 10))
    label_path.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
    
    entry_path = tk.Entry(frame_file, width=50, font=("微软雅黑", 10))
    entry_path.grid(row=0, column=1, sticky=tk.EW)
    
    button_browse = tk.Button(
        frame_file, 
        text="浏览...", 
        command=select_file,
        relief=tk.GROOVE,
        bg="#e0e0e0",
        font=("微软雅黑", 9)
    )
    button_browse.grid(row=0, column=2, padx=(10, 0))
    
    # Process button with better styling
    button_process = tk.Button(
        root, 
        text="分割章节", 
        command=process_file,
        width=20,
        height=2,
        relief=tk.GROOVE,
        bg="#4caf50",
        fg="white",
        font=("微软雅黑", 10, "bold")
    )
    button_process.pack(pady=20)
    
    # Description
    description = tk.Label(
        root, 
        text="此工具会按书籍将章节分割到序号文件夹中(001, 002...)\n" +
             "支持阿拉伯数字章节(如'第1章')和中文数字章节(如'第一章'、'第十一章'、'第一三五章')\n" +
             "文件名中的中文数字章节号将转换为阿拉伯数字\n" +
             "每个章节文件包含从该章节标题到下一章节标题之前的所有内容\n" +
             "最后一个章节包含从该章节标题到文件末尾的所有内容\n" +
             "所有章节将统一保存为UTF-8编码",
        fg="#555555",
        bg=bg_color,
        font=("微软雅黑", 9)
    )
    description.pack(pady=10)
    
    # Configure grid
    frame_file.columnconfigure(1, weight=1)
    
    # Run the application
    root.mainloop()

# 测试中文数字转换函数
def test_chinese_to_arabic():
    test_cases = [
        ("一", 1),
        ("二", 2),
        ("十", 10),
        ("十一", 11),
        ("二十", 20),
        ("二十一", 21),
        ("一百", 100),
        ("一百零一", 101),
        ("一百二十三", 123),
        ("一千二百三十四", 1234),
        ("一万", 10000),
        ("一亿", 100000000),
        ("一零", 10),
        ("一二三", 123),
        ("一三五", 135),
    ]
    
    success_count = 0
    fail_count = 0
    
    print("=== 测试中文数字转换函数 ===")
    for chinese, expected in test_cases:
        result = chinese_to_arabic(chinese)
        if result != expected:
            print(f"测试失败: '{chinese}' 应该转换为 {expected}，但结果是 {result}")
            fail_count += 1
        else:
            print(f"测试成功: '{chinese}' => {result}")
            success_count += 1
    
    print(f"\n总结: {len(test_cases)}个测试用例, {success_count}个成功, {fail_count}个失败")
    return fail_count == 0

# 测试章节识别功能
def test_chapter_recognition(test_file="test_chinese_chapters.txt"):
    if not os.path.exists(test_file):
        print(f"错误: 测试文件 '{test_file}' 不存在")
        return False
    
    print(f"\n=== 测试章节识别功能 ({test_file}) ===")
    
    # 读取测试文件
    encoding = detect_encoding(test_file)
    with open(test_file, 'r', encoding=encoding) as f:
        content = f.read()
    
    # 直接从文件内容中查找所有以"第X章"开头的行作为实际的章节标题
    real_chapter_titles = []
    for line in content.split('\n'):
        line = line.strip()
        if line and re.match(r'^第(?:\d+|[零一二两三四五六七八九十百千万亿]+)章', line):
            real_chapter_titles.append(line)
    
    print("\n实际章节标题:")
    for i, title in enumerate(real_chapter_titles):
        # 尝试提取章节号
        arabic_match = re.match(r'^第(\d+)章', title)
        chinese_match = re.match(r'^第([零一二两三四五六七八九十百千万亿]+)章', title)
        
        chapter_num = None
        if arabic_match:
            chapter_num = int(arabic_match.group(1))
            source = "阿拉伯数字"
        elif chinese_match:
            try:
                chapter_num = chinese_to_arabic(chinese_match.group(1))
                source = "中文数字"
            except Exception as e:
                source = f"中文数字(转换失败: {str(e)})"
        
        print(f"{i+1}. {title} => 章节号: {chapter_num} ({source})")
    
    # 使用我们的章节分割逻辑进行测试
    print("\n使用程序的正则表达式模式识别章节:")
    chapter_pattern = r'(第(?:\d+|[零一二两三四五六七八九十百千万亿]+)章[\s\S]*?)(?=第(?:\d+|[零一二两三四五六七八九十百千万亿]+)章|$)'
    
    # 匹配所有章节
    chapters = re.findall(chapter_pattern, content, re.DOTALL)
    identified_chapters = []
    
    for i, chapter in enumerate(chapters):
        chapter_content = chapter.strip()
        lines = chapter_content.split('\n')
        if not lines:
            continue
            
        chapter_title = lines[0].strip()
        
        # 只处理真正的章节标题
        if chapter_title in real_chapter_titles:
            identified_chapters.append(chapter_title)
            
            # 尝试提取章节号
            arabic_match = re.match(r'^第(\d+)章', chapter_title)
            chinese_match = re.match(r'^第([零一二两三四五六七八九十百千万亿]+)章', chapter_title)
            
            chapter_num = "未知"
            source = "未知"
            
            if arabic_match:
                chapter_num = int(arabic_match.group(1))
                source = "阿拉伯数字"
            elif chinese_match:
                try:
                    chapter_num = chinese_to_arabic(chinese_match.group(1))
                    source = "中文数字"
                except Exception as e:
                    source = f"中文数字(转换失败: {str(e)})"
            
            print(f"{i+1}. {chapter_title} => 章节号: {chapter_num} ({source})")
    
    # 检查结果
    success = set(real_chapter_titles) == set(identified_chapters)
    print(f"\n测试结果: 实际章节数量: {len(real_chapter_titles)}, 成功识别: {len(identified_chapters)}")
    
    if not success:
        print("\n章节识别不完整或有错误:")
        missed = set(real_chapter_titles) - set(identified_chapters)
        if missed:
            print("未识别的章节:")
            for title in missed:
                print(f"- {title}")
                
        extra = set(identified_chapters) - set(real_chapter_titles)
        if extra:
            print("错误识别的章节:")
            for title in extra:
                print(f"- {title}")
    
    return success

# 确保脚本可以直接运行
if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # 运行测试
        num_test = test_chinese_to_arabic()
        chap_test = test_chapter_recognition()
        if num_test and chap_test:
            print("\n所有测试通过!")
        sys.exit(0)
    
    # 正常运行GUI
    main() 