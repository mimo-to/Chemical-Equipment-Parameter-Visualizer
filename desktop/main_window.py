from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1024, 768)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.placeholder_label = QLabel("Desktop Application Placeholder")
        self.layout.addWidget(self.placeholder_label)
        self.setCentralWidget(self.central_widget)

        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        help_menu.addAction(about_action)
