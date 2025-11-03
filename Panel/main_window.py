from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGroupBox, QPushButton, QLabel, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from Framework.config_reader_module import ConfigReaderInst


def tool_onclick(key):
    # print(key)
    if key == "file_rename":
        print(123)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        cfg = ConfigReaderInst.get_cfg("window_cfg")
        self.setWindowTitle(cfg.get("name"))
        self.setGeometry(100,100,cfg.get("width"),cfg.get("height"))

        self.boxGroup = QGroupBox()
        self.setCentralWidget((self.boxGroup))

        mainHLayout = QHBoxLayout(self.boxGroup)

        box = QGroupBox(self)
        box.setFixedWidth(cfg.get("tool_width"))
        box.setStyleSheet("background-color: #e0e0e0; border: 1px solid #a0a0a0;")

        layout = QVBoxLayout(box)
        self.init_tools(layout)
        layout.addStretch()
        box.setLayout(layout)
        mainHLayout.addWidget(box)

        # 右侧区域
        self.toolView = QWidget(self)
        self.toolView.setMinimumWidth(200)
        QLabel("123",self.toolView)
        mainHLayout.addWidget((self.toolView))
        self.toolView.setStyleSheet("background-color: #f0f0f0; border: 1px solid #a0a0a0;")

        # 右侧布局
        # right_layout = QVBoxLayout(self.toolView)
        # right_layout.addWidget(QLabel("可变宽度区域"))
        # self.text_edit = QTextEdit()
        # self.text_edit.setPlaceholderText("这个区域会随着窗口大小变化而调整宽度...")
        # right_layout.addWidget(self.text_edit)
        mainHLayout.addWidget(self.boxGroup)
        mainHLayout.addWidget(self.toolView)

        self.setLayout(mainHLayout)
        mainHLayout.setStretchFactor(self.boxGroup, 0)  # 不拉伸
        mainHLayout.setStretchFactor(self.toolView, 1)  # 拉伸


    def init_tools(self,layout:QVBoxLayout):
        cfg = ConfigReaderInst.get_cfg("tools_cfg")
        for k in cfg.keys():
            btn = QPushButton(cfg.get(k).get("name"),self)
            btn.clicked.connect(lambda: tool_onclick(k))
            layout.addWidget(btn,alignment=Qt.AlignTop)

