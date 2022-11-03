from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel


def set_align_center(label: QLabel):
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label

