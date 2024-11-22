import datetime
import os.path
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

def add_event(summary, location, description, start_time, end_time):
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


# get_calendar_events()

# summary = "Họp nhóm dự án"
# location = "Hồ Chí Minh, Việt Nam"
# description = "Thảo luận tiến độ dự án."
# start_time = "2024-11-24T10:00:00+07:00"  
# end_time = "2024-11-24T11:00:00+07:00"    
# add_event(summary, location, description, start_time, end_time)
