from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment
from google.cloud import texttospeech
import os
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

def load_google_credentials():
   
    credentials_path = os.path.join(os.getcwd(), "my_key.json")
    
   
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Không tìm thấy file credentials tại: {credentials_path}")
    
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    print(f"Đã load credentials từ: {credentials_path}")

def speak_female(text):
    load_google_credentials()
    try:
        client = texttospeech.TextToSpeechClient()

        input_text = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="vi-VN",  
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE  
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3  
        )

        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
       
        output_file = "sound/output.mp3"
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        print(f"Giọng nói đã được lưu vào file: {output_file}")

        playsound(output_file)

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

def speak_male(text):
    load_google_credentials()  
    try:
        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="vi-VN",  
            name="vi-VN-Standard-B",  
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3  
        )
        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        output_file = "sound/output.mp3"
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        print(f"Giọng nói đã được lưu vào file: {output_file}")

        playsound(output_file)

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")


# Ngôn ngữ: ['vi-VN']
# SSML Gender: FEMALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Neural2-D
# Ngôn ngữ: ['vi-VN']
# SSML Gender: MALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Standard-A
# Ngôn ngữ: ['vi-VN']
# SSML Gender: FEMALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Standard-B
# Ngôn ngữ: ['vi-VN']
# SSML Gender: MALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Standard-C
# Ngôn ngữ: ['vi-VN']
# SSML Gender: FEMALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Standard-D
# Ngôn ngữ: ['vi-VN']
# SSML Gender: MALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Wavenet-A
# Ngôn ngữ: ['vi-VN']
# SSML Gender: FEMALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Wavenet-B
# Ngôn ngữ: ['vi-VN']
# SSML Gender: MALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Wavenet-C
# Ngôn ngữ: ['vi-VN']
# SSML Gender: FEMALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Wavenet-D
# Ngôn ngữ: ['vi-VN']
# SSML Gender: MALE
# Tần số mẫu: 24000
