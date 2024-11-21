import re

def is_device_command(command):
    actions = ["bật", "mở", "tắt", "đóng", "tăng", "giảm", "điều chỉnh", "chỉnh"]
    rooms = ["phòng khách", "phòng ngủ", "phòng bếp", "phòng làm việc"]
    devices = ["đèn", "cửa", "máy lạnh"]
    
    # regex
    action_pattern = r'\b(' + '|'.join(actions) + r')\b'
    room_pattern = r'\b(' + '|'.join(rooms) + r')\b'
    device_pattern = r'\b(' + '|'.join(devices) + r')\b'
    
    
    return bool(re.search(action_pattern, command)) or \
           bool(re.search(room_pattern, command)) or \
           bool(re.search(device_pattern, command))
