from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QMainWindow, QTableWidget, QVBoxLayout, QWidget, QTableWidgetItem, \
    QPushButton, QMessageBox, QAbstractItemView, QInputDialog, QHeaderView


class HistoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.k_adi = None

        self.setWindowTitle("Geçmiş Siparişler")

        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Tarih, Ürünler, Yorum Butonu
        self.table.setHorizontalHeaderLabels(["Tarih", "Ürünler", "Yorum"])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.cell_double_click_event)

        self.load_orders()  # Sipariş verilerini yükler

        # Back Button
        self.back_button = QPushButton("Geri dön")

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.back_button)
        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def cell_double_click_event(self, row, column):
        QMessageBox.information(self, "Bilgi", self.table.item(row, column).text())

    def load_orders(self):
        # Örnek veriler
        #*********************
        orders = []
        kullanici_orders = []
        with open("database/siparisler.txt", "r", encoding='utf-8') as file:

            for satir in file:
                bilgiler = satir.strip().split(",")
                map(str.rstrip, bilgiler)
                #!!!!!!!!!!!!!!!!!!!!!!!!
                orders.append({"k_adi": bilgiler[0], "date": bilgiler[1], "time": bilgiler[2], "items": bilgiler[3],
                               "fiyat": bilgiler[4], "yorum": bilgiler[5]})
                if bilgiler[0] == self.k_adi:
                    kullanici_orders.append({"k_adi": bilgiler[0], "date": bilgiler[1], "time": bilgiler[2],
                                             "items": bilgiler[3], "fiyat": bilgiler[4], "yorum": bilgiler[5]})

        self.table.setRowCount(len(kullanici_orders))
        for i, order in enumerate(kullanici_orders):

            self.table.setItem(i, 0, QTableWidgetItem(order["date"]))
            self.table.setItem(i, 1, QTableWidgetItem(order["items"]))

            if order["yorum"] == "x":
                # Add Comment Button
                btn_comment = QPushButton('Yorum Yap')
                btn_comment.clicked.connect(lambda ch=True, row=i: self.make_comment(row, orders, kullanici_orders))
                self.table.setCellWidget(i, 2, btn_comment)
            else:
                self.table.setItem(i, 2, QTableWidgetItem(order["yorum"]))

    # (WIP) Khalili
    def make_comment(self, row, orders, kullanici_orders):
        comment, ok = QInputDialog().getText(None, "Input Dialog", "Bir metin girin:")
        if ok and comment:
            self.table.setCellWidget(row, 2, None)
            self.table.setItem(row, 2, QTableWidgetItem(comment))

        # Save comment to the database

        if kullanici_orders[row] in orders:
            row_index = orders.index(kullanici_orders[row])
            orders[row_index]["yorum"] = comment

        with open("database/siparisler.txt", "w", encoding='utf-8') as file:
            for j in range(len(orders)):
                file.write(orders[j]["k_adi"] + "," + orders[j]["date"] + "," + orders[j]["time"] + "," + orders[j][
                    "items"] + "," + orders[j]["fiyat"] + "," + orders[j]["yorum"] + "\n")

    def update_k_adi(self, k_adi):
        self.k_adi = k_adi
        self.load_orders()


class OrderHistoryWindow(HistoryWindow):

    def __init__(self, go_order_page):
        super().__init__()

        # Function Pointer Yöntemiyle OrderWindow'a gitmek için
        self.go_order_page = go_order_page

        self.timer = QTimer()
        # Connect the timeout signal of the timer to the load_orders method
        self.timer.timeout.connect(self.load_orders)
        # Start the timer to trigger every 5 seconds
        self.timer.start(5000)

        self.k_adi = None

        self.setWindowTitle("Geçmiş Siparişler")

        self.table = QTableWidget()
        self.table.setColumnCount(4)  # Tarih, Ürünler, Yorum Butonu
        self.table.setHorizontalHeaderLabels(["Tarih", "Saat", "Sipariş Durumu", "Sipariş İptali"])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.cell_double_click_event)

        self.load_orders()  # Sipariş verilerini yükler

        # Back Button
        self.back_button = QPushButton("Geri dön")

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.back_button)
        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def cell_double_click_event(self, row, column):
        QMessageBox.information(self, "Bilgi", self.table.item(row, column).text())

    def load_orders(self):
        orders = []
        kullanici_orders = []
        with open("database/aktif_siparisler.txt", "r", encoding='utf-8') as file:

            for satir in file:
                bilgiler = satir.strip().split(",")
                map(str.rstrip, bilgiler)
                #!!!!!!!!!!!!!!!!!!!!!!!!
                orders.append({"k_adi": bilgiler[0], "tarih": bilgiler[1], "saat": bilgiler[2], "items": bilgiler[3],
                               "fiyat": bilgiler[4]})
                if bilgiler[0] == self.k_adi:
                    kullanici_orders.append(
                        {"k_adi": bilgiler[0], "tarih": bilgiler[1], "saat": bilgiler[2], "items": bilgiler[3],
                         "fiyat": bilgiler[4]})

        self.table.setRowCount(len(kullanici_orders))
        for i, order in enumerate(kullanici_orders):

            self.table.setItem(i, 0, QTableWidgetItem(order["tarih"]))
            self.table.setItem(i, 1, QTableWidgetItem(order["saat"]))

            # Add Cancel Button
            btn_cancel = QPushButton('İptal')
            btn_cancel.clicked.connect(lambda ch=True, row=i: self.delete_order(row))
            self.table.setCellWidget(i, 3, btn_cancel)

            if order["items"] == "x":
                # Add Comment Button
                btn_order = QPushButton('Sipariş Yap')
                btn_order.clicked.connect(lambda ch=True, x=order: self.go_order_page(x))
                self.table.setCellWidget(i, 2, btn_order)
            else:
                self.table.removeCellWidget(i, 2)
                self.table.setItem(i, 2, QTableWidgetItem("Sipariş Yapılmış"))

    def delete_order(self, row):
        with open("database/aktif_siparisler.txt", "r", encoding='utf-8') as file:
            orders = [line.strip().split(",") for line in file]
        order_to_remove = (self.table.item(row, 0).text(),
                           self.table.item(row, 1).text())
        for order in orders:
            if (order[1], order[2]) == order_to_remove:
                orders.remove(order)
                break
        with open("database/aktif_siparisler.txt", "w", encoding='utf-8') as dosya:
            for order in orders:
                dosya.write(",".join(order) + "\n")
        self.load_orders()

    def update_k_adi(self, k_adi):
        self.k_adi = k_adi
        self.load_orders()
