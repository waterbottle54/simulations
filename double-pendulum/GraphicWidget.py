from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QPen, QColor, QPainter
from PyQt5.QtCore import QPoint, Qt, QPointF, QRectF, QTimer
from Record import *

class GraphicWidget(QGraphicsView):

    frame: Frame = None

    scene: QGraphicsScene
    pen: QPen
    painter: QPainter

    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QColor.fromRgb(0, 0, 0))
        self.setScene(self.scene)

        self.pen = QPen()
        self.pen.setColor(QColor(0xFFFFFFFF))
        self.pen.setWidth(0)
    
        self.scale(250.0, 250.0)

    def set_frame(self, frame: Frame):
        self.frame = frame
        self.drawShapes()
        
    def drawShapes(self):
        
        self.scene.clear()

        if (self.frame is None):
            return

        p1 = self.frame.data.p1
        p2 = self.frame.data.p2
        x1, y1 = p1.to_cartesian()
        x2, y2 = p2.to_cartesian()
        x2 = x1 + x2
        y2 = y1 + y2
        r = 0.05
        
        self.scene.addEllipse(x1 - r, y1 - r, 2*r, 2*r, self.pen, QColor(0xFFFF00))
        self.scene.addEllipse(x2 - r, y2 - r, 2*r, 2*r, self.pen, QColor(0xFFFF00))
        
        self.scene.addLine(0, 0, x1, y1, self.pen)
        self.scene.addLine(x1, y1, x2, y2, self.pen)

       