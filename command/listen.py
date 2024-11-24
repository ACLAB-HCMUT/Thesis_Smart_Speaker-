import speech_recognition as sr
from speak import *

def listen_command(max_attempts=2):
    recognizer = sr.Recognizer()
    attempts = 0
    while attempts < max_attempts:
        with sr.Microphone() as source:
            print("Listening........................")
            recognizer.adjust_for_ambient_noise(source, duration=1)  
            try:
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=7)
                command = recognizer.recognize_google(audio, language="vi-VN")
                print(f"Lệnh của bạn: {command}")
                return command.lower()
            except sr.UnknownValueError:
                attempts += 1
                print("Không thể nhận diện được giọng nói.")
                playsound("./command/sound/listen_error.mp3")
            except sr.WaitTimeoutError:
                attempts += 1
                print("Không nghe thấy giọng nói. Hãy thử lại.")
                playsound("./command/sound/noise_error.mp3")
            except sr.RequestError as e:
                print(f"Không thể yêu cầu dịch vụ Google Speech Recognition; {e}")
                playsound("./command/sound/network_error.mp3")
                return None
    playsound("./command/sound/see_again.mp3")
    return None
