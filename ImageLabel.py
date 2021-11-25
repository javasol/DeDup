from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6 import QtGui


class ImageLabel(QLabel):
    def __init__(self, img):
        super(ImageLabel, self).__init__()
        self.pixmap = QPixmap(img)

    def paintEvent(self, event):
        size = self.size()
        painter = QPainter(self)
        point = QPoint(0, 0)
        scaledPix = self.pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio,
                                       transformMode=Qt.TransformationMode.SmoothTransformation)
        point.setX((size.width() - scaledPix.width()) / 2)
        point.setY((size.height() - scaledPix.height()) / 2)
        painter.drawPixmap(point, scaledPix)

    def changePixmap(self, img):
        self.pixmap = QtGui.QPixmap(img)
        self.repaint()
