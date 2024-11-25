import os
import requests
import json
import re
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')
CHATGPT_API_URL = os.getenv('CHATGPT_API_URL')

def normalize_math_expression(expression):
    expression = expression.lower()
    expression = re.sub(r"\b của\b", "", expression) 
    expression = re.sub(r"\b(bằng bao nhiêu)\b", "", expression)
    expression = re.sub(r"\b(bằng mấy)\b", "", expression)
    expression = expression.replace("bình phương", "^2")
    expression = expression.replace("mũ", "^")
    expression = expression.replace("cộng", "+")
    expression = expression.replace("trừ", "-")
    expression = expression.replace("nhân", "*")
    expression = expression.replace("chia", "/")
    expression = expression.replace("bằng", "=")
    expression = expression.replace("căn bậc ba", "cbrt")
    expression = re.sub(r"căn bậc (\d+)", r"nthroot(\1,", expression)
    expression = expression.replace("căn bậc hai", "sqrt")
    expression = expression.replace("căn", "sqrt")
    expression = expression.replace("giai thừa", "!")
    expression = expression.replace("phần trăm", "%")
    expression = expression.replace("tích phân", "integrate")
    expression = expression.replace("đạo hàm", "derivative")
    expression = expression.replace("hàm số mũ", "exp")
    expression = expression.replace("logarit", "log")
    expression = expression.replace("sin", "sin")
    expression = expression.replace("cos", "cos")
    expression = expression.replace("tan", "tan")
    expression = expression.replace("pi", "π")
    expression = expression.replace("e mũ", "e^")
    expression = expression.replace("dấu ngoặc mở", "(")
    expression = expression.replace("dấu ngoặc đóng", ")")
    expression = expression.replace("chuyển vị", "transpose")
    expression = expression.replace("định thức", "det")
    expression = expression.replace("logarit tự nhiên", "ln")
    expression = expression.replace("lập phương", "^3")
    expression = re.sub(r"căn bậc (\d+)", r"nthroot(\1,", expression)
    if "nthroot(" in expression and not expression.endswith(")"):
        expression += ")"
    expression = " ".join(expression.split())  
    return expression

def math_calculation(prompt):
    headers = {
        "Content-Type":"application/json",
        "Authorization":f"Bearer {API_KEY}"  
    }
    
    prompt= normalize_math_expression(prompt)
    print("Mathhhhhhh--------------------- :",prompt)
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Bạn là một trợ lý toán học, chỉ trả về kết quả ngắn gọn, không trình bày các bước giải, không trả về các kí hiệu toán học dài dòng, hãy trả lời với ngôn ngữ nói."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100,
        "stream": False,
        "temperature": 0.5,
        "top_p": 1
    }

    try:
        response = requests.post(CHATGPT_API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
    
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"-----------------> Error calling ChatGPT API: {e}")
        return "Xin lỗi, không thể kết nối với dịch vụ API."
