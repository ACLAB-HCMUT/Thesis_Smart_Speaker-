import os
from playsound import playsound
from speak import speak
SOUND_FOLDER = "sound/animals"

def play_sound_animal(command):
    
    animals = {
        "mèo": "cat.mp3",
        "chó": "dog.mp3",
        "gà": "chicken.mp3",
        "vịt": "duck.mp3",
        "bò": "cow.mp3",
        "ngựa": "horse.mp3"
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
