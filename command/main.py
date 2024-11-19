import random
import sys
from process import *
from listen import *
sys.path.append(os.path.dirname(__file__))


def main():
	end_keywords_pattern = re.compile(r"\b(hết rồi|hết|kết|kết thúc|cảm ơn|that's all|thankss|thank you)\b", re.IGNORECASE)
	greetings = ["Ơi, Aya đây", "Tui nè, có gì không"]
	follow_up_questions = [
        "Còn gì nữa không?",
        "Bạn cần gì thêm không?",
        "Tôi có thể giúp gì nữa không?",
        "Có yêu cầu nào khác không?",
        "Có cần tôi làm gì nữa không?"
    ]

	playsound("sound/welcome.mp3")
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
			process_command(command)
			follow_up = random.choice(follow_up_questions)
			print(follow_up)
			speak(follow_up)

if __name__ == "__main__":
    main()
