import os
import requests
from dotenv import load_dotenv
from collections import deque

load_dotenv()
API_KEY = os.getenv('API_KEY')
CHATGPT_API_URL = os.getenv('CHATGPT_API_URL')

if not API_KEY:
    raise ValueError("API_KEY không được thiết lập trong biến môi trường.")
if not CHATGPT_API_URL:
    raise ValueError("CHATGPT_API_URL không được thiết lập trong biến môi trường.")

MAX_HISTORY = 10
conversation_history = deque(maxlen=MAX_HISTORY)

session = requests.Session()
session.headers.update({
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
})

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Bạn là một trợ lý điều khiển nhà thông minh tên là Aya! "
        "Bạn cũng là một trợ lý ảo thông minh giống như Alexa. "
        "Người dùng mà bạn đang hỗ trợ là chủ sở hữu của hệ thống này, "
        "hãy luôn nhớ rằng đây là người bạn phục vụ."
    )
}

def get_response(prompt):
  
    conversation_history.append({"role": "user", "content": prompt})

    messages = [SYSTEM_PROMPT] + list(conversation_history)
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 100,
        "stream": False,
        "temperature": 0.5,
        "top_p": 1
    }

    try:
        response = session.post(CHATGPT_API_URL, json=data)
        response.raise_for_status()
        result = response.json()

        chatgpt_reply = result['choices'][0]['message']['content'].strip()

        conversation_history.append({"role": "assistant", "content": chatgpt_reply})
        return chatgpt_reply

    except requests.exceptions.RequestException as e:
        print(f"-----------------> Error calling ChatGPT API: {e}")
        return "Xin lỗi, không thể kết nối với dịch vụ API."