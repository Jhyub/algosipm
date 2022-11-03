from PyQt6.QtWidgets import QWidget, QLayout, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
import toml
import os.path


class Element:
    def __init__(self, filename):  # Read file and generate element
        with open(os.path.dirname(__file__) + f"/../data/{filename}", "r") as f:
            element_info = toml.load(f)
            self.name = element_info["Element"]["name"]
            self.symbol = element_info["Element"]["symbol"]
            self.period = element_info["Element"]["period"]
            self.group = element_info["Element"]["group"]
            self.content = element_info["Element"]["content"]

    @staticmethod
    def load():  # Get list of files and provide a list of elements
        return [Element(i) for i in os.listdir(os.path.dirname(__file__) + "/../data")]


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
        layout = QVBoxLayout()

        first_line = QHBoxLayout()
        first_line.addWidget(self.image())
        first_line.addWidget(QLabel(f"{element.name}; {element.symbol}"))
        layout.addLayout(first_line)

        layout.addWidget(QLabel(element.content))

        self.setLayout(layout)

    def image(self):
        return QPushButton("대충3D그래픽(희망사항)")
