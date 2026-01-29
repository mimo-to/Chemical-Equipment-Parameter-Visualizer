import requests
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedWidth(360)
        self.setStyleSheet("background-color: white;")  
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        
        title = QLabel("Chemical Visualizer")
        font = title.font()
        font.setFamily("Segoe UI") 
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #333333; margin-bottom: 5px;")
        layout.addWidget(title)
        
        subtitle = QLabel("Welcome back")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666666; font-size: 12px; margin-bottom: 20px;")
        layout.addWidget(subtitle)

     
        input_style = """
            QLineEdit {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 8px 10px;
                background-color: #f9f9f9;
                font-size: 13px;
                color: #333;
            }
            QLineEdit:focus {
                border: 1px solid #333;
                background-color: #fff;
            }
        """

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet(input_style)
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet(input_style)
        layout.addWidget(self.password_input)

        layout.addSpacing(10)

       
        self.login_button = QPushButton("Sign In")
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setFixedHeight(40)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #222222;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #000000;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background: transparent; 
                color: #888888;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover {
                color: #333333;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)

        layout.addStretch()
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/login/",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                self.token = response.json().get("token")
                self.accept()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials.")
        except requests.RequestException:
            QMessageBox.critical(self, "Network Error", "Could not connect to server.")
