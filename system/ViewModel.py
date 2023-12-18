from PyQt5.QtCore import QObject, pyqtSignal
from LiveData import *
from History import *
from Cell import *
import time
import random
import numpy as np
import Theory
from typing import Dict

class Event: pass

class ViewModel(QObject):

    event: pyqtSignal = pyqtSignal(Event)

    width: float
    height: float
    
    cells: MutableLiveData
    history: MutableLiveData
    millis = 0
    last_millis: int = None

    number_a = 50
    number_b = 50
    fatality_a = 0.02
    fatality_b = 0.01


    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.generate_cells()
        
    def generate_cells(self):
        self.cells = MutableLiveData([])
        self.history = MutableLiveData(History())

        cell_list = []

        for i in np.arange(0, self.number_a):
            x = float(random.randrange(0, self.width))
            y = float(random.randrange(0, self.height))

            new = Cell(
                'immune cell',
                ['virus'],
                self.fatality_a,
                [255, 255, 255],
                5.0, 
                x, y,
            )
            cell_list.append(new)

        for i in np.arange(0, self.number_b):
            x = float(random.randrange(0, self.width))
            y = float(random.randrange(0, self.height))

            new = Cell(
                'virus',
                ['immune cell'],
                self.fatality_b,
                [255, 0, 0],
                5.0, 
                x, y,
            )
            cell_list.append(new)

        self.cells.set_value(cell_list)
        
    def on_tick(self):

        interval = 100
        now = int(time.perf_counter() * 1000)

        if self.last_millis is not None:
            interval = now - self.last_millis
            
        self.last_millis = now

        for cell in self.cells.value:
            if cell.alive:
                cell.update(interval, self.cells.value)

        new_list = []
        for cell in self.cells.value:
            if cell.alive:
                new_list.append(cell)

        self.cells.set_value(new_list)

        current_frame = Frame(self.millis, self.cells.value)
        last_frame: Frame = None
        
        if len(self.history.value.frames) > 0:
            last_frame = self.history.value.frames[-1]

        if self.millis == 0:
            self.history.value.add_frame(current_frame)
            self.history.publish()
        elif current_frame.get_identity_count() >= 2:
            self.history.value.add_frame(current_frame)
            self.history.publish()
        elif (last_frame is not None) and (last_frame.get_identity_count() > 1):
            self.history.value.add_frame(current_frame)
            self.history.publish()

        self.millis += interval

    def get_theory_y_a_data(self):
        seconds_data = self.history.value.get_seconds_data()
        y_a0 = self.number_a
        y_b0 = self.number_b
        k_a = self.fatality_a
        k_b = self.fatality_b
        
        y_a_data = []
        i_end = -1
        for i, t in enumerate(seconds_data):
            y = Theory.y_a(t, y_a0, y_b0, k_a, k_b)
            if y > 0:
                y_a_data.append(y)
            else:
                i_end = t
                break;

        return y_a_data, i_end
    
    def get_theory_y_b_data(self):
        seconds_data = self.history.value.get_seconds_data()
        y_a0 = self.number_a
        y_b0 = self.number_b
        k_a = self.fatality_a
        k_b = self.fatality_b
        
        y_b_data = []
        i_end = -1
        for i, t in enumerate(seconds_data):
            y = Theory.y_b(t, y_a0, y_b0, k_a, k_b)
            if y > 0:
                y_b_data.append(y)
            else:
                i_end = i
                break;

        return y_b_data, i_end
    
    def get_theory_data(self):
        y_a, i_end_a = self.get_theory_y_a_data()
        y_b, i_end_b = self.get_theory_y_b_data()
        if (i_end_a == -1) and (i_end_b == -1):
            return y_a, y_b, len(y_a)
        elif (i_end_a != -1) and (i_end_b != -1):
            i_min = np.min(i_end_a, i_end_b)
            return y_a[:i_min], y_b[:i_min], i_min
        elif i_end_a != -1:
            return y_a[:i_end_a], y_b[:i_end_a], i_end_a
        elif i_end_b != -1:
            return y_a[:i_end_b], y_b[:i_end_b], i_end_b
        




