from Adafruit_IO import Client, Data
import os
from dotenv import load_dotenv

load_dotenv()
AIO_USERNAME = os.getenv('AIO_USERNAME')
AIO_KEY = os.getenv('AIO_KEY')
aio = Client(AIO_USERNAME, AIO_KEY)

def control_device(action,feed_name): 
    value = "ON" if action == 'on' else "OFF"
    # print("action",action)
    # print("feed_name",feed_name)
    aio.send_data(feed_name, value)
    print(f"Đã gửi lệnh {value} tới feed '{feed_name}'.")


def control_volume(payload):
    try:
        volume = int(payload)
        os.system(f"amixer sset 'Master' {volume}%")
        print(f"Volume set to {volume}%")
    except ValueError:
        print("Invalid volume value received")


def set_volume(volume_level):
    feed_name = 'volume'
    aio.send_data(feed_name, volume_level)  
    control_volume(volume_level)  

# set_volume(70)