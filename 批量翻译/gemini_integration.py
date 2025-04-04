import google.generativeai as genai

class GeminiIntegration:
    def __init__(self, api_key, temperature=0.7, top_p=0.8):
        """初始化Gemini API客户端"""
        genai.configure(api_key=api_key,transport='rest')
        generation_config = genai.GenerationConfig(
            temperature=temperature,
            top_p=top_p
        )
        self.model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25', generation_config=generation_config)
    
    def generate_text(self, prompt):
        """调用Gemini模型生成文本"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"生成文本时出错: {str(e)}"

if __name__ == "__main__":
    # 使用示例
    api_key = "AIzaSyDS9TuQCWE-r3SwWrE_SvMxYJASBFHIwW0"
    gemini = GeminiIntegration(api_key, temperature=0.7, top_p=0.8)
    
    while True:
        user_input = input("请输入您的提示(输入'退出'结束): ")
        if user_input.lower() == '退出':
            break
            
        print("正在生成...")
        response = gemini.generate_text(user_input)
        print("Gemini回复:", response)