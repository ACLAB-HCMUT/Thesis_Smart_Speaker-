from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_youtube(query):
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
        print(f"Found video: {video_title}")
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        print("No results found.")
        return None


def play_youtube_video(video_url):
    print(f"Playing: {video_url}")
    os.system(f"xdg-open {video_url}")
if __name__ == "__main__":
    search_query = "Joji - NITROUS"
    video_url = search_youtube(search_query)
    if video_url:
        play_youtube_video(video_url)
