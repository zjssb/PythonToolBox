import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QStackedWidget, QLabel,
                             QMessageBox, QAction)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from Framework.config_reader_module import ConfigReader


class ToolButton(QPushButton):
    """自定义工具按钮"""

    def __init__(self, text, description="", icon_path="", parent=None):
        super().__init__(text, parent)
        self.description = description
        self.setToolTip(description)
        self.setMinimumHeight(60)
        self.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 2px solid #cccccc;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-color: #aaaaaa;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)

        # 设置图标
        if icon_path and os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(32, 32))


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.config_reader = ConfigReader()
        self.sub_windows = {}  # 存储子窗口
        self.current_overlay = None  # 当前覆盖窗口

        self.setup_ui()
        self.load_tools()

    def setup_ui(self):
        """设置主界面UI"""
        self.setWindowTitle("可配置工具箱")
        self.setGeometry(100, 100, 1000, 700)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QHBoxLayout(central_widget)

        # 左侧工具栏
        self.toolbar_widget = QWidget()
        self.toolbar_layout = QVBoxLayout(self.toolbar_widget)
        self.toolbar_layout.setSpacing(10)
        self.toolbar_widget.setMaximumWidth(250)
        self.toolbar_widget.setStyleSheet("background-color: #f8f8f8;")

        # 工具栏标题
        toolbar_title = QLabel("工具箱")
        toolbar_title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        toolbar_title.setAlignment(Qt.AlignCenter)
        self.toolbar_layout.addWidget(toolbar_title)

        self.toolbar_layout.addStretch()

        # 右侧内容区域
        self.content_stack = QStackedWidget()

        # 默认欢迎界面
        welcome_widget = QWidget()
        welcome_layout = QVBoxLayout(welcome_widget)
        welcome_label = QLabel("欢迎使用工具箱\n\n请从左侧选择工具")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; color: #666; margin: 50px;")
        welcome_layout.addWidget(welcome_label)
        self.content_stack.addWidget(welcome_widget)

        main_layout.addWidget(self.toolbar_widget)
        main_layout.addWidget(self.content_stack, 1)

        # 创建菜单栏
        self.create_menu()

    def create_menu(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu('文件')

        refresh_action = QAction('刷新配置', self)
        refresh_action.triggered.connect(self.refresh_config)
        file_menu.addAction(refresh_action)

        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 帮助菜单
        help_menu = menubar.addMenu('帮助')

        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def load_tools(self):
        """加载所有工具"""
        interfaces = self.config_reader.get_all_interfaces()

        if not interfaces:
            no_tools_label = QLabel("未找到可用的工具配置")
            no_tools_label.setAlignment(Qt.AlignCenter)
            self.toolbar_layout.addWidget(no_tools_label)
            return

        for interface_name in interfaces:
            self.add_tool_button(interface_name)

    def add_tool_button(self, interface_name):
        """添加工具按钮"""
        display_name = self.config_reader.get_display_name(interface_name)
        description = self.config_reader.get_description(interface_name)
        icon_path = self.config_reader.get_icon(interface_name)

        button = ToolButton(display_name, description, icon_path)
        button.clicked.connect(lambda checked, name=interface_name: self.open_tool(name))

        self.toolbar_layout.insertWidget(self.toolbar_layout.count() - 1, button)

    def open_tool(self, interface_name):
        """打开工具"""
        open_mode = self.config_reader.get_open_mode(interface_name)

        if open_mode == "new_window":
            self.open_new_window(interface_name)
        else:  # overlay mode
            self.open_overlay(interface_name)

    def open_new_window(self, interface_name):
        """在新窗口中打开工具"""
        if interface_name in self.sub_windows:
            # 如果窗口已存在，则激活它
            self.sub_windows[interface_name].raise_()
            self.sub_windows[interface_name].activateWindow()
            return

        # 创建新窗口
        sub_window = SubWindow(interface_name, self.config_reader, self)
        sub_window.show()
        self.sub_windows[interface_name] = sub_window

    def open_overlay(self, interface_name):
        """在当前窗口中覆盖显示工具"""
        # 移除当前覆盖窗口
        if self.current_overlay:
            self.content_stack.removeWidget(self.current_overlay)
            self.current_overlay.deleteLater()

        # 创建新界面
        try:
            tool_interface = self.config_reader.create_widget_instance(interface_name, self)
            self.content_stack.addWidget(tool_interface)
            self.content_stack.setCurrentWidget(tool_interface)
            self.current_overlay = tool_interface
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法创建工具界面: {e}")

    def refresh_config(self):
        """刷新配置"""
        self.config_reader.load_config()

        # 清空当前工具栏
        while self.toolbar_layout.count() > 2:  # 保留标题和stretch
            item = self.toolbar_layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()

        # 重新加载工具
        self.load_tools()

        QMessageBox.information(self, "刷新完成", "配置已重新加载")

    def show_about(self):
        """显示关于信息"""
        QMessageBox.about(self, "关于工具箱",
                          "可配置工具箱\n\n"
                          "基于PyQt5开发\n"
                          "支持通过配置文件动态加载工具界面")


class SubWindow(QMainWindow):
    """子窗口"""

    def __init__(self, interface_name, config_reader, parent=None):
        super().__init__(parent)
        self.interface_name = interface_name
        self.config_reader = config_reader

        self.setup_ui()

    def setup_ui(self):
        """设置子窗口UI"""
        display_name = self.config_reader.get_display_name(self.interface_name)
        self.setWindowTitle(display_name)
        self.setGeometry(200, 200, 600, 400)

        # 创建工具界面
        try:
            tool_interface = self.config_reader.create_widget_instance(self.interface_name, self)
            self.setCentralWidget(tool_interface)
        except Exception as e:
            error_label = QLabel(f"无法创建工具界面: {e}")
            error_label.setAlignment(Qt.AlignCenter)
            self.setCentralWidget(error_label)

    def closeEvent(self, event):
        """关闭事件处理"""
        if self.parent():
            # 从父窗口的sub_windows中移除
            main_window = self.parent()
            if self.interface_name in main_window.sub_windows:
                del main_window.sub_windows[self.interface_name]
        event.accept()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # 设置应用程序样式
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())