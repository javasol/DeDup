from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QHBoxLayout


class IconRibbon:

    def __init__(self, scrollAreaWidgetContents: QHBoxLayout):
        self.icon_button_x = 10
        self.scrollAreaWidgetContents = scrollAreaWidgetContents
        self.icon_button_x = 10
        self.icons_in_ribbon = []
        self.current_selected_icon = None

    def add_icon(self, file_name, mouse_press_event):
        image = QImage(file_name)
        imageLabel = QLabel()
        imageLabel.setStyleSheet("QLabel { border: 1px solid red }")
        imageLabel.setFixedHeight(60)
        imageLabel.setFixedWidth(60)
        imageLabel.setScaledContents(True)
        imageLabel.setPixmap(QPixmap.fromImage(image))
        imageLabel.setVisible(True)
        imageLabel.mousePressEvent = lambda e: self.icon_selected(e, imageLabel, mouse_press_event)
        self.icons_in_ribbon.append(imageLabel)
        self.icon_button_x += 70
        self.scrollAreaWidgetContents.addWidget(imageLabel)

    def icon_selected(self, e, imageLabel, mouse_pressed_event):
        if self.current_selected_icon is not None:
            self.current_selected_icon.setStyleSheet("QLabel { border: 1px solid red }")
        imageLabel.setStyleSheet("QLabel { border: 1px solid yellow }")
        self.current_selected_icon = imageLabel
        mouse_pressed_event(e)



    def remove_icon(self, index):
        self.icons_in_ribbon.pop(index).deleteLater()
        self.icon_button_x -= 70
