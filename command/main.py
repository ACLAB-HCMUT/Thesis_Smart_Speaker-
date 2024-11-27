import random
import sys
import os
sys.path.append(os.path.dirname(__file__))
from process import *
from notification import monitor_temperature, monitor_moisture
from listen import listen_command
from playsound import playsound
WELCOME_SOUND="sound/welcome.mp3"
def main():
	end_keywords_pattern = re.compile(r"\b(hết rồi|hết|kết|kết thúc|cảm ơn|thanks|thank you)\b", re.IGNORECASE)
	greetings = ["Em nghe", "Dạ", "Có em", "Vâng, em nghe"]
	follow_up_questions = [
        "Bạn cần gì thêm ạ?",
        "Tôi có thể giúp gì nữa ạ?",
    ]

	playsound(WELCOME_SOUND)
	# monitor_temperature()
	# monitor_moisture()
	greeting = random.choice(greetings)
	speak(greeting)
	while True:
		command = listen_command()
		if command is None:
			print("Terminated due to failure to recognize speech.")
			break
		command= command.lower()
		if end_keywords_pattern.search(command):
			speak("Dạ vâng ạ")
			print(f"End-----------------")
			break
		else:
			end_program=process_command(command)
			if end_program == 1:
				break
			follow_up = random.choice(follow_up_questions)
			print(follow_up)
			speak(follow_up)

if __name__ == "__main__":
    main()
