import sys
from PyQt5.QtWidgets import QApplication, QDialog
from main_window import MainWindow
from login_dialog import LoginDialog

from logger import setup_logging

def main():
    logger = setup_logging()
    logger.info("Application starting...")
    
    app = QApplication(sys.argv)
    
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        logger.info("Login successful, showing main window")
        window = MainWindow(login.token)
        window.show()
        exit_code = app.exec_()
        logger.info(f"Application exiting with code {exit_code}")
        sys.exit(exit_code)
    else:
        logger.info("Login cancelled or failed, exiting")
        sys.exit()

if __name__ == "__main__":
    main()
