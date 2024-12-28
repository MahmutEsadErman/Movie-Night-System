import sys
import datetime

from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QVBoxLayout, QWidget, QTableWidgetItem, \
    QPushButton, QMessageBox, QAbstractItemView, QHeaderView
from PySide6.QtCore import QTimer


class OrdersWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Siparişler")

        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Tarih, Ürünler
        self.table.setHorizontalHeaderLabels(["Saat", "Ürünler", "Bitirme"])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.cell_double_click_event)

        # Back Button
        self.back_button = QPushButton("Geri dön")


        self.load_orders()  # Sipariş verilerini yükler
        self.order_timer = QTimer(self)
        self.order_timer.timeout.connect(self.load_orders)
        self.order_timer.start(1000)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.back_button)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def cell_double_click_event(self, row, column):
        QMessageBox.information(self, "Bilgi", self.table.item(row, column).text())

    def load_orders(self):
        data = []
        today = datetime.date.today().strftime("%Y-%m-%d")

        with open("database/aktif_siparisler.txt", "r", encoding='utf-8') as file:

            for satir in file:
                bilgiler = satir.strip().split(",")
                #map(str.rstrip, bilgiler)
                if bilgiler[3] != "x" and bilgiler[1] == today:
                    data.append({"date": bilgiler[2], "items": bilgiler[3]})

        self.table.setRowCount(len(data))
        for i, order in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(order["date"]))
            self.table.setItem(i, 1, QTableWidgetItem(order["items"]))

            # Add Comment Button
            btn_finalize = QPushButton('Bitti')
            btn_finalize.clicked.connect(lambda ch=True, row=i: self.finalize_order(row))
            self.table.setCellWidget(i, 2, btn_finalize)

    # (WIP) KHALİLİ  Garsonun Sistemi belli bir saniyede bir güncellenecekki yeni siparişler gözüksün
    # Bitti butonuna basıldığında siparişin bitirilmesini sağlar
    def finalize_order(self, row):
        with open("database/aktif_siparisler.txt", "r", encoding='utf-8') as file:
            orders = [line.strip().split(",") for line in file]

        order_to_remove = (self.table.item(row, 0).text(),  # date
                           self.table.item(row, 1).text())  # items

        for order in orders:
            if (order[2], order[3]) == order_to_remove:

                with open("database/siparisler.txt", "a", encoding='utf-8') as dosya:
                    dosya.write(order[0] + "," + order[1] + "," + order[2] + "," + order[3] + "," + order[4] + ",x\n")

                orders.remove(order)
                break

        with open("database/aktif_siparisler.txt", "w", encoding='utf-8') as dosya:
            for order in orders:
                dosya.write(",".join(order) + "\n")

        self.load_orders()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OrdersWindow()
    window.show()
    sys.exit(app.exec())
