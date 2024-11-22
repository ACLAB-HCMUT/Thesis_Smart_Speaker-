from Adafruit_IO import Client, Data
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from speak import speak

load_dotenv()
AIO_USERNAME = os.getenv("AIO_USERNAME")
AIO_KEY = os.getenv("AIO_KEY")
aio = Client(AIO_USERNAME, AIO_KEY)

MOISTURE_FEED = "mois"
LOW_MOISTURE_THRESHOLD = 100  

last_notified_time = None
notification_cooldown = timedelta(minutes=30)

def read_moisture():
    try:
        moisture_data = aio.receive(MOISTURE_FEED)
        value = moisture_data.value.strip()
        print(f"Giá trị nhận từ feed: {value}")

        if value.upper() == "OFF":
            print("Cảm biến đang tắt.")
            return None  

        if value.upper() == "ON":
            print("Cảm biến đang bật, nhưng chưa có giá trị độ ẩm thực.")
            return None
        return float(value)
    except Exception as e:
        print(f"Lỗi khi đọc dữ liệu độ ẩm: {e}")
        return None

def set_sensor_status(is_on):
    try:
        value = "ON" if is_on else "OFF"
        aio.send_data(MOISTURE_FEED, value)
        print(f"Đã cập nhật trạng thái cảm biến: {'BẬT' if is_on else 'TẮT'}.")
        speak(f"Cảm biến đã được {'bật' if is_on else 'tắt'}.")
    except Exception as e:
        print(f"Lỗi khi cập nhật trạng thái cảm biến: {e}")

def notify_low_moisture():
    print("Độ ẩm thấp hơn ngưỡng cho phép!")
    speak("Cảnh báo! Độ ẩm trong phòng thấp. Vui lòng kiểm tra.")

def monitor_moisture():
    global last_notified_time

    moisture_value = read_moisture()

    if moisture_value is None:
        return

    if moisture_value < LOW_MOISTURE_THRESHOLD:
        current_time = datetime.now()
        if not last_notified_time or (current_time - last_notified_time > notification_cooldown):
            notify_low_moisture()
            last_notified_time = current_time
    else:
        last_notified_time = None


# monitor_moisture()

# set_sensor_status(True)