from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QCheckBox, QFrame
)
from PyQt5.QtCore import Qt
from worker import LoginWorker

THEME = """
QDialog {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #03045e, stop:1 #012a5e);
}
QFrame#card {
    background-color: #023e8a;
    border: 1px solid #0077b6;
    border-radius: 6px;
}
QLabel {
    color: #caf0f8;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 14px;
    background: transparent;
}
QLabel#title {
    font-size: 28px;
    font-weight: bold;
    color: #00b4d8;
    padding: 8px 0;
}
QLabel#subtitle {
    font-size: 13px;
    color: #90e0ef;
    letter-spacing: 2px;
}
QLabel#fieldLabel {
    font-size: 12px;
    color: #90e0ef;
    text-transform: uppercase;
    letter-spacing: 1px;
}
QLineEdit {
    background-color: #012a5e;
    border: 1px solid #0077b6;
    border-radius: 4px;
    color: #caf0f8;
    padding: 14px 16px;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 15px;
    selection-background-color: #00b4d8;
}
QLineEdit:focus {
    border: 2px solid #00b4d8;
    background-color: #03045e;
}
QLineEdit:disabled {
    background-color: #03045e;
    color: #90e0ef;
}
QPushButton {
    background-color: #00b4d8;
    color: #03045e;
    border: none;
    border-radius: 4px;
    padding: 14px 28px;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 0.5px;
}
QPushButton:hover {
    background-color: #0096c7;
}
QPushButton:pressed {
    background-color: #0077b6;
}
QPushButton:disabled {
    background-color: #555555;
    color: #888888;
}
QPushButton#cancel {
    background-color: transparent;
    border: 1px solid #d62828;
    color: #d62828;
}
QPushButton#cancel:hover {
    background-color: #d62828;
    color: white;
}
QCheckBox {
    color: #90e0ef;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 13px;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #0077b6;
    border-radius: 3px;
    background-color: #023e8a;
}
QCheckBox::indicator:checked {
    background-color: #06ffa5;
    border-color: #06ffa5;
}
QCheckBox::indicator:hover {
    border-color: #00b4d8;
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
        self.setFixedSize(460, 500)
        self.setStyleSheet(THEME)
        
        outer = QVBoxLayout()
        outer.setContentsMargins(30, 30, 30, 30)
        
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 24, 28, 24)
        card_layout.setSpacing(10)
        
        title = QLabel("CHEM-VIS")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        
        subtitle = QLabel("AUTHENTICATION REQUIRED")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)
        
        card_layout.addSpacing(20)
        
        username_label = QLabel("USERNAME")
        username_label.setObjectName("fieldLabel")
        card_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        card_layout.addWidget(self.username_input)
        
        card_layout.addSpacing(8)
        
        password_label = QLabel("PASSWORD")
        password_label.setObjectName("fieldLabel")
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password_input)
        
        self.show_password = QCheckBox("Show password")
        self.show_password.toggled.connect(self.toggle_password)
        card_layout.addWidget(self.show_password)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ff6b6b; font-size: 13px; padding: 8px 0;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        card_layout.addWidget(self.error_label)
        
        card_layout.addStretch(1)
        
        buttons = QHBoxLayout()
        buttons.setSpacing(12)
        
        self.cancel_btn = QPushButton("CANCEL")
        self.cancel_btn.setObjectName("cancel")
        self.cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(self.cancel_btn)
        
        self.login_btn = QPushButton("ACCESS SYSTEM")
        self.login_btn.clicked.connect(self.handle_login)
        buttons.addWidget(self.login_btn)
        
        card_layout.addLayout(buttons)
        
        outer.addWidget(card)
        self.setLayout(outer)
        
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        
    def toggle_password(self, checked):
        self.password_input.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)
        
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
        self.accept()
        
    def on_error(self, message):
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
        self.login_btn.setText("AUTHENTICATING..." if loading else "ACCESS SYSTEM")
