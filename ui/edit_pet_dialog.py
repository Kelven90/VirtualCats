from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
)


class EditPetDialog(QDialog):
    def __init__(self, pet):
        super().__init__()
        self.setWindowTitle(f"Edit Pet: {pet.name}")
        self.setFixedSize(300, 180)

        layout = QVBoxLayout()

        self.name_input = QLineEdit(pet.name)
        self.personality_input = QComboBox()
        self.personality_input.addItems(
            ["Affectionate", "Playful", "Lazy", "Curious", "Shy", "Aggressive"]
        )
        index = self.personality_input.findText(pet.personality.capitalize())
        if index != -1:
            self.personality_input.setCurrentIndex(index)

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Personality:"))
        layout.addWidget(self.personality_input)

        self.save_button = QPushButton("Save")
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.save_button.clicked.connect(self.accept)

    def get_updated_info(self):
        return (self.name_input.text(), self.personality_input.currentText().lower())
