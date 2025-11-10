import os

from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout

from .base_panel import BasePanel

class FileRename(BasePanel):
    def __init__(self):
        super().__init__()
        self.paths = []
        self.setFixedWidth(200)
        self.setAcceptDrops(True)

        horLayout = QHBoxLayout()
        self.setLayout(horLayout)

        self.fileListWidget = QWidget()
        fileVerLayout = QVBoxLayout()
        self.fileListWidget.setLayout(fileVerLayout)
        horLayout.addWidget(self.fileListWidget)

        


    def show(self):
        # 调用Drops方法
        pass



    # 鼠标拖入事件
    def dragEnterEvent(self, evn):
        file = evn.mimeData().urls()[0].toLocalFile()  # ==> 获取文件路径
        if file not in self.paths:
            self.paths.append(file)
        # 鼠标放开函数事件
        evn.accept()

    # 鼠标放开执行
    def dropEvent(self, evn):
        print('鼠标放开了')