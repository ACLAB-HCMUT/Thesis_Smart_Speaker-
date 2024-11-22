from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()
account_sid = os.getenv('YOUR_ACCOUNT_SID')
auth_token = os.getenv('YOUR_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def make_call(to_number, from_number, message):
    call = client.calls.create(
        to=to_number,               
        from_=from_number,          
        twiml=f'<Response><Say>{message}</Say></Response>'  
    )
    print(f"Đã thực hiện cuộc gọi, SID: {call.sid}")


make_call("+84914620279", "+12406604160", "Xin chào, đây là cuộc gọi thử nghiệm từ hệ thống loa thông minh.")
