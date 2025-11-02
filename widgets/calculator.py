from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QGridLayout)
from PyQt5.QtCore import Qt
from .base import BaseToolInterface


class CalculatorTool(BaseToolInterface):
    """计算器工具"""

    def __init__(self, interface_name, config_reader, parent=None):
        super().__init__(interface_name, config_reader, parent)
        self.current_input = ""
        self.result_display = None

    def create_content(self):
        """创建计算器界面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 显示区域
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setAlignment(Qt.AlignRight)
        self.result_display.setStyleSheet("""
            QLineEdit {
                font-size: 20px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
        """)
        layout.addWidget(self.result_display)

        # 按钮区域
        button_layout = QGridLayout()
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0, 1, 4)  # 清除按钮，跨4列
        ]

        for btn in buttons:
            if len(btn) == 4:  # 跨列按钮
                text, row, col, row_span, col_span = btn
                button = QPushButton(text)
                button_layout.addWidget(button, row, col, row_span, col_span)
            else:
                text, row, col = btn
                button = QPushButton(text)
                button_layout.addWidget(button, row, col)

            button.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            button.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: #e0e0e0;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QPushButton:pressed {
                    background-color: #c0c0c0;
                }
            """)

        layout.addLayout(button_layout)
        return widget

    def on_button_click(self, text):
        """按钮点击处理"""
        if text == '=':
            try:
                result = eval(self.current_input)
                self.current_input = str(result)
                self.result_display.setText(self.current_input)
            except:
                self.current_input = ""
                self.result_display.setText("Error")
        elif text == 'C':
            self.current_input = ""
            self.result_display.setText("")
        else:
            self.current_input += text
            self.result_display.setText(self.current_input)