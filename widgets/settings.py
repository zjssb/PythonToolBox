from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QCheckBox, QComboBox,
                             QSpinBox, QLabel, QPushButton)
from PyQt5.QtCore import Qt
from .base import BaseToolInterface


class SettingsTool(BaseToolInterface):
    """设置工具"""

    def __init__(self, interface_name, config_reader, parent=None):
        super().__init__(interface_name, config_reader, parent)

    def create_content(self):
        """创建设置界面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 界面设置组
        ui_group = QGroupBox("界面设置")
        ui_layout = QVBoxLayout(ui_group)

        # 主题设置
        theme_layout = QHBoxLayout()
        theme_label = QLabel("主题:")
        theme_combo = QComboBox()
        theme_combo.addItems(["浅色", "深色", "自动"])
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(theme_combo)
        theme_layout.addStretch()
        ui_layout.addLayout(theme_layout)

        # 字体大小
        font_layout = QHBoxLayout()
        font_label = QLabel("字体大小:")
        font_spin = QSpinBox()
        font_spin.setRange(8, 20)
        font_spin.setValue(12)
        font_layout.addWidget(font_label)
        font_layout.addWidget(font_spin)
        font_layout.addStretch()
        ui_layout.addLayout(font_layout)

        layout.addWidget(ui_group)

        # 功能设置组
        func_group = QGroupBox("功能设置")
        func_layout = QVBoxLayout(func_group)

        auto_save = QCheckBox("自动保存配置")
        auto_refresh = QCheckBox("启动时自动刷新工具列表")

        func_layout.addWidget(auto_save)
        func_layout.addWidget(auto_refresh)

        layout.addWidget(func_group)
        layout.addStretch()

        # 按钮
        button_layout = QHBoxLayout()
        save_btn = QPushButton("保存设置")
        reset_btn = QPushButton("恢复默认")

        save_btn.clicked.connect(self.save_settings)
        reset_btn.clicked.connect(self.reset_settings)

        button_layout.addStretch()
        button_layout.addWidget(reset_btn)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

        return widget

    def save_settings(self):
        """保存设置"""
        print("设置已保存")

    def reset_settings(self):
        """恢复默认设置"""
        print("设置已重置")