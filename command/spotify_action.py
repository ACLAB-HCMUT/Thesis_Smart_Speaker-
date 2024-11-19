import aiohttp
import os
import base64
import asyncio
import logging
from aiohttp import web


logging.basicConfig(level=logging.INFO)



client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
redirect_uri =  os.getenv('redirect_uri')



def create_auth_url():
    scope = "user-modify-playback-state"
    auth_url = (
        f"https://accounts.spotify.com/authorize?client_id={client_id}"
        f"&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    )
    return auth_url


async def get_access_token(auth_code):
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = base64.b64encode(auth_string.encode()).decode()
    token_url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": f"Basic {auth_bytes}"}
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(token_url, headers=headers, data=data) as response:
            if response.status == 200:
                token_data = await response.json()
                return token_data.get("access_token")
            else:
                error_text = await response.text()
                print(f"Error obtaining access token: {error_text}")
                return None


async def spotify_action(text: str, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"text": text}
    spotify_url = "https://api.spotify.com/v1/me/player/play"  

    async with aiohttp.ClientSession() as session:
        async with session.put(spotify_url, headers=headers, json=payload) as response:
            if response.status == 204:
                return "Phát nhạc thành công trên Spotify!"
            else:
                content_text = await response.text()
                print(content_text)
                return f"Lỗi khi điều khiển Spotify: {content_text}"


async def handle_callback(request):
    auth_code = request.query.get("code")
    if not auth_code:
        return web.Response(text="Không có mã xác thực!")

    access_token = await get_access_token(auth_code)
    if access_token:
        result = await spotify_action("phát nhạc Joji", access_token)
        return web.Response(text=result)
    else:
        return web.Response(text="Không thể lấy mã truy cập từ Spotify.")


async def main():
    auth_url = create_auth_url()
    print(f"Vui lòng mở URL sau trong trình duyệt để xác thực: {auth_url}")

   
    app = web.Application()
    app.router.add_get("/callback", handle_callback)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 8080)  
    await site.start()

    print("Đang chờ mã xác thực từ Spotify...")
    await asyncio.sleep(3600)  


asyncio.run(main())