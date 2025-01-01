import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox

from Pages.Login import LoginWindow
from Pages.Register import RegisterWindow
from Pages.MainMenu import MainMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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
        self.loginWindow = LoginWindow(self)
        self.mainmenu = MainMenu(self)
        self.registerWindow = RegisterWindow(self)

        self.stackedWidget.addWidget(self.loginWindow)
        self.stackedWidget.addWidget(self.registerWindow)
        self.stackedWidget.addWidget(self.mainmenu)

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
