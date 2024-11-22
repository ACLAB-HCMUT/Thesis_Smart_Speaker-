import random
import sys
import os
sys.path.append(os.path.dirname(__file__))
from process import *
from listen import *
from notification import monitor_temperature, monitor_moisture


def main():
	end_keywords_pattern = re.compile(r"\b(hết rồi|hết|kết|kết thúc|cảm ơn|tắt|không|thanks|thank you)\b", re.IGNORECASE)
	greetings = ["Ơi, Aya đây", "Tui nè, có gì không"]
	follow_up_questions = [
        "Còn gì nữa không?",
        "Bạn cần gì thêm không?",
        "Tôi có thể giúp gì nữa không?",
        "Có yêu cầu nào khác không?",
        "Có cần tôi làm gì nữa không?"
    ]

	playsound("sound/welcome.mp3")
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
			playsound("sound/end_command.mp3")
			print(f"End-----------------")
			break
		else:
			end_program=process_command(command)
			if end_program == None:
				break
			follow_up = random.choice(follow_up_questions)
			print(follow_up)
			speak(follow_up)

if __name__ == "__main__":
    main()
