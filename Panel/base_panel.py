from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
class BasePanel(QWidget):
    def __init__(self):
        super().__init__()

    def show(self):
        layout = QHBoxLayout(self)
        layout.addWidget(QLabel("Hello world"),alignment=Qt.AlignHCenter)
        self.setLayout(layout)