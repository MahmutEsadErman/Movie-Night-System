from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSizePolicy, QDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
import sys


class TrailerWidget(QDialog):
    def __init__(self, parent=None, url=""):
        super().__init__(parent)
        self.parent = parent

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

        self.button.clicked.connect(self.accept)

    def closeEvent(self, event):
        self.browser.setUrl("about:blank")
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    url = "https://www.youtube.com/embed/QC3sDbVcAbw?si=GRM0H7NBIhLTMeHH"
    window = TrailerWidget(url=url)
    window.show()
    sys.exit(app.exec())
