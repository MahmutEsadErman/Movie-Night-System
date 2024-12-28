import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the ui file
        if __name__ == "__main__":
            ui_file_name = "../uifolder/Login.ui"
        else:
            ui_file_name = "uifolder/Login.ui"
        ui_file = QFile(ui_file_name)
        self.ui = QUiLoader().load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

    def girisYap(self, user_type):
        e_posta = self.ui.lineEdit.text()
        sifre = self.ui.lineEdit_2.text()

        if user_type == "customer":
            with open("database/kullanicilar.txt", "r", encoding='utf-8') as dosya:
                for satir in dosya:
                    bilgiler = satir.strip().split("-")
                    if bilgiler[2] == e_posta and bilgiler[4] == sifre:
                        k_adi = bilgiler[1]
                        return True, k_adi
            return False, None
        elif user_type == "manager":
            admin_username = "admin"
            admin_password = "admin"
            if e_posta == admin_username and sifre == admin_password:
                k_adi = admin_username
                return True, k_adi
            return False, None
        elif user_type == "worker":
            admin_username = "worker"
            admin_password = "worker"
            if e_posta == admin_username and sifre == admin_password:
                k_adi = admin_username
                return True, k_adi
            return False, None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
