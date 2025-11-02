from PyQt5.QtWidgets import QMainWindow
from Framework.config_reader_module import ConfigReaderInst
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Init()

    def Init(self):
        cfg = ConfigReaderInst.get_cfg("window_cfg")
        self.setWindowTitle(cfg.get("name"))
        self.setGeometry(100,100,cfg.get("width"),cfg.get("height"))