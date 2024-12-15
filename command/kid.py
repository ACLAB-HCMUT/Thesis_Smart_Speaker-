import os
from playsound import playsound
from speak import speak
import random
import subprocess
from listen import standalone_listen  
SOUND_FOLDER = "sound/animals"
SOUND_FOLDER_STORIES = "sound/story"
# SOUND_FOLDER = "animals"
# SOUND_FOLDER_STORIES = "story"

def play_sound_animal(command):
    animals = {
        "mèo": "cat.mp3",
        "chó": "dog.mp3",
        "gà": "chicken.mp3",
        "vịt": "duck.mp3",
        "bò": "cow.mp3",
        "ngựa": "horse.mp3",
        "cá": "alligator.mp3",
        "dế": "crickets.mp3",
        "quạ": "crow.mp3",
        "ong": "bee.mp3",
        "voi": "elephant.mp3",
        "cú": "owl.mp3",
        "sử tử": "lion.mp3",
        "hổ": "tiger.mp3",
        "sói": "wolf.mp3",
        "heo": "pig.mp3",
        "cừu": "lamb.mp3",
        "dê": "lamb.mp3",
    }

    animal_found = None
    for animal in animals.keys():
        if animal in command:
            animal_found = animal
            break

    if animal_found:
        sound_file = os.path.join(SOUND_FOLDER, animals[animal_found])
        if os.path.exists(sound_file):
            response = f"Đang phát tiếng {animal_found} kêu."
            print(response)
            playsound(sound_file)
        else:
            response = f"Không tìm thấy âm thanh cho {animal_found}."
            print(response)
            speak(response)
    else:
        response = "Không xác định được con vật nào. Vui lòng thử lại với tên con vật cụ thể."
        print(response)
        speak(response)


story_process = None

def play_story_sound():
    global story_process
    try:
        sound_files = [file for file in os.listdir(SOUND_FOLDER_STORIES) if file.endswith(".mp3") or file.endswith(".wav")]
        
        if not sound_files:
            print("Không tìm thấy tệp âm thanh nào trong thư mục câu chuyện.")
            speak("Không có câu chuyện nào để kể.")
            return

        selected_sound = random.choice(sound_files)
        sound_path = os.path.join(SOUND_FOLDER_STORIES, selected_sound)

        print(f"Đang phát câu chuyện: {selected_sound}")
        
        story_process = subprocess.Popen(["ffplay", "-nodisp", "-autoexit", sound_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        listen_for_stop_command()  

    except Exception as e:
        print(f"Lỗi khi phát âm thanh câu chuyện: {e}")
        speak("Đã xảy ra lỗi khi kể chuyện.")

def listen_for_stop_command():
    while story_process.poll() is None:  
        command = standalone_listen()  
        if command and ("dừng câu chuyện" in command or "tắt câu chuyện" in command or "tắt" in command):
            stop_story_sound()  
            break

def stop_story_sound():
    global story_process
    if story_process and story_process.poll() is None:  
        story_process.terminate() 
        print("Câu chuyện đã được dừng.")
        speak("Câu chuyện đã dừng.")
        story_process = None
    else:
        print("Không có câu chuyện nào đang được phát.")
        speak("Hiện không có câu chuyện nào đang kể.")
