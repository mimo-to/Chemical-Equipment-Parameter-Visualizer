import sys
from PyQt5.QtWidgets import QApplication, QDialog
from main_window import MainWindow
from login_dialog import LoginDialog
from logger import setup_logging


def main():
    setup_logging()
    app = QApplication(sys.argv)
    
    while True:
        login = LoginDialog()
        if login.exec_() != QDialog.Accepted:
            break
            
        window = MainWindow(login.token)
        window.show()
        
        if app.exec_() != 0:
            break
    
    sys.exit()


if __name__ == "__main__":
    main()

