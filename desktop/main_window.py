from PyQt5.QtWidgets import QMainWindow, QAction, QVBoxLayout, QWidget, QTabWidget
from PyQt5.QtCore import Qt
from upload_widget import UploadWidget
from charts_widget import ChartsWidget
from history_widget import HistoryWidget

class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1024, 768)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.setup_dashboard_tab()
        self.setup_history_tab()

        self.create_menu_bar()

    def setup_dashboard_tab(self):
        dashboard_tab = QWidget()
        layout = QVBoxLayout(dashboard_tab)

        self.upload_widget = UploadWidget(self.token)
        layout.addWidget(self.upload_widget)

        self.charts_widget = ChartsWidget()
        layout.addWidget(self.charts_widget, stretch=1)

        self.upload_widget.upload_success.connect(self.charts_widget.update_charts)
        
        self.tabs.addTab(dashboard_tab, "Dashboard")

    def setup_history_tab(self):
        self.history_widget = HistoryWidget(self.token)
        # Connect upload success to history refresh
        self.upload_widget.upload_success.connect(self.history_widget.fetch_history)
        self.tabs.addTab(self.history_widget, "History")

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        help_menu.addAction(about_action)
