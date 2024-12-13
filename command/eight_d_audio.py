import pygame
import math
import time
import threading

class EightDAudio:
    def __init__(self, sound_file, loops=-1, fade_ms=1000, stride=0.5, speed=0.05):
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(sound_file)
        self.channel = pygame.mixer.find_channel()
        if self.channel is None:
            pygame.mixer.set_num_channels(pygame.mixer.get_num_channels() + 1)
            self.channel = pygame.mixer.Channel(pygame.mixer.get_num_channels() - 1)
        self.channel.play(self.sound, loops=loops, fade_ms=fade_ms)
        self.channel.set_volume(0.5, 0.5)  

        self.stride = stride  
        self.speed = speed    
        self.angle = 0       

        self.running = True
        self.thread = threading.Thread(target=self.update_volume)
        self.thread.start()

    def update_volume(self):
        while self.running:
            left = 0.5 * (1 + math.sin(math.radians(self.angle)))
            right = 0.5 * (1 + math.cos(math.radians(self.angle)))
            self.channel.set_volume(left, right)

            self.angle = (self.angle + self.stride) % 360

            time.sleep(self.speed)

    def stop(self):
        self.running = False
        self.thread.join()
        self.channel.stop()