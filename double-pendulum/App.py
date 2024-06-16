import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolBar, QAction, QProgressBar
from PyQt5.QtGui import QIcon, QMouseEvent
from PyQt5.QtCore import QTimer
from ViewModel import *
from GraphicWidget import *
from ChartWidget import *

class MainWindow(QMainWindow):

    width = 1400
    height = 800

    view_model: ViewModel
    layout: QHBoxLayout

    progress_animation: QProgressBar
    progress_calculation: QProgressBar
    graphic_widget: GraphicWidget

    toolbar: QToolBar
    status_label: QLabel

    timer: QTimer


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Double Pendulum")
        self.setWindowIcon(QIcon('icons/pendulum.png'))
        self.setGeometry(0, 0, self.width, self.height)

        self.view_model = ViewModel()
        self.layout = QVBoxLayout()

        self.setup_toolbar()

        self.progress_animation = QProgressBar()
        self.progress_animation.setFixedHeight(10)
        self.progress_animation.setTextVisible(False)
        self.layout.addWidget(self.progress_animation)

        self.layout_sub = QHBoxLayout()
        self.layout.addLayout(self.layout_sub)

        self.graphic_widget = GraphicWidget()
        self.layout_sub.addWidget(self.graphic_widget)

        self.chart_widget = ChartWidget()
        self.layout_sub.addWidget(self.chart_widget)

        self.progress_calculation = QProgressBar()
        self.progress_calculation.setFixedHeight(10)
        self.progress_calculation.setTextVisible(False)
        self.layout.addWidget(self.progress_calculation)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.view_model.on_tick)

        self.view_model.event.connect(self.on_event)

        self.view_model.millis_calculation.observe(self.update_calculation_millis_ui)
        self.view_model.is_calculation_done.observe(self.update_calculation_status_ui)
        self.view_model.is_calculatable.observe(lambda is_calculatable: self.action_start_calculation.setEnabled(is_calculatable))
        self.view_model.is_cancellable.observe(lambda is_cancellable: self.action_cancel_calculation.setEnabled(is_cancellable))
        self.view_model.is_playable.observe(lambda is_playable: self.action_play.setEnabled(is_playable))
        self.view_model.is_pausable.observe(lambda is_pausable: self.action_pause.setEnabled(is_pausable))
        self.view_model.is_stoppable.observe(lambda is_stoppable: self.action_stop.setEnabled(is_stoppable))
        self.view_model.current_frame.observe(lambda frame: self.graphic_widget.set_frame(frame))
        self.view_model.millis_animation.observe(lambda millis: self.progress_animation.setValue(int(millis)))

        def update_chart(index):
            if self.view_model.is_chart_visible.value is True:
                interval = self.view_model.interval_animation
                self.chart_widget.update_chart(index, interval, self.view_model.record)

        self.view_model.index_frame.observe(update_chart)
        self.view_model.is_chart_visible.observe(lambda is_visible: self.chart_widget.setVisible(is_visible))

    def update_calculation_status_ui(self, is_calculation_done):
        if is_calculation_done:
            self.statusBar().showMessage(f'Calculation Done!')
            self.progress_animation.setMaximum(int(self.view_model.record.get_duration()))

    def update_calculation_millis_ui(self, millis):
        self.statusBar().showMessage(f'{int(millis/1000.0)} Seconds...')
        self.progress_calculation.setMaximum(int(self.view_model.duration_calculation))
        self.progress_calculation.setValue(int(millis))

    def setup_toolbar(self):

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.action_start_calculation = QAction("Start Calculation", self, icon=QIcon("icons/calculation.png"))
        self.action_start_calculation.triggered.connect(self.view_model.on_start_calculation_click)
        self.toolbar.addAction(self.action_start_calculation)
        
        self.action_cancel_calculation = QAction("Cancel Calculation", self, icon=QIcon("icons/cancel.png"))
        self.action_cancel_calculation.triggered.connect(self.view_model.on_cancel_calculation_click)
        self.toolbar.addAction(self.action_cancel_calculation)

        self.toolbar.addSeparator()

        self.action_play = QAction("Play", self, icon=QIcon("icons/play.png"))
        self.action_play.triggered.connect(self.view_model.on_play_click)
        self.toolbar.addAction(self.action_play)

        self.action_pause = QAction("Pause", self, icon=QIcon("icons/pause.png"))
        self.action_pause.triggered.connect(self.view_model.on_pause_click)
        self.toolbar.addAction(self.action_pause)

        self.action_stop = QAction("Stop", self, icon=QIcon("icons/stop.png"))
        self.action_stop.triggered.connect(self.view_model.on_stop_click)
        self.toolbar.addAction(self.action_stop)

        self.toolbar.addSeparator()

        self.action_alt_chart = QAction("Chart", self, icon=QIcon("icons/chart.png"))
        self.action_alt_chart.triggered.connect(self.view_model.on_alt_chart_click)
        self.toolbar.addAction(self.action_alt_chart)

    def on_event(self, event):
        if isinstance(event, StartSimultationTimer):
            self.timer.setInterval(int(event.tick_interval))
            self.timer.start()
        elif isinstance(event, StopSimulationTimer):
            self.timer.stop()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())