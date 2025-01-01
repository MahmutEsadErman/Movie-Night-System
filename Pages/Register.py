import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QFile


class RegisterWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        # Load the ui file
        if __name__ == "__main__":
            ui_file_name = "../uifolder/Register.ui"
        else:
            ui_file_name = "uifolder/Register.ui"
        ui_file = QFile(ui_file_name)
        self.ui = QUiLoader().load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

        # Register Window
        self.ui.signup_btn.clicked.connect(self.register)
        self.ui.login_btn.clicked.connect(lambda: self.parent.goto_page(self.parent.loginWindow))

    def register_btn_callback(self):
        if self.parent.registerWindow.register():
            self.parent.goto_page(self.parent.loginWindow)

### DİKKAT! BU FONKSİYON DEĞİŞTİRİLECEKTİR ###
    def register(self):

        ad_soyad = self.ui.name_le.text()

        kullanici_adi = self.ui.username_le.text()

        e_posta = self.ui.email_le.text()

        cep_telefonu = self.ui.phone_le.text()

        sifre = self.ui.password_le.text()

        k_adlari = []
        mailler = []
        numaralar = []

        with open("database/kullanicilar.txt", "r", encoding='utf-8') as dosya:
            for satir in dosya:
                bilgiler = satir.strip().split("-")
                k_adlari.append(bilgiler[1])
                mailler.append(bilgiler[2])
                numaralar.append(bilgiler[3])

        if kullanici_adi in k_adlari:
            QMessageBox.warning(self, "Uyarı", "Bu kullanıcı adı zaten alınmış.")
            return False
        elif e_posta in mailler:
            QMessageBox.warning(self, "Uyarı", "Bu E-posta zaten alınmış.")
            return False
        elif cep_telefonu in numaralar:
            QMessageBox.warning(self, "Uyarı", "Bu telefon numarası zaten alınmış.")
            return False
        else:
            with open("database/kullanicilar.txt", "a", encoding='utf-8') as dosya:
                dosya.write(ad_soyad + "-" + kullanici_adi + "-" + e_posta + "-" + cep_telefonu + "-" + sifre + "\n")
            return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec())
