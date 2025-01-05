import sys
import psycopg2

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QFile


class RegisterWindow(QMainWindow):
    def __init__(self, parent=None, db_connection=None):
        super().__init__(parent)
        self.parent = parent

        self.db_connection = db_connection

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

        ad = self.ui.name_le.text()

        soyad = self.ui.surname_le.text()

        e_posta = self.ui.email_le.text()

        sifre = self.ui.password_le.text()

        try:
            # Veritabanı bağlantısı

            cursor = self.db_connection.cursor()

            # Kullanıcı adı kontrolü
            cursor.execute("SELECT COUNT(*) FROM kullanici WHERE email = %s", (e_posta,))
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Uyarı", "Bu e posta zaten alınmış.")
                return False

            # Yeni kullanıcıyı ekleme
            query = """
                INSERT INTO kullanici (fname, lname, email, sifre_hash) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (ad, soyad, e_posta, sifre))
            self.db_connection.commit()

            return True
        
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {str(e)}")
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec())
