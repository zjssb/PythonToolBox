from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class BaseToolInterface(QWidget):
    """基础工具界面"""

    def __init__(self, interface_name, config_reader, parent=None):
        super().__init__(parent)
        self.interface_name = interface_name
        self.config_reader = config_reader
        self.setup_ui()

    def setup_ui(self):
        """设置界面UI"""
        layout = QVBoxLayout(self)

        # 标题
        title_label = QLabel(self.config_reader.get_display_name(self.interface_name))
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 描述
        description = self.config_reader.get_description(self.interface_name)
        if description:
            desc_label = QLabel(description)
            desc_label.setStyleSheet("color: #666; margin: 5px;")
            desc_label.setWordWrap(True)
            desc_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(desc_label)

        # 内容区域
        content_widget = self.create_content()
        if content_widget:
            layout.addWidget(content_widget)

        layout.addStretch()

    def create_content(self):
        """创建界面内容，子类需要重写此方法"""
        label = QLabel("这是基础工具界面")
        label.setAlignment(Qt.AlignCenter)
        return label