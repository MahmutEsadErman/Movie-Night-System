from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSizePolicy, QDialog, QMessageBox
from PySide6.QtWebEngineWidgets import QWebEngineView
import sys


class TrailerWidget(QDialog):
    def __init__(self, parent=None, db_connection=None, url="", oy=False, event_id=None, f_id=None):
        super().__init__(parent)
        self.parent = parent

        self.db_connection = db_connection
        self.oy = oy
        self.event_id = event_id
        self.f_id = f_id

        self.setWindowTitle("Fragman")

        with open("uifolder/default stylesheet.qss", "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

        layout = QVBoxLayout()

        # QWebEngineView widget'ı
        self.browser = QWebEngineView()
        self.browser.setUrl(url)
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.browser)

        self.button = QPushButton("Seç")
        self.button.setMinimumWidth(150)
        self.button.setMaximumWidth(300)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        self.button.clicked.connect(self.on_button_click)

    
    def showEvent(self, event):
        super().showEvent(event)
        self.oy_ekrani()  # Trailer sayfası açıldığında tetiklenir

    def oy_ekrani(self):
        if self.oy:
            self.button.setText("Oy Ver")

    def on_button_click(self):
        if self.oy:

            cursor = self.db_connection.cursor()
            try:
                cursor.execute("""
                    UPDATE e_film_liste
                    SET oylar = oylar + 1
                    WHERE e_idf = %s AND f_idf  = %s
                """, (self.event_id, self.f_id))

                self.db_connection.commit()

            except Exception as e:
                self.db_connection.rollback()
                QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")
            finally:
                cursor.close()

        self.accept()

    def closeEvent(self, event):
        self.browser.setUrl("about:blank")
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    url = "https://www.youtube.com/embed/QC3sDbVcAbw?si=GRM0H7NBIhLTMeHH"
    window = TrailerWidget(url=url)
    window.show()
    sys.exit(app.exec())
