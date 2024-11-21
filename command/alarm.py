import re
from datetime import datetime, timedelta
from threading import Timer, Thread
import subprocess
from listen import *

alarms = {}
active_alarm_thread = None  

def play_alarm_sound():
    global active_alarm_thread
    try:
        process = subprocess.Popen(["aplay", "sound/alarm.wav"])
        active_alarm_thread = process
        process.wait()
    except Exception as e:
        print(f"Lỗi khi phát âm thanh: {e}")

def set_alarm(minute, hour, day_of_month, month, comment=None):
    now = datetime.now()
    alarm_time = now.replace(minute=minute, hour=hour, day=day_of_month, month=month, second=0, microsecond=0)

    if alarm_time < now:
        alarm_time += timedelta(days=1)

    delay = (alarm_time - now).total_seconds()

    if not comment:
        comment = alarm_time.strftime("%Y-%m-%d %H:%M")
    
    def alarm_trigger():
        print(f"Báo thức '{comment}' đang kêu!")
        sound_thread = Thread(target=play_alarm_sound)
        sound_thread.start()

        while True:
            user_input = listen_command()
            if "tắt" in user_input or "dừng" in user_input:
                stop_active_alarm()
                break

    timer = Timer(delay, alarm_trigger)
    timer.start()
    alarms[comment] = timer  
    return f"Báo thức đã được đặt cho {alarm_time.strftime('%Y-%m-%d %H:%M')} với tên '{comment}'."

def delete_alarm(comment=None):
    global alarms
    if comment is None:  
        for timer in alarms.values():
            timer.cancel()  
        alarms.clear()  
        return "Tất cả báo thức đã được xóa."
    else:
        comment = comment.strip()
        if comment in alarms:
            alarms[comment].cancel()  
            del alarms[comment]  
            return f"Báo thức '{comment}' đã được xóa."
        else:
            return f"Không tìm thấy báo thức '{comment}'."


def stop_active_alarm():
    global active_alarm_thread
    if active_alarm_thread:
        active_alarm_thread.terminate()
        active_alarm_thread = None
        print("Báo thức đã được tắt.")
    else:
        print("Không có báo thức nào đang kêu.")

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
    set_match = re.search(
        r'\b(?:đặt|tạo|lên lịch|báo thức|đánh thức tôi|hẹn giờ)\b.*?\b(?:lúc|trong|sau)?\s*(\d{1,2}:\d{2}|\d+\s*(?:phút|giờ))\b',        text, 
        re.IGNORECASE
    )
    delete_match = re.search(
        r'\b(?:xóa|hủy)\s+(?:một\s+)?báo\s+thức\b.*?\b(?:tên|gọi\s+là)?\s*([\w\s:-]+)?', 
        text, 
        re.IGNORECASE
    )
    stop_match = re.search(
        r'\b(?:tắt|dừng)\s+báo\s+thức\b', 
        text, 
        re.IGNORECASE
    )
    if set_match:
        time_expression = set_match.group(1)
        minute, hour, day, month = parse_time_expression(time_expression)
        return set_alarm(minute, hour, day, month)

    elif delete_match:
        comment = delete_match.group(1)
        return delete_alarm(comment)

    elif stop_match:
        return stop_active_alarm()

    else:
        return "Không nhận diện được yêu cầu. Vui lòng thử lại."
