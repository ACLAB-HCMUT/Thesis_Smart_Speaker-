from gtts import gTTS
import os


messages = {
    "ask_more": "test",
    
}

for filename, message in messages.items():
    tts = gTTS(text=message, lang='vi')
    tts.save(f"sound/{filename}.mp3")
    print(f"Đã tạo file {filename}.mp3")