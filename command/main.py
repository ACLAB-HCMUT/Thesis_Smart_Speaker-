import re
import random
import speech_recognition as sr
from gtts import gTTS
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')
# request chatpt 
def chatgpt_response(prompt):
    url = "https://yescale.one/v1/chat/completions"
    headers = {
        "Content-Type":"application/json",
        "Authorization":f"Bearer {API_KEY}"  
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "assistant", "content": prompt}
        ],
        "max_tokens": 50,
        "stream": False,
        "temperature": -1,
        "top_p": 1
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        # retrun from chatgpt
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error calling ChatGPT API: {e}")
        return "Xin lỗi, không thể kết nối với dịch vụ ChatGPT."

def speak(text):
    tts = gTTS(text=text, lang='vi')
    tts.save("command.mp3")
    if os.system("mpg123 command.mp3") != 0:  
        os.system("aplay command.mp3")  

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Đang lắng nghe...")
        audio = recognizer.listen(source, timeout=5)
        try:
            command = recognizer.recognize_google(audio, language='vi-VN')
            print(f"Lệnh của bạn: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Không thể nhận diện được giọng nói.")
            return None
        except sr.RequestError as e:
            print(f"Không thể yêu cầu dịch vụ Google Speech Recognition; {e}")
            return None

def is_device_command(command):
    actions = ['bật', 'mở', 'tắt', 'đóng']
    rooms = ['phòng khách', 'phòng ngủ', 'phòng bếp', 'phòng làm việc']
    devices = ['đèn', 'cửa', 'máy lạnh']
    
    # regex
    action_pattern = r'\b(' + '|'.join(actions) + r')\b'
    room_pattern = r'\b(' + '|'.join(rooms) + r')\b'
    device_pattern = r'\b(' + '|'.join(devices) + r')\b'
    
    
    return bool(re.search(action_pattern, command)) or \
           bool(re.search(room_pattern, command)) or \
           bool(re.search(device_pattern, command))
# def process_command(command):
    
#     # Action
#     actions = {
#         'bật': 'on',
#         'mở': 'on',
#         'tắt': 'off',
#         'đóng': 'off'
#     }
#     rooms = ['phòng khách', 'phòng ngủ', 'phòng bếp', 'phòng làm việc']
#     devices = ['đèn', 'cửa', 'máy lạnh']

#     # regex
#     room_pattern = r'\b(' + '|'.join(rooms) + r')\b'
#     device_pattern = r'\b(' + '|'.join(devices) + r')\b'
#     action_pattern = r'\b(' + '|'.join(actions.keys()) + r')\b'

#     # search for key words
#     room_match = re.search(room_pattern, command, re.IGNORECASE)
#     device_match = re.search(device_pattern, command, re.IGNORECASE)
#     action_match = re.search(action_pattern, command, re.IGNORECASE)
#     response=""
#     # case 1: full command 
#     if room_match and device_match and action_match:
#         room = room_match.group(0)
#         device = device_match.group(0)
#         action = actions[action_match.group(0).lower()]
#         response=f"Đang {action_match.group(0).lower()} {device} ở {room}"
    
#     # case 2: missing device, but room, action are present
#     elif room_match and action_match and not device_match:
#         room = room_match.group(0)
#         action = actions[action_match.group(0).lower()]
#         response=f"Vui lòng chỉ định thiết bị để {action_match.group(0).lower()} ở {room}."
    
#     # case 3: missing action, but room, device are present
#     elif room_match and device_match and not action_match:
#         room = room_match.group(0)
#         device = device_match.group(0)
#         response=f"Vui lòng chỉ định hành động cho {device} ở {room}."
    
#     # case 4: room mentioned but missing both action and device
#     elif room_match and not action_match and not device_match:
#         room = room_match.group(0)
#         response=f"Vui lòng chỉ định thiết bị và hành động ở {room}."
    
