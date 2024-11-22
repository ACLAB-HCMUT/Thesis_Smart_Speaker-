import os
from playsound import playsound
from speak import speak
import random
SOUND_FOLDER = "sound/animals"

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

def play_story_sound():
    sound_folder = "./sound/story"  
    try:
        sound_files = [file for file in os.listdir(sound_folder) if file.endswith(".mp3") or file.endswith(".wav")]
        if not sound_files:
            print("Không tìm thấy tệp âm thanh nào trong thư mục sound.")
            speak("Không có câu chuyện nào để kể.")
            return
        selected_sound = random.choice(sound_files)
        sound_path = os.path.join(sound_folder, selected_sound)
        print(f"Đang phát tệp âm thanh: {selected_sound}")
        playsound(sound_path)  
    except Exception as e:
        print(f"Lỗi khi phát âm thanh: {e}")
        speak("Đã xảy ra lỗi khi kể chuyện.")
