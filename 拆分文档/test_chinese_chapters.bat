@echo off
rem 自动测试中文章节标题识别
echo 测试中文章节标题识别功能...

rem 添加简单的非阻塞GUI测试
echo 添加代码用于测试分析...

echo 在Python中创建临时测试脚本
echo import os, sys > temp_test.py
echo import re >> temp_test.py
echo from chapter_splitter import chinese_to_arabic, detect_encoding >> temp_test.py
echo. >> temp_test.py
echo def test_file(file_path): >> temp_test.py
echo     print(f"测试文件: {file_path}") >> temp_test.py
echo     encoding = detect_encoding(file_path) >> temp_test.py
echo     with open(file_path, 'r', encoding=encoding) as f: >> temp_test.py
echo         content = f.read() >> temp_test.py
echo. >> temp_test.py
echo     # 定义章节匹配模式 >> temp_test.py
echo     chapter_pattern = r'(第(?:\d+|[零一二两三四五六七八九十百千万亿]+)章[\s\S]*?)(?=第(?:\d+|[零一二两三四五六七八九十百千万亿]+)章|$)' >> temp_test.py
echo     chapters = re.findall(chapter_pattern, content, re.DOTALL) >> temp_test.py
echo. >> temp_test.py
echo     print(f"找到 {len(chapters)} 个章节") >> temp_test.py
echo     for i, chapter in enumerate(chapters): >> temp_test.py
echo         # 提取章节标题 >> temp_test.py
echo         chapter_title = chapter.strip().split('\n')[0].strip() >> temp_test.py
echo         print(f"{i+1}. {chapter_title}") >> temp_test.py
echo. >> temp_test.py
echo         # 尝试提取章节号 >> temp_test.py
echo         arabic_match = re.match(r'^第(\d+)章', chapter_title) >> temp_test.py
echo         chinese_match = re.match(r'^第([零一二两三四五六七八九十百千万亿]+)章', chapter_title) >> temp_test.py
echo. >> temp_test.py
echo         if arabic_match: >> temp_test.py
echo             chapter_num = int(arabic_match.group(1)) >> temp_test.py
echo             print(f"   章节号: {chapter_num} (阿拉伯数字)") >> temp_test.py
echo         elif chinese_match: >> temp_test.py
echo             try: >> temp_test.py
echo                 chapter_num = chinese_to_arabic(chinese_match.group(1)) >> temp_test.py
echo                 print(f"   章节号: {chapter_num} (中文数字)") >> temp_test.py
echo             except Exception as e: >> temp_test.py
echo                 print(f"   无法解析章节号: {str(e)}") >> temp_test.py
echo         else: >> temp_test.py
echo             print("   未能识别章节号") >> temp_test.py
echo. >> temp_test.py
echo if __name__ == "__main__": >> temp_test.py
echo     if len(sys.argv) > 1: >> temp_test.py
echo         test_file(sys.argv[1]) >> temp_test.py
echo     else: >> temp_test.py
echo         print("请指定测试文件路径") >> temp_test.py

echo 运行测试...
python temp_test.py test_chinese_chapters.txt

echo 测试完成，准备删除临时文件
rem del temp_test.py

pause 