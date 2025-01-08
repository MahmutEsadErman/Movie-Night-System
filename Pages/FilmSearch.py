import sys

from PySide6.QtGui import QPixmap, QImage, QPainter, QPainterPath
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel, QInputDialog, \
    QSizePolicy, QDialog
from PySide6.QtCore import QFile, Qt, QEvent, QByteArray

from Pages.Trailer import TrailerWidget


class FilmSearch(QDialog):
    def __init__(self, parent=None, db_connection=None, event_id=None):
        super().__init__(parent)
        self.parent = parent
        self.db_connection = db_connection
        self.event_id = event_id
        # Load the ui file
        if __name__ == "__main__":
            ui_file_name = "../uifolder/FilmSearch.ui"
        else:
            ui_file_name = "uifolder/FilmSearch.ui"
        ui_file = QFile(ui_file_name)
        self.ui = QUiLoader().load(ui_file)
        ui_file.close()

        self.setWindowTitle("Film Arama")

        layout = QVBoxLayout()
        layout.addWidget(self.ui)
        self.setLayout(layout)

        # Button Functions
        self.ui.search_btn.clicked.connect(self.search)

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
        self.film = None

        # Set Container stylesheet
        with open("uifolder/film_box.qss", "r") as stylesheet:
            self.containerStyleSheet = stylesheet.read()

        self.oldtarget = QWidget()

        self.initialize_films()

    # WIP - Bu fonksiyonu daha sonra düzenleyeceğiz
    def search(self):
        
        # Kullanıcının arama çubuğuna yazdığı metni alın
        search_text = self.ui.search_le.text()

        # SQL sorgusunu oluşturun
        query = """
            SELECT f_id, f_adi, f_resim, fragman_url 
            FROM filmler
            WHERE f_adi LIKE %s
        """
        try:
            # Eski filmleri temizle
            for i in reversed(range(self.filmsWidget.layout().count())):
                widget = self.filmsWidget.layout().itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            self.films = {}
            self.films_no = 0
            self.row = 0
            self.column = 0

            cursor = self.db_connection.cursor()
            # '%search_text%' ile arama yapın
            cursor.execute(query, (f"%{search_text}%",))
            films = cursor.fetchall()

            # Filmleri ekleyin
            for film in films:
                f_id, f_adi, f_resim, fragman_url = film
                byte_array = QByteArray(bytes(f_resim))
                # Create QImage from QByteArray
                image = QImage()
                image.loadFromData(byte_array)

                # Oyları sorgula
                vote_query = """
                SELECT oylar
                FROM e_film_liste
                WHERE f_idf = %s
                """
                cursor.execute(vote_query, (f_id,))
                vote = cursor.fetchone()

                # Filmi ekle
                self.add_film(image, f_adi, fragman_url, f_id, vote)
                
        except Exception as e:
            print(f"Error searching films: {e}")
        finally:
            cursor.close()

    # WIP - Bu fonksiyonu daha sonra düzenleyeceğiz
    def initialize_films(self):

        query = """
            SELECT f_id, f_adi, f_resim, fragman_url 
            FROM filmler
        """

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(query)
            films = cursor.fetchall()

            # Add films to the UI
            for film in films:
                f_id, f_adi, f_resim, fragman_url = film
                byte_array = QByteArray(bytes(f_resim))
                # Create QImage from QByteArray
                image = QImage()
                image.loadFromData(byte_array)

                vote_query = """
                SELECT oylar
                FROM e_film_liste
                WHERE f_idf = %s
                """
                cursor.execute(vote_query, (f_id,))
                vote = cursor.fetchone()

                self.add_film(image, f_adi, fragman_url, f_id, vote)

        except Exception as e:
            print(f"Error loading films: {e}")
        finally:
            cursor.close()



        #paul_url = "https://www.youtube.com/embed/QC3sDbVcAbw?si=GRM0H7NBIhLTMeHH"
        #for i in range(10):
        #    self.add_film(QImage("database/deneme.jpg"), "ayı filmi", paul_url)

    # WIP - Bu fonksiyonu daha sonra düzenleyeceğim
    def add_film(self, image, name, url, id, vote):
        # Create a new target
        self.films_no += 1
        self.films[self.films_no] = {"image": image, "name": name, "vote_no": vote[0], "url": url, "id": id}
        # Create a container widget for the target
        film_box = self.create_film_box(f"film{self.films_no}", QPixmap.fromImage(image), name)

        # Add the film_box widget to the grid layout
        self.filmsWidget.layout().addWidget(film_box, self.row, self.column)

        self.column += 1
        if self.column > 3:  # Adjust this value to change the number of columns
            self.column = 0
            self.row += 1

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
        #vote_label = QLabel(str(0))
        #vote_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        #layout.addWidget(vote_label)

        # Set click event for container
        film_box.installEventFilter(self)

        return film_box

    # WIP
    def eventFilter(self, obj, event):
        if not obj.objectName().find("film"):
            # When double clicked open a new window
            if event.type() == QEvent.MouseButtonDblClick:
                no = int(obj.objectName().lstrip("film"))
                dialog = TrailerWidget(url=self.films[no]["url"])
                if dialog.exec() == QDialog.Accepted:
                    self.film = self.films[no]
                    self.accept()


        return super().eventFilter(obj, event)

    def exec(self):
        super().exec()
        return self.film

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FilmSearch()
    window.show()
    sys.exit(app.exec())