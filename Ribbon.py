from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QScrollArea, QLabel
from PyQt6 import QtWidgets, QtCore


class IconRibbon(QScrollArea):


    def __init__(self, parent=None):
        QScrollArea.__init__(self, parent)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 539, 62))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

    def add_icon(self, file_name, mouse_press_event):
        image = QImage(file_name)
        imageLabel = QLabel()
        imageLabel.setParent(self.scrollAreaWidgetContents)
        imageLabel.setStyleSheet("QLabel { border: 1px solid red }")
        imageLabel.setGeometry(QtCore.QRect(self.icon_button_x, 10, 60, 60))
        imageLabel.setScaledContents(True)
        imageLabel.setPixmap(QPixmap.fromImage(image))
        imageLabel.setVisible(True)
        imageLabel.mousePressEvent = mouse_press_event

    def remove_icon(self, index):
        print("hi")