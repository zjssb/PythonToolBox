from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QTreeView, QFileSystemModel, QPushButton,
                             QLabel, QSplitter, QTextEdit)
from PyQt5.QtCore import QDir, Qt
from .base import BaseToolInterface


class FileManagerTool(BaseToolInterface):
    """文件管理器工具"""

    def __init__(self, interface_name, config_reader, parent=None):
        super().__init__(interface_name, config_reader, parent)
        self.tree_view = None
        self.file_model = None

    def create_content(self):
        """创建文件管理器界面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 路径显示
        path_label = QLabel("文件浏览器")
        path_label.setStyleSheet("font-weight: bold; margin: 5px;")
        layout.addWidget(path_label)

        # 文件树
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.currentPath())

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(QDir.currentPath()))
        self.tree_view.setAnimated(False)
        self.tree_view.setIndentation(20)
        self.tree_view.setSortingEnabled(True)

        # 隐藏大小、类型、修改日期列
        self.tree_view.hideColumn(1)
        self.tree_view.hideColumn(2)
        self.tree_view.hideColumn(3)

        layout.addWidget(self.tree_view)

        return widget