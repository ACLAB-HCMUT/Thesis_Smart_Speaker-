import re
from datetime import datetime, timedelta
import os
import pytz
sound_file_path = "/home/johnny/capstone11/Thesis_Smart_Speaker/command/sound/alarm.wav"
def add_alarm_to_cron(minute, hour, day, month, comment=None):
    if not comment:
        comment = f"Báo thức {hour}:{minute} - {day}/{month}"
    
    cron_command = f'{minute} {hour} {day} {month} * DISPLAY=:0 XDG_RUNTIME_DIR=/run/user/\$(id -u) /usr/bin/aplay {sound_file_path}' # # comment
    os.system(f'(crontab -l; echo "{cron_command}") | crontab -')
    return f"Báo thức đã được thêm vào với tên 'Báo thức {hour}:{minute} phút - Ngày {day} tháng {month}'."
def stop_alarm_sound():
    os.system("pkill -f aplay")

def remove_alarm_from_cron(comment=None):
    if not comment:
        stop_alarm_sound()
        os.system("crontab -r")  
        return "Tất cả báo thức đã bị xóa."
    else:
        stop_alarm_sound()
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
    # now = datetime.now()
    tz = pytz.timezone('Asia/Ho_Chi_Minh')  # Thay đổi múi giờ nếu cần
    now = datetime.now(tz)
    
    print("Thời gian hiện tại:", now)
    print("Time expression nhận được:", time_expression)
    time_expression = time_expression.lower().replace("đúng", "").strip()
    time_expression = time_expression.lower().replace("đúng", "").replace("nữa", "").strip()
    print("Time expression nhận được:", time_expression)
    if re.match(r'(\d{1,2})\s*giờ\s*(\d{1,2})\s*phút', time_expression):  
        match = re.search(r'(\d{1,2})\s*giờ\s*(\d{1,2})\s*phút', time_expression)
        hour = int(match.group(1))
        minute = int(match.group(2))
        print(f"DEBUG - Khớp định dạng giờ và phút: hour = {hour}, minute = {minute}")
        return minute, hour, now.day, now.month
    # Kiểm tra trường hợp "hh:mm"
    # Kiểm tra trường hợp giờ và phút không có từ "phút"
    elif re.match(r'(\d{1,2})\s*giờ\s*(\d{1,2})$', time_expression):  # Xử lý "22 giờ 10"
        match = re.search(r'(\d{1,2})\s*giờ\s*(\d{1,2})$', time_expression)
        hour = int(match.group(1))
        minute = int(match.group(2))
        print(f"DEBUG - Khớp định dạng giờ và phút không có từ 'phút': hour = {hour}, minute = {minute}")
        return minute, hour, now.day, now.month
    elif re.match(r'^(\d{1,2})\s*giờ(\s*đúng)?$', time_expression):
        hour = int(re.search(r'(\d{1,2})', time_expression).group())
        print(f"DEBUG - Khớp định dạng giờ đúng: hour = {hour}, minute = 0")
        return 0, hour, now.day, now.month
    elif re.match(r'(\d{1,2}):(\d{2})', time_expression):  
        hour, minute = map(int, re.findall(r'(\d{1,2}):(\d{2})', time_expression)[0])
        return minute, hour, now.day, now.month

    # Kiểm tra trường hợp "phút"
    elif re.match(r'(\d+)\s*phút', time_expression):  
        minutes = int(re.search(r'(\d+)', time_expression).group())
        future_time = now + timedelta(minutes=minutes)
        return future_time.minute, future_time.hour, future_time.day, future_time.month
    
    # Kiểm tra trường hợp "giờ"
    elif re.match(r'(\d+)\s*giờ', time_expression):  
        hours = int(re.search(r'(\d+)', time_expression).group())
        future_time = now + timedelta(hours=hours)
        return future_time.minute, future_time.hour, future_time.day, future_time.month
    
    # Kiểm tra trường hợp giờ là "0 giờ"
    elif re.match(r'0\s*giờ\s*(\d+)\s*phút', time_expression):  # Xử lý "0 giờ 43 phút"
        minutes = int(re.search(r'(\d+)', time_expression).group())
        return minutes, 0, now.day, now.month
    
    else:
        raise ValueError("Thời gian không hợp lệ.")

def alarm_reminder_action(text):
    print("checkpoint:  ",text)
    if re.search(r'\b(xem|danh sách|hiện tại)\s+báo\s+thức\b', text, re.IGNORECASE):
        return list_alarms_from_cron()
    set_match = re.search(
        r'\b(?:đặt|tạo|lên lịch|báo thức|đánh thức tôi|hẹn giờ)\b.*?\b(?:lúc|trong|sau)?\s*(\d{1,2}\s*giờ\s*\d{1,2}|\d{1,2}\s*giờ|\d+\s*phút(?:\s*nữa)?)',
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
    turn_off_alarm_match = re.search(r'\b(tắt|dừng|hủy|hủy bỏ|tắt)\s+báo\s+thức\b', text, re.IGNORECASE)
    if set_match:
        time_expression = set_match.group(1)
        try:
            minute, hour, day, month = parse_time_expression(time_expression)
            print("minute: ",minute,"hour: ", hour, "day: ", day,"month: ", month)
            return add_alarm_to_cron(minute, hour, day, month)
        except ValueError:
            return "Thời gian báo thức không hợp lệ. Vui lòng kiểm tra lại."
    elif turn_off_alarm_match:
        return remove_alarm_from_cron()
    elif delete_all_match:
        return remove_alarm_from_cron()
    elif delete_match:
        comment = delete_match.group(1)
        if not comment.strip():
            return "Vui lòng cung cấp tên của báo thức cần xóa."
        return remove_alarm_from_cron(comment)
    else:
        return "Không nhận diện được yêu cầu. Vui lòng thử lại."


# alarm_reminder_action("đặt báo thức 22 giờ 10")
# alarm_reminder_action("đặt báo thức 1 phút nữa")
# alarm_reminder_action("đặt báo thức 22 giờ 10 phút")
# alarm_reminder_action("đặt báo thức 22 giờ đúng")
# alarm_reminder_action("đặt báo thức 22 giờ 0 phút")
# alarm_reminder_action("đặt báo thức 7 giờ 10")
# alarm_reminder_action("đặt báo thức 7 giờ 00")



# alarm_reminder_action("đặt báo thức 0 giờ 60")

