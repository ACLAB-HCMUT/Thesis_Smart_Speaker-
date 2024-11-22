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
TEMPERATURE_FEED = "temp"
TEMPERATURE_MIN = 22  
TEMPERATURE_MAX = 26  
HUMIDITY_MIN = 40  
HUMIDITY_MAX = 60  
last_moisture_notification_time = None
last_temperature_notification_time = None
notification_cooldown = timedelta(minutes=30)

def read_feed(feed_key):
    try:
        data = aio.receive(feed_key)
        value = data.value.strip()
        print(f"Giá trị nhận từ feed {feed_key}: {value}")

        if value.upper() == "OFF":
            print(f"Cảm biến {feed_key} đang tắt.")
            return None  

        if value.upper() == "ON":
            print(f"Cảm biến {feed_key} đang bật, nhưng chưa có giá trị thực.")
            return None

        return float(value)
    except Exception as e:
        print(f"Lỗi khi đọc dữ liệu từ feed {feed_key}: {e}")
        return None

def set_sensor_status(feed_key, is_on):
    try:
        value = "ON" if is_on else "OFF"
        aio.send_data(feed_key, value)
        print(f"Đã cập nhật trạng thái cảm biến {feed_key}: {'BẬT' if is_on else 'TẮT'}.")
        speak(f"Cảm biến {feed_key} đã được {'bật' if is_on else 'tắt'}.")
    except Exception as e:
        print(f"Lỗi khi cập nhật trạng thái cảm biến {feed_key}: {e}")

def notify(message):
    print(message)
    speak(message)

def monitor_moisture():
    global last_moisture_notification_time

    moisture_value = read_feed(MOISTURE_FEED)

    if moisture_value is None:
        return

    if moisture_value < HUMIDITY_MIN:
        current_time = datetime.now()
        if not last_moisture_notification_time or (current_time - last_moisture_notification_time > notification_cooldown):
            notify(f"Cảnh báo! Độ ẩm trong phòng thấp hơn ngưỡng lý tưởng: {moisture_value}%. Vui lòng điều chỉnh.")
            last_moisture_notification_time = current_time
    elif moisture_value > HUMIDITY_MAX:
        current_time = datetime.now()
        if not last_moisture_notification_time or (current_time - last_moisture_notification_time > notification_cooldown):
            notify(f"Cảnh báo! Độ ẩm trong phòng cao hơn ngưỡng lý tưởng: {moisture_value}%. Vui lòng điều chỉnh.")
            last_moisture_notification_time = current_time
    else:
        print(f"Độ ẩm phòng ổn định: {moisture_value}%.")
        last_moisture_notification_time = None

def monitor_temperature():
    global last_temperature_notification_time

    temperature_value = read_feed(TEMPERATURE_FEED)

    if temperature_value is None:
        return

    if temperature_value < TEMPERATURE_MIN:
        current_time = datetime.now()
        if not last_temperature_notification_time or (current_time - last_temperature_notification_time > notification_cooldown):
            notify(f"Cảnh báo! Nhiệt độ trong phòng thấp hơn ngưỡng lý tưởng: {temperature_value}°C. Vui lòng điều chỉnh.")
            last_temperature_notification_time = current_time
    elif temperature_value > TEMPERATURE_MAX:
        current_time = datetime.now()
        if not last_temperature_notification_time or (current_time - last_temperature_notification_time > notification_cooldown):
            notify(f"Cảnh báo! Nhiệt độ trong phòng cao hơn ngưỡng lý tưởng: {temperature_value}°C. Vui lòng điều chỉnh.")
            last_temperature_notification_time = current_time
    else:
        print(f"Nhiệt độ phòng ổn định: {temperature_value}°C.")
        last_temperature_notification_time = None
