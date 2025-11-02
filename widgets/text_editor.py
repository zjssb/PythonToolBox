from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QPushButton, QFileDialog,
                             QMessageBox)
from PyQt5.QtCore import Qt
from .base import BaseToolInterface


class TextEditorTool(BaseToolInterface):
    """文本编辑器工具"""

    def __init__(self, interface_name, config_reader, parent=None):
        super().__init__(interface_name, config_reader, parent)
        self.text_edit = None
        self.current_file = None

    def create_content(self):
        """创建文本编辑器界面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 按钮工具栏
        toolbar = QHBoxLayout()

        new_btn = QPushButton("新建")
        open_btn = QPushButton("打开")
        save_btn = QPushButton("保存")
        save_as_btn = QPushButton("另存为")

        new_btn.clicked.connect(self.new_file)
        open_btn.clicked.connect(self.open_file)
        save_btn.clicked.connect(self.save_file)
        save_as_btn.clicked.connect(self.save_file_as)

        toolbar.addWidget(new_btn)
        toolbar.addWidget(open_btn)
        toolbar.addWidget(save_btn)
        toolbar.addWidget(save_as_btn)
        toolbar.addStretch()

        layout.addLayout(toolbar)

        # 文本编辑区域
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, 'Courier New', monospace;
                font-size: 12px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.text_edit)

        return widget

    def new_file(self):
        """新建文件"""
        self.text_edit.clear()
        self.current_file = None

    def open_file(self):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开文件", "", "文本文件 (*.txt);;所有文件 (*)")

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_edit.setText(content)
                    self.current_file = file_path
            except Exception as e:
                QMessageBox.warning(self, "错误", f"无法打开文件: {e}")

    def save_file(self):
        """保存文件"""
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                QMessageBox.information(self, "成功", "文件已保存")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"无法保存文件: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        """另存为文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存文件", "", "文本文件 (*.txt);;所有文件 (*)")

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.current_file = file_path
                QMessageBox.information(self, "成功", "文件已保存")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"无法保存文件: {e}")