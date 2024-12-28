import sys
from datetime import datetime

from PySide6.QtGui import QColor, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, \
    QInputDialog, QItemDelegate, QHeaderView
from PySide6.QtCore import QFile

class StockWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the ui file
        if __name__ == "__main__":
            ui_file_name = "../uifolder/ProductManagement.ui"
        else:
            ui_file_name = "uifolder/ProductManagement.ui"
        ui_file = QFile(ui_file_name)
        self.ui = QUiLoader().load(ui_file)
        self.setCentralWidget(self.ui)
        ui_file.close()

        foods = []
        adetler = []

        with open("database/stoklar.txt", "r", encoding='utf-8') as file:
            for lines in file:
                line = lines.split(",")
                foods.append(line[0])
                adetler.append(line[1])

        # Set the table properties
        self.ui.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.table.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Set the table headers
        self.ui.table.setRowCount(len(foods))
        self.ui.table.setColumnCount(3)
        self.ui.table.setHorizontalHeaderLabels(("Ürün", "Adet", "Gider"))

        # Set the table items
        for i in range(len(foods)):
            self.ui.table.setItem(i, 0, QTableWidgetItem(foods[i]))
            self.ui.table.setItem(i, 1, QTableWidgetItem(adetler[i][:-1]))# sayıların sonundaki \n karakterini siler

        # Set button actions
        self.ui.add_button.clicked.connect(self.add_item)
        self.ui.remove_button.clicked.connect(self.remove_item)
        self.ui.save_button.clicked.connect(self.save_items)

    def add_item(self):
        self.ui.table.insertRow(self.ui.table.rowCount())

    def remove_item(self):
        self.ui.table.removeRow(self.ui.table.currentRow())

    # (WIP)
    def save_items(self):
        # Khalili

        gider = 0
        urunler = []
        fiyatlar = []

        with open("database/urun_fiyat.txt", "r", encoding='utf-8') as fiyatlar_file:
            for lines in fiyatlar_file:
                line = lines.split(",")
                urunler.append(line[0])
                fiyatlar.append(line[1])

        with open("database/urun_fiyat.txt", "w", encoding='utf-8') as fiyatlar_file:

            with open("database/stoklar.txt", "w", encoding='utf-8') as stoklar_file:
                for i in range(self.ui.table.rowCount()):
                    urun = self.ui.table.item(i, 0).text().rstrip()

                    if urun not in urunler:
                        fiyatlar.append("0")

                    if self.ui.table.item(i, 1) is not None:
                        adet = self.ui.table.item(i, 1).text().rstrip()
                    else:
                        adet = 0

                    if self.ui.table.item(i, 2) is not None and self.ui.table.item(i, 2) != '':
                        gider += int(self.ui.table.item(i, 2).text().rstrip())

                    stoklar_file.write(f"{urun},{adet}\n")
                    fiyatlar_file.write(f"{urun},{fiyatlar[i]}")

            with open("database/gider.txt", "a", encoding='utf-8') as giderler_file:
                giderler_file.write(str(datetime.now().year) + " " + str(datetime.now().month) + " " + str(gider) + "\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockWindow()
    window.show()
    sys.exit(app.exec())
