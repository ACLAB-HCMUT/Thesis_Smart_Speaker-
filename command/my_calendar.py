import datetime
import os
import re
from datetime import timezone, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from audio_utils import speak
from listen import listen_command
from fuzzywuzzy import fuzz # type: ignore
SCOPES = ["https://www.googleapis.com/auth/calendar"]
def normalize_date(raw_date):
    raw_date = raw_date.lower().strip()
    try:
        match = re.match(r"ngày (\d{1,2}) tháng (\d{1,2}) năm (\d{4})", raw_date)
        if match:
            day, month, year = match.groups()
           
            print(f"Extracted Date: Day={day}, Month={month}, Year={year}")
          
            date_object = datetime.datetime(year=int(year), month=int(month), day=int(day))
            return date_object.strftime("%Y-%m-%d")
        print(f"No match for raw_date: {raw_date}")
        return None
    except Exception as e:
        print(f"Error in normalize_date: {e}")
        return None

def normalize_time(input_time):
    try:
        input_time = input_time.strip().lower()
        print(f"Input time: {input_time}") 
    
        if "đúng" in input_time:
            input_time = input_time.replace("đúng", "").strip()  
        
        if "giờ sáng" in input_time or "sáng" in input_time:
            hour = int(re.search(r"(\d{1,2})", input_time).group(1))
            if hour == 12:  
                hour = 0
            return f"{hour:02d}:00:00"
        
        if "giờ chiều" in input_time or "chiều" in input_time:
            hour = int(re.search(r"(\d{1,2})", input_time).group(1))
            if hour < 12:  
                hour += 12
            return f"{hour:02d}:00:00"
        
        if "rưỡi" in input_time:
            hour_match = re.match(r"(\d{1,2})\s*giờ", input_time)
            if hour_match:
                hour = int(hour_match.group(1))
                return f"{hour:02d}:30:00"  
        
        match = re.match(r"^(\d{1,2})\s*giờ\s*(\d{1,2})?\s*phút?$", input_time)
        if match:
            hour = int(match.group(1))  
            minute = int(match.group(2)) if match.lastindex >= 2 and match.group(2) else 0  # Default minute to 0
            return f"{hour:02d}:{minute:02d}:00"
        
        match = re.match(r"^(\d{1,2})\s*giờ$", input_time)
        if match:
            hour = int(match.group(1))
            return f"{hour:02d}:00:00"
        
        match = re.match(r"^(\d{1,2})\s*giờ\s*(\d{1,2})$", input_time)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            return f"{hour:02d}:{minute:02d}:00"
        
       
        match = re.match(r"^(\d{1,2}):(\d{1,2})$", input_time)
        if match:
            hour = int(match.group(1))  
            minute = int(match.group(2)) 
            return f"{hour:02d}:{minute:02d}:00"

        print(f"No match for input_time: {input_time}")
        return None

    except Exception as e:
        print(f"Error in normalize_time: {e}")
        return None

def normalize_datetime(date, time):
    if date and time:
        print(f"Normalizing datetime: {date}T{time}+07:00")
        return f"{date}T{time}+07:00"
    print(f"Invalid datetime: date={date}, time={time}")
    return None

def add_event(summary, location, description, start_time, end_time):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time, 
                "timeZone": "Asia/Ho_Chi_Minh",
            },
            "end": {
                "dateTime": end_time,  
                "timeZone": "Asia/Ho_Chi_Minh",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},  
                    {"method": "popup", "minutes": 10},  
                ],
            },
        }

        event_result = service.events().insert(calendarId="primary", body=event).execute()

        print(f"Đã tạo sự kiện thành công: {event_result.get('htmlLink')}")

    except HttpError as error:
        print(f"Đã xảy ra lỗi: {error}")


def input_for_add_event():
    
    

    while (1):
        speak("tiêu đề là gì ạ")
        summary = listen_command()
        if ("Bỏ qua" in summary or "bỏ qua" in summary):
            summary = None
        speak("Ngày nào bắt đầu ạ")
        start_day = listen_command()
        if ("Bỏ qua" in start_day or "bỏ qua" in start_day):
            start_day = None
        speak("Ngày kết thúc ạ")
        end_day = listen_command()
        if ("Bỏ qua" in end_day or "bỏ qua" in end_day):
            end_day = None
        speak("Bắt đầu mấy giờ ạ")
        start_time = listen_command()
        if ("Bỏ qua" in start_time or "bỏ qua" in start_time):
            start_time = None
        speak("Kết thúc mấy giờ ạ")
        end_time = listen_command()
        if ("Bỏ qua" in end_time or "bỏ qua" in end_time):
            end_time = None
        speak("Địa điểm ở đâu ạ")
        location = listen_command()
        if ("Bỏ qua" in location or "bỏ qua" in location):
            location = None
        description = "Lịch được tạo bởi trợ lý ảo Aya"
        if start_time is None or end_time is None:
            speak("Xin vui lòng cung cấp thời gian bắt đầu và kết thúc hợp lệ.")
            return
    
        speak(f"Lịch của bạn tên là {summary}, tại {location}, với ghi chú {description}, bắt đầu lúc {start_time}:{start_day} và kết thúc lúc {end_time}:{end_day}. Có sai ở đâu không ?")
        confirm_speech = listen_command()

        if ("Đúng" in confirm_speech or "đúng" in confirm_speech or "chính xác" in confirm_speech):
            break
        else:
            continue
    if start_day:
        start_day = normalize_date(start_day)
    if end_day:
        end_day = normalize_date(end_day)
    if start_time:
        start_time = normalize_time(start_time)
    if end_time:
        end_time = normalize_time(end_time)

    start_datetime = normalize_datetime(start_day, start_time)
    end_datetime = normalize_datetime(end_day, end_time)

    print("----start_time:", start_datetime)
    print("endtime____________-", end_datetime)
    if start_datetime and end_datetime:
        print(f"Lịch của bạn tên là {summary}, tại {location}, với ghi chú {description}, bắt đầu lúc {start_datetime} và kết thúc lúc {end_datetime}")
        add_event(summary, location, description, start_datetime, end_datetime)
    else:
        print("Có lỗi xảy ra, không thể lưu lịch.")

