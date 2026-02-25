from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QProgressBar, QMessageBox, QSpacerItem, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, QTimer, QRect
from PySide6.QtGui import QPixmap
from pet.persistence import save_pets


class PetProfileWindow(QWidget):
    def __init__(self, pet, all_pets, on_stats_changed=None):
        super().__init__()
        self.pet = pet
        self.all_pets = all_pets
        self.on_stats_changed = on_stats_changed
        self.cooldowns = {"feed": False, "play": False, "rest": False}

        self.setWindowTitle(f"{pet.name}'s Profile")
        self.setFixedSize(750, 500)
        self.setObjectName("profileWindow")
        self.setStyleSheet(
            """
            QWidget#profileWindow {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #e7efff,
                    stop: 1 #fdf7ff
                );
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
                font-size: 10pt;
                color: #1f2933;
            }
            QFrame#infoCard {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #d6e0f0;
            }
            QLabel#nameLabel {
                font-size: 16px;
                font-weight: 600;
            }
            QLabel#moodLabel {
                color: #f97316;
                font-weight: 500;
            }
            QLabel#stateLabel {
                color: #4c7df0;
                font-weight: 500;
            }
            QWidget#profileWindow QPushButton {
                background-color: #4c7df0;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 14px;
                font-weight: 500;
            }
            QWidget#profileWindow QPushButton:hover {
                background-color: #668ef5;
            }
            QWidget#profileWindow QPushButton:pressed {
                background-color: #3b63c5;
            }
            QWidget#profileWindow QPushButton:disabled {
                background-color: #a0aec0;
            }
            QProgressBar {
                border-radius: 6px;
                background-color: #edf2ff;
                text-align: center;
            }
            QProgressBar::chunk {
                border-radius: 6px;
                background-color: #4c7df0;
            }
            QProgressBar#hungerBar::chunk {
                background-color: #fb7185;
            }
            QProgressBar#happinessBar::chunk {
                background-color: #34d399;
            }
            QProgressBar#energyBar::chunk {
                background-color: #facc15;
            }
            """
        )

        # Progress bars
        self.hunger_bar = QProgressBar()
        self.hunger_bar.setObjectName("hungerBar")
        self.happiness_bar = QProgressBar()
        self.happiness_bar.setObjectName("happinessBar")
        self.energy_bar = QProgressBar()
        self.energy_bar.setObjectName("energyBar")
        for bar in (self.hunger_bar, self.happiness_bar, self.energy_bar):
            bar.setRange(0, 100)

        # Labels
        self.name_label = QLabel(f"{pet.name} 🐾")
        self.name_label.setObjectName("nameLabel")
        self.species_label = QLabel(f"Species: {pet.species.capitalize()}")
        self.personality_label = QLabel(f"Personality: {pet.personality.capitalize()}")
        self.mood_label = QLabel(f"Mood: {pet.mood()}")
        self.mood_label.setObjectName("moodLabel")
        self.mood_label.setAlignment(Qt.AlignLeft)

        self.state_label = QLabel(f"State: {pet.state}")
        self.state_label.setObjectName("stateLabel")
        self.state_label.setAlignment(Qt.AlignCenter)

        # Sprite
        sprite_path = f"assets/PetMobileGameAsset/Cats/RetroCats/{self.pet.sprite_name}.png"
        pixmap = QPixmap(sprite_path)

        frame_width = 64
        frame_height = 64
        x, y = 0, 0

        if not pixmap.isNull():
            cropped = pixmap.copy(QRect(x, y, frame_width, frame_height))
        else:
            cropped = QPixmap(frame_width, frame_height)

        self.pet_sprite = QLabel()
        self.pet_sprite.setPixmap(
            cropped.scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        self.pet_sprite.setAlignment(Qt.AlignCenter)
        self.pet_sprite.setMinimumHeight(80)

        # Buttons
        self.feed_button = QPushButton("Feed 🍽️")
        self.feed_button.clicked.connect(self.feed_pet)
        self.play_button = QPushButton("Play 🎾")
        self.play_button.clicked.connect(self.play_with_pet)
        self.rest_button = QPushButton("Rest 😴")
        self.rest_button.clicked.connect(self.rest_pet)

        # Relationships
        self.relationships_label = QLabel("Friendliness with Other Cats 💕:")
        self.relationships_info = QLabel("")
        self.relationships_info.setWordWrap(True)

        # LEFT: Info layout
        info_layout = QVBoxLayout()
        info_layout.setSpacing(10)
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.species_label)
        info_layout.addWidget(self.personality_label)
        info_layout.addWidget(self.mood_label)
        info_layout.addWidget(QLabel("Hunger:"))
        info_layout.addWidget(self.hunger_bar)
        info_layout.addWidget(QLabel("Happiness:"))
        info_layout.addWidget(self.happiness_bar)
        info_layout.addWidget(QLabel("Energy:"))
        info_layout.addWidget(self.energy_bar)
        info_layout.addWidget(self.feed_button)
        info_layout.addWidget(self.play_button)
        info_layout.addWidget(self.rest_button)
        info_layout.addWidget(self.relationships_label)
        info_layout.addWidget(self.relationships_info)
        info_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        info_card = QFrame()
        info_card.setObjectName("infoCard")
        info_card.setLayout(info_layout)

        # VERTICAL LINE SEPARATOR
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setLineWidth(1)
        separator.setMidLineWidth(0)
        separator.setMinimumWidth(2)

        # RIGHT: Sprite + state
        sprite_layout = QVBoxLayout()
        sprite_layout.setContentsMargins(0, 20, 0, 20)
        sprite_layout.setSpacing(10)
        sprite_layout.addStretch()
        sprite_layout.addWidget(self.pet_sprite, alignment=Qt.AlignCenter)
        sprite_layout.addWidget(self.state_label, alignment=Qt.AlignCenter)
        sprite_layout.addStretch()

        # Wrap sprite in container widget for sizing control
        sprite_container = QWidget()
        sprite_container.setMinimumWidth(200)
        sprite_container.setLayout(sprite_layout)

        # Combine all in HBox
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.addWidget(info_card, stretch=2)
        main_layout.addWidget(separator)
        main_layout.addWidget(sprite_container, stretch=1)

        self.setLayout(main_layout)
        self.update_stats()

    def update_stats(self):
        self.hunger_bar.setValue(self.pet.hunger)
        self.happiness_bar.setValue(self.pet.happiness)
        self.energy_bar.setValue(self.pet.energy)
        mood = self.pet.mood()
        mood_emoji = {
            "Hungry": "🍽️",
            "Tired": "😴",
            "Sad": "😿",
            "Happy": "😺",
        }.get(mood, "")
        self.mood_label.setText(f"Mood: {mood} {mood_emoji}")
        self.state_label.setText(f"State: {self.pet.state}")

        if self.pet.relationships:
            lines = [f"- {name}: {score}" for name, score in self.pet.relationships.items()]
            self.relationships_info.setText("\n".join(lines))
        else:
            self.relationships_info.setText("No relationships yet.")

    def interact_with_pet(self, action):
        if self.cooldowns[action]:
            QMessageBox.information(
                self, "Slow down!",
                self.get_personality_prefix() + f"{self.pet.name} needs a moment before {action} again."
            )
            return

        if self.pet.sleeping:
            QMessageBox.information(
                self, "Sleeping...",
                f"{self.pet.name} is sleeping and won't respond right now. 😴"
            )
            return

        if action == "feed":
            if self.pet.hunger < 20:
                QMessageBox.information(self, "Too Full",
                    self.get_personality_prefix() + f"{self.pet.name} is already full! 🍽️")
                return
            self.pet.feed()
            # After feeding, pet calms down to idle
            self.pet.state = "idle"

        elif action == "play":
            if self.pet.energy < 20:
                QMessageBox.information(self, "Too Tired",
                    self.get_personality_prefix() + f"{self.pet.name} is too tired to play. 😴")
                return
            self.pet.play()
            # Playing explicitly sets a playful state
            self.pet.state = "playing"

        elif action == "rest":
            if self.pet.energy > 90:
                QMessageBox.information(self, "Too Energized",
                    self.get_personality_prefix() + f"{self.pet.name} is already well-rested! ⚡")
                return
            self.pet.rest()
            # Resting moves the pet into a sleeping/resting state
            self.pet.state = "sleeping"

        self.start_cooldown(action)
        self.pet.requested_attention = False
        save_pets(self.all_pets)
        self.update_stats()
        if self.on_stats_changed:
            self.on_stats_changed()

    def feed_pet(self):
        self.interact_with_pet("feed")

    def play_with_pet(self):
        self.interact_with_pet("play")

    def rest_pet(self):
        self.interact_with_pet("rest")

    def get_personality_prefix(self):
        p = self.pet.personality
        if p == "affectionate":
            return f"{self.pet.name} purrs sweetly. "
        elif p == "aggressive":
            return f"{self.pet.name} growls under their breath. "
        elif p == "shy":
            return f"{self.pet.name} glances away nervously. "
        elif p == "playful":
            return f"{self.pet.name} jumps in excitement. "
        return ""

    def start_cooldown(self, action, seconds=5):
        self.cooldowns[action] = True
        button = {
            "feed": self.feed_button,
            "play": self.play_button,
            "rest": self.rest_button
        }.get(action)

        if button:
            button.setEnabled(False)
            timer = QTimer(self)
            timer.setSingleShot(True)

            def end_cooldown():
                self.cooldowns[action] = False
                button.setEnabled(True)

            timer.timeout.connect(end_cooldown)
            timer.start(seconds * 1000)
