import time
from datetime import datetime
from audio_utils import speak
def get_current_time():
    current_time = time.strftime("%H:%M", time.localtime())
    response = f"Bây giờ là {current_time}."
    print(response)
    speak(response)

def get_current_date_vn_format():
    current_date = datetime.now()
    vn_format = current_date.strftime("Hôm nay là ngày %d tháng %m năm %Y")

    return vn_format