# input_for_add_event()
# print(get_calendar_events())

# summary = "Họp nhóm dự án"
# location = "Hồ Chí Minh, Việt Nam"
# description = "Thảo luận tiến độ dự án."
# start_time = "2024-11-24T10:00:00+07:00"  
# end_time = "2024-11-24T11:00:00+07:00"    
# add_event(summary, location, description, start_time, end_time)
# update_event_by_name_or_time(
#     summary="Họp nhóm dự án", 
#     new_summary="Họp nhóm cải tiến dự án", 
#     new_location="Phòng họp tầng 2", 
#     new_description="Thảo luận cải tiến quy trình.", 
#     new_start_time="2024-11-25T14:00:00+07:00", 
#     new_end_time="2024-11-25T15:00:00+07:00"
# )

def get_calendar_events():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        print("Đang lấy sự kiện sắp tới...")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return "Bạn không có sự kiện nào trong lịch sắp tới."
        result = "Danh sách sự kiện sắp tới:\n"
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event["summary"]
            result += f"- Vào lúc {start}, sự kiện: {summary}\n"
        return result.strip()

    except HttpError as error:
        print(f"Đã xảy ra lỗi: {error}")
        print("Tôi không thể lấy thông tin lịch. Vui lòng thử lại sau.")

def delete_event_by_name_or_time(summary=None, start_time=None):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=50,  
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        event_to_delete = None
        for event in events:
            event_summary = event.get("summary", "")
            event_start = event["start"].get("dateTime", event["start"].get("date"))
            
            # Sử dụng khớp chính xác hoặc so sánh mờ (fuzzy matching)
            if summary and summary.lower() == event_summary.lower():
                event_to_delete = event
                break
            if summary and fuzz.ratio(summary.lower(), event_summary.lower()) > 80:  # So sánh mờ với ngưỡng 80%
                event_to_delete = event
                break

        if not event_to_delete:
            print("Không tìm thấy sự kiện phù hợp để xóa.")
            return "Không tìm thấy sự kiện phù hợp để xóa."
        
        event_id = event_to_delete["id"]
        
        # Ghi lại sự kiện trước khi xóa để kiểm tra
        print(f"Sự kiện trước khi xóa: {event_to_delete.get('summary')}, ID: {event_id}")

        # Thực hiện xóa sự kiện
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        
        # Kiểm tra lại tất cả các sự kiện
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=50,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        events = events_result.get("items", [])
        event_deleted = True
        for event in events:
            if event['id'] == event_id:
                event_deleted = False
                break

        if event_deleted:
            print(f"Sự kiện đã bị xóa thành công: {event_to_delete.get('summary')}")
            return f"Sự kiện {event_to_delete.get('summary')} đã bị xóa thành công."
        else:
            print(f"Sự kiện vẫn còn tồn tại: {event_to_delete.get('summary')}")
            return f"Sự kiện {event_to_delete.get('summary')} vẫn còn tồn tại."

    except HttpError as error:
        print(f"Đã xảy ra lỗi khi xóa sự kiện: {error}")
        return f"Đã xảy ra lỗi khi xóa sự kiện: {error}"
def update_event_by_name_or_time(summary=None, start_time=None, new_summary=None, new_location=None, new_description=None, new_start_time=None, new_end_time=None):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=50,  
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        event_to_update = None
        for event in events:
            event_summary = event.get("summary", "")
            event_start = event["start"].get("dateTime", event["start"].get("date"))
            
            if summary and summary.lower() in event_summary.lower():
                event_to_update = event
                break
            if start_time and start_time in event_start:
                event_to_update = event
                break

        if not event_to_update:
            print("Không tìm thấy sự kiện phù hợp để cập nhật.")
            return

        event_id = event_to_update["id"]
        updated_event = event_to_update

        if new_summary:
            updated_event["summary"] = new_summary
        if new_location:
            updated_event["location"] = new_location
        if new_description:
            updated_event["description"] = new_description
        if new_start_time and new_end_time:
            updated_event["start"]["dateTime"] = new_start_time
            updated_event["end"]["dateTime"] = new_end_time

        updated_result = service.events().update(calendarId="primary", eventId=event_id, body=updated_event).execute()
        print(f"Đã cập nhật sự kiện thành công: {updated_result.get('htmlLink')}")

    except HttpError as error:
        print(f"Đã xảy ra lỗi khi cập nhật sự kiện: {error}")

def extract_time_from_command(command):
    match = re.search(r"\b(\d{1,2})\s*(tháng|day)?\s*(\d{1,2})\s*(năm|year)?\s*(\d{4})\b", command)
    if match:
        day = int(match.group(1))
        month = int(match.group(3))
        year = int(match.group(5))
       
        date_time_str = f"{year}-{month:02d}-{day:02d}T00:00:00+07:00"
        return date_time_str
    return None


def extract_event_name_from_command(command):
    keywords = ["họp nhóm", "hội thảo", "bữa tiệc", "cuộc họp", "sự kiện"]
    for keyword in keywords:
        if keyword in command:
            return keyword 
    return None
