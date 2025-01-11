import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QVBoxLayout, QLabel, QPushButton, \
    QHBoxLayout
from PySide6.QtCore import QFile, Qt


class MainMenu(QMainWindow):
    def __init__(self, parent=None, db_connection=None, kullanici_id=None):
        super().__init__(parent)
        self.parent = parent

        self.db_connection = db_connection
        self.kullanici_id = kullanici_id
        self.room_list = []

        # Load the ui file
        if __name__ == "__main__":
            ui_file_name = "../uifolder/Mainmenu.ui"
        else:
            ui_file_name = "uifolder/Mainmenu.ui"
        ui_file = QFile(ui_file_name)
        self.ui = QUiLoader().load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

        # Button functions
        self.ui.new_room_btn.clicked.connect(self.add_event)
        self.ui.join_btn.clicked.connect(lambda: self.join_event(self.ui.room_id_le.text(), False))
        self.ui.exit_btn.clicked.connect(lambda: self.parent.goto_page(self.parent.loginWindow))

        # Set Widget inside Film Scroll Area
        self.invitation_widget = QWidget()
        self.invitation_widget.setObjectName("widget")
        self.invitation_widget.setLayout(QVBoxLayout())
        self.invitation_widget.layout().setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.ui.invitation_sa.setWidget(self.invitation_widget)

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
            self.parent.data_thread.event_id = event_id
            self.parent.goto_page(self.parent.roomPage)
    
    def join_event(self, room_id, is_invitation=False):

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
                if is_invitation:
                    self.delete_invitation(room_id)

                # Oda bulunduysa, ilgili odaya geçiş yap
                self.parent.roomPage.kullanici_id = self.kullanici_id
                self.parent.roomPage.event_id = room_id
                self.parent.data_thread.event_id = room_id
                self.parent.goto_page(self.parent.roomPage)  # Oda sayfasına geçiş
            else:

                # Oda bulunamadıysa, hata mesajı göster
                QMessageBox.warning(self, "Hata", "Girilen Oda ID'si bulunamadı!")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Odaya katılma sırasında bir hata oluştu: {e}")

        finally:
            cursor.close()

    def add_invitation(self, room_id):
        # Do not add the same room twice
        if room_id in self.room_list:
            return

        print("Adding invitation to the list")
        self.room_list.append(room_id)
        # Create a container widget for the target
        invitation_box = self.create_invitation_box(room_id)

        # Add the invitation_box widget to the grid layout
        self.invitation_widget.layout().addWidget(invitation_box)

    def create_invitation_box(self, room_id):
        inv_box = QWidget(objectName="oda"+str(room_id), styleSheet="QWidget#oda"+str(room_id)+"{background-color: #2c3a50; border-radius: 10px;}")
        inv_box.setProperty("room_id", room_id)
        layout = QVBoxLayout()
        inv_box.setLayout(layout)
        layout.addWidget(QLabel(f"Oda ID: {room_id}", alignment=Qt.AlignCenter, styleSheet="color: white;"))
        self.setStyleSheet("")
        btn_frame = QWidget(objectName="oda"+str(room_id))
        btn_frame.setLayout(QHBoxLayout())
        join_btn = QPushButton(text="Katıl", styleSheet="margin: 3px;")
        join_btn.setMinimumSize(80, 20)
        join_btn.clicked.connect(lambda: self.join_event(room_id,True))
        btn_frame.layout().addWidget(join_btn)
        delete_btn = QPushButton(text="Sil", styleSheet="margin: 3px;")
        delete_btn.setMinimumSize(50, 20)
        delete_btn.clicked.connect(lambda: inv_box.deleteLater())
        delete_btn.clicked.connect(lambda: self.delete_invitation(room_id))
        btn_frame.layout().addWidget(delete_btn)

        layout.addWidget(btn_frame)

        return inv_box

    def remove_invitation(self, room_id):
        # Check if the room_id exists in the list
        if room_id not in self.room_list:
            return

        print("Removing invitation from the list")
        self.room_list.remove(room_id)

        # Iterate over all widgets in the layout to find the one with the given room_id
        layout = self.invitation_widget.layout()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None and widget.property("room_id") == room_id:
                # Remove the widget from the layout
                layout.takeAt(i)
                widget.deleteLater()  # Delete the widget to free up memory
                break
        
    def delete_invitation(self, room_id):
        self.remove_invitation(room_id)
        try:
            
            cursor = self.db_connection.cursor()
            query = """
                Delete from davetliler
                where e_idnum = %s;
            """
            cursor.execute(query, (room_id,))
            self.db_connection.commit()
        except Exception as e:
            print(f"Error deleting invitation: {e}")

        finally:
            cursor.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec())
