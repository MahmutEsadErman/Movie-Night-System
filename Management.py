import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox

from Pages.Login import LoginWindow

from Management.MainMenu import MainMenu
from Management.CommentsWindow import CommentsWindow
from Management.ProductManagementWindow import ProductManagementWindow
from Management.ReportWindow import ReportWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window Title
        self.setWindowTitle("Restoran Sistemi (Yönetici)")

        # Set initial windows size
        self.screenSize = QApplication.primaryScreen().size()
        self.resize(800, 640)

        # Setting Pages
        self.stackedWidget = QStackedWidget()
        self.loginWindow = LoginWindow()
        self.mainmenu = MainMenu()
        self.commentswindow = CommentsWindow()
        self.productmanagementwindow = ProductManagementWindow()
        self.reportwindow = ReportWindow()

        self.stackedWidget.addWidget(self.loginWindow)
        self.stackedWidget.addWidget(self.mainmenu)
        self.stackedWidget.addWidget(self.commentswindow)
        self.stackedWidget.addWidget(self.productmanagementwindow)
        self.stackedWidget.addWidget(self.reportwindow)
        self.stackedWidget.setCurrentWidget(self.loginWindow)

        # Add Stacked Widget to the layout
        self.setCentralWidget(self.stackedWidget)

        #  SET BUTTONS
        #  Main Menu
        self.mainmenu.ui.button1.clicked.connect(lambda: self.gotoPage(self.productmanagementwindow))
        self.mainmenu.ui.button2.clicked.connect(lambda: self.gotoPage(self.commentswindow))
        self.mainmenu.ui.button3.clicked.connect(lambda: self.gotoPage(self.reportwindow))
        self.mainmenu.ui.button4.clicked.connect(lambda: self.gotoPage(self.loginWindow))
        #  Login Window
        self.loginWindow.ui.login_button.clicked.connect(self.login)
        self.loginWindow.ui.register_button.hide()
        #  Product Management Window
        self.productmanagementwindow.ui.back_button.clicked.connect(lambda: self.gotoPage(self.mainmenu))
        #  Comments Window
        self.commentswindow.back_button.clicked.connect(lambda: self.gotoPage(self.mainmenu))
        #  Report Window
        self.reportwindow.back_button.clicked.connect(lambda: self.gotoPage(self.mainmenu))

    def gotoPage(self, window):
        self.stackedWidget.setCurrentWidget(window)

    def login(self):
        success, k_adi = self.loginWindow.girisYap("manager")
        if success:
            self.gotoPage(self.mainmenu)
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
