from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QCheckBox, QWidget, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont

from logger import get_logger
from worker import LoginWorker

log = get_logger(__name__)

THEME = """
QDialog {
    background-color: #03045e;
    color: #caf0f8;
}
QLabel {
    color: #caf0f8;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 12px;
}
QLabel#title {
    font-size: 24px;
    font-weight: bold;
    color: #00b4d8;
}
QLabel#subtitle {
    font-size: 11px;
    color: #90e0ef;
}
QLineEdit {
    background-color: #023e8a;
    border: 1px solid #0077b6;
    color: #caf0f8;
    padding: 8px 12px;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 12px;
}
QLineEdit:focus {
    border-color: #00b4d8;
}
QLineEdit:disabled {
    background-color: #03045e;
    color: #90e0ef;
}
QPushButton {
    background-color: #0077b6;
    color: #caf0f8;
    border: none;
    padding: 10px 20px;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 12px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #00b4d8;
}
QPushButton:pressed {
    background-color: #023e8a;
}
QPushButton:disabled {
    background-color: #023e8a;
    color: #90e0ef;
}
QPushButton#cancel {
    background-color: transparent;
    border: 1px solid #0077b6;
}
QPushButton#cancel:hover {
    background-color: #023e8a;
}
QCheckBox {
    color: #90e0ef;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 11px;
}
QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border: 1px solid #0077b6;
    background-color: #023e8a;
}
QCheckBox::indicator:checked {
    background-color: #06ffa5;
    border-color: #06ffa5;
}
"""


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.token = None
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("CHEM-VIS Authentication")
        self.setFixedSize(380, 340)
        self.setStyleSheet(THEME)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)
        
        title = QLabel("CHEM-VIS")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Authentication Required")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(16)
        
        self.username_label = QLabel("Username")
        layout.addWidget(self.username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        layout.addWidget(self.username_input)
        
        self.password_label = QLabel("Password")
        layout.addWidget(self.password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        self.show_password = QCheckBox("Show password")
        self.show_password.toggled.connect(self.toggle_password)
        layout.addWidget(self.show_password)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ff6b6b;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        layout.addStretch()
        
        buttons = QHBoxLayout()
        buttons.setSpacing(12)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancel")
        self.cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(self.cancel_btn)
        
        self.login_btn = QPushButton("Access System")
        self.login_btn.clicked.connect(self.handle_login)
        buttons.addWidget(self.login_btn)
        
        layout.addLayout(buttons)
        self.setLayout(layout)
        
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        
    def toggle_password(self, checked):
        mode = QLineEdit.Normal if checked else QLineEdit.Password
        self.password_input.setEchoMode(mode)
        
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error("Username and password required")
            return
            
        self.set_loading(True)
        self.error_label.hide()
        
        self.worker = LoginWorker(username, password)
        self.worker.success.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()
        
    def on_success(self, token):
        self.token = token
        log.info("Login successful")
        self.accept()
        
    def on_error(self, message):
        log.error(f"Login failed: {message}")
        self.show_error(message)
        self.set_loading(False)
        
    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()
        
    def set_loading(self, loading):
        self.username_input.setEnabled(not loading)
        self.password_input.setEnabled(not loading)
        self.login_btn.setEnabled(not loading)
        self.cancel_btn.setEnabled(not loading)
        self.login_btn.setText("Authenticating..." if loading else "Access System")
