import time
import pyaudio
import queue

class MicrophoneStream:
    def __init__(self, rate, chunk, timeout_duration=7):
        self.rate = rate
        self.chunk = chunk
        self.buff = queue.Queue()
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = None
        self.timeout_duration = timeout_duration 

    def __enter__(self):
        self.audio_stream = self.audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self.callback,
        )
        self.last_audio_time = time.time() 
        self.start_time = time.time()  
        return self

    def __exit__(self, type, value, traceback):
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.buff.put(None)
        self.audio_interface.terminate()

    def callback(self, in_data, frame_count, time_info, status):
        self.last_audio_time = time.time()  
        self.buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while True:
            chunk = self.buff.get()
            if chunk is None:
                return

            if time.time() - self.start_time > self.timeout_duration:
                print("Timeout: Không có âm thanh trong 7 giây")
                self.audio_stream.stop_stream()  
                self.audio_stream.close()
                self.buff.put(None)
                return
                

            yield chunk
