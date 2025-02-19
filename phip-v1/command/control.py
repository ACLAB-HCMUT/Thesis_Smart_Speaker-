from Adafruit_IO import Client
import os
from dotenv import load_dotenv
from httpx import RequestError

load_dotenv()
AIO_USERNAME = os.getenv("AIO_USERNAME")
AIO_KEY = os.getenv("AIO_KEY")
try:
    aio = Client(AIO_USERNAME, AIO_KEY)
    print("Đã kết nối thành công với Adafruit IO.")
except Exception as e:
    print(f"Lỗi khi kết nối với Adafruit IO: {e}")
    raise



def control_device(action,feed_name): 
    value = 1 if action == 'on' else 0
    try:
        aio.send_data(feed_name, value)
        print(f"Đã gửi lệnh {value} tới feed '{feed_name}'.")
    except RequestError as e:
        print(f"Lỗi khi gửi dữ liệu đến feed '{feed_name}': {e}")
    except Exception as e:
        print(f"Lỗi không mong muốn: {e}")


def control_volume(payload):
    try:
        volume = int(payload)
        os.system(f"amixer sset 'Master' {volume}%")
        print(f"Volume set to {volume}%")
    except ValueError:
        print("Invalid volume value received")


def set_volume(volume_level):
    feed_name = "speaker.volume"
    try:
        aio.send_data(feed_name, volume_level)
        print(f"Đã gửi mức âm lượng {volume_level} tới feed '{feed_name}'.")
    except RequestError as e:
        print(f"Lỗi khi gửi mức âm lượng đến feed '{feed_name}': {e}")
    except Exception as e:
        print(f"Lỗi không mong muốn: {e}")
