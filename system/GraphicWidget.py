from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen, QColor, QPainter
from Cell import *


class GraphicWidget(QGraphicsView):

    scene: QGraphicsScene
    cells: list[Cell] = []

    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QColor.fromRgb(0, 0, 0))
        self.setScene(self.scene)

    def set_cells(self, cells: list[Cell]):
        self.cells = cells
        self.drawShapes()

    def drawShapes(self):
        self.scene.clear()

        for cell in self.cells:
            r, g, b = cell.color[0], cell.color[1], cell.color[2]
            self.scene.addEllipse(
                cell.position[0] - cell.radius,
                cell.position[1] - cell.radius,
                cell.radius * 2,
                cell.radius * 2,
                QColor.fromRgb(r, g, b),
                QColor.fromRgb(r, g, b, 128)
            )