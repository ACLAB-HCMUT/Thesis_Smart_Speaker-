from yt_dlp import YoutubeDL
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import subprocess
from speak import speak
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_youtube(query):
    try:
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=1
        )
        response = request.execute()
        if response["items"]:
            video_id = response["items"][0]["id"]["videoId"]
            video_title = response["items"][0]["snippet"]["title"]
            print(f"Tìm thấy video: {video_title}")
            speak(f"Mời bạn nghe bài hát {video_title}.")
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            print("Không tìm thấy kết quả.")
            return None
    except Exception as e:
        print("Lỗi khi tìm kiếm YouTube:", e)
        return None

music_process = None
audio_temp_file = "audio.webm"
def delete_old_audio_file():
    if os.path.exists(audio_temp_file):
        os.remove(audio_temp_file)
        print(f"Đã xóa file nhạc cũ: {audio_temp_file}")
def download_and_play_youtube_audio(video_url):
    global music_process
    try:
        delete_old_audio_file()
        options = {
            'format': 'bestaudio/best',  
            'outtmpl': 'audio.%(ext)s', 
            'noplaylist': True,          
        }
        
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(video_url, download=True)
            audio_file = ydl.prepare_filename(info)
        
        music_process = subprocess.Popen(["ffplay", "-nodisp", "-autoexit", audio_file])

        music_process.wait()

     
        os.remove(audio_file)
        print("Hoàn tất!")
    except Exception as e:
        print("Đã xảy ra lỗi:", e)
        music_process = None

def stop_music():
    global music_process
    if music_process and music_process.poll() is None:  
        music_process.terminate()
        print("Nhạc đã được dừng.")
        music_process = None
    else:
        print("Không có nhạc đang phát.")
