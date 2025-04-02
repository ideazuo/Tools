#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import tempfile
import shutil

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

def test_chapter_content():
    """测试章节内容分割是否正确，验证每个章节文件包含从该章节到下一章节之前的所有内容"""
    # 创建一个临时目录来存放测试文件
    test_dir = tempfile.mkdtemp()
    try:
        # 创建测试文件
        test_file_path = os.path.join(test_dir, "test_chapter_content.txt")
        test_content = """第一章 测试章节一
这是第一章的内容。
这是第一章的更多内容。

这里有一些其他段落。

第二章 测试章节二
这是第二章的内容。
这包含第二章的所有文本。

中间有一些段落。

第三章 测试章节三
这是第三章的内容。
最后一章没有下一章，但应该包含到文件末尾的所有内容。

最后一行内容。"""

        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print("=== 测试章节内容分割 ===")
        print(f"创建测试文件: {test_file_path}")
        
        # 解析章节内容
        with open(test_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查换行符
        windows_newlines = content.count('\r\n')
        unix_newlines = content.count('\n') - windows_newlines
        print("文件中包含 " + str(windows_newlines) + " 个Windows换行符(\\r\\n)")
        print("文件中包含 " + str(unix_newlines) + " 个Unix换行符(\\n)")
        
        # 使用章节分割的正则表达式 - 注意处理多行匹配
        chapter_pattern = r'(^第(?:\d+|[零一二两三四五六七八九十百千万亿]+)章.*?(?:\n|$)[\s\S]*?)(?=^第(?:\d+|[零一二两三四五六七八九十百千万亿]+)章|$)'
        
        # 确保内容以换行符结束，这有助于正则表达式匹配的一致性
        if not content.endswith('\n'):
            content += '\n'
        
        # 将内容转换为统一的换行符格式
        normalized_content = content.replace('\r\n', '\n')
        
        chapters = re.findall(chapter_pattern, normalized_content, re.DOTALL | re.MULTILINE)
        
        print(f"分割后的章节数量: {len(chapters)}")
        print(f"原始内容长度: {len(normalized_content)} 字符")
        
        # 打印每个匹配章节的长度，检查是否有遗漏内容
        total_matched_length = 0
        for i, chap in enumerate(chapters):
            chap_len = len(chap)
            total_matched_length += chap_len
            print(f"章节 {i+1} 长度: {chap_len} 字符")
        
        print(f"所有章节总长度: {total_matched_length} 字符")
        
        # 对比提取的章节和原始文本
        for i, chapter in enumerate(chapters):
            chapter_content = chapter.strip()
            chapter_lines = chapter_content.split('\n')
            chapter_title = chapter_lines[0].strip() if chapter_lines else ""
            
            print(f"\n章节 {i+1}: {chapter_title}")
            print(f"开始内容: {chapter_content[:50]}...")
            print(f"结束内容: ...{chapter_content[-50:] if len(chapter_content) > 50 else chapter_content}")
            
            # 打印章节的所有行，对于调试很有用
            print(f"章节的行数: {len(chapter_lines)}")
            for j, line in enumerate(chapter_lines):
                if j < 10:  # 只打印前10行
                    print(f"  行 {j+1}: {line[:50]}...")
                
        # 使用直接分割方法来分割章节
        title_pattern = r'^第(?:\d+|[零一二两三四五六七八九十百千万亿]+)章.*?$'
        title_matches = list(re.finditer(title_pattern, normalized_content, re.MULTILINE))
        
        print(f"找到 {len(title_matches)} 个章节标题")
        
        # 根据标题位置分割内容
        direct_chapters = []
        for i, match in enumerate(title_matches):
            start_pos = match.start()
            if i < len(title_matches) - 1:
                end_pos = title_matches[i+1].start()
                chapter_text = normalized_content[start_pos:end_pos]
            else:
                chapter_text = normalized_content[start_pos:]
            direct_chapters.append(chapter_text)
            
        print(f"直接分割后的章节数量: {len(direct_chapters)}")
        
        # 对比章节内容
        for i, chapter in enumerate(direct_chapters):
            chapter_content = chapter.strip()
            chapter_lines = chapter_content.split('\n')
            chapter_title = chapter_lines[0].strip() if chapter_lines else ""
            
            print(f"\n章节 {i+1}: {chapter_title}")
            print(f"章节长度: {len(chapter)} 字符")
            print(f"行数: {len(chapter_lines)}")
            
            # 打印章节的前几行和后几行
            if len(chapter_lines) > 0:
                print("\n前几行:")
                for j in range(min(3, len(chapter_lines))):
                    print(f"  {chapter_lines[j]}")
                    
                if len(chapter_lines) > 3:
                    print("  ...")
                    
                    if len(chapter_lines) > 6:
                        print("\n后几行:")
                        for j in range(max(3, len(chapter_lines) - 3), len(chapter_lines)):
                            print(f"  {chapter_lines[j]}")
        
        # 验证章节分割是否正确
        expected_titles = ["第一章 测试章节一", "第二章 测试章节二", "第三章 测试章节三"]
        
        # 验证章节数量
        if len(direct_chapters) == len(expected_titles):
            print("\n章节数量正确")
        else:
            print(f"\n章节数量不匹配: 预期 {len(expected_titles)}, 实际 {len(direct_chapters)}")
            
        # 验证每个章节标题
        title_correct = True
        for i, chapter in enumerate(direct_chapters):
            if i < len(expected_titles):
                chapter_title = chapter.strip().split('\n')[0].strip()
                if chapter_title != expected_titles[i]:
                    title_correct = False
                    print(f"章节 {i+1} 标题不匹配: 预期 '{expected_titles[i]}', 实际 '{chapter_title}'")
        
        if title_correct:
            print("所有章节标题正确")
            
        # 验证章节是否包含预期的内容片段
        expected_content_parts = [
            ["这是第一章的内容", "这是第一章的更多内容", "这里有一些其他段落"],
            ["这是第二章的内容", "这包含第二章的所有文本", "中间有一些段落"],
            ["这是第三章的内容", "最后一章没有下一章", "最后一行内容"]
        ]
        
        content_correct = True
        for i, chapter in enumerate(direct_chapters):
            if i < len(expected_content_parts):
                for part in expected_content_parts[i]:
                    if part not in chapter:
                        content_correct = False
                        print(f"章节 {i+1} 缺少内容: '{part}'")
        
        if content_correct:
            print("所有章节内容正确")
            
        print("\n=== 测试结论 ===")
        if len(direct_chapters) == len(expected_titles) and title_correct and content_correct:
            print("测试通过: 章节分割正确")
        else:
            print("测试失败: 章节分割有问题")
            
        print("\n=== 测试完成 ===")
        
    finally:
        # 清理临时目录
        shutil.rmtree(test_dir)

if __name__ == "__main__":
    test_chapter_content() 