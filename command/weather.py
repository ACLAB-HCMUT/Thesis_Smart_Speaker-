import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_KEY")
LAT = 10.8231
LON = 106.6297


def fetch_weather_data():
    if not API_KEY:
        raise ValueError("API Key is not set. Please check your .env file.")

    weather_api_url = (
        f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang=vi"
    )

    try:
        response = requests.get(weather_api_url)
        response.raise_for_status()  

        weather_data = response.json()

        city_name = weather_data.get('name', 'Không rõ')
        country = weather_data['sys'].get('country', 'Không rõ')
        temp = weather_data['main'].get('temp', 'Không rõ')
        feels_like = weather_data['main'].get('feels_like', 'Không rõ')
        weather_description = weather_data['weather'][0].get('description', 'Không rõ')
        humidity = weather_data['main'].get('humidity', 'Không rõ')
        wind_speed = weather_data['wind'].get('speed', 'Không rõ')

        weather_info = f"Thời tiết hôm nay Nhiệt độ: {temp}°C "
        weather_info += f"Cảm giác như: {feels_like}°C "
        weather_info += f"Mô tả: {weather_description} "
        weather_info += f"Độ ẩm: {humidity}% "
        weather_info += f"Tốc độ gió: {wind_speed} m/s "

        return weather_info

    except requests.exceptions.RequestException as e:
        return f"Lỗi khi lấy dữ liệu thời tiết: {e}"

# if __name__ == "__main__":
#     weather_info = fetch_weather_data()
#     print(weather_info)
