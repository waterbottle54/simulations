from PyQt5.QtCore import QObject, pyqtSignal
from System import *
from Record import *
from random import *
from LiveData import *

class Event: 
    pass
class StartSimultationTimer(Event): 
    tick_interval: float
    def __init__(self, interval):
        self.tick_interval = interval
class StopSimulationTimer(Event):
    pass

class ViewModel(QObject):

    event: pyqtSignal = pyqtSignal(Event)

    duration_calculation: float
    interval_calculation: float
    interval_animation: float

    system: System = None
    record: Record = None

    millis_calculation: MutableLiveData
    is_calculation_in_progress: MutableLiveData 

    is_playing_in_progress = MutableLiveData
    is_calculation_done = MutableLiveData
    millis_animation: MutableLiveData
    index_frame = LiveData
    current_frame: LiveData

    is_calculatable: LiveData
    is_cancellable: LiveData
    is_playable: LiveData
    is_pausable: LiveData
    is_stoppable: LiveData

    is_chart_visible: MutableLiveData

    def __init__(self):
        super().__init__()

        self.duration_calculation = 60000.0
        self.interval_calculation = 1.0
        self.interval_animation = 30.0

        self.millis_calculation = MutableLiveData(0)
        self.is_calculation_in_progress = MutableLiveData(False)
        self.is_calculation_done = MutableLiveData(False)
        self.is_playing_in_progress = MutableLiveData(False)
        self.millis_animation = MutableLiveData(0)

        self.is_chart_visible = MutableLiveData(False)

        def map_index_frame(millis):
            if (self.record is None):
                return -1
            return self.record.find_frame_index(0, millis)
        self.index_frame = map(self.millis_animation, map_index_frame)

        def map_current_frame(index):
            if (self.record is None) or (index == -1) or (index > len(self.record.frames) - 1):
                return None
            return self.record.frames[index]
        self.current_frame = map(self.index_frame, map_current_frame)

        def map_is_calculatable(is_calculation_in_progress, is_playing_in_progress):
            return (is_calculation_in_progress is False) and (is_playing_in_progress is False)
        self.is_calculatable = map2(self.is_calculation_in_progress, self.is_playing_in_progress, map_is_calculatable)

        def map_is_cancellable(is_calculation_in_progress, is_calculation_done, is_playing_in_progress):
            if (is_playing_in_progress is True):
                return False
            return (is_calculation_in_progress is True) or (is_calculation_done is True)
        self.is_cancellable = map3(self.is_calculation_in_progress, self.is_calculation_done, self.is_playing_in_progress, map_is_cancellable)

        def map_is_playable(is_calculation_done, is_playing_in_progress):
            return (is_calculation_done is True) and (is_playing_in_progress is False)
        self.is_playable = map2(self.is_calculation_done, self.is_playing_in_progress, map_is_playable)

        def map_is_pausable(is_playing_in_progress):
            return (is_playing_in_progress is True)
        self.is_pausable = map(self.is_playing_in_progress, map_is_pausable)

        def map_is_stoppable(is_playing_in_progress):
            return (is_playing_in_progress is True)
        self.is_stoppable = map(self.is_playing_in_progress, map_is_stoppable)

    def on_start_calculation_click(self):

        if (self.is_calculatable.value is False):
            return

        p1 = Pendulum(1.0, 1.0, np.pi/4, 0.0)
        p2 = Pendulum(1.0, 1.0, 0.0, 0.0)
        self.system = System(p1, p2)

        self.record = Record(self.interval_calculation)

        self.millis_calculation.set_value(0)
        self.is_calculation_in_progress.set_value(True)
        self.is_calculation_done.set_value(False)
        self.is_playing_in_progress.set_value(False)
        self.millis_animation.set_value(0)

        self.calculate()

    def on_cancel_calculation_click(self):

        if (self.is_cancellable.value is False):
            return

        self.millis_calculation.set_value(0)
        self.is_calculation_in_progress.set_value(False)
        self.is_calculation_done.set_value(False)
        self.is_playing_in_progress.set_value(False)
        self.millis_animation.set_value(0)

        self.system = None
        self.record = None

    def on_play_click(self):

        if (self.is_playable.value is False):
            return
        
        self.is_playing_in_progress.set_value(True)
        if (self.millis_animation.value == 0) or (self.millis_animation.value >= self.record.get_duration()):
            self.millis_animation.set_value(0)

        self.event.emit(StartSimultationTimer(self.interval_animation))

    def on_pause_click(self):

        if (self.is_pausable.value is False):
            return
        
        self.is_playing_in_progress.set_value(False)
        self.event.emit(StopSimulationTimer())

    def on_stop_click(self):

        if (self.is_stoppable.value is False):
            return
        
        self.is_playing_in_progress.set_value(False)
        self.millis_animation.set_value(0)

        self.event.emit(StopSimulationTimer())

    def on_alt_chart_click(self):
        if self.is_chart_visible.value is True:
            self.is_chart_visible.set_value(False)
        else:
            self.is_chart_visible.set_value(True)

    def on_tick(self):

        if (self.is_playing_in_progress.value is False):
            return

        millis = self.millis_animation.value
        if (millis + self.interval_animation) <= self.record.get_duration():
            self.millis_animation.set_value(millis + self.interval_animation)
        else:
            self.on_pause_click()

    def calculate(self):
         
         while (self.is_calculation_in_progress.value is True) and (self.is_calculation_done.value is False):
            interval = self.record.interval
            millis_calculation = self.millis_calculation.value

            self.system.update(interval)
            system_view = self.system.get_view()
            self.record.add_frame(Frame(millis_calculation, system_view))

            self.millis_calculation.set_value(millis_calculation + interval)
            if self.is_calculation_finished() is True:
                self.is_calculation_in_progress.set_value(False)
                self.is_calculation_done.set_value(True)            

    def is_calculation_finished(self):
        return self.millis_calculation.value > self.duration_calculation

    

        
    