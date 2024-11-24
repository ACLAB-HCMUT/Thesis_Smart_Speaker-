from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment

def speak(text):
    try:
        tts = gTTS(text=text, lang='vi')
        tts.save("./command/sound/command.mp3")
        audio = AudioSegment.from_file("./command/sound/command.mp3")
        audio = audio.speedup(playback_speed=1.25)
        audio.export("./command/sound/command.mp3", format="mp3")
        playsound("./command/sound/command.mp3")
    except Exception as e:
        print(f"Lỗi: {e}")
