import sys

from PySide6.QtGui import QPixmap, QImage
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout, QLabel
from PySide6.QtCore import QFile, Qt, QEvent


class Room(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
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
        self.ui.add_film_btn.clicked.connect(lambda: self.add_film(QImage("../database/deneme.jpg"),"ayı filmi"))

        # Set Widget inside Film Scroll Area
        self.filmsWidget = QWidget()
        self.filmsWidget.setLayout(QGridLayout())
        self.filmsWidget.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.row = 0
        self.column = 0
        self.ui.films_sa.setWidget(self.filmsWidget)

        # Targets Dictionary
        self.films = {}
        self.number_of_films = 0

        # Set Container stylesheet varible
        self.containerStyleSheet = """QWidget:hover{border: 2px solid rgb(64, 71, 88);} QLabel::hover{border: 0px;}"""

        self.oldtarget = QWidget()

        # Set Widget inside Mobile Scroll Area
        # self.usersWidget = QWidget()
        # self.usersWidget.setLayout(QVBoxLayout())
        # self.usersWidget.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)
        # self.users_scrollarea.setWidget(self.usersWidget)

    def add_film(self, image, name):
        # Create a new target
        self.number_of_films += 1
        self.films[self.number_of_films] = {"image": image, "name": name, "vote_no": 0}

        # Create a container widget for the target
        container = self.create_container(f"film{self.number_of_films}", QPixmap.fromImage(image), name)

        # Add the container widget to the grid layout
        self.filmsWidget.layout().addWidget(container, self.row, self.column)

        self.column += 1
        if self.column > 5:  # Adjust this value to change the number of columns
            self.column = 0
            self.row += 1

    def create_container(self, objectname, pixmap, name):
        # Create a QWidget to hold both labels
        container = QWidget(objectName=objectname)
        layout = QVBoxLayout()
        container.setLayout(layout)
        container.setStyleSheet(self.containerStyleSheet)
        container.setMinimumSize(80, 80)
        container.setMaximumSize(150, 150)

        # Create the image label
        scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation)
        image_label = QLabel()
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
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
        container.installEventFilter(self)

        return container

    # WIP
    def eventFilter(self, obj, event):
        if obj.objectName()[:-1] == "film":
            # When double clicked open a new window
            if event.type() == QEvent.MouseButtonDblClick:
                no = int(obj.objectName()[-1])
                self.newWindow = QWidget()
                self.newWindow.show()
        elif obj.objectName()[:-1] == "user":
            if event.type() == QEvent.MouseButtonDblClick:
                no = int(obj.objectName()[-1])
                self.newWindow = QWidget()
                self.newWindow.show()

        # When clicked change the border color
        if event.type() == QEvent.MouseButtonPress:
            if event.buttons() == Qt.LeftButton:
                self.oldtarget.setStyleSheet(self.containerStyleSheet)
                obj.setStyleSheet("""
                    QWidget{border: 2px solid rgb(64, 71, 88);}
                    QLabel{border: 0px;}
                            """)
                self.oldtarget = obj
                return True

        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Room()
    window.show()
    sys.exit(app.exec())
