import os
import requests
import json
from dotenv import load_dotenv
from pydub import AudioSegment
load_dotenv()
API_KEY = os.getenv('API_KEY')
CHATGPT_API_URL = os.getenv('CHATGPT_API_URL')
silence = AudioSegment.silent(duration=500)
# request chatpt 
def chatgpt_response(prompt):
    headers = {
        "Content-Type":"application/json",
        "Authorization":f"Bearer {API_KEY}"  
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Bạn là một trợ lý điều khiển nhà thông minh tên là Aya!"},
            {"role": "assistant", "content": prompt}
        ],
        "max_tokens": 70,
        "stream": False,
        "temperature": -1,
        "top_p": 1
    }

    try:
        response = requests.post(CHATGPT_API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        # retrun from chatgpt
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error calling ChatGPT API: {e}")
        return "Xin lỗi, không thể kết nối với dịch vụ API."
