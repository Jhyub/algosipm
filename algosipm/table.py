from PyQt6.QtWidgets import QGridLayout, QLabel

from algosipm.element import Element, ElementButton
from algosipm.filter import Filter
from algosipm.util import set_align_center


class Table(QGridLayout):
    def __init__(self):
        super().__init__()
        ac = lambda x: set_align_center(x)
        self.addWidget(ac(QLabel("\\", self.widget())), 0, 0)
        for i in range(1, 19):
            self.addWidget(ac(QLabel(f"{i}", self.widget())), 0, i)
        for i in range(1, 10):
            if i == 8:
                self.addWidget(ac(QLabel("La", self.widget())), i, 0)
                continue
            if i == 9:
                self.addWidget(ac(QLabel("Ac", self.widget())), i, 0)
                continue
            self.addWidget(ac(QLabel(f"{i}", self.widget())), i, 0)
        for i in Element.load():
            self.addWidget(ElementButton(i), i.period, i.group)

    def filterWith(self, f: Filter):
        for i in Element.load():
            self.addWidget(ElementButton(i, f.check(i)), i.period, i.group)
