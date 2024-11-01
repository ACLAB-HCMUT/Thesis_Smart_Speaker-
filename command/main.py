import random
import sys
import os

from pydub import AudioSegment
from pydub.playback import play

sys.path.append(os.path.dirname(__file__))

from process import *

def main():
	end_keywords = ["không", "hết rồi", "hết", "kết thúc", "cảm ơn"]
	greetings = ["Ơi, Aya đây", "Tui nè, có gì không", "Hở, có chuyện gì không"]
	greeting = random.choice(greetings)
	follow_up_questions = [
        "Còn gì nữa không?",
        "Bạn cần gì thêm không?",
        "Tôi có thể giúp gì nữa không?",
        "Có yêu cầu nào khác không?",
        "Có cần tôi làm gì nữa không?"
    ]
	pydub_play(AudioSegment.from_file("welcome.mp3"))
	#speak(greeting)
	while True:
		command = listen_command()
		# command = "Tôn đức thắng là ai"
		# command ="bật đèn phòng khách cho tôi"
		# command ="bật quạt phòng khách cho tôi"
		# command ="Tăng âm lượng lên 80%"
		if command is None:
			print("ket thuc do khong nhan dien duoc giong noi")
			break
		command= command.lower()

		if any(keyword in command for keyword in end_keywords):
			speak("Không có chi")
			print(f"ket chuc chuong trinh")
			break
		else:
			process_command(command)
			# break
			follow_up = random.choice(follow_up_questions)
			print(follow_up)
			speak(follow_up)

if __name__ == "__main__":
    main()
