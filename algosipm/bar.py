from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLineEdit, QVBoxLayout, QLabel, QWidget

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
        self.w = None
        self.helpButton = QPushButton()
        self.helpButton.setText("?")
        self.helpButton.clicked.connect(self.showHelp)
        self.hbox.addWidget(self.helpButton)
        self.addLayout(self.hbox)
        self.errorLabel = QLabel("")
        self.errorLabel.hide()
        self.errorLabel.setMaximumHeight(15)
        self.addWidget(self.errorLabel)

    def showHelp(self):
        if self.w is None:
            self.w = QWidget()
            self.w.setWindowTitle("Help")
            layout = QVBoxLayout()

            layout.addWidget(QLabel("Q. 검색하는 방법?"))
            layout.addWidget(QLabel("A. 적절한 조건을 입력해 주세요. 조건은 and나 or를 이용해서 연쇄적으로 적용할 수 있고 괄호를 쳐서 묶을 수 있습니다."))
            layout.addWidget(QLabel(""))
            layout.addWidget(QLabel("Q. 아닌 것을 고르고 싶습니다."))
            layout.addWidget(QLabel("A. !를 앞에 붙이면 조건이 반전됩니다."))
            layout.addWidget(QLabel(""))
            layout.addWidget(QLabel("Q. 검색할 수 있는 조건으로 무엇이 있을까요?"))
            layout.addWidget(QLabel("""
            A. 아무런 추가 요소 없이 문자열을 입력하시면 원소 이름을 기준으로 유도리 있게 검색합니다.
      쌍따옴표 안에 문자열을 입력하시면 원소 이름을 기준으로 엄격하게 검색합니다.
      다른 검색 기준을 이용하시리 경우, (기준이름): (값) 형식으로 검색하실 수 있습니다. 띄어쓰기의 형식이 중요합니다.
      다음은 가능한 기준 이름 목록입니다.
      name - 원소 이름 (엄격하게)
      symbol - 원소 기호
      period - 주기
      group - 족, 1~18 외에도 'la', 'ac'을 입력할 수 있습니다.
      metal - 금속 여부, 가능한 값으로는 metal, nonmetal, metalloid, unknown이 있습니다.
            """.strip()))

            self.w.setLayout(layout)
        self.w.show()

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
