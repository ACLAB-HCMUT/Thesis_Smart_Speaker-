import requests
import json
import os
from control import control_device
from dotenv import load_dotenv
# from speak import speak
load_dotenv()
API_KEY = os.getenv('API_FT_KEY')
adafruit_base_url = "https://io.adafruit.com/api/feeds"

action_on = "1001"  # Bật
action_off = "1000"  # Tắt
light_code = "4103"  # Đèn
fan_code = "4203"  # Quạt
living_room_code = "7106"  # Phòng khách
bedroom_code = "7206"  
sub_light_code = "4104"

api_key = API_KEY

url = "https://api.openai.com/v1/chat/completions"

def control(command):

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "ft:gpt-3.5-turbo-0125:personal::AcE70vZT",
        "messages": [
            {"role": "user", "content": f"{command}"}],
        "max_tokens": 100
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    actions = []
    devices = []
    locations = []

    if response.status_code == 200:
        response_data = response.json()
        
        if 'choices' in response_data and len(response_data['choices']) > 0:
            content = response_data['choices'][0]['message']['content']
            print("-----------------------------------response:",content )
            try:
                action = content.split(';')[0].split(':')[1].strip()
                device = content.split(';')[1].split(':')[1].strip()
                location = content.split(';')[2].split(':')[1].strip()

           
                actions=action.split(',') 
                devices=device.split(',')
                locations=location.split(',')

                
                print(f"Actions array: {actions}")
                print(f"Devices array: {devices}")
                print(f"Locations array: {locations}")
            except IndexError as e:
                print(f"Error processing response content: {e}")
                return 0  
            
            for i in range(max(len(actions), len(devices), len(locations))):
                
                current_action = actions[i] if i < len(actions) else actions[0]
                current_device = devices[i] if i < len(devices) else devices[0]
                current_location = locations[i] if i < len(locations) else locations[0]

                if current_action == action_on:
                    action_value = "on"
                elif current_action == action_off:
                    action_value = "off"
                else:
                    print(f"Invalid action: {current_action}")
                    return 0
                    continue  
                
                
                if current_device == light_code:
                    if current_location == living_room_code:
                        device_code = "living-room.main-light"
                    elif current_location == bedroom_code:
                        device_code = "bedroom.main-light"
                    else:
                        print("Invalid location for light.")
                        return 0
                        continue
                    
                elif current_device == sub_light_code:  
                    if current_location == living_room_code:
                        device_code = "living-room.sub-light" 
                    elif current_location == bedroom_code:
                        device_code = "bedroom.sub-light"  
                    else:
                        print("Invalid location for sub-light.")
                        return 0
                        continue        

                elif current_device == fan_code:
                    if current_location == living_room_code:
                        device_code = "living-room.fan"
                    elif current_location == bedroom_code:
                        device_code = "bedroom.fan"
                    else:
                        print("Invalid location for fan.")
                        return 0
                        continue
                else:
                    print("Invalid device code.")
                    return 0
                    continue
                print("-----------------")
                print(device_code)
                print(action_value)
                control_device(action_value,device_code)
            # speak("Em đã thực hiện lệnh ạ.")
            return 1
        else:
            return 0
            print("Không có dữ liệu phản hồi hợp lệ.")

    else:
        return 0
        print(f"Lỗi khi gửi yêu cầu: {response.status_code}")


# print(control("tắt đèn phòng khách"))