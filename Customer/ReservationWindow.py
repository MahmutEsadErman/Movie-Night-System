import sys
from datetime import datetime

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Qt, QFile, QDateTime


class ReservationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.k_adi = None

        # Load the ui file
        if __name__ == "__main__":
            ui_file_name = "../uifolder/Reservation.ui"
        else:
            ui_file_name = "uifolder/Reservation.ui"

        ui_file = QFile(ui_file_name)
        self.ui = QUiLoader().load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

    def end_reservation(self):

        selected_date = self.ui.calendarWidget.selectedDate()
        selected_time = self.ui.timeEdit.time()

        if self.is_datetime_before_current(selected_date, selected_time):
            QMessageBox.warning(self, "Hata", "Eski tarihe rezervasyon alınamaz!")
        else:
            QMessageBox.information(self, "Bilgi",
                                    "Rezervasyon işlemi başarılı!\nİsterseniz siparişi başka tarihte verebilirsiniz.")
            with open("database/aktif_siparisler.txt", "a", encoding='utf-8') as file:
                file.write(self.k_adi + "," + selected_date.toString('yyyy-MM-dd') + "," +
                           selected_time.toString("HH:mm") + ",x,x\n")
            with open("database/gelir.txt", "a", encoding='utf-8') as file:
                file.write(str(datetime.now().year) + " " + str(datetime.now().month) + " 100\n")

    def is_datetime_before_current(self, selected_date, selected_time):
        # Get the current datetime
        current_datetime = QDateTime.currentDateTime()

        # Combine the selected date and time into a QDateTime object
        selected_datetime = QDateTime(selected_date, selected_time)

        # Compare the selected datetime with the current datetime
        return selected_datetime < current_datetime

    def update_k_adi(self, k_adi):

        self.k_adi = k_adi


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReservationWindow()
    window.show()
    sys.exit(app.exec())
