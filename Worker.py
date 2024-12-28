import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox

from General.LoginWindow import LoginWindow
from Worker.MainMenu import MainMenu
from Worker.OrdersWindow import OrdersWindow
from Worker.StockWindow import StockWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window Title
        self.setWindowTitle("Restoran Sistemi (Worker)")

        # Set initial windows size
        self.screenSize = QApplication.primaryScreen().size()
        self.resize(800, 640)

        # Move Window to Center
        self.move(self.screenSize.width() / 2, self.screenSize.height() / 2)

        # Setting Pages
        self.stackedWidget = QStackedWidget()
        self.loginWindow = LoginWindow()
        self.mainmenu = MainMenu()
        self.orderswindow = OrdersWindow()
        self.stockwindow = StockWindow()

        self.stackedWidget.addWidget(self.loginWindow)
        self.stackedWidget.addWidget(self.mainmenu)
        self.stackedWidget.addWidget(self.orderswindow)
        self.stackedWidget.addWidget(self.stockwindow)
        self.stackedWidget.setCurrentWidget(self.loginWindow)

        # Add Stacked Widget to the layout
        self.setCentralWidget(self.stackedWidget)

        #  SET BUTTONS
        #  Main Menu
        self.mainmenu.ui.button1.clicked.connect(lambda: self.gotoPage(self.orderswindow))
        self.mainmenu.ui.button2.clicked.connect(lambda: self.gotoPage(self.stockwindow))
        self.mainmenu.ui.button4.clicked.connect(lambda: self.gotoPage(self.loginWindow))
        #  Login Window
        self.loginWindow.ui.login_button.clicked.connect(self.login)
        self.loginWindow.ui.register_button.hide()
        #  Stock Window
        self.stockwindow.ui.back_button.clicked.connect(lambda: self.gotoPage(self.mainmenu))
        #  Orders Window
        self.orderswindow.back_button.clicked.connect(lambda: self.gotoPage(self.mainmenu))

    def gotoPage(self, window):
        self.stackedWidget.setCurrentWidget(window)

    def login(self):
        success, k_adi = self.loginWindow.girisYap("worker")
        if success:
            self.gotoPage(self.mainmenu)
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
