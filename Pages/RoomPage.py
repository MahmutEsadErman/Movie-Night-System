import sys

from PySide6.QtGui import QPixmap, QImage, QPainter, QPainterPath
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout, QLabel, QInputDialog, \
    QSizePolicy, QDialog, QMessageBox
from PySide6.QtCore import QFile, Qt, QEvent, QByteArray

from Pages.FilmSearch import FilmSearch
from Pages.Trailer import TrailerWidget

from io import BytesIO


def create_circular_image_label(pixmap, size):
    # Create a circular mask
    mask = QPixmap(size, size)
    mask.fill(Qt.transparent)
    painter = QPainter(mask)
    painter.setRenderHint(QPainter.Antialiasing)
    path = QPainterPath()
    path.addEllipse(0, 0, size, size)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, size, size, pixmap)
    painter.end()

    # Create a QLabel and set the masked pixmap
    label = QLabel()
    label.setPixmap(mask)
    return label


class RoomPage(QMainWindow):
    def __init__(self, parent=None, db_connection=None, kullanici_id= None, event_id = None):
        super().__init__(parent)
        self.parent = parent
        self.db_connection = db_connection
        self.kullanici_id = kullanici_id
        self.event_id = event_id
        # Load the ui file
        if __name__ == "__main__":
            ui_file_name = "../uifolder/Room.ui"
        else:
            ui_file_name = "uifolder/Room.ui"
        ui_file = QFile(ui_file_name)
        self.ui = QUiLoader().load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

        # Button Functions
        paul_url = "https://www.youtube.com/embed/QC3sDbVcAbw?si=GRM0H7NBIhLTMeHH"
        self.ui.add_film_btn.clicked.connect(self.choose_film)
        self.ui.invite_btn.clicked.connect(self.invite_friend)
        self.ui.exit_btn.clicked.connect(self.exit)

        # Set Widget inside Film Scroll Area
        self.filmsWidget = QWidget()
        self.filmsWidget.setObjectName("films_widget")
        self.filmsWidget.setLayout(QGridLayout())
        self.filmsWidget.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.row = 0
        self.column = 0
        self.ui.films_sa.setWidget(self.filmsWidget)

        # Dictionaries
        self.films = {}
        self.films_no = 0
        self.friends = {}
        self.friends_no = 0

        # Set Container stylesheet
        with open("uifolder/film_box.qss", "r") as stylesheet:
            self.containerStyleSheet = stylesheet.read()

        self.oldtarget = QWidget()

        # Set Widget inside Friends Scroll Area
        self.friendsWidget = QWidget()
        self.friendsWidget.setLayout(QGridLayout())
        self.friendsWidget.layout().setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.ui.friends_sa.setWidget(self.friendsWidget)


    def showEvent(self, event):
        # RoomPage açıldığında filmleri yükle
        self.load_films_for_event()  # Bu satırda fonksiyon çağrılıyor
        super().showEvent(event)  # Super sınıfın showEvent fonksiyonunu çağır

    def vote_film(self, no):
        pass

    def choose_film(self):

        new_dialog = FilmSearch(self, self.db_connection)
        film = new_dialog.exec()
        if film:
            # Film seçildiğinde, veritabanına kaydediyoruz
            self.add_film(film)
            
            cursor = self.db_connection.cursor()
            try:
                # Seçilen filmi e_film_liste tablosuna ekle
                insert_query = """
                INSERT INTO e_film_liste (e_idf, f_idf, oylar) 
                VALUES (%s, %s, %s);
                """

                cursor.execute(insert_query, (self.event_id, film["id"], 0))  
                self.db_connection.commit()
            except Exception as e:
                self.db_connection.rollback()
                QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")
            finally:
                cursor.close()
    
    def load_films_for_event(self):
        cursor = self.db_connection.cursor()
        try:
            # Etkinlikteki filmleri e_film_liste tablosundan al
            select_query = """
            SELECT f.f_id, f.f_adi, f.f_resim, f.fragman_url, ef.oylar
            FROM e_film_liste ef, filmler f
            WHERE ef.e_idf = %s and ef.f_idf = f.f_id;
            """
            cursor.execute(select_query, (self.event_id,))
            films = cursor.fetchall()

            # Filmleri ekle
            for film in films:
                
                f_id, f_adi, f_resim, fragman_url, oylar = film
                byte_array = QByteArray(bytes(f_resim))
                # Create QImage from QByteArray
                image = QImage()
                image.loadFromData(byte_array)
                self.add_film({"image": image,"name": f_adi, "vote_no": oylar, "url": fragman_url, "id": f_id})  # QImage nesnesini kullan})

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")
        finally:
            cursor.close()
    
    def exit(self):

        cursor = self.db_connection.cursor()

        try:
            # Kullanıcıyı katılımcı tablosundan sil
            delete_participant_query = """
            DELETE FROM katilimci 
            WHERE k_idnum = %s and e_idnum = %s;
            """
            cursor.execute(delete_participant_query, (self.kullanici_id, self.event_id))
            self.db_connection.commit()

        except Exception as e:
            self.db_connection.rollback()
            QMessageBox.critical(self, "Hata", f"Veritabani hatasi: {e}")

        finally:
            cursor.close()


        self.clear_films()

        # Ana menüye dön
        self.parent.goto_page(self.parent.mainmenu)

    def clear_films(self):
        # self.filmsWidget'teki tüm widget'ları temizle
        for i in reversed(range(self.filmsWidget.layout().count())):
            widget = self.filmsWidget.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Widget'ı kaldır

        # Film listelerini sıfırla
        self.films.clear()
        self.films_no = 0
        self.row = 0
        self.column = 0


    # WIP - Bu fonksiyonu daha sonra düzenleyeceğim
    def invite_friend(self):
        # ok, msg = QInputDialog.getText(self, "Invite", "Enter the username:")
        ok = True
        if ok:
            # Add the user to the list
            self.add_friend(QImage("database/esad.jpg"), "ahmet")

    # WIP - Bu fonksiyonu daha sonra düzenleyeceğim
    def add_film(self, film):
        # Create a new target
        self.films_no += 1
        self.films[self.films_no] = film

        # Create a container widget for the target
        film_box = self.create_film_box(f"film{self.films_no}", QPixmap.fromImage(film["image"]), film["name"])

        # Add the film_box widget to the grid layout
        self.filmsWidget.layout().addWidget(film_box, self.row, self.column)

        self.column += 1
        if self.column > 3:  # Adjust this value to change the number of columns
            self.column = 0
            self.row += 1

    def add_friend(self, image, name):
        # Create a new target
        self.friends[self.friends_no] = {"image": image, "name": name}

        # Create a container widget for the target
        friend_box = self.create_friend_box(f"friend{self.friends_no}", QPixmap.fromImage(image), name)

        # Add the container widget to the grid layout
        self.friendsWidget.layout().addWidget(friend_box, 0, self.friends_no)
        self.friends_no += 1

    def create_film_box(self, objectname, pixmap, name):
        # Create a QWidget to hold both labels
        film_box = QWidget(objectName=objectname)
        layout = QVBoxLayout()
        film_box.setLayout(layout)
        film_box.setStyleSheet(self.containerStyleSheet)
        film_box.setMinimumSize(200, 250)
        film_box.setMaximumSize(200, 200)

        # Create the image label
        scaled_pixmap = pixmap.scaled(180, 220, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation)
        image_label = QLabel()
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        image_label.sizePolicy().setVerticalPolicy(QSizePolicy.Expanding)
        layout.addWidget(image_label)

        # Create the text label
        name_label = QLabel(str(name))
        name_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        layout.addWidget(name_label)

        # Create the text label
        vote_label = QLabel(str(0))
        vote_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        layout.addWidget(vote_label)

        # Set click event for container
        film_box.installEventFilter(self)

        return film_box

    def create_friend_box(self, objectname, pixmap, name):
        # Create a QWidget to hold both labels
        friend_box = QWidget(objectName=objectname)
        layout = QVBoxLayout()
        friend_box.setLayout(layout)
        friend_box.setStyleSheet(self.containerStyleSheet)
        friend_box.setMinimumSize(90, 90)
        friend_box.setMaximumSize(120, 120)

        # Create the image label
        scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        image_label = create_circular_image_label(scaled_pixmap, 50)
        image_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        layout.addWidget(image_label)

        # Create the text label
        name_label = QLabel(str(name))
        name_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        layout.addWidget(name_label)

        # Set click event for container
        friend_box.installEventFilter(self)

        return friend_box

    # WIP
    def eventFilter(self, obj, event):

        if not obj.objectName().find("film"):
            # When double clicked open a new window
            if event.type() == QEvent.MouseButtonDblClick:
                no = int(obj.objectName().lstrip("film"))
                dialog = TrailerWidget(url=self.films[no]["url"])
                if dialog.exec() == QDialog.Accepted:
                    self.vote_film(no)

        # When clicked change the border color
        if event.type() == QEvent.MouseButtonPress:
            if event.buttons() == Qt.LeftButton:
                self.oldtarget.setStyleSheet(self.containerStyleSheet)
                obj.setStyleSheet("""
                    QWidget{border: 2px solid rgb(64, 71, 88);border-radius: 10px;color: white; background-color: rgba(39, 44, 54, 120);}
                    QLabel{border: 0px;}
                            """)
                self.oldtarget = obj
                return True

        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoomPage()
    window.show()
    sys.exit(app.exec())
