import time
from speak import speak
def get_current_time():
    current_time = time.strftime("%H:%M", time.localtime())
    response = f"Bây giờ là {current_time}."
    print(response)
    speak(response)
