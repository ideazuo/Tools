import os, sys 
import re 
from chapter_splitter import chinese_to_arabic, detect_encoding 
 
def test_file(file_path): 
    print(f"测试文件: {file_path}") 
    encoding = detect_encoding(file_path) 
    with open(file_path, 'r', encoding=encoding) as f: 
        content = f.read() 
 
    # 定义章节匹配模式 
