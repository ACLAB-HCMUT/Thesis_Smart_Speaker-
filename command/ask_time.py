from datetime import datetime
from speak import speak
def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")  
    response = f"Bây giờ là {current_time}."
    print(response)
    speak(response)
