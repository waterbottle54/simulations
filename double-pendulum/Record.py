from System import *

class Frame:

    millis: float
    data: System.View

    def __init__(self, millis, data: System.View):
        self.millis = millis
        self.data = data

class Record:

    frames: list[Frame]
    interval: float

    def __init__(self, interval: float):
        self.frames = []
        self.interval = interval

    def add_frame(self, frame: Frame):
        self.frames.append(frame)

    def find_frame_index(self, start_index, millis):
        if (start_index < 0) or (start_index > len(self.frames) - 1):
            return -1
        for i, frame in enumerate(self.frames[start_index:]):
            if millis <= frame.millis:
                return start_index + i
        return -1
    
    def get_duration(self):
        size = len(self.frames)
        if size == 0:
            return 0
        return self.frames[size - 1].millis