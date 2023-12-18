import sys
from GraphicWidget import *
from ChartWidget import *
from ViewModel import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):

    width = 600.0
    height = 600.0
    interval = 30.0
    
    graphic_widget: GraphicWidget
    chart_widget: ChartWidget
    view_model: ViewModel

    def __init__(self):
        super().__init__()
        
        self.view_model = ViewModel(self.width, self.height)

        self.setWindowTitle('System')
        self.setGeometry(0, 0, int(self.width * 2), int(self.height))
        
        layout = QHBoxLayout()
        self.graphic_widget = GraphicWidget()
        self.chart_widget = ChartWidget(self.view_model)
        layout.addWidget(self.graphic_widget)
        layout.addWidget(self.chart_widget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.view_model.cells.observe(self.update_graphic)
        
        timer = QTimer(self)
        timer.setInterval(int(self.interval))
        timer.timeout.connect(self.view_model.on_tick)
        timer.start()

    def update_graphic(self, particles: list):
        self.graphic_widget.set_cells(particles)

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
