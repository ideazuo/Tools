import re

class TextFormatter:
    def __init__(self):
        self.selected_file = ""
    
    def process_file(self, file_path=None):
        if file_path:
            self.selected_file = file_path
        
        try:
            # 读取文件并转换为UTF-8
            with open(self.selected_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 处理换行逻辑
            processed_content = self.process_line_breaks(content)
            processed_content = self.double_newlines(processed_content)
            
            # 保存新文件
            new_file = self.selected_file.replace('.txt', '_formatted.txt')
            with open(new_file, 'w', encoding='utf-8') as f:
                f.write(processed_content)
                
            return True, new_file
            
        except Exception as e:
            return False, str(e)
    
    def double_newlines(self, text):
        """在已有换行符后添加额外换行符"""
        result = []
        i = 0
        while i < len(text):
            if text[i] == '\n':
                # 检查前后字符是否为换行符
                prev_char = text[i-1] if i > 0 else None
                next_char = text[i+1] if i < len(text)-1 else None
                if prev_char != '\n' and next_char != '\n':
                    result.append('\n\n')
                else:
                    result.append('\n')
                i += 1
            else:
                result.append(text[i])
                i += 1
        return ''.join(result)
        
    def process_line_breaks(self, text):
        # 处理引号内的内容
        in_quotes = False
        result = []
        i = 0
        
        while i < len(text):
            char = text[i]
            
            # 处理中文引号
            if char == '“':
                in_quotes = True
                result.append(char)
                i += 1
                continue
                
            if char == '”':
                in_quotes = False
                result.append(char)
                i += 1
                continue
                
            # 如果在引号内，不处理换行
            if in_quotes:
                result.append(char)
                i += 1
                continue
                
            # 处理基础符号换行
            if not in_quotes and char in {'。', '！', '？', '；'}:
                
                # 检查连续符号
                j = i + 1
                while j < len(text) and text[j] in {'。', '！', '？', '；',}:
                    j += 1
                    
                if j > i + 1:
                    result.extend(text[i:j-1])
                    result.append(text[j-1])
                    # 检查下一个字符是否为换行符
                    if j < len(text) and text[j] != '\n':
                        result.append('\n')
                    i = j
                else:
                    result.append(char)
                    # 检查下一个字符是否为换行符
                    if i+1 < len(text) and text[i+1] != '\n':
                        result.append('\n')
                    i += 1
            else:
                result.append(char)
                i += 1
                
        return ''.join(result)
    
if __name__ == "__main__":
    print("请使用batch_text_formatter.py进行批量处理")