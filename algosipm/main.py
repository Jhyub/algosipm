import sys

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout

from algosipm.bar import Bar
from algosipm.table import Table


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Periodic Table - algosipm")

        layout = QVBoxLayout()
        t = Table()
        layout.addLayout(Bar(t))
        layout.addLayout(t)

        widget = QWidget()
        widget.setLayout(layout)

        self.setMinimumSize(960, 540)
        self.setCentralWidget(widget)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
