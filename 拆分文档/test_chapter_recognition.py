import os
import re
import sys

# 直接复制必要的函数，而不是导入
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

def chinese_to_arabic(chinese_str):
    """将中文数字转换为阿拉伯数字"""
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

def test_file(file_path):
    print(f"测试文件: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在 - {file_path}")
        return
        
    encoding = detect_encoding(file_path)
    print(f"文件编码: {encoding}")
    
    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()
    
    # 定义章节匹配模式 - 更精确的模式
    chapter_pattern = r'(^第(?:\d+|[零一二两三四五六七八九十百千万亿]+)章.*?(?:\n|$)[\s\S]*?)(?=^第(?:\d+|[零一二两三四五六七八九十百千万亿]+)章|$)'
    chapters = re.findall(chapter_pattern, content, re.DOTALL | re.MULTILINE)
    
    print(f"找到 {len(chapters)} 个章节")
    for i, chapter in enumerate(chapters):
        # 提取章节标题
        lines = chapter.strip().split('\n')
        if not lines:
            continue
            
        chapter_title = lines[0].strip()
        print(f"\n{i+1}. {chapter_title}")
        
        # 尝试提取章节号
        arabic_match = re.match(r'^第(\d+)章', chapter_title)
        chinese_match = re.match(r'^第([零一二两三四五六七八九十百千万亿]+)章', chapter_title)
        
        if arabic_match:
            chapter_num = int(arabic_match.group(1))
            print(f"   章节号: {chapter_num} (阿拉伯数字)")
        elif chinese_match:
            try:
                chinese_num = chinese_match.group(1)
                chapter_num = chinese_to_arabic(chinese_num)
                print(f"   章节号: {chapter_num} (中文数字 '{chinese_num}')")
            except Exception as e:
                print(f"   无法解析章节号: {str(e)}")
        else:
            print("   未能识别章节号")
    
    # 特别测试是否能正确识别和处理第一章节
    print("\n检查是否正确识别\"第一章\"类型的章节开始:")
    first_chapter_pattern = r'第(?:1|一|壹)章'
    first_chapters = re.findall(first_chapter_pattern, content)
    
    if first_chapters:
        print(f"找到 {len(first_chapters)} 个\"第一章\"类型的章节:")
        for i, title in enumerate(first_chapters):
            print(f"{i+1}. {title}")
    else:
        print("未找到任何\"第一章\"类型的章节")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_file(sys.argv[1])
    else:
        # 默认测试文件
        test_file("test_chinese_chapters.txt") 