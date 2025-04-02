import tkinter as tk
from tkinter import filedialog
from text_formatter import TextFormatter

class BatchTextFormatter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("批量文本换行处理器")
        
        # 创建界面组件
        self.file_label = tk.Label(self.root, text="选择多个文件:")
        self.file_label.pack()
        
        self.select_button = tk.Button(self.root, text="选择多个TXT文件", command=self.select_files)
        self.select_button.pack()
        
        self.process_button = tk.Button(self.root, text="批量处理并保存", command=self.process_files, state=tk.DISABLED)
        self.process_button.pack()
        
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack()
        
        self.selected_files = []
    
    def select_files(self):
        self.selected_files = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
        if self.selected_files:
            self.process_button.config(state=tk.NORMAL)
            self.status_label.config(text=f"已选择 {len(self.selected_files)} 个文件")
    
    def process_files(self):
        try:
            for file_path in self.selected_files:
                formatter = TextFormatter()
                formatter.selected_file = file_path
                formatter.process_file()
            
            self.status_label.config(text=f"批量处理完成! 共处理 {len(self.selected_files)} 个文件")
            
        except Exception as e:
            self.status_label.config(text=f"错误: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BatchTextFormatter()
    app.run()