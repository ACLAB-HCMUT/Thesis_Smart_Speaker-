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

def normalize_time(hour, minute):
    additional_hours = minute // 60
    minute = minute % 60
    hour += additional_hours
    hour = hour % 24  
    return hour, minute

def remove_alarm_from_cron(comment=None):
    print("tat bao thuc------------------")
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
    time_expression = time_expression.lower().strip()
    # Kiểm tra trường hợp "x tiếng y phút nữa"
    # Kiểm tra xem có chứa "ngày mai" không
    is_tomorrow = False
    is_tomorrow2 = False
    if 'ngày mai' in time_expression:
        is_tomorrow = True
        # Loại bỏ "ngày mai" khỏi biểu thức để xử lý phần thời gian
        time_expression = time_expression.replace("ngày mai", "").strip()
        is_tomorrow = False
    elif 'ngày mốt' in time_expression:
        is_tomorrow2 = True
        # Loại bỏ "ngày mốt" khỏi biểu thức để xử lý phần thời gian
        time_expression = time_expression.replace("ngày mốt", "").strip()
    match = re.match(r'(\d{1,2})\s*tiếng\s*(\d{1,2})\s*phút\s*nữa', time_expression)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        future_time = now + timedelta(hours=hours, minutes=minutes)
        print(f"DEBUG - Khớp định dạng 'tiếng phút nữa': hours = {hours}, minutes = {minutes}")
        return future_time.minute, future_time.hour, future_time.day, future_time.month
    # Kiểm tra trường hợp "1 tiếng nữa"
    match = re.match(r'(\d{1,2})\s*tiếng\s*nữa', time_expression)
    if match:
        hours = int(match.group(1))
        future_time = now + timedelta(hours=hours)
        print(f"DEBUG - Khớp định dạng 'tiếng nữa': hours = {hours}")
        return future_time.minute, future_time.hour, future_time.day, future_time.month
    match = re.match(r'(\d{1,2})\s*giờ\s*(\d{1,2})\s*phút\s*nữa', time_expression)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        future_time = now + timedelta(hours=hours, minutes=minutes)
        print(f"DEBUG - Khớp định dạng 'giờ phút nữa': hours = {hours}, minutes = {minutes}")
        return future_time.minute, future_time.hour, future_time.day, future_time.month
    # *Thêm kiểm tra cho trường hợp "x giờ nữa"*
    match = re.match(r'(\d{1,2})\s*giờ\s*nữa', time_expression)
    if match:
        hours = int(match.group(1))
        future_time = now + timedelta(hours=hours)
        print(f"DEBUG - Khớp định dạng 'giờ nữa': hours = {hours}")
        return future_time.minute, future_time.hour, future_time.day, future_time.month

    # Thay thế "tiếng" bằng "giờ" cho các trường hợp khác
    time_expression = time_expression.replace("tiếng", "giờ")
    
    # Loại bỏ từ "đúng" và "nữa" nếu còn
    time_expression = time_expression.replace("đúng", "").replace("nữa", "").strip()
    print("Time expression sau khi xử lý:", time_expression)
 
    print("Time expression nhận được:", time_expression)
    if re.match(r'(\d{1,2})\s*giờ\s*(\d{1,2})\s*phút', time_expression):  
        match = re.search(r'(\d{1,2})\s*giờ\s*(\d{1,2})\s*phút', time_expression)
        hour = int(match.group(1))
        minute = int(match.group(2))
        hour, minute = normalize_time(hour, minute)
        print(f"DEBUG - Khớp định dạng giờ và phút: hour = {hour}, minute = {minute}")
        
        return minute, hour, now.day, now.month
    # Kiểm tra trường hợp "hh:mm"
    # Kiểm tra trường hợp giờ và phút không có từ "phút"
    elif re.match(r'(\d{1,2})\s*giờ\s*(\d{1,2})$', time_expression):  # Xử lý "22 giờ 10"
        match = re.search(r'(\d{1,2})\s*giờ\s*(\d{1,2})$', time_expression)
        hour = int(match.group(1))
        minute = int(match.group(2))
        hour, minute = normalize_time(hour, minute)
        print(f"DEBUG - Khớp định dạng giờ và phút không có từ 'phút': hour = {hour}, minute = {minute}")
        # Xác định ngày và tháng
        day = now.day
        month = now.month
        year = now.year
        
        if is_tomorrow:
            future_date = now + timedelta(days=1)
            day = future_date.day
            month = future_date.month
            year = future_date.year
            print("DEBUG - Đặt báo thức cho ngày mai:", future_date)
        elif is_tomorrow2:
            future_date = now + timedelta(days=2)
            day = future_date.day
            month = future_date.month
            year = future_date.year
            print("DEBUG - Đặt báo thức cho ngày mốt:", future_date)
        else:
            # Kiểm tra nếu thời gian đã qua trong ngày hôm nay, có thể tự động đặt cho ngày mai
            if hour < now.hour or (hour == now.hour and minute <= now.minute):
                future_date = now + timedelta(days=1)
                day = future_date.day
                month = future_date.month
                year = future_date.year
                print("DEBUG - Đặt báo thức cho ngày mai vì thời gian đã qua:", future_date)
        return minute, hour, day, month
    elif re.match(r'^(\d{1,2})\s*giờ(\s*đúng)?$', time_expression):
        hour = int(re.search(r'(\d{1,2})', time_expression).group())
        minute=0
        hour, minute = normalize_time(hour, minute)
        print(f"DEBUG - Khớp định dạng giờ đúng: hour = {hour}, minute = 0")
        # Xác định ngày và tháng
        day = now.day
        month = now.month
        year = now.year
        
        if is_tomorrow:
            future_date = now + timedelta(days=1)
            day = future_date.day
            month = future_date.month
            year = future_date.year
            print("DEBUG - Đặt báo thức cho ngày mai:", future_date)
        elif is_tomorrow2:
            future_date = now + timedelta(days=2)
            day = future_date.day
            month = future_date.month
            year = future_date.year
            print("DEBUG - Đặt báo thức cho ngày mốt:", future_date)
        else:
            # Kiểm tra nếu thời gian đã qua trong ngày hôm nay, có thể tự động đặt cho ngày mai
            if hour < now.hour or (hour == now.hour and minute <= now.minute):
                future_date = now + timedelta(days=1)
                day = future_date.day
                month = future_date.month
                year = future_date.year
                print("DEBUG - Đặt báo thức cho ngày mai vì thời gian đã qua:", future_date)
        return 0, hour, day, month
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
        hour, minute = normalize_time(hour, minute)
        return minutes, 0, now.day, now.month
    
    else:
        raise ValueError("Thời gian không hợp lệ.")

