#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    unit = 1
    
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
    
    for chinese, expected in test_cases:
        result = chinese_to_arabic(chinese)
        if result != expected:
            print(f"错误: '{chinese}' 应该是 {expected}，但结果是 {result}")
        else:
            print(f"正确: '{chinese}' => {result}")

if __name__ == "__main__":
    print("=== 测试中文数字转换 ===")
    test_chinese_to_arabic()
    print("=== 测试完成 ===") 