#     # case 5: command not recognized
#     else:
#         response="Lệnh không được nhận diện, vui lòng thử lại."
#     print(response)
#     speak(response)

def process_command(command):
    if is_device_command(command):
        actions = {
            'bật': 'on',
            'mở': 'on',
            'tắt': 'off',
            'đóng': 'off'
        }
        rooms = ['phòng khách', 'phòng ngủ', 'phòng bếp', 'phòng làm việc']
        devices = ['đèn', 'cửa', 'máy lạnh']

        room_pattern = r'\b(' + '|'.join(rooms) + r')\b'
        device_pattern = r'\b(' + '|'.join(devices) + r')\b'
        action_pattern = r'\b(' + '|'.join(actions.keys()) + r')\b'

        room_match = re.search(room_pattern, command, re.IGNORECASE)
        device_match = re.search(device_pattern, command, re.IGNORECASE)
        action_match = re.search(action_pattern, command, re.IGNORECASE)
        response=""
        
        # case 1: full command
        if room_match and device_match and action_match:
            room = room_match.group(0)
            device = device_match.group(0)
            action = actions[action_match.group(0).lower()]
            response=f"Đang {action_match.group(0).lower()} {device} ở {room}"
        
        # case 2: missing device, but room, action are present
        elif room_match and action_match and not device_match:
            room = room_match.group(0)
            action = actions[action_match.group(0).lower()]
            response=f"Vui lòng chỉ định thiết bị để {action_match.group(0).lower()} ở {room}."

        # case 3: missing action, but room, device are present
        elif room_match and device_match and not action_match:
            room = room_match.group(0)
            device = device_match.group(0)
            response=f"Vui lòng chỉ định hành động cho {device} ở {room}."
        
        # case 4: room mentioned but missing both action and device
        elif room_match and not action_match and not device_match:
            room = room_match.group(0)
            response=f"Vui lòng chỉ định thiết bị và hành động ở {room}."
        elif action_match and device_match and not room_match:
            device = device_match.group(0)
            action = action_match.group(0)
            response = f"Vui lòng chỉ định phòng để {action_match.group(0).lower()} {device}."
        elif action_match and device_match and not room_match:
            device = device_match.group(0)
            action = action_match.group(0)
            response = f"Vui lòng chỉ định phòng để {action_match.group(0).lower()} {device}."
        # case 5: command not recognized
        else:
            response="Lệnh không được nhận diện, vui lòng thử lại."
        
        print(response)
        speak(response)
    else:
        print("Gửi yêu cầu đến ChatGPT API...")
        chatgpt_answer = chatgpt_response(command)
        print(f"ChatGPT trả lời: {chatgpt_answer}")
        speak(chatgpt_answer)


# test
# print("API key",API_KEY)
# a= listen_command()
# print("command", a)
# print(is_device_command(a)) 
# query=listen_command()

# process_command("elon musk là ai")
# process_command("bật đèn phòng khách lên")
# process_command(listen_command())

# speak(chatgpt_response(listen_command()))

def main():
	text1 = "Ơi, Aya đây"
	text2 = "Tui nè, có gì không"
	text3 = "Hở, có chuyện gì không"
	text4 = "À há"
	num = random.randint(1,3)
	if (num == 1):
		print(f"{text1}")
		speak(text1)
	elif (num == 2):
		print(f"{text2}")
		speak(text2)
	elif (num == 3):
		print(f"{text3}")
		speak(text3)
	else:
		print(f"{text4}")
		speak(text4)
	while 1:
		# print("APT key", API_KEY)
		command = listen_command()
		if "cảm ơn" in command.lower() or "Cảm ơn" in command.lower():
			chatgpt_answer = "Không có gì"
			print(f"ChatGPT trả lời: {chatgpt_answer}")
			speak(chatgpt_answer)
			break
		else:
			process_command(command)
			print(f"Còn gì nữa không")
			speak("Còn gì nữa không")


if __name__ == "__main__":
    main()

