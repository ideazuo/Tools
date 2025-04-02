#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

# 直接复制必要的函数，而不是导入，防止导入问题
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

def test_filename_conversion():
    """测试中文数字章节标题到阿拉伯数字文件名的转换"""
    test_cases = [
        ("第一章 引子", "第1章 引子"),
        ("第二章 开始", "第2章 开始"),
        ("第十章 转折", "第10章 转折"),
        ("第十一章 高潮", "第11章 高潮"),
        ("第二十章 结局", "第20章 结局"),
        ("第一零零章 特殊章节", "第100章 特殊章节"),
        ("第一三五章 特殊章节", "第135章 特殊章节"),
        ("第一百章 百位数章节", "第100章 百位数章节"),
        ("第一千章 千位数章节", "第1000章 千位数章节"),
    ]
    
    print("=== 测试中文数字章节标题到阿拉伯数字文件名的转换 ===")
    success_count = 0
    fail_count = 0
    
    for chinese_title, expected_filename in test_cases:
        print(f"\n测试: '{chinese_title}'")
        # 将章节标题中的中文数字转换为阿拉伯数字
        filename_title = chinese_title
        # 匹配"第X章"格式
        chinese_chapter_match = re.match(r'^第([零一二两三四五六七八九十百千万亿]+)章(.*?)$', filename_title)
        if chinese_chapter_match:
            try:
                chinese_num = chinese_chapter_match.group(1)
                print(f"  提取的中文数字: '{chinese_num}'")
                arabic_num = chinese_to_arabic(chinese_num)
                print(f"  转换为阿拉伯数字: {arabic_num}")
                rest_of_title = chinese_chapter_match.group(2)
                print(f"  标题剩余部分: '{rest_of_title}'")
                filename_title = f"第{arabic_num}章{rest_of_title}"
                print(f"  生成的文件名: '{filename_title}'")
            except Exception as e:
                print(f"  转换失败: {str(e)}")
        else:
            print(f"  未识别为中文数字章节标题")
                
        if filename_title == expected_filename:
            print(f"  测试成功: '{chinese_title}' => '{filename_title}'")
            success_count += 1
        else:
            print(f"  测试失败: '{chinese_title}' 应该转换为 '{expected_filename}'，但结果是 '{filename_title}'")
            fail_count += 1

    print(f"\n测试结果: 总共 {len(test_cases)} 个测试用例, 成功 {success_count} 个, 失败 {fail_count} 个")

if __name__ == "__main__":
    test_filename_conversion() 