import sqlite3
from process import *
# import re
# from control import *
# from chatgpt import *
# from gtts import gTTS
# from playsound import playsound
# import speech_recognition as sr

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

# SETUP FOR LOCAL CALENDAR
conn = sqlite3.connect("calendar_events.db")
cursor = conn.cursor()
#cursor.execute("DROP TABLE IF EXISTS events")
cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	event_name TEXT NOT NULL,
	date TEXT NOT NULL,		-- Store date as YYYY-MM-DD
	start_time TEXT NOT NULL,		-- Store start_time as HH:MM
	stop_time TEXT NOT NULL,		-- Store stop_time as HH:MM
	location TEXT,
	description TEXT
)
""")
conn.commit()
print("Database and table setup complete.")

#SET UP FOR GOOGLE CALENDAR
# def authenticate_google_calendar():
#     """Authenticate with Google Calendar API."""
#     creds = None
#     # Token file to store access/refresh tokens
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If no valid credentials, log in again
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save credentials for next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#     return build('calendar', 'v3', credentials=creds)

# def speak(text):
# 	tts = gTTS(text=text, lang='vi')
# 	tts.save("./sound/command.mp3")
# 	playsound("./sound/command.mp3")

# 	# audio = AudioSegment.from_file("command.mp3")
# 	# audio = audio.speedup(playback_speed=1.1)
# 	# audio.export("command.mp3", format="mp3")
# 	# audio_segment = AudioSegment.from_file("command.mp3")  
# 	# pydub_play(silence + audio_segment)

# def listen_command():
# 	recognizer = sr.Recognizer()
# 	with sr.Microphone() as source:
# 		print("Đang lắng nghe...")
# 		audio = recognizer.listen(source, timeout=5)
# 		try:
# 			vitext = recognizer.recognize_google(audio, language='vi-VN')
# 			return vitext.lower()
# 			# vitext = recognizer.recognize_google(audio, language='vi-VN')
# 			# if len(entext) > len(vitext):
# 			# 	print(f"Your command: {entext}")
# 			# 	return entext.lower()
# 			# elif len(vitext) > len(entext):
# 			# 	print(f"Lệnh của bạn: {vitext}")
# 			# 	return vitext.lower()
# 		except sr.UnknownValueError:
# 			print("Không thể nhận diện được giọng nói.")
# 			speak("Bạn nói gì tôi nghe không rõ.")
# 			return None
# 		except sr.RequestError as e:
# 			print(f"Không thể yêu cầu dịch vụ Google Speech Recognition; {e}")
# 			return None

def process_of_add_event():
	speak("Lịch mới của bạn tên gì ?")
	event_name = listen_command()
	print(f"{event_name}")
	confirm_flag = 0
	while (confirm_flag != 1):
		speak(f"Lịch mới của bạn tên là {event_name}, đúng hay sai ?")
		confirm_speech = listen_command()
		print(f"{confirm_speech}")

		if ("Đúng" in confirm_speech or "đúng" in confirm_speech or "chính xác" in confirm_speech):
			confirm_flag = 1
		else: # apply for case true but speed don't reconize exactly and case false
			confirm_flag = 0

		if confirm_flag == 1:
			break
		else:
			speak("Bạn đọc lại tên lịch nhé !")
			event_name = listen_command()
			print(f"{event_name}")
	speak("Ok. Lịch này ngày tháng năm nào vậy ?")

	date = listen_command()
	print(f"{date}")
	confirm_flag = 0
	while (confirm_flag != 1):
		speak(f"Ngày của lịch là {date}, đúng hay sai ?")
		confirm_speech = listen_command()
		print(f"{confirm_speech}")

		if ("Đúng" in confirm_speech or "đúng" in confirm_speech or "chính xác" in confirm_speech):
			confirm_flag = 1
		else:
			confirm_flag = 0

		if confirm_flag == 1:
			break
		else:
			speak("Bạn đọc lại ngày tháng năm lịch nhé !")
			date = listen_command()
			print(f"{date}")
	speak("Ok. Khi nào lịch bắt đầu ?")

	start_time = listen_command()
	print(f"{start_time}")
	confirm_flag = 0
	while (confirm_flag != 1):
		speak(f"Lịch bắt đầu lúc {start_time}, đúng hay sai ?")
		confirm_speech = listen_command()
		print(f"{confirm_speech}")

		if ("Đúng" in confirm_speech or "đúng" in confirm_speech or "chính xác" in confirm_speech):
			confirm_flag = 1
		else:
			confirm_flag = 0

		if confirm_flag == 1:
			break
		else:
			speak("Bạn đọc lại thời gian bắt đầu nhé !")
			start_time = listen_command()
			print(f"{start_time}")
	speak("Ok. Khi nào lịch kết thúc ?")

	stop_time = listen_command()
	print(f"{stop_time}")
	confirm_flag = 0
	while (confirm_flag != 1):
		speak(f"Lịch kết thúc lúc {stop_time}, đúng hay sai ?")
		confirm_speech = listen_command()
		print(f"{confirm_speech}")

		if ("Đúng" in confirm_speech or "đúng" in confirm_speech or "chính xác" in confirm_speech):
			confirm_flag = 1
		else:
			confirm_flag = 0

		if confirm_flag == 1:
			break
		else:
			speak("Bạn đọc lại thời gian kết thúc nhé !")
			stop_time = listen_command()
			print(f"{stop_time}")
	speak("Ok. Địa điểm diễn ra mục lịch này ở đâu ?")

	location = listen_command()
	print(f"{location}")
	confirm_flag = 0
	while (confirm_flag != 1):
		speak(f"Địa điểm là ở {location}, đúng hay sai ?")
		confirm_speech = listen_command()
		print(f"{confirm_speech}")

		if ("Đúng" in confirm_speech or "đúng" in confirm_speech or "chính xác" in confirm_speech):
			confirm_flag = 1
		else:
			confirm_flag = 0

		if confirm_flag == 1:
			break
		else:
			speak("Bạn nói lại địa điểm nhé !")
			location = listen_command()
			print(f"{location}")
	speak("Ok. Có chú thích hay lưu ý gì không ?")

	description = listen_command()
	print(f"{description}")
	confirm_flag = 0
	while (confirm_flag != 1):
		speak(f"Chú thích của lịch là {description}, đúng hay sai ?")
		confirm_speech = listen_command()
		print(f"{confirm_speech}")
		if ("Đúng" in confirm_speech or "đúng" in confirm_speech or "chính xác" in confirm_speech):
			confirm_flag = 1
		else:
			confirm_flag = 0

		if confirm_flag == 1:
			break
		else:
			speak("Bạn đọc lại chú thích nhé !")
			description = listen_command()
			print(f"{description}")
	speak("Ok, tôi đã lưu lịch. Cảm ơn nhé")

	add_event(event_name, date, start_time, stop_time, location, description)
	retrieve_events(date)
	#delete_event(event_name, date, start_time)

def add_event(event_name, date, start_time, stop_time, location, description):
	cursor.execute("""SELECT * FROM events WHERE event_name = ? AND date = ? AND start_time = ? AND stop_time = ? AND location = ? AND description = ?""", (event_name, date, start_time, stop_time, location, description))

	if cursor.fetchone() is None:
		cursor.execute("INSERT INTO events (event_name, date, start_time, stop_time, location, description) VALUES (?,?,?,?,?,?)", (event_name, date, start_time, stop_time, location, description))
		conn.commit()
		print(f"Event {event_name} added to calendar.")
	else:
		print(f"Event {event_name} already exists in the calendar.")
	# """Add an event to Google Calendar."""
	# event = {
    #     'summary': name,
    #     'location': location,
    #     'description': description,
    #     'start': {
    #         'dateTime': f"{date}T{start_time}:00",
    #         'timeZone': 'UTC',  # Adjust timezone as needed
    #     },
    #     'end': {
    #         'dateTime': f"{date}T{stop_time}:00",
    #         'timeZone': 'UTC',  # Adjust timezone as needed
    #     },
    # }
	# created_event = service.events().insert(calendarId='primary', body=event).execute()
	# print(f"Event created: {created_event['htmlLink']}")
	# return created_event

def get_event(date):
	cursor.execute("SELECT * FROM events WHERE date = ?", (date,))
	events = cursor.fetchall()
	if events:
		for event in events:
			print(f"Event: {event[1]}, Start Time: {event[3]}, Stop Time: {event[4]}, Location: {event[5]}, Description: {event[6]}")
	else:
		print("No events found for that date.")
	# """Retrieve events. Optionally filter by a specific date."""
	# events_result = service.events().list(
    #     calendarId='primary',
    #     timeMin=f"{date}T00:00:00Z" if date else None,  # Start of the day
    #     timeMax=f"{date}T23:59:59Z" if date else None,  # End of the day
    #     maxResults=max_results,
    #     singleEvents=True,
    #     orderBy='startTime'
    # ).execute()
    
	# events = events_result.get('items', [])
	# if not events:
	# 	print("No events found.")
	# 	return []
	# for event in events:
	# 	start = event['start'].get('dateTime', event['start'].get('date'))
	# 	print(f"{start} - {event['summary']}")
	# return events

def edit_event(event_name, new_name=None, new_date=None, new_start_time=None, new_stop_time=None, new_location=None, new_description=None):
	cursor.execute("SELECT * FROM events WHERE event_name = ?", (event_name,))
	event = cursor.fetchone()

	if not event:
		print(f"Event {event_name} not found.")
		return

	updated_name = new_name if new_name else event[1]
	updated_date = new_date if new_date else event[2]
	updated_start_time = new_start_time if new_start_time else event[3]
	updated_stop_time = new_stop_time if new_stop_time else event[4]
	updated_location = new_location if new_location else event [5]
	updated_description = new_description if new_description else event[6]

	if updated_name == event[1] and updated_date == event[2] and updated_start_time == event[3] and updated_stop_time == event[4] and updated_location == event[5] and updated_description == event[6]:
		print(f"Event {event[1]} already exists in the calendar.")
		return
	else:
		cursor.execute("DELETE FROM events WHERE event_name = ?", (event_name,))

		cursor.execute("""
			UPDATE events
			SET event_name = ?, date = ?, start_time = ?, stop_time = ?, location = ?, description = ?""", (updated_name, updated_date, updated_start_time, updated_stop_time, updated_location, updated_description))
		conn.commit()
		print("Event updated.")
	# """
    # Edit an event by updating its fields.
    # `updates` is a dictionary containing fields to update.
    # Example: {'summary': 'New Name', 'location': 'New Location'}
    # """
	# try:
	# 	event = service.events().get(calendarId='primary', eventId=event_id).execute()
	# 	for key, value in updates.items():
	# 		event[key] = value
	# 	updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
	# 	print(f"Event updated: {updated_event['htmlLink']}")
	# 	return updated_event
	# except Exception as e:
	# 	print(f"Error occurred: {e}")

