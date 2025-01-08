import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QFile
from Pages.CheckDavetliler import CheckDavetliler

class MainMenu(QMainWindow):
    def __init__(self, parent=None, db_connection=None, kullanici_id=None):
        super().__init__(parent)
        self.parent = parent

        self.db_connection = db_connection
        self.kullanici_id = kullanici_id

        # Load the ui file
        if __name__ == "__main__":
            ui_file_name = "../uifolder/Mainmenu.ui"
        else:
            ui_file_name = "uifolder/Mainmenu.ui"
        ui_file = QFile(ui_file_name)
        self.ui = QUiLoader().load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

        self.ui.new_room_btn.clicked.connect(self.add_event)
        self.ui.join_btn.clicked.connect(self.join_event)
        self.ui.exit_btn.clicked.connect(lambda: self.parent.goto_page(self.parent.loginWindow))


        # Start the davetliler check thread
        self.check_davetliler_thread = CheckDavetliler(self.db_connection, self.kullanici_id)
        self.check_davetliler_thread.result_signal.connect(self.handle_davetliler_check)
        self.check_davetliler_thread.start()
    
    def handle_davetliler_check(self, found, event_ids):
        if found:
            # Display the list of events the user is invited to
            event_ids_str = ", ".join(map(str, event_ids))
            QMessageBox.information(self, "Davetler", f"Bir etkinlikte davetlisiniz! Etkinlik ID'leri: {event_ids_str}")

    def add_event(self):

        try:
            # Veritabanına etkinlik ekle
            cursor = self.db_connection.cursor()
            query = """
                INSERT INTO etkinlik (kurucu_id)
                VALUES (%s)
                RETURNING e_id;
            """
            cursor.execute(query, (self.kullanici_id,))
            event_id = cursor.fetchone()[0]

            insert_katilimci_query = """
            INSERT INTO katilimci (e_idnum, k_idnum)
            VALUES (%s, %s);
            """
            cursor.execute(insert_katilimci_query, (event_id, self.kullanici_id))
            self.db_connection.commit()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabani hatasi: {e}")

        finally:
            cursor.close()
            self.parent.roomPage.kullanici_id = self.kullanici_id
            self.parent.roomPage.event_id = event_id
            self.parent.goto_page(self.parent.roomPage)

    def join_event(self):
        room_id = self.ui.room_id_le.text()

        try:
            # Veritabanında room_id kontrolü
            cursor = self.db_connection.cursor()
            query = """
                SELECT COUNT(*) 
                FROM etkinlik 
                WHERE e_id = %s
            """
            cursor.execute(query, (room_id,))
            result = cursor.fetchone()

            if result and result[0] > 0:

                insert_katilimci_query = """
                INSERT INTO katilimci (e_idnum, k_idnum)
                VALUES (%s, %s);
                """
                cursor.execute(insert_katilimci_query, (room_id, self.kullanici_id))
                self.db_connection.commit()

                # Oda bulunduysa, ilgili odaya geçiş yap
                self.parent.roomPage.kullanici_id = self.kullanici_id
                self.parent.roomPage.event_id = room_id
                self.parent.goto_page(self.parent.roomPage)  # Oda sayfasına geçiş
            else:

                # Oda bulunamadıysa, hata mesajı göster
                QMessageBox.warning(self, "Hata", "Girilen Oda ID'si bulunamadı!")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Odaya katılma sırasında bir hata oluştu: {e}")

        finally:
            cursor.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec())
