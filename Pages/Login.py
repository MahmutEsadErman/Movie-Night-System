import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QFile

from Pages.UpdateData import UpdateData


class LoginWindow(QMainWindow):
    def __init__(self, parent=None, db_connection=None):
        super().__init__(parent)
        self.parent = parent

        self.db_connection = db_connection

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
        self.ui.register_btn.clicked.connect(lambda: self.parent.goto_page(self.parent.registerWindow))

    # WIP - This function will be changed
    def login(self):
        success, k_id = self.giris_yap()
        if success:
            self.k_id = k_id
            self.parent.mainmenu.kullanici_id = k_id
            self.parent.goto_page(self.parent.mainmenu)
            # Initialize the update_data thread
            self.parent.data_thread.kullanici_id = k_id
            self.parent.data_thread.start()


        else:
            QMessageBox.warning(self, "Hata", "E-Posta veya şifre yanlış!")

    def giris_yap(self):
        e_posta = self.ui.email_le.text()
        sifre = self.ui.password_le.text()

        try:
            # Veritabanında kullanıcı doğrulama
            cursor = self.db_connection.cursor()

            query = """
                SELECT email, sifre_hash, k_id 
                FROM kullanici 
                WHERE email = %s AND sifre_hash = %s
            """

            cursor.execute(query, (e_posta, sifre))
            result = cursor.fetchone()

            if result:
                k_id = result[2]
                return True, k_id
            else:
                return False, None

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabani hatasi: {e}")
            return False, None

        finally:
            cursor.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
