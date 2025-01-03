import sys

from PySide6.QtGui import QPixmap, QImage, QPainter, QPainterPath
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel, QInputDialog, \
    QSizePolicy, QDialog
from PySide6.QtCore import QFile, Qt, QEvent

from Pages.Trailer import TrailerWidget


class FilmSearch(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
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
        pass

    # WIP - Bu fonksiyonu daha sonra düzenleyeceğiz
    def initialize_films(self):
        paul_url = "https://www.youtube.com/embed/QC3sDbVcAbw?si=GRM0H7NBIhLTMeHH"
        for i in range(10):
            self.add_film(QImage("database/deneme.jpg"), "ayı filmi", paul_url)

    # WIP - Bu fonksiyonu daha sonra düzenleyeceğim
    def add_film(self, image, name, url):
        # Create a new target
        self.films_no += 1
        self.films[self.films_no] = {"image": image, "name": name, "vote_no": 0, "url": url}

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
        vote_label = QLabel(str(0))
        vote_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        layout.addWidget(vote_label)

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
