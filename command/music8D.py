from yt_dlp import YoutubeDL
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import pygame
import threading
from listen import standalone_listen
from eight_d_audio import EightDAudio

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_youtube8(query):
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
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            print("Không tìm thấy kết quả.")
            return None
    except Exception as e:
        print("Lỗi khi tìm kiếm YouTube:", e)
        return None

current_eight_d_audio = None

def stop_music8():
    global current_eight_d_audio
    if current_eight_d_audio:
        current_eight_d_audio.stop()
        print("Nhạc đã được dừng.")
        current_eight_d_audio = None
    else:
        print("Không có nhạc đang phát.")

def listen_for_stop_command():
    while True:
        command = standalone_listen()
        if command and ("dừng nhạc" in command or "tắt nhạc" in command or "tắt" in command):
            stop_music8()
            break

def delete_old_audio_file():
    audio_temp_file = "audio.webm"
    if os.path.exists(audio_temp_file):
        os.remove(audio_temp_file)
        print(f"Đã xóa file nhạc cũ: {audio_temp_file}")
    audio_part_file = f"audio.webm.part"
    if os.path.exists(audio_part_file):
        os.remove(audio_part_file)
        print(f"Đã xóa file tạm thời: {audio_part_file}")

def download_youtube_audio(video_url, download_path='downloads'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, 'audio.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        audio_file = ydl.prepare_filename(info)
        audio_file = os.path.splitext(audio_file)[0] + '.mp3'
    return audio_file

def download_and_play_youtube_audio8(video_url):
    global current_eight_d_audio
    try:
        delete_old_audio_file()
        download_path = 'downloads'
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        
        audio_file = download_youtube_audio(video_url, download_path=download_path)
        print(f"Đã tải xuống âm thanh: {audio_file}")

        if current_eight_d_audio:
            current_eight_d_audio.stop()
        
        current_eight_d_audio = EightDAudio(audio_file, loops=0, fade_ms=1000, stride=0.5, speed=0.05)
        
        stop_thread = threading.Thread(target=listen_for_stop_command)
        stop_thread.start()
        
    except Exception as e:
        print("Đã xảy ra lỗi:", e)
        current_eight_d_audio = None
