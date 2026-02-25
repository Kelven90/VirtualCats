from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QLabel,
    QMessageBox,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtCore import Qt


class AddPetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adopt New Cat")
        self.setFixedSize(320, 230)
        self.setObjectName("addPetDialog")
        self.setStyleSheet("""
            QDialog#addPetDialog {
                background-color: #f7f5ff;
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
                font-size: 10pt;
                color: #1f2933;
            }
            QLabel#titleLabel {
                font-size: 15px;
                font-weight: 600;
            }
            QLineEdit, QComboBox {
                background-color: #ffffff;
                border-radius: 6px;
                border: 1px solid #d1d5e5;
                padding: 4px 8px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #4c7df0;
            }
            QPushButton#adoptButton {
                background-color: #4c7df0;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 14px;
                font-weight: 500;
            }
            QPushButton#adoptButton:hover {
                background-color: #668ef5;
            }
            QPushButton#adoptButton:pressed {
                background-color: #3b63c5;
            }
            """)

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        title = QLabel("Adopt a new cat 🐾")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Cat name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Cat name")
        self.name_input.setMinimumHeight(22)
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        # Personality dropdown
        self.personality_selector = QComboBox()
        self.personality_selector.addItems(
            ["affectionate", "playful", "lazy", "curious", "shy"]
        )
        self.personality_selector.setMinimumHeight(22)
        layout.addWidget(QLabel("Personality:"))
        layout.addWidget(self.personality_selector)

        # Color dropdown
        self.color_selector = QComboBox()
        self.color_selector.addItems(
            ["BrownWhite", "Black", "Grey", "GreyWhite", "Orange", "White"]
        )
        self.color_selector.setMinimumHeight(22)
        layout.addWidget(QLabel("Color:"))
        layout.addWidget(self.color_selector)

        # Adopt button
        button_row = QHBoxLayout()
        button_row.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )
        self.button = QPushButton("Adopt")
        self.button.setObjectName("adoptButton")
        self.button.clicked.connect(self.adopt)
        button_row.addWidget(self.button)
        layout.addLayout(button_row)

        self.setLayout(layout)

    def adopt(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(
                self, "Missing Name", "Please enter a name for your cat."
            )
            return
        self.accept()

    def get_pet_info(self):
        name = self.name_input.text().strip()
        personality = self.personality_selector.currentText()
        color = self.color_selector.currentText()
        return name, "cat", personality, color
