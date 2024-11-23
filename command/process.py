from control import *
from chatgpt import *
from is_device import *
from speak import *
from fine_tuning import *
from search_agent import *
from alarm import *
from music import *
from notification import *
from my_calendar import *
from listen import *
from kid import play_sound_animal,play_story_sound

def process_command(command):
    if "lấy lịch" in command:
        print("Đang lấy danh sách sự kiện...")
        speak(get_calendar_events())
    elif "thêm lịch" in command:
        input_for_add_event() # add_event inside here
        # print("Đang tạo sự kiện mới...")
        # summary = "Họp nhóm dự án"
        # location = "Hồ Chí Minh, Việt Nam"
        # description = "Thảo luận tiến độ dự án."
        # start_time = "2024-11-24T10:00:00+07:00"
        # end_time = "2024-11-24T11:00:00+07:00"
        # add_event(summary, location, description, start_time, end_time)
    elif "bật cảm biến" in command or "tắt cảm biến" in command:
        if "độ ẩm" in command:
            if "bật" in command:
                set_sensor_status(MOISTURE_FEED, True)
            elif "tắt" in command:
                set_sensor_status(MOISTURE_FEED, False)
        elif "nhiệt độ" in command:
            if "bật" in command:
                set_sensor_status(TEMPERATURE_FEED, True)
            elif "tắt" in command:
                set_sensor_status(TEMPERATURE_FEED, False)
    elif  'âm lượng' in command or 'loa' in command:
        volume_level = re.search(r'\d+', command)
        if volume_level:
            volume_level = int(volume_level.group())
            if volume_level > 100:
                volume_level = 100
            elif volume_level < 0:
                volume_level = 0
        else:
            volume_level = 50
        set_volume(volume_level)
        response = f"Đã điều chỉnh âm lượng đến {volume_level}%."
        print(response)
        speak(response)
    elif any(keyword in command for keyword in ['phát nhạc', 'nhạc']):
    
        query = command
        for keyword in ['phát nhạc', 'mở nhạc']:
            query = query.replace(keyword, '').strip()
        if query:
            video_url = search_youtube(query)
            if video_url:
                speak(f"Đang mở bài hát {query}.")
                play_youtube_video(video_url)
            else:
                speak("Không tìm thấy bài hát trên YouTube.")
        else:
            speak("Vui lòng nói rõ tên bài hát bạn muốn phát.")
    elif "kêu" in command or ("tiếng" in command and "kêu" in command):
        play_sound_animal(command)
    elif "kể" in command and ("truyện" in command or "chuyện" in command):
        print("Đang kể truyện...")
        play_story_sound()
    elif is_device_command(command):
        actions = {
            'bật': 'on',
            'mở': 'on',
            'tắt': 'off',
            'đóng': 'off'
        }
        devices = {
            'đèn': 'led1',
            'quạt': 'fan',  
            'cửa': 'door',
            'máy lạnh': 'ac'
        }
        rooms = ['phòng khách', 'phòng ngủ', 'phòng bếp', 'phòng làm việc']

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
            response=f"Đã {action_match.group(0).lower()} {device} ở {room}"
            feed_name=devices[device]
            control_device(action,feed_name)  
      
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
    elif any(keyword in command for keyword in ["thời tiết", "tin tức", "hôm nay"]):
        tavily_answer=search_and_summarize(command)
        speak(tavily_answer)
        print(f"Final Answer: {tavily_answer}")
    elif any(keyword in command for keyword in ["báo thức", "nhắc nhở","hẹn giờ", "alarm", "reminder"]):
        response = alarm_reminder_action(command)
        print(response)
        speak(response)
        return None
    else:
        print("Gửi yêu cầu đến ChatGPT API...")
        chatgpt_answer = chatgpt_response(command)
        print(f"ChatGPT trả lời: {chatgpt_answer}")
        speak(chatgpt_answer)
