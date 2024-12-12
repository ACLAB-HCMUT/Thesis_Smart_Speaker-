import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')
CHATGPT_API_URL = os.getenv('CHATGPT_API_URL')

conversation_history = []

def chatgpt_response(prompt):
    global conversation_history
    conversation_history.append({"role": "user", "content": prompt})
    headers = {
        "Content-Type":"application/json",
        "Authorization":f"Bearer {API_KEY}"  
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Bạn là một trợ lý điều khiển nhà thông minh tên là Aya! Bạn cũng là một trợ lý ảo thông minh giống như Alexa.Người dùng mà bạn đang hỗ trợ là chủ sở hữu của hệ thống này, hãy luôn nhớ rằng đây là người bạn phục vụ."},
            # {"role": "user", "content": prompt}
        ]+ conversation_history,
        "max_tokens": 100,
        "stream": False,
        "temperature": 0.5,
        "top_p": 1
    }

    try:
        response = requests.post(CHATGPT_API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
    
        # return result['choices'][0]['message']['content']
        chatgpt_reply = result['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": chatgpt_reply})
        return chatgpt_reply

    except requests.exceptions.RequestException as e:
        print(f"-----------------> Error calling ChatGPT API: {e}")
        return "Xin lỗi, không thể kết nối với dịch vụ API."
