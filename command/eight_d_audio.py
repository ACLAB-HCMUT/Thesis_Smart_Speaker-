# eight_d_audio.py
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
        self.channel.set_volume(0.5, 0.5)  # Bắt đầu với âm lượng trung bình cho cả hai kênh

        self.stride = stride  # Bước tăng giảm góc
        self.speed = speed    # Tốc độ cập nhật âm lượng
        self.angle = 0        # Góc hiện tại để tính toán âm lượng

        self.running = True
        self.thread = threading.Thread(target=self.update_volume)
        self.thread.start()

    def update_volume(self):
        while self.running:
            # Tính toán âm lượng dựa trên góc hiện tại
            left = 0.5 * (1 + math.sin(math.radians(self.angle)))
            right = 0.5 * (1 + math.cos(math.radians(self.angle)))
            self.channel.set_volume(left, right)

            # Cập nhật góc
            self.angle = (self.angle + self.stride) % 360

            time.sleep(self.speed)

    def stop(self):
        self.running = False
        self.thread.join()
        self.channel.stop()