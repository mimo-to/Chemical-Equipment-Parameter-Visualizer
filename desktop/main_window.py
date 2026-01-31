from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpacerItem, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from upload_widget import UploadWidget
from charts_widget import ChartsWidget
from history_widget import HistoryWidget
from theme import COLORS

HEADER_STYLE = f"""
QFrame#header {{
    background-color: {COLORS['background']};
    border-bottom: 1px solid {COLORS['border']};
}}
QLabel#title {{
    color: {COLORS['primary']};
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 18px;
    font-weight: bold;
    letter-spacing: 2px;
    background: transparent;
}}
QPushButton#logout {{
    background-color: transparent;
    border: 2px solid {COLORS['error']};
    border-radius: 4px;
    color: {COLORS['error']};
    padding: 8px 20px;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1px;
}}
QPushButton#logout:hover {{
    background-color: {COLORS['error']};
    color: {COLORS['background']};
}}
"""

TAB_STYLE = f"""
QTabWidget::pane {{
    border: none;
    background-color: {COLORS['background']};
}}
QTabBar {{
    background-color: {COLORS['background']};
}}
QTabBar::tab {{
    background-color: {COLORS['card']};
    color: {COLORS['muted']};
    border: 1px solid {COLORS['border']};
    border-bottom: none;
    padding: 14px 36px;
    margin-right: 4px;
    min-width: 140px;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 0.5px;
}}
QTabBar::tab:selected {{
    background-color: {COLORS['background']};
    color: {COLORS['primary']};
    border-top: 2px solid {COLORS['primary']};
}}
QTabBar::tab:hover:!selected {{
    background-color: {COLORS['background']};
    color: {COLORS['text']};
}}
QTabBar::tab:disabled {{
    background-color: #1a1a2e;
    color: #444455;
    border-color: #333344;
}}
"""

MAIN_STYLE = f"""
QMainWindow {{
    background-color: {COLORS['background']};
}}
"""


class MainWindow(QMainWindow):
    logout_requested = pyqtSignal()
    
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setMinimumSize(1100, 750)
        self.setStyleSheet(MAIN_STYLE)
        
        central = QWidget()
        central.setStyleSheet(f"background-color: {COLORS['background']};")
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        header = QFrame()
        header.setObjectName("header")
        header.setStyleSheet(HEADER_STYLE)
        header.setFixedHeight(60)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 0, 24, 0)
        
        title = QLabel("ANALYSIS WORKSTATION")
        title.setObjectName("title")
        header_layout.addWidget(title)
        
        header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        logout_btn = QPushButton("LOGOUT")
        logout_btn.setObjectName("logout")
        logout_btn.clicked.connect(self.handle_logout)
        header_layout.addWidget(logout_btn)
        
        main_layout.addWidget(header)
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(TAB_STYLE)
        
        self.upload_widget = UploadWidget(self.token)
        self.upload_widget.upload_success.connect(self.on_upload_success)
        self.tabs.addTab(self.upload_widget, "DATA SUMMARY")
        
        self.charts_widget = ChartsWidget(self.token)
        self.tabs.addTab(self.charts_widget, "VISUALIZATION")
        self.tabs.setTabEnabled(1, False)
        
        self.history_widget = HistoryWidget(self.token)
        self.tabs.addTab(self.history_widget, "EXPERIMENT LOG")
        
        main_layout.addWidget(self.tabs)
        self.setCentralWidget(central)
        
    def on_upload_success(self, dataset_id):
        self.tabs.setTabEnabled(1, True)
        self.charts_widget.load_data(dataset_id)
        self.history_widget.refresh()
        
    def handle_logout(self):
        self.logout_requested.emit()
        self.close()
