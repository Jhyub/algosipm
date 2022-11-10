import os.path

import toml
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout


class Element:
    elements = []

    def __init__(self, filename):  # Read file and generate element
        with open(os.path.dirname(__file__) + f"/../data/{filename}", "r") as f:
            print(f"debug / loading file {f.name}")
            element_info = toml.load(f)
            self.name = element_info["Element"]["name"]
            self.symbol = element_info["Element"]["symbol"]
            self.period = int(element_info["Element"]["period"])
            self.group = int(element_info["Element"]["group"])
            self.metal = int(element_info["Element"]["metal"])
            self.content = element_info["Element"]["content"]

    @staticmethod
    def load():  # Get list of files and provide a list of elements
        if len(Element.elements) == 0:
            Element.elements = [Element(i) for i in os.listdir(os.path.dirname(__file__) + "/../data")]
        return Element.elements


class ElementButton(QPushButton):
    def __init__(self, element: Element, enabled: bool = True):  # Make button out of element
        super(ElementButton, self).__init__()
        self.element = element
        self.setEnabled(enabled)
        self.setText(f"{element.symbol}")
        self.w = None
        self.clicked.connect(self.show_window)

    def show_window(self):
        if self.w is None:
            self.w = ElementWindow(self.element)
        self.w.show()


class ElementWindow(QWidget):
    def __init__(self, element: Element):
        super().__init__()
        self.element = element
        self.setWindowTitle(f"{element.symbol} - {element.name}")
        self.setMinimumSize(200, 200)
        layout = QVBoxLayout()

        first_line = QHBoxLayout()
        first_line.addWidget(QLabel(f"{element.name}; {element.symbol}"))
        layout.addLayout(first_line)

        period = element.period
        group = str(element.group)
        metal = "불명"
        if period in [8, 9]:
            period = period - 2
            if period == 6:
                group = "란타넘족"
            if period == 7:
                group = "악티늄족"
        if element.metal == 0:
            metal = "비금속"
        elif element.metal == 1:
            metal = "준금속"
        elif element.metal == 2:
            metal = "금속"

        content = QLabel(element.content)
        content.setWordWrap(True)

        layout.addWidget(QLabel(f"주기: {period}"))
        layout.addWidget(QLabel(f"족 : {group}"))
        layout.addWidget(QLabel(metal))
        layout.addWidget(content)

        self.setLayout(layout)

    def image(self):
        return QPushButton("대충3D그래픽(희망사항)")
