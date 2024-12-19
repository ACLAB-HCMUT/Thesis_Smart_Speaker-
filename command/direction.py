import requests
import os
from dotenv import load_dotenv
import re
from speak import speak
from listen import listen_command
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
            steps=route["legs"][0]["steps"]
            instructions = [step["html_instructions"] for step in steps]
            guide=" "
            for instruction in instructions:
                guide+=instruction
                guide+=" "
            return f"Khoảng cách từ '{origin_full_address}' đến '{destination_full_address}' là {distance}, thời gian di chuyển khoảng {duration}. {guide}"
        else:
            return "Không tìm thấy lộ trình phù hợp."
    else:
        return f"Lỗi API Direction: {response.status_code} - {response.text}"

address_data = {"origin": None, "destination": None}

def process_direction(command):
    global address_data

    pattern = r"từ\s+(.+?)\s+(đến|tới)\s+(.+)"
    match = re.search(pattern, command)

    if match:
        origin_address = match.group(1).strip()
        destination_address = match.group(3).strip()

        address_data["origin"] = origin_address
        address_data["destination"] = destination_address

        print(f"Đang tìm đường từ '{origin_address}' tới '{destination_address}'...")

        try:
            result = get_directions(address_data["origin"], address_data["destination"])
            if result:
                print(result)
                speak(result)
            else:
                response = "Xin lỗi, không tìm thấy đường từ địa chỉ bạn yêu cầu. Vui lòng thử lại."
                print(response)
                speak(response)
        except Exception as e:
            response = "Có lỗi xảy ra khi tìm đường. Vui lòng thử lại sau."
            print(f"Lỗi: {e}")
            speak(response)

    else:
        if not address_data["origin"]:
            response = "Vui lòng cung cấp địa điểm hiện tại của bạn:"
            print(response)
            speak(response)
            address_data["origin"] = listen_command().strip()

        if not address_data["destination"]:
            response = "Vui lòng cung cấp địa điểm đích đến:"
            print(response)
            speak(response)
            address_data["destination"] = listen_command().strip()

        if address_data["origin"] and address_data["destination"]:
            print(f"Đang tìm đường từ '{address_data['origin']}' tới '{address_data['destination']}'...")
            try:
                result = get_directions(address_data["origin"], address_data["destination"])
                if result:
                    print(result)
                    speak(result)
                else:
                    response = "Xin lỗi, không tìm thấy đường từ địa chỉ bạn yêu cầu. Vui lòng thử lại."
                    print(response)
                    speak(response)
            except Exception as e:
                response = "Có lỗi xảy ra khi tìm đường. Vui lòng thử lại sau."
                print(f"Lỗi: {e}")
                speak(response)

# process_direction("Hỏi đường từ trường đại học Bách Khoa TPHCM đến quận 9")
# process_direction("Hỏi đường từ trường đại học Bách Khoa TPHCM tới quận 9")
# process_direction("Hỏi đường tới quận 9")
