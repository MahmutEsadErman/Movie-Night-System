import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QFile


class LoginWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        # Load the ui file
        if __name__ == "__main__":
            ui_file_name = "../uifolder/Login.ui"
        else:
            ui_file_name = "uifolder/Login.ui"
        ui_file = QFile(ui_file_name)
        self.ui = QUiLoader().load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

        #  SET BUTTONS FUNCTIONS
        # Login Window
        self.ui.login_btn.clicked.connect(self.login)
        self.ui.register_btn.clicked.connect(lambda: self.gotoPage(self.registerWindow))

    # WIP - This function will be changed
    def login(self):
        success, k_adi = self.giris_yap("customer")
        if success:
            self.k_adi = k_adi
            self.parent.goto_page(self.parent.mainmenu)

            self.orderWindow.k_adi = k_adi

            self.historyWindow.k_adi = k_adi
            self.historyWindow.update_k_adi(k_adi)

            self.orderHistoryWindow.k_adi = k_adi
            self.orderHistoryWindow.update_k_adi(k_adi)

            self.reservationWindow.k_adi = k_adi
            self.reservationWindow.update_k_adi(k_adi)

        else:
            QMessageBox.warning(self, "Hata", "E-Posta veya şifre yanlış!")

    def giris_yap(self, user_type):
        e_posta = self.ui.email_le.text()
        sifre = self.ui.password_le.text()

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
