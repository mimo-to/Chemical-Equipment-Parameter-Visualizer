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
        if login.exec_() == QDialog.Accepted:
            window = MainWindow(login.token)
            
            logged_out = [False]
            window.logout_requested.connect(lambda: logged_out.__setitem__(0, True))
            
            window.show()
            app.exec_()
            
            if not logged_out[0]:
                break
        else:
            break
    
    sys.exit()


if __name__ == "__main__":
    main()

