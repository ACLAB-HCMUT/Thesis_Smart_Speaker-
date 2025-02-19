from control import set_volume
from chatgpt import get_response
from device_utils import is_device_command
from audio_utils import speak, set_default_voice
from search_agent import search_and_summarize
from reminders import alarm_reminder_action
# from music8D import search_youtube8,download_and_play_youtube_audio8,stop_music8
from music import search_youtube,download_and_play_youtube_audio,stop_music
# from notification import *
from my_calendar import get_calendar_events, input_for_add_event,extract_time_from_command,delete_event_by_name_or_time,extract_event_name_from_command
from time_utils import get_current_time,get_current_date_vn_format
from kid_mode import play_sound_animal, play_story_sound
from navigation import process_direction
# from math_calculation import math_calculation
from tuning import control
from weather import fetch_weather_data 
import re

current_eight_d_audio = None
def process_command(command):
    global music_process
    global default_voice
    global current_eight_d_audio
    command=command.lower()
    # if any(keyword in command for keyword in ["8d","8D","tám đê", "8 đê"]):

    #     query = command
    #     for keyword in ["phát nhạc", "mở nhạc", "mở bài","8D", "8d"]:
    #         query = query.replace(keyword, "").strip()
    #     if query:
    #         video_url = search_youtube8(query)
    #         if video_url:
    #             speak(f"Mời bạn nghe nhạc {query}.")
    #             download_and_play_youtube_audio8(video_url)
    #         else:
    #             speak("Không tìm thấy bài hát trên YouTube.")
    #     else:
    #         speak("Vui lòng nói rõ tên bài hát bạn muốn phát.")
    if any(keyword in command for keyword in ["phát nhạc", "nhạc", "mở bài"]):

        query = command
        for keyword in ["phát nhạc", "mở nhạc", "mở bài"]:
            query = query.replace(keyword, "").strip()
        if query:
            video_url = search_youtube(query)
            if video_url:
                speak(f"Mời bạn nghe nhạc {query}.")
                download_and_play_youtube_audio(video_url)
            else:
                speak("Không tìm thấy bài hát trên YouTube.")
        else:
            speak("Vui lòng nói rõ tên bài hát bạn muốn phát.")
    elif any(
        keyword in command
        for keyword in ["báo thức", "nhắc nhở", "hẹn giờ"]
    ):
        print ("process:", command)
        response = alarm_reminder_action(command)
        print(response)
        speak(response)
        return 1
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
        rooms = ['phòng khách', 'phòng ngủ', 'phòng bếp']

        room_pattern = r'\b(' + '|'.join(rooms) + r')\b'
        device_pattern = r'\b(' + '|'.join(devices) + r')\b'
        action_pattern = r'\b(' + '|'.join(actions.keys()) + r')\b'

        room_match = re.search(room_pattern, command, re.IGNORECASE)
        device_match = re.search(device_pattern, command, re.IGNORECASE)
        action_match = re.search(action_pattern, command, re.IGNORECASE)
        response=""
        
        # case 1: full command
        if room_match and device_match and action_match:
            check=control(command)
            # if check==1:
            #     return 1 
            response="Em đã thực hiện lệnh ạ."           
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
    elif command =="hôm nay":
        today= get_current_date_vn_format()
        today += " "
        today += fetch_weather_data()
        speak(today)
    elif command=="thời tiết" or command=="thời tiết hôm nay":
        speak(fetch_weather_data())

    elif any(
        keyword in command
        for keyword in ["giọng nữ", "giọng con gái", "giọng đàn bà", "giọng phụ nữ"]
    ):
        set_default_voice("female")
        return 
    elif any(
        keyword in command
        for keyword in ["giọng nam", "giọng con trai", "giọng đàn ông"]
    ):
        set_default_voice("male")
        return
    # elif "giọng mặc định" in command:
    #     set_default_voice("default")
    #     return
    elif any(
        keyword in command
        for keyword in ["lấy lịch", "xem lịch", "hiển thị lịch", "danh sách sự kiện", "xem sự kiện"]
    ):
        print("Đang lấy danh sách sự kiện...")
        speak(get_calendar_events())
    
    elif any(
        keyword in command
        for keyword in [
            "bây giờ là mấy giờ",
            "mấy giờ rồi",
            "giờ hiện tại",
            "bây giờ đang là mấy giờ",
            "hiện tại đang mấy giờ",
            "hiện tại mấy giờ",
        ]
    ):
        get_current_time()
    elif any(
        keyword in command
        for keyword in ["xóa sự kiện", "gỡ sự kiện", "xóa lịch", "gỡ lịch", "hủy sự kiện"]
    ):
        print("Đang xóa sự kiện...")

        if "vào" in command or "ngày" in command:
            time_to_delete = extract_time_from_command(command)
            if time_to_delete:
                response = delete_event_by_name_or_time(start_time=time_to_delete)
                print(f"Đã xóa sự kiện vào {time_to_delete}.")
            else:
                response = "Không thể xác định thời gian của sự kiện. Vui lòng thử lại."
            speak(response)

        else:
           
            event_name = extract_event_name_from_command(command)
            if event_name:
                response = delete_event_by_name_or_time(summary=event_name)
                print(f"Đã xóa sự kiện '{event_name}'.")
            else:
                response = "Vui lòng cung cấp tên sự kiện bạn muốn xóa."
                speak(response)

        print(response)
        speak(response)
    elif any(
        keyword in command for keyword in ["thêm sự kiện", "tạo sự kiện", "lên sự kiện","thêm lịch", "lên lịch"]
    ):  
        input_for_add_event()  # add_event inside here
        # print("Đang tạo sự kiện mới...")
        # summary = "Họp nhóm dự án"
        # location = "Hồ Chí Minh, Việt Nam"
        # description = "Thảo luận tiến độ dự án."
        # start_time = "2024-11-24T10:00:00+07:00"
        # end_time = "2024-11-24T11:00:00+07:00"
        # add_event(summary, location, description, start_time, end_time)
    # elif "bật cảm biến" in command or "tắt cảm biến" in command:
    #     if "độ ẩm" in command:
    #         if "bật" in command:
    #             set_sensor_status(MOISTURE_FEED, True)
    #         elif "tắt" in command:
    #             set_sensor_status(MOISTURE_FEED, False)
    #     elif "nhiệt độ" in command:
    #         if "bật" in command:
    #             set_sensor_status(TEMPERATURE_FEED, True)
    #         elif "tắt" in command:
    #             set_sensor_status(TEMPERATURE_FEED, False)
    elif "âm lượng" in command or "loa" in command:
        volume_level = re.search(r"\d+", command)
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
    elif any(keyword in command for keyword in ["dừng nhạc", "tắt nhạc"]):
        stop_music()
        # stop_music8()

    elif "kêu" in command or ("tiếng" in command and "kêu" in command):
        play_sound_animal(command)
    elif "kể" in command and ("truyện" in command or "chuyện" in command):
        print("Đang kể truyện...")
        play_story_sound()
    elif any(keyword in command for keyword in ["đường từ", "tìm đường", "chỉ đường", "hướng dẫn đường", "đường đi từ", "hỏi đường"]):
        process_direction(command)
    elif any(
        keyword in command
        for keyword in ["thời tiết", "tin tức", "hôm nay", "hiện nay", "thời sự"]
    ):
        tavily_answer = search_and_summarize(command)
        speak(tavily_answer)
        print(f"Final Answer: {tavily_answer}")
    
    # elif any(
    #     keyword in command
    #     for keyword in [
    #         "căn",
    #         "giai thừa",
    #         "đạo hàm",
    #         "tích phân",
    #         "bình phương",
    #         "phép tính",
    #         "chia",
    #         "nhân",
    #         "cộng",
    #         "trừ",
    #         "hàm số mũ",
    #         "logarit",
    #         "lập phương",
    #         "+",
    #         "/",
    #         "x",
    #     ]
    # ):
    #     try:
    #         result = math_calculation(command)
    #         print(f"Kết quả toán học: {result}")
    #         speak(result)
    #     except Exception as e:
    #         print(f"Lỗi xử lý toán học: {e}")
    #         speak("Xin lỗi, tôi không thể xử lý phép toán này.")
    else:
        print("Gửi yêu cầu đến ChatGPT API...")
        chatgpt_answer = get_response(command)
        print(f"ChatGPT trả lời: {chatgpt_answer}")
        speak(chatgpt_answer)
