from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLineEdit, QVBoxLayout, QLabel

from algosipm.filter import FilterChain
from algosipm.table import Table


class Bar(QVBoxLayout):
    def __init__(self, table: Table):
        super(Bar, self).__init__()
        self.table = table
        self.hbox = QHBoxLayout()
        self.barInput = BarInput(self)
        self.hbox.addWidget(self.barInput)
        self.clearButton = QPushButton()
        self.clearButton.setText("Clear")
        self.clearButton.setEnabled(False)
        self.clearButton.clicked.connect(self.barInput.clear)
        self.hbox.addWidget(self.clearButton)
        self.addLayout(self.hbox)
        self.errorLabel = QLabel("")
        self.errorLabel.hide()
        self.errorLabel.setMaximumHeight(15)
        self.addWidget(self.errorLabel)

    def updateError(self, error: str):
        self.errorLabel.setText(error)
        if error:
            self.errorLabel.show()
        else:
            self.errorLabel.hide()


class BarInput(QLineEdit):
    def __init__(self, bar: Bar):
        super(BarInput, self).__init__()
        self.bar = bar
        self.textChanged.connect(self.onTextChanged)

    def onTextChanged(self):
        if not self.text():
            self.bar.clearButton.setEnabled(False)
        else:
            self.bar.clearButton.setEnabled(True)
        fc = FilterChain.fromQuery(self.text())
        self.bar.table.filterWith(fc)
        self.bar.updateError(fc.error)
