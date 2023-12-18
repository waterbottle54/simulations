from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ViewModel import *
from Cell import *
import Theory

class ChartWidget(QWidget):

    view_model: ViewModel

    figure: Figure
    canvas: FigureCanvas
    axes = None #: Axes


    def __init__(self, view_model):
        super().__init__()

        self.view_model = view_model

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.axes = self.figure.add_subplot(111)
        self.axes.set_ylabel('count')
        self.axes.set_xlabel('seconds')

        layout.addWidget(self.canvas)

        self.view_model.history.observe(self.update_chart)

    def update_chart(self, history: History):
        
        self.axes.clear()

        if len(history.frames) == 0:
            return

        identities = history.get_identities()
        seconds_data = history.get_seconds_data()

        colors = { 'immune cell':'blue', 'virus':'red' }
        for idendity in identities:
            count_data = history.get_count_data(idendity)
            self.axes.plot(seconds_data, count_data, label=idendity, color=colors[idendity])
        
        if history.frames[-1].get_identity_count() == 1:
            y_a, y_b, size = self.view_model.get_theory_data()
            self.axes.plot(seconds_data[:size], y_a, label='y1(t)', color=colors['immune cell'])
            self.axes.plot(seconds_data[:size], y_b, label='y2(t)', color=colors['virus'])

        self.axes.legend()
        self.canvas.draw()