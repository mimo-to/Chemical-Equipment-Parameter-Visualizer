import sys
from PyQt5.QtWidgets import QApplication, QDialog
from main_window import MainWindow
from login_dialog import LoginDialog

def main():
    app = QApplication(sys.argv)
    
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        window = MainWindow(login.token)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()

if __name__ == "__main__":
    main()
