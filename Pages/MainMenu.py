import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile


class MainMenu(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        # Load the ui file
        if __name__ == "__main__":
            ui_file_name = "../uifolder/Mainmenu.ui"
        else:
            ui_file_name = "uifolder/Mainmenu.ui"
        ui_file = QFile(ui_file_name)
        self.ui = QUiLoader().load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)

        self.ui.new_room_btn.clicked.connect(lambda: self.parent.goto_page(self.parent.roomPage))
        self.ui.join_btn.clicked.connect(lambda: self.parent.goto_page(self.parent.roomPage))
        self.ui.exit_btn.clicked.connect(lambda: self.parent.goto_page(self.parent.loginWindow))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec())
