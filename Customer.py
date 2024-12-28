import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox

from Customer.PaymentWindow import PaymentWindow
from General.LoginWindow import LoginWindow
from General.RegisterWindow import RegisterWindow
from Customer.MainMenu import MainMenu, OrderMenu
from Customer.OrderWindow import OrderWindow
from Customer.ReservationWindow import ReservationWindow
from Customer.HistoryWindow import HistoryWindow, OrderHistoryWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.k_adi = None

        # Set Window Title
        self.setWindowTitle("Restoran Sistemi (Müşteri)")

        # Set initial windows size
        self.screenSize = QApplication.primaryScreen().size()
        self.resize(800, 640)

        # Setting Pages
        self.stackedWidget = QStackedWidget()
        self.loginWindow = LoginWindow()
        self.mainmenu = MainMenu()
        self.registerWindow = RegisterWindow()
        self.orderWindow = OrderWindow()
        self.orderMenu = OrderMenu()
        self.reservationWindow = ReservationWindow()
        self.historyWindow = HistoryWindow()
        self.orderHistoryWindow = OrderHistoryWindow(self.go_order_window)
        self.paymentWindow = PaymentWindow()

        self.stackedWidget.addWidget(self.loginWindow)
        self.stackedWidget.addWidget(self.registerWindow)
        self.stackedWidget.addWidget(self.mainmenu)
        self.stackedWidget.addWidget(self.orderWindow)
        self.stackedWidget.addWidget(self.reservationWindow)
        self.stackedWidget.addWidget(self.historyWindow)
        self.stackedWidget.addWidget(self.orderMenu)
        self.stackedWidget.addWidget(self.orderHistoryWindow)
        self.stackedWidget.addWidget(self.paymentWindow)
        self.stackedWidget.setCurrentWidget(self.loginWindow)


        # Add Stacked Widget to the layout
        self.setCentralWidget(self.stackedWidget)

        #  SET BUTTONS FUNCTIONS
        # Login Window
        self.loginWindow.ui.login_button.clicked.connect(self.login)
        self.loginWindow.ui.register_button.clicked.connect(lambda: self.gotoPage(self.registerWindow))
        # Register Window
        self.registerWindow.ui.signup_button.clicked.connect(self.register)
        self.registerWindow.ui.login_button.clicked.connect(lambda: self.gotoPage(self.loginWindow))
        # MainMenu Window
        self.mainmenu.ui.button1.clicked.connect(lambda: self.gotoPage(self.reservationWindow))
        self.mainmenu.ui.button2.clicked.connect(lambda: self.gotoPage(self.orderMenu))
        self.mainmenu.ui.button3.clicked.connect(lambda: self.gotoPage(self.historyWindow))
        self.mainmenu.ui.button4.clicked.connect(lambda: self.gotoPage(self.loginWindow))
        # Order Window
        self.orderWindow.ui.back_button.clicked.connect(lambda: self.gotoPage(self.orderMenu))
        self.orderMenu.ui.button1.clicked.connect(self.instant_order)
        self.orderMenu.ui.button2.clicked.connect(lambda: self.gotoPage(self.orderHistoryWindow))
        self.orderMenu.ui.button4.clicked.connect(lambda: self.gotoPage(self.mainmenu))
        self.orderWindow.ui.order_button.clicked.connect(lambda: self.gotoPage(self.paymentWindow))
        # Reservation Window
        self.reservationWindow.ui.back_button.clicked.connect(lambda: self.gotoPage(self.mainmenu))
        self.reservationWindow.ui.signup_button.clicked.connect(self.reservation)
        # History Window
        self.historyWindow.back_button.clicked.connect(lambda: self.gotoPage(self.mainmenu))
        self.orderHistoryWindow.back_button.clicked.connect(lambda: self.gotoPage(self.orderMenu))
        # Payment Window
        self.paymentWindow.ui.odeme_butonu.clicked.connect(self.pay)
        self.paymentWindow.ui.exit_button.clicked.connect(lambda: self.gotoPage(self.orderWindow))

    def register(self):
        if self.registerWindow.uyeOl():
            self.gotoPage(self.loginWindow)

    def login(self):
        success, k_adi = self.loginWindow.girisYap("customer")
        if success:
            self.k_adi = k_adi
            self.gotoPage(self.mainmenu)

            self.orderWindow.k_adi = k_adi

            self.historyWindow.k_adi = k_adi
            self.historyWindow.update_k_adi(k_adi)

            self.orderHistoryWindow.k_adi = k_adi
            self.orderHistoryWindow.update_k_adi(k_adi)

            self.reservationWindow.k_adi = k_adi
            self.reservationWindow.update_k_adi(k_adi)

        else:
            QMessageBox.warning(self, "Hata", "E-Posta veya şifre yanlış!")

    def reservation(self):
        if self.reservationWindow.end_reservation():
            self.gotoPage(self.orderWindow)

    def instant_order(self):
        self.orderWindow.order_type = 0
        self.gotoPage(self.orderWindow)

    def go_order_window(self, order):
        self.orderWindow.order_type = 1
        self.orderWindow.selected_order = order
        self.gotoPage(self.orderWindow)

    def pay(self):
        if not self.orderWindow.bosMu():
            self.orderWindow.siparisVer()
            self.stackedWidget.setCurrentWidget(self.mainmenu)
            self.orderHistoryWindow.load_orders()

    def gotoPage(self, window):
        self.stackedWidget.setCurrentWidget(window)

        if window == self.historyWindow:
            self.historyWindow.load_orders()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
