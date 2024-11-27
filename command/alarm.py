import re
from datetime import datetime, timedelta
import os
sound_file_path = "/home/pi/Desktop/Thesis_Smart_Speaker/command/sound/alarm.wav"
def add_alarm_to_cron(minute, hour, day, month, comment=None):
    if not comment:
        comment = f"Báo thức {hour}:{minute} - {day}/{month}"
    
    cron_command = f'{minute} {hour} {day} {month} * DISPLAY=:0 XDG_RUNTIME_DIR=/run/user/\$(id -u) /usr/bin/aplay {sound_file_path}' # # comment
    os.system(f'(crontab -l; echo "{cron_command}") | crontab -')
    return f"Báo thức đã được thêm vào với tên '{comment}'."

def remove_alarm_from_cron(comment=None):
    if not comment:
        os.system("crontab -r")  
        return "Tất cả báo thức đã bị xóa."
    else:
        os.system(f'crontab -l | grep -v "# {comment}" | crontab -')
        return f"Báo thức với tên '{comment}' đã được xóa."

def list_alarms_from_cron():
    try:
        result = os.popen("crontab -l").read()
        if not result.strip():
            return "Hiện không có báo thức nào."
        alarms = [line for line in result.split('\n') if "aplay" in line]
        if not alarms:
            return "Hiện không có báo thức nào."
        return "Danh sách báo thức:\n" + "\n".join(alarms)
    except Exception as e:
        return f"Lỗi khi liệt kê báo thức: {e}"

def parse_time_expression(time_expression):
    now = datetime.now()
    if re.match(r'\d+:\d+', time_expression):  
        hour, minute = map(int, time_expression.split(':'))
        return minute, hour, now.day, now.month
    elif re.match(r'\d+\s*phút', time_expression):  
        minutes = int(re.search(r'\d+', time_expression).group())
        future_time = now + timedelta(minutes=minutes)
        return future_time.minute, future_time.hour, future_time.day, future_time.month
    elif re.match(r'\d+\s*giờ', time_expression):  
        hours = int(re.search(r'\d+', time_expression).group())
        future_time = now + timedelta(hours=hours)
        return future_time.minute, future_time.hour, future_time.day, future_time.month
    else:
        raise ValueError("Thời gian không hợp lệ.")

def alarm_reminder_action(text):
    if re.search(r'\b(xem|danh sách|hiện tại)\s+báo\s+thức\b', text, re.IGNORECASE):
        return list_alarms_from_cron()
    set_match = re.search(
        r'\b(?:đặt|tạo|lên lịch|báo thức|đánh thức tôi|hẹn giờ)\b.*?\b(?:lúc|trong|sau)?\s*(\d{1,2}:\d{2}|\d+\s*(?:phút|giờ))\b',
        text, re.IGNORECASE
    )
    delete_match = re.search(
        r'\b(?:xóa|hủy)\s+(?:một\s+)?báo\s+thức\b.*?\b(?:tên|gọi\s+là)?\s*([\w\s:-]+)?',
        text, re.IGNORECASE
    )
    delete_all_match = re.search(
    r'\b(?:xóa|hủy)\s+tất\s+cả\s+báo\s+thức\b', 
    text, re.IGNORECASE
    )
    if set_match:
        time_expression = set_match.group(1)
        try:
            minute, hour, day, month = parse_time_expression(time_expression)
            return add_alarm_to_cron(minute, hour, day, month)
        except ValueError:
            return "Thời gian báo thức không hợp lệ. Vui lòng kiểm tra lại."
    elif delete_all_match:
        return remove_alarm_from_cron()
    elif delete_match:
        comment = delete_match.group(1)
        if not comment.strip():
            return "Vui lòng cung cấp tên của báo thức cần xóa."
        return remove_alarm_from_cron(comment)
    else:
        return "Không nhận diện được yêu cầu. Vui lòng thử lại."