def delete_event(event_name, date, start_time):
	cursor.execute("SELECT * FROM events WHERE event_name = ? AND date = ? AND start_time = ?", (event_name, date, start_time))
	event = cursor.fetchone()
	if not event:
		print(f"Event {event_name} already deleted from calendar.")
		return
	else:
		cursor.execute("DELETE FROM events WHERE event_name = ? AND date = ? AND start_time = ?", (event_name, date, start_time))
		conn.commit()
		print(f"Event {event_name} deleted from calendar.")
	# """Delete an event by its event ID."""
	# try:
	# 	service.events().delete(calendarId='primary', eventId=event_id).execute()
	# 	print("Event deleted.")
	# except Exception as e:
	# 	print(f"Error occurred: {e}")

def main():
# 	service = authenticate_google_calendar()
# 	add_event(service, name="Team Meeting", date="2024-11-02", start_time="14:00", stop_time="15:00", location="Zoom",description="Discuss project updates.") 
# 	get_events(service, date="2024-11-02")
# 	edit_event(service, event_id="event-id-from-google-calendar",
# 	updates={
#         'summary': 'Updated Meeting Name',
#         'location': 'New Zoom Link'
#     }
# )
# 	delete_event(service, event_id="event-id-from-google-calendar")
	process_of_add_event()
	# add_event("Party tonight", "2023-10-04", "13:27", "14:00", "Friend's House", "None")
	# add_event("Do exercise", "2024-12-15", "12:44", "14:44", "House", "None")
	# retrieve_events("2024-12-15")
	# retrieve_events("2023-10-04")
	# delete_event("Do exercise", "2024-12-15", "12:44")
if __name__== "__main__":
	main()