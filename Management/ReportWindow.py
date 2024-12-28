import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QComboBox, \
    QStackedWidget, QSpinBox

from Management import Raporlar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


# (Still WORK IN PROGRESS)
class ReportWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Back Button
        self.back_button = QPushButton("Geri dön")
        self.back_button.setMaximumSize(140, 50)

        # Plots Combobox
        self.plots_combobox = QComboBox()
        plots_names = ["Yıllık Gelir", "Yıllık Gider", "Yıllık Gelir-Gider", "Yemek Populerligi"]
        self.plots_combobox.addItems(plots_names)
        self.plots_combobox.currentIndexChanged.connect(self.change_plot)

        # Year Selection
        self.year_spinbox = QSpinBox()
        self.year_spinbox.setMinimum(2000)
        self.year_spinbox.setMaximum(2050)

        # Bottom Layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.back_button)
        bottom_layout.addWidget(self.year_spinbox)
        bottom_layout.addWidget(self.plots_combobox)
        bottom_frame = QWidget()
        bottom_frame.setLayout(bottom_layout)

        # Stacked Widget
        self.stackedWidget = QStackedWidget()
        self.plot = None

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(bottom_frame)
        self.main_layout.addWidget(self.stackedWidget)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def change_plot(self):
        self.stackedWidget.removeWidget(self.plot)
        if self.plots_combobox.currentIndex() == 0:
            self.plot = FigureCanvasQTAgg(Raporlar.yillik_gelir(self.year_spinbox.value()))
        elif self.plots_combobox.currentIndex() == 1:
            self.plot = FigureCanvasQTAgg(Raporlar.yillik_gider(self.year_spinbox.value()))
        elif self.plots_combobox.currentIndex() == 2:
            self.plot = FigureCanvasQTAgg(Raporlar.yillik_gelir_gider(self.year_spinbox.value()))
        elif self.plots_combobox.currentIndex() == 3:
            self.plot = FigureCanvasQTAgg(Raporlar.yemek_populerlik())
        self.stackedWidget.addWidget(self.plot)
        self.stackedWidget.setCurrentWidget(self.plot)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportWindow()
    window.show()
    sys.exit(app.exec())
