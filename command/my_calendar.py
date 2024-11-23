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
            
            if summary and summary.lower() in event_summary.lower():
                event_to_delete = event
                break
            if start_time and start_time in event_start:
                event_to_delete = event
                break

        if not event_to_delete:
            print("Không tìm thấy sự kiện phù hợp để xóa.")
            return "Không tìm thấy sự kiện phù hợp để xóa."
        
        event_id = event_to_delete["id"]
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print(f"Đã xóa sự kiện: {event_to_delete.get('summary')} thành công.")
        return f"Đã xóa sự kiện: {event_to_delete.get('summary')} thành công."

    except HttpError as error:
        print(f"Đã xảy ra lỗi khi xóa sự kiện: {error}")

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

# print(get_calendar_events())
# delete_event_by_name_or_time(summary="Họp nhóm dự án")
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
