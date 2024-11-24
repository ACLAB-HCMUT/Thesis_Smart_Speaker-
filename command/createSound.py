from gtts import gTTS
from pydub import AudioSegment

messages = {
    "see_again": "Hẹn gặp lại!",
}

for filename, message in messages.items():
   
    tts = gTTS(text=message, lang="vi")
    tts.save(f"./command/sound/{filename}.mp3")  
    
   
    audio = AudioSegment.from_file(f"./command/sound/{filename}.mp3")
    audio = audio.speedup(playback_speed=1.25)  
    audio.export(f"./command/sound/{filename}.mp3", format="mp3")  
    
    print(f"Đã tạo file {filename}.mp3 với tốc độ 1.15")
