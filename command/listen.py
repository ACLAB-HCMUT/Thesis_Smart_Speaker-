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
                command = recognizer.recognize_google(audio, language='vi-VN')
                print(f"Lệnh của bạn: {command}")
                return command.lower()
            except sr.UnknownValueError:
                attempts += 1
                print("Không thể nhận diện được giọng nói.")
                speak("Bạn nói gì tôi nghe không rõ.")
            except sr.WaitTimeoutError:
                attempts += 1
                print("Không nghe thấy giọng nói. Hãy thử lại.")
                speak("Môi trường có vẻ hơi ồn. Hãy thử lại trong một nơi yên tĩnh hơn.")
            except sr.RequestError as e:
                print(f"Không thể yêu cầu dịch vụ Google Speech Recognition; {e}")
                speak("Có vấn đề với dịch vụ nhận diện. Vui lòng kiểm tra kết nối mạng.")
                return None
    speak("Hẹn gặp lại!")
    return None

