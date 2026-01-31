from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

from upload_widget import UploadWidget
from charts_widget import ChartsWidget
from history_widget import HistoryWidget

THEME = """
QMainWindow {
    background-color: #03045e;
}
QTabWidget::pane {
    background-color: #023e8a;
    border: 1px solid #0077b6;
    border-top: none;
}
QTabBar {
    background-color: #03045e;
}
QTabBar::tab {
    background-color: #023e8a;
    color: #90e0ef;
    border: 1px solid #0077b6;
    border-bottom: none;
    padding: 12px 30px;
    margin-right: 4px;
    min-width: 120px;
    font-family: Consolas, monospace;
    font-size: 13px;
    font-weight: bold;
}
QTabBar::tab:selected {
    background-color: #03045e;
    color: #00b4d8;
    border-bottom: 3px solid #06ffa5;
}
QTabBar::tab:hover:!selected {
    background-color: #0077b6;
}
QTabBar::tab:disabled {
    color: #555555;
}
"""


class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setMinimumSize(1000, 700)
        self.resize(1100, 750)
        self.setStyleSheet(THEME)
        
        tabs = QTabWidget()
        tabs.setDocumentMode(False)
        
        self.upload_widget = UploadWidget(self.token)
        self.charts_widget = ChartsWidget(self.token)
        self.history_widget = HistoryWidget(self.token)
        
        self.upload_widget.upload_success.connect(self.on_upload_success)
        
        tabs.addTab(self.upload_widget, "  Data Input  ")
        tabs.addTab(self.charts_widget, "  Visualization  ")
        tabs.addTab(self.history_widget, "  Experiment Log  ")
        
        tabs.setTabEnabled(1, False)
        self.tabs = tabs
        
        self.setCentralWidget(tabs)
        
    def on_upload_success(self, dataset_id):
        self.tabs.setTabEnabled(1, True)
        self.charts_widget.load_data(dataset_id)
        self.history_widget.refresh()
