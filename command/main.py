import random
from process import *

def main():
	greetings = ["Ơi, Aya đây", "Tui nè, có gì không", "Hở, có chuyện gì không", "À há"]
	greeting = random.choice(greetings)
	follow_up_questions = [
        "Còn gì nữa không?",
        "Bạn cần gì thêm không?",
        "Tôi có thể giúp gì nữa không?",
        "Có yêu cầu nào khác không?",
        "Có cần tôi làm gì nữa không?"
    ]
	speak(greeting)
	while True:
		command = listen_command()
		if "cảm ơn" in command.lower() or "Cảm ơn" in command.lower():
			chatgpt_answer = "Không có gì"
			print(f"ChatGPT trả lời: {chatgpt_answer}")
			speak(chatgpt_answer)
			break
		else:
			process_command(command)
			follow_up = random.choice(follow_up_questions)
			print(follow_up)
			speak(follow_up)


if __name__ == "__main__":
    main()
