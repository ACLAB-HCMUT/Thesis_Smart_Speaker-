from Adafruit_IO import Client, Data
import os
from dotenv import load_dotenv

load_dotenv()
AIO_USERNAME = os.getenv('AIO_USERNAME')
AIO_KEY = os.getenv('AIO_KEY')
aio = Client(AIO_USERNAME, AIO_KEY)

# control light 
def control_light(action):
    feed_name = 'led'  
    value = "ON" if action == 'on' else "OFF"
    aio.send_data(feed_name, value)
    print(f"Đã gửi lệnh {value} tới feed '{feed_name}'.")