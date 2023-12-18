from Cell import *


class Frame:
    millis: int
    count_dict: dict
    
    def __init__(self, millis, cells):
        self.millis = millis
        self.count_dict = dict()
        for cell in cells:
            cell: Cell
            count = self.count_dict.get(cell.identity)
            if count is None:
                self.count_dict[cell.identity] = 1
            else:
                self.count_dict[cell.identity] = count + 1

    def get_identity_count(self):
        return len(list(self.count_dict.keys()))

class History: 

    frames: list[Frame]

    def __init__(self):
        self.frames = []

    def add_frame(self, frame: Frame):
        self.frames.append(frame)

    def get_identities(self):
        all_keys = set()
        for frame in self.frames:
            for key in frame.count_dict.keys():
                all_keys.add(key)
        return all_keys

    def get_seconds_data(self):
        millis_data = []
        for frame in self.frames:
            millis_data.append(frame.millis / 1000)
        return millis_data
    
    def get_count_data(self, identity: str):
        count_data = []
        for frame in self.frames:
            frame: Frame
            count = frame.count_dict.get(identity)
            if count is not None:
                count_data.append(count)
            else:
                count_data.append(0)
        return count_data