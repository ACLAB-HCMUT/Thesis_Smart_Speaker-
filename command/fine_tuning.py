import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")
CHATGPT_API_URL = os.getenv("CHATGPT_API_URL")
MODEL = os.getenv("MODEL")

def fine_tuning_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    
    data = {
        "model": MODEL, 
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }

    try:
        
        response = requests.post(CHATGPT_API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        
       
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Error calling ChatGPT API: {e}")
        return "Xin lỗi, không thể kết nối với API."
