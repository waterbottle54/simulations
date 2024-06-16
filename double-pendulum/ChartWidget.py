from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Record import *

class ChartWidget(QWidget):

    figure: Figure
    canvas: FigureCanvas
    axes = None #: Axes

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.axes = self.figure.add_subplot(111)
        
        layout.addWidget(self.canvas)

    def update_chart(self, index: int, interval: int, record: Record):

        self.axes.set_title('Energy of System')
        self.axes.set_ylabel('Energy(J)')
        self.axes.set_xlabel('Time(ms)')

        if (record is None) or (index < 0) or (index > len(record.frames) - 1):
            self.axes.clear()
            return
        
        self.axes.clear()
        
        end = record.frames[index].millis 
        start = max(0, end - 4000)
        start_index = record.find_frame_index(0, start)
    
        frames = []
        indice = []
        for t in np.arange(start, end, interval):
            index = record.find_frame_index(start_index, t)
            if (index != -1) and (index not in indice):
                frames.append(record.frames[index])
                indice.append(index)

        if len(frames) == 0:
            return

        ts = [ frame.millis for frame in frames ]
        pes = [ frame.data.potential_energy for frame in frames ]
        kes = [ frame.data.kinetic_energy for frame in frames ]
        es = [ kes[i] + pes[i] for i in range(len(pes)) ]

        self.axes.plot(ts, pes, label='P.E', color='orange')
        self.axes.plot(ts, kes, label='K.E', color='red')
        self.axes.plot(ts, es, label='P.E + K.E', color='blue')

        self.axes.annotate(f'{pes[-1]:.1f}J', (ts[-1], pes[-1]), textcoords="offset points", xytext=(0,-10), ha='center')
        self.axes.annotate(f'{kes[-1]:.1f}J', (ts[-1], kes[-1]), textcoords="offset points", xytext=(0,10), ha='center')
        self.axes.annotate(f'{es[-1]:.1f}J', (ts[-1], es[-1]), textcoords="offset points", xytext=(0,10), ha='center')

        self.axes.legend()
        self.canvas.draw()