import random
import sys
import os

sys.path.append(os.path.dirname(__file__))

from process import *

def main():
	end_keywords = ["hết rồi", "hết", "kết thúc", "cảm ơn","that's all","thankss","thank you"]
	greetings = ["Ơi, Aya đây", "Tui nè, có gì không", "Hở, có chuyện gì không"]
	cauhoi_tieptheo = [
        "Còn gì nữa không?",
        "Bạn cần gì thêm không?",
        "Tôi có thể giúp gì nữa không?",
        "Có yêu cầu nào khác không?",
        "Có cần tôi làm gì nữa không?"
    ]
	follow_up_questions = [
        "Anything else ?",
        "What do you need more ?",
        "Can I help more ?",
        "Another request ?",
        "What else ?"
    ]    	
	song = AudioSegment.from_file("welcome.mp3")
	playobj = sa.play_buffer(song.raw_data, num_channels=2, bytes_per_sample=2, sample_rate=song.frame_rate)
	playobj.wait_done()
	#greeting = random.choice(greetings)
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
		lang_detected = detect(command)
		if any(keyword in command for keyword in end_keywords):
			if lang_detected == 'en':
				speak("Your Welcome")
				print(f"End the program")
			if lang_detected == 'vi':
				speak("Không có chi")
				print(f"ket chuc chuong trinh")
			break
		else:
			process_command(command)
			# break
			if lang_detected == 'en':
				follow_up = random.choice(follow_up_questions)
			elif lang_detected == 'vi':
				follow_up = random.choice(cauhoi_tieptheo)
			print(follow_up)
			speak(follow_up)

if __name__ == "__main__":
    main()
