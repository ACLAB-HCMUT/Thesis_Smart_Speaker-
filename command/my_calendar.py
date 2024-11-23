import datetime
import os.path
from process import *
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

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

def normalize_time(input_time):
    try:
        # Standardize input (strip whitespace, lowercase)
        input_time = input_time.strip().lower()

        # Patterns for matching various time formats
        patterns = [
            r"^(\d{1,2})\s*giờ\s*(\d{1,2})?\s*phút?$", 
            r"^(\d{1,2}):(\d{1,2})$",                  
            r"^(\d{1,2}):\s*$",                       
            r"^(\d{1,2})$",                     
        ]

        for pattern in patterns:
            match = re.match(pattern, input_time)
            if match:
                hour = int(match.group(1))  # First group is the hour
                minute = int(match.group(2)) if match.lastindex >= 2 and match.group(2) else 0  # Default minute to 0
                if 0 <= hour < 24 and 0 <= minute < 60:  # Validate range
                    return f"{hour:02d}:{minute:02d}:00"

        return None  # Return None if no pattern matches or input is invalid
    except Exception as e:
        print(f"Error: {e}")
        return None

def normalize_date(raw_date): # Chuyển chuỗi ngày tiếng Việt sang định dạng YYYY-MM-DD
    raw_date = raw_date.lower()
    try:
        date_object = datetime.strptime(raw_date, "ngày %d tháng %m năm %Y")
        return date_object.strftime("%Y-%m-%d")
    except ValueError:
        return None

def input_for_add_event():
    speak("Tên lịch là gì ?")
    summary = listen_command()
    if ("Bỏ qua" in summary or "bỏ qua" in summary):
        summary = None
    speak("Ngày nào bắt đầu ?")
    start_day = listen_command()
    if ("Bỏ qua" in start_day or "bỏ qua" in start_day):
        start_day = None
    speak("Bắt đầu mấy giờ ?")
    start_time = listen_command()
    if ("Bỏ qua" in start_time or "bỏ qua" in start_time):
        start_time = None
    speak("Ngày nào kết thúc ?")
    end_day = listen_command()
    if ("Bỏ qua" in end_day or "bỏ qua" in end_day):
        end_day = None
    speak("Kết thúc mấy giờ ?")
    end_time = listen_command()
    if ("Bỏ qua" in end_time or "bỏ qua" in end_time):
        end_time = None
    speak("Địa điểm ở đâu ?")
    location = listen_command()
    if ("Bỏ qua" in location or "bỏ qua" in location):
        location = None
    speak("Ghi chú là gì ?")
    description = listen_command()
    if ("Bỏ qua" in description or "bỏ qua" in description):
        description = None

    while (1):
        speak(f"Lịch của bạn tên là {summary}, tại {location}, với ghi chú {description}, bắt đầu lúc {start_time}:{start_day} và kết thúc lúc {end_time}:{end_day}. Có sai ở đâu không ?")
        confirm_speech = listen_command()

        if ("Đúng" in confirm_speech or "đúng" in confirm_speech or "chính xác" in confirm_speech):
            break
        elif ("Sai" in confirm_speech or "sai" in confirm_speech):
            if ("Tên lịch" in confirm_speech or "tên lịch" in confirm_speech):
                speak("Đọc lại tên lịch")
                summary = listen_command()
            if ("Địa điểm" in confirm_speech or "địa điểm" in confirm_speech):
                speak("Đọc lại địa điểm")
                location = listen_command()
            if ("Ghi chú" in confirm_speech or "ghi chú" in confirm_speech):
                speak("Đọc lại ghi chú")
                location = listen_command()
            if ("Ngày bắt đầu" in confirm_speech or "ngày bắt đầu" in confirm_speech):
                speak("Đọc lại ngày bắt đầu")
                start_day = listen_command()
            if ("Ngày kết thúc" in confirm_speech or "ngày kết thúc" in confirm_speech):
                speak("Đọc lại ngày kết thúc")
                end_day = listen_command()
            if ("Giờ bắt đầu" in confirm_speech or "giờ bắt đầu" in confirm_speech):
                speak("Đọc lại giờ bắt đầu")
                start_time = listen_command()
            if ("Giờ kết thúc" in confirm_speech or "giờ kết thúc" in confirm_speech):
                speak("Đọc lại giờ kết thúc")
                end_time = listen_command()
        else:
            speak("Có lỗi xảy ra. Thử lại")
    
    if start_day is None:
        start_day = normalize_date(start_day)
    if end_day is None:
        end_day = normalize_date(end_day)
    if start_time is None:
        start_time = normalize_time(start_time)
    if end_time is None:
        end_time = normalize_time(end_time)
    speak("Ok, tôi đã lưu lịch. Cảm ơn nhé")
    print(f"Lịch của bạn tên là {summary}, tại {location}, với ghi chú {description}, bắt đầu lúc {start_time}:{start_day} và kết thúc lúc {end_time}:{end_day}")
    # add_event(summary, location, description, start_day, start_time, end_day, end_time)

def add_event(summary, location, description, start_day, start_time, end_day, end_time):
    creds = None
    # Tải token đã lưu nếu có
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
                "dateTime": start_day + "T" + start_time + ":00+07:00", 
                "timeZone": "Asia/Ho_Chi_Minh",
            },
            "end": {
                "dateTime": end_day + "T" + end_time + ":00+07:00",  
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


# get_calendar_events()

# summary = "Họp nhóm dự án"
# location = "Hồ Chí Minh, Việt Nam"
# description = "Thảo luận tiến độ dự án."
# start_time = "2024-11-24T10:00:00+07:00"  
# end_time = "2024-11-24T11:00:00+07:00"    
# add_event(summary, location, description, start_time, end_time)
