import sys
import psycopg2

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox

from Pages.Login import LoginWindow
from Pages.Register import RegisterWindow
from Pages.MainMenu import MainMenu
from Pages.RoomPage import RoomPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        try:
            self.db_connection = psycopg2.connect(
                dbname="movie_night",
                user="postgres",
                password="halil123",
                host="localhost",
                port= "5432"
            )
            print("Veritabanına bağlantı başarılı!")

        except psycopg2.Error as e:

            print(f"Veritabanı bağlantı hatası: {e}")
            sys.exit(1)

        self.k_adi = None

        # Set Window Title
        self.setWindowTitle("Movie Night")

        # Set Stylesheet
        with open("uifolder/default stylesheet.qss", "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # Set initial windows size
        self.screenSize = QApplication.primaryScreen().size()
        self.resize(800, 640)

        # Setting Pages
        self.stackedWidget = QStackedWidget()
        self.loginWindow = LoginWindow(self, self.db_connection)
        self.registerWindow = RegisterWindow(self, self.db_connection)
        self.mainmenu = MainMenu(self, self.db_connection)
        self.roomPage = RoomPage(self, self.db_connection)

        self.stackedWidget.addWidget(self.loginWindow)
        self.stackedWidget.addWidget(self.registerWindow)
        self.stackedWidget.addWidget(self.mainmenu)
        self.stackedWidget.addWidget(self.roomPage)

        self.stackedWidget.setCurrentWidget(self.loginWindow)

        # Add Stacked Widget to the layout
        self.setCentralWidget(self.stackedWidget)

    def goto_page(self, window):
        self.stackedWidget.setCurrentWidget(window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
