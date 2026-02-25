# ui/settings_dialog.py

from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QScrollArea,
    QFrame,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtCore import Qt

import os


class SettingsDialog(QDialog):
    def __init__(self, selected_background, set_background_callback, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(700, 180)

        self.selected_background = selected_background
        self.set_background_callback = set_background_callback
        self.thumbnail_labels = {}

        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(120)

        scroll_content = QFrame()
        thumb_layout = QHBoxLayout(scroll_content)
        thumb_layout.setSpacing(10)

        for i in range(1, 21):
            filename = f"{i}.png"
            full_path = os.path.join(
                "assets", "PetMobileGameAsset", "Backgrounds", filename
            )
            pixmap = QPixmap(full_path).scaled(
                100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

            thumb = QLabel()
            thumb.setPixmap(pixmap)
            thumb.setFixedSize(100, 100)
            thumb.setStyleSheet(self.get_style(filename))
            thumb.setCursor(QCursor(Qt.PointingHandCursor))
            thumb.mousePressEvent = self.make_click_handler(filename)

            thumb_layout.addWidget(thumb)
            self.thumbnail_labels[filename] = thumb

        scroll_content.setLayout(thumb_layout)
        scroll.setWidget(scroll_content)

        layout.addWidget(scroll)

    def get_style(self, filename):
        if filename == self.selected_background:
            return "border: 3px solid #44aaff;"
        else:
            return "border: 1px solid gray;"

    def make_click_handler(self, filename):
        def handler(event):
            self.selected_background = filename
            self.set_background_callback(filename)
            for fname, label in self.thumbnail_labels.items():
                label.setStyleSheet(self.get_style(fname))

        return handler
