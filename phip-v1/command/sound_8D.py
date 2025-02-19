import pygame
import math
import time
import datetime
pygame.init()


clock = pygame.time.Clock()


sound_file = "sound/alarm.wav"  
sound = pygame.mixer.Sound(sound_file)
channel = pygame.mixer.find_channel()
channel.play(sound, loops=-1, fade_ms=1000)
channel.set_volume(1.0)

stride = 0.19  
speed = 0.3   
a, b = 1.0, 0.0  
temp = [-1, 1]
muted = False
paused = False
angle = 0

x = datetime.datetime.now()

while True:
    time_delta = clock.tick(60) / 1000.0 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    current_time = datetime.datetime.now()
    if (current_time - x).total_seconds() > speed:
        a += temp[0] * stride
        b += temp[1] * stride
        if a < 0.01 and b > 0.9:
            a, b = 0, 1
            temp[0], temp[1] = temp[1], temp[0]
        if b < 0.01 and a > 0.9:
            a, b = 1, 0
            temp[0], temp[1] = temp[1], temp[0]
        
        if not paused:
            if not muted:
                channel.set_volume(abs(a), b)
        x = current_time

    angle -= 5
    angle = angle % 360  

    
    if not paused and not muted:
        x_pos = 130 * math.cos(math.radians(angle))
        y_pos = 130 * math.sin(math.radians(angle))

    time.sleep(0.0167)  