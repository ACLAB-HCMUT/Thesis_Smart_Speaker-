import googlemaps

API_KEY = "" 
gmaps = googlemaps.Client(key=API_KEY)

def get_directions(origin, destination):
    try:
       
        directions_result = gmaps.directions(
            origin=origin,
            destination=destination,
            mode="driving",  # Các chế độ: "walking", "bicycling", "transit"
            departure_time="now"
        )

        if not directions_result:
            return "Không tìm thấy lộ trình phù hợp."

       
        route = directions_result[0]["legs"][0]
        distance = route["distance"]["text"] 
        duration = route["duration"]["text"] 
        steps = route["steps"]

        directions = "\n".join(step["html_instructions"] for step in steps)
        result = (
            f"Lộ trình từ {origin} đến {destination} dài {distance}, "
            f"mất khoảng {duration}. Các bước đi:\n{directions}"
        )
        return result

    except Exception as e:
        return f"Đã xảy ra lỗi khi lấy lộ trình: {e}"

origin = "Hồ Chí Minh"
destination = "Hà Nội"

result = get_directions(origin, destination)
print(result)