def alarm_reminder_action(text):
    print("checkpoint:  ",text)
    if re.search(r'\b(xem|danh sách|hiện tại)\s+báo\s+thức\b', text, re.IGNORECASE):
        return list_alarms_from_cron()
    # set_match = re.search(
    #     r'\b(?:đặt|tạo|lên lịch|báo thức|đánh thức tôi|hẹn giờ)\b.*?\b(?:lúc|trong|sau)?\s*' +
    #     r'(' +
    #         r'\d{1,2}\s*tiếng\s*\d{1,2}\s*phút\s*nữa|' +  # "x tiếng y phút nữa"
    #         r'\d{1,2}\s*giờ\s*\d{1,2}\s*phút\s*nữa|' +   # "x giờ y phút nữa"
    #         r'\d{1,2}\s*tiếng\s*nữa|' +                  # "x tiếng nữa"
    #         r'\d{1,2}\s*giờ\s*nữa|' +                    # "x giờ nữa"
    #         r'giờ\s*này|' +                               # "giờ này"
    #         r'\d{1,2}\s*giờ\s*đúng|' +                    # "x giờ đúng"
    #         r'\d{1,2}\s*giờ\s*\d{1,2}|' +                 # "x giờ y"
    #         r'\d+\s*phút(?:\s*nữa)?|' +                  # "x phút" hoặc "x phút nữa"
    #         r'\d+:\d+' +                                  # "hh:mm"
    #     r')',
    #     text, re.IGNORECASE
    # )
    set_match = re.search(
        r'\b(?:đặt|tạo|lên lịch|báo thức|đánh thức tôi|hẹn giờ)\b.*?\b(?:lúc|trong|sau)?\s*' +
        r'(' +
            r'\d{1,2}\s*tiếng\s*\d{1,2}\s*phút\s*nữa|' +  # "x tiếng y phút nữa"
            r'\d{1,2}\s*giờ\s*\d{1,2}\s*phút\s*nữa|' +   # "x giờ y phút nữa"
            r'\d{1,2}\s*tiếng\s*nữa|' +                  # "x tiếng nữa"
            r'\d{1,2}\s*giờ\s*nữa|' +                    # "x giờ nữa"
            r'giờ\s*này|' +                               # "giờ này"
            r'\d{1,2}\s*giờ(?:\s*đúng)?|' +                  # "x giờ đúng"
            r'\d{1,2}\s*giờ\s*\d{1,2}|' +                 # "x giờ y"
            r'\d+\s*phút(?:\s*nữa)?|' +                  # "x phút" hoặc "x phút nữa"
            r'\d+:\d+' +                                  # "hh:mm"
            r'|' +
            r'ngày\s+mai' +                               # Thêm "ngày mai"
        r')',
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
            # print("minute: ",minute,"hour: ", hour, "day: ", day,"month: ", month)
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
# list_alarms_from_cron()
# remove_alarm_from_cron()
# list_alarms_from_cron()

# alarm_reminder_action("đặt báo thức 22 giờ 10 phút")
# alarm_reminder_action("đặt báo thức 22 giờ đúng ngày mai")
# alarm_reminder_action("đặt báo thức 22 giờ 0 phút")
# alarm_reminder_action("đặt báo thức 7 giờ 10")
# alarm_reminder_action("đặt báo thức 7 giờ 00")
# alarm_reminder_action("đặt báo thức 1 tiếng nữa")

# alarm_reminder_action("đặt báo thức 1 giờ nữa")
# alarm_reminder_action("đặt báo thức 1 giờ 10 phút nữa")
# alarm_reminder_action("đặt báo thức sau 1 phút nữa")
# alarm_reminder_action("đặt báo thức sau 1 giờ nữa")
# alarm_reminder_action("đặt báo thức sau 1 phút ")
# alarm_reminder_action("đặt báo thức sau 1 giờ")
# alarm_reminder_action("đặt báo thức sau 1 giờ 10 phút")

# alarm_reminder_action("đặt báo thức 1 tiếng 10 phút nữa")

# alarm_reminder_action("đặt báo thức 10 giờ 62")

# alarm_reminder_action("đặt báo thức 22 giờ 10 phút ngày mai")
# alarm_reminder_action("đặt báo thức 7 giờ ")
# alarm_reminder_action("đặt báo thức 0 giờ ")
