from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGroupBox, QPushButton, QWidget, QHBoxLayout, QStackedWidget, QSplitter
from PyQt5.QtCore import Qt
from Framework.config_reader_module import ConfigReaderInst
import importlib

class MainWindow(QMainWindow):        
    def __init__(self):
        super().__init__()
        self.tool_index = {}
        self.init()

    def init(self):
        cfg = ConfigReaderInst.get_cfg("window_cfg")
        self.setWindowTitle(cfg.get("name"))
        self.setGeometry(100,100,cfg.get("width"),cfg.get("height"))
        self.Splitter = QSplitter()
        self.setCentralWidget(self.Splitter)
        mainHLayout = QHBoxLayout()
        self.Splitter.setLayout(mainHLayout)

        # 右侧
        self.stack = QStackedWidget(self.Splitter)

        # 左侧
        self.toolBox = QGroupBox(self.Splitter)
        self.toolBox.setTitle("tool")
        self.toolBox.setFixedWidth(cfg.get("tool_width"))

        # 左侧内容设置
        layout = QVBoxLayout(self.toolBox)
        self.init_tools(layout)
        layout.addStretch()
        self.toolBox.setLayout(layout)

        self.Splitter.addWidget(self.toolBox)
        self.Splitter.addWidget(self.stack)

        self.Splitter.setStretchFactor(0, 0)
        self.Splitter.setStretchFactor(1, 1)


    def init_tools(self,layout:QVBoxLayout):
        """初始化工具"""
        cfg = ConfigReaderInst.get_cfg("tools_cfg")
        for key in cfg.keys():
            btn = QPushButton(cfg.get(key).get("name"),self)
            btn.setObjectName(key)
            btn.clicked.connect(self.tool_onclick)
            layout.addWidget(btn,alignment=Qt.AlignTop)
        
    def tool_onclick(self):
        """工具按钮点击"""
        key = self.sender().objectName()
        if key not in self.tool_index.keys():
            cfg = ConfigReaderInst.get_cfg("tools_cfg")
            widget = self.get_tool_widget(cfg[key])
            widget.show()
            self.tool_index[key] = self.stack.addWidget(widget)
            
        self.stack.setCurrentIndex(self.tool_index[key])


    def get_tool_widget(self,cfg)->QWidget:
        """获得工具面板对象"""
        str_obj = cfg["class"]
        module_name = cfg["module"]
        try:
            module_obj = importlib.import_module(f"Panel.{module_name}")
        except:
            print(f"面板模块加载错误:{module_name}-{str_obj}")
            module_obj = importlib.import_module(f"Panel.BasePanel")
        return getattr(module_obj, str_obj)()

