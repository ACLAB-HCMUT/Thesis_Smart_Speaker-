import requests
import os
from dotenv import load_dotenv
load_dotenv()
API_MAP_KEY = os.getenv('API_MAP_KEY')

def autocomplete_place(input_text, location=None, radius=50000):
  
    url = "https://rsapi.goong.io/Place/AutoComplete"
    params = {
        "input": input_text,
        "api_key": API_MAP_KEY,
        "radius": radius,  
    }
    if location:
        params["location"] = location  
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "predictions" in data and data["predictions"]:
            return data["predictions"][0]["description"]
        else:
            return None
    else:
        print(f"Lỗi API Autocomplete: {response.status_code} - {response.text}")
        return None

def get_coordinates(address):
    """
    Convert an address to coordinates using Goong Geocoding API.
    """
    url = "https://rsapi.goong.io/geocode"
    params = {
        "address": address,
        "api_key": API_MAP_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and data["results"]:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            return None, None  
    else:
        print(f"Lỗi API Geocoding: {response.status_code} - {response.text}")
        return None, None  

def get_directions(origin_address, destination_address, location=None, vehicle="car"):
    origin_full_address = autocomplete_place(origin_address, location=location)
    if not origin_full_address:
        return f"Không tìm thấy địa chỉ phù hợp cho '{origin_address}'."

    destination_full_address = autocomplete_place(destination_address, location=location)
    if not destination_full_address:
        return f"Không tìm thấy địa chỉ phù hợp cho '{destination_address}'."
    
    origin_lat, origin_lng = get_coordinates(origin_full_address)
    if origin_lat is None or origin_lng is None:
        return f"Không tìm thấy tọa độ cho địa chỉ gốc: '{origin_full_address}'."

    destination_lat, destination_lng = get_coordinates(destination_full_address)
    if destination_lat is None or destination_lng is None:
        return f"Không tìm thấy tọa độ cho địa chỉ đích: '{destination_full_address}'."
    
    origin = f"{origin_lat},{origin_lng}"
    destination = f"{destination_lat},{destination_lng}"
    
    url = "https://rsapi.goong.io/Direction"
    params = {
        "origin": origin,
        "destination": destination,
        "vehicle": vehicle,
        "api_key": API_MAP_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "routes" in data and data["routes"]:
            route = data["routes"][0]
            distance = route["legs"][0]["distance"]["text"]
            duration = route["legs"][0]["duration"]["text"]
            return f"Khoảng cách từ '{origin_full_address}' đến '{destination_full_address}' là {distance}, thời gian di chuyển khoảng {duration}."
        else:
            return "Không tìm thấy lộ trình phù hợp."
    else:
        return f"Lỗi API Direction: {response.status_code} - {response.text}"

# if _name_ == "_main_":
#     origin_address = "Đại học Bách Khoa Hồ​ Chí Minh quận 10"
#     destination_address = "Kí túc xá khu B đại học quốc gia tp.hcm"
    
   
#     result = get_directions(origin_address, destination_address)
#     print(result)
