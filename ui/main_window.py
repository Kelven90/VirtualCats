from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QMessageBox,
    QAbstractItemView, QTextEdit, QLineEdit, QFrame, QMainWindow, QSizePolicy, QMenu
)
from PySide6.QtCore import QTimer, Qt, QPoint
from PySide6.QtGui import QPixmap
from ui.pet_sprite import PetSprite
from ui.add_pet_dialog import AddPetDialog
from ui.edit_pet_dialog import EditPetDialog
from ui.pet_profile_window import PetProfileWindow
from ui.settings_dialog import SettingsDialog
from pet.config import load_config, save_config
from pet.pet import VirtualPet
from pet.persistence import load_pets, save_pets
from pet.interactions import process_interaction
from pet.animation_config import ANIMATION_CONFIGS
import random

STATE_TO_ANIMATION = {
    "idle": ["sitting", "resting_lazy", "laying"],
    "sleeping": ["sleeping", "deep_sleep"],
    "walking": ["running"],
    "playing": ["dancing", "box_headup"],
    "praying": ["praying_closed", "praying_open"],
    "collapsed": ["collapse_open", "collapse_closed"],
    "waking": ["waking"]
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Virtual Cat App")
        self.config = load_config()
        self.current_background = self.config.get("background", "1.png")

        self.resize(900, 600)
        self.setStyleSheet(
            """
            QWidget {
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
                font-size: 10pt;
                color: #1f2933;
            }
            QMainWindow {
                background-color: #dfe7ff;
            }
            QWidget#centralWidget {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #e7f0ff,
                    stop: 1 #f7fafc
                );
            }
            QListWidget {
                background-color: #ffffff;
                border-radius: 6px;
                border: 1px solid #dde1eb;
                padding: 6px;
            }
            QListWidget::item {
                padding: 4px 2px;
            }
            QListWidget::item:selected {
                background-color: #e0ebff;
                color: #1f2933;
            }
            QTextEdit {
                background-color: #ffffff;
                border-radius: 6px;
                border: 1px solid #dde1eb;
                padding: 6px;
            }
            QTextEdit#logBox {
                background-color: #fff7ed;
                border: 1px solid #f3c78c;
                color: #823b11;
            }
            QLineEdit {
                background-color: #ffffff;
                border-radius: 6px;
                border: 1px solid #dde1eb;
                padding: 6px 8px;
            }
            QLineEdit:focus {
                border-color: #4c7df0;
            }
            """
        )

        self.pets = load_pets()
        self.pet_sprites = {}

        # === Layout ===
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        self.setCentralWidget(central_widget)

        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        # === Scene with background ===
        self.scene_widget = QWidget()
        self.scene_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scene_layout = QVBoxLayout(self.scene_widget)
        scene_layout.setContentsMargins(0, 0, 0, 0)

        self.background_label = QLabel()
        self.background_label.setScaledContents(True)
        self.background_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scene_layout.addWidget(self.background_label)
        self.set_background(self.current_background)

        # === Right panel ===
        right_panel = QVBoxLayout()
        right_panel.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search cats...")
        self.search_input.textChanged.connect(self.refresh_pet_list)

        self.pet_list = QListWidget()
        self.pet_list.setObjectName("petList")
        self.pet_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.pet_list.itemDoubleClicked.connect(self.open_pet_profile)
        self.pet_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pet_list.customContextMenuRequested.connect(self.show_pet_context_menu)

        # Empty state widget (shown when there are no pets)
        self.empty_state_widget = QWidget()
        empty_layout = QVBoxLayout(self.empty_state_widget)
        empty_layout.setContentsMargins(12, 24, 12, 24)
        empty_layout.setSpacing(8)
        empty_label = QLabel("You don't have any cats yet.")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_label.setWordWrap(True)
        empty_sub = QLabel("Adopt your first virtual cat to get started!")
        empty_sub.setAlignment(Qt.AlignCenter)
        empty_sub.setWordWrap(True)
        self.empty_adopt_button = QPushButton("Adopt your first cat")
        self.empty_adopt_button.clicked.connect(self.show_add_pet_dialog)
        self.empty_adopt_button.setCursor(Qt.PointingHandCursor)
        empty_layout.addStretch(1)
        empty_layout.addWidget(empty_label)
        empty_layout.addWidget(empty_sub)
        empty_layout.addWidget(self.empty_adopt_button, alignment=Qt.AlignCenter)
        empty_layout.addStretch(2)
        self.empty_state_widget.hide()

        self.add_pet_button = QPushButton("Adopt New Cat")
        self.edit_pet_button = QPushButton("Edit Selected Cat")
        self.settings_button = QPushButton("Settings")
        self.help_button = QPushButton("?")
        self.help_button.setFixedWidth(32)

        self.add_pet_button.clicked.connect(self.show_add_pet_dialog)
        self.edit_pet_button.clicked.connect(self.edit_selected_pet)
        self.settings_button.clicked.connect(self.open_settings_dialog)
        self.help_button.clicked.connect(self.show_help_dialog)

        # Button styling
        primary_style = """
            QPushButton {
                background-color: #4c7df0;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #668ef5;
            }
            QPushButton:pressed {
                background-color: #3b63c5;
            }
            QPushButton:disabled {
                background-color: #a0aec0;
            }
        """

        for btn in (self.add_pet_button, self.edit_pet_button, self.settings_button, self.empty_adopt_button):
            btn.setStyleSheet(primary_style)
            btn.setCursor(Qt.PointingHandCursor)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_pet_button)
        button_layout.addWidget(self.edit_pet_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.settings_button)

        self.log_box = QTextEdit()
        self.log_box.setObjectName("logBox")
        self.log_box.setReadOnly(True)
        self.log_box.setFixedHeight(120)

        # === Assemble right panel ===
        right_panel.addWidget(self.search_input)
        right_panel.addWidget(self.pet_list, stretch=1)
        right_panel.addWidget(self.empty_state_widget, stretch=1)
        right_panel.addLayout(button_layout)
        right_panel.addWidget(self.log_box)

        # === Combine panels ===
        top_layout.addWidget(self.scene_widget, stretch=3)
        top_layout.addLayout(right_panel, stretch=1)

        # === Timers ===
        self.interaction_timer = QTimer(self, timeout=self.random_pet_interaction)
        self.interaction_timer.start(10000)

        self.stat_decay_timer = QTimer(self, timeout=self.auto_decay_stats)
        self.stat_decay_timer.start(60000)

        self.animation_timer = QTimer(self, timeout=self.update_pet_sprites)
        self.animation_timer.start(500)

        self.animation_variation_timer = QTimer(self, timeout=self.rotate_pet_animations)
        self.animation_variation_timer.start(30000)

        self.refresh_pet_list()
        self.refresh_pet_scene()

    def show_help_dialog(self):
        QMessageBox.information(
            self,
            "How to Play",
            (
                "Welcome to Virtual Cat App!\n\n"
                "• Hunger: goes up over time. Feed your cat to bring it down.\n"
                "• Happiness: goes up when you play or when cats cuddle; drops if ignored.\n"
                "• Energy: goes down when playing and over time, up when your cat rests or sleeps.\n\n"
                "Random interactions:\n"
                "• Every so often, two cats will interact on their own. Their personalities decide\n"
                "  whether they cuddle, play, or keep their distance, changing their stats and friendship.\n\n"
                "Interacting with your cats:\n"
                "• Double‑click a cat in the list or click its sprite in the room to open its profile.\n"
                "• From the profile, use Feed / Play / Rest to care for your cat.\n"
                "• Watch the icons next to each cat's name for hunger (🍽️), tiredness (😴),\n"
                "  and low happiness (😿).\n"
            ),
        )

    def open_settings_dialog(self):
        dialog = SettingsDialog(
            selected_background=self.current_background,
            set_background_callback=self.set_background,
            parent=self
        )
        dialog.exec()

    def set_background(self, filename):
        path = f"assets/PetMobileGameAsset/Backgrounds/{filename}"
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            self.background_label.setPixmap(pixmap)
            self.current_background = filename
            self.config["background"] = filename
            save_config(self.config)  # ← persist it
        else:
            self.background_label.clear()



    def refresh_pet_list(self):
        query = self.search_input.text().lower()
        self.pet_list.clear()
        if not self.pets:
            self.pet_list.hide()
            self.empty_state_widget.show()
            return

        self.pet_list.show()
        self.empty_state_widget.hide()

        for pet in self.pets:
            display = f"{pet.name} ({pet.species.capitalize()}, {pet.personality})"
            icons = []
            if pet.hunger > 80:
                icons.append("🍽️")
            if pet.energy < 20:
                icons.append("😴")
            if pet.happiness < 30:
                icons.append("😿")
            if icons:
                display += " " + "".join(icons)
            if query in display.lower():
                self.pet_list.addItem(display)

    def refresh_pet_scene(self):
        for child in self.scene_widget.findChildren(QWidget):
            if child is not self.background_label:
                child.setParent(None)

        self.pet_sprites.clear()

        scene_height = self.scene_widget.height()
        sprite_height = 96  # Known sprite display height (adjust if you change it)

        for idx, pet in enumerate(self.pets):
            sprite_path = f"assets/PetMobileGameAsset/Cats/RetroCats/{pet.sprite_name}.png"

            sprite = PetSprite(
                sprite_path=sprite_path,
                species=pet.species,
                animation_config=ANIMATION_CONFIGS[pet.species],
                state=pet.state,
                pet=pet,
            )

            self.configure_sprite_animation(sprite, pet)
            sprite.setParent(self.scene_widget)

            x = 32 + idx * 96
            y = scene_height - sprite_height - 10  # fixed height used

            sprite.move(x, y)
            sprite.show()
            sprite.clicked.connect(self.open_pet_profile_from_sprite)
            self.pet_sprites[pet.name] = sprite


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.refresh_pet_scene()

    def update_pet_sprites(self):
        for pet in self.pets:
            sprite = self.pet_sprites.get(pet.name)
            if sprite:
                self.configure_sprite_animation(sprite, pet)

    def configure_sprite_animation(self, sprite, pet):
        anim_keys = STATE_TO_ANIMATION.get(pet.state, [])
        config_dict = ANIMATION_CONFIGS[pet.species]

        # Reset animation if state changed
        if pet.state != getattr(pet, "_last_state", None):
            pet._current_animation_key = None
            pet._last_state = pet.state

        # Pick new animation only if not set
        if not pet._current_animation_key:
            valid_keys = [k for k in anim_keys if k in config_dict]
            if valid_keys:
                pet._current_animation_key = random.choice(valid_keys)

        key = pet._current_animation_key
        if key and key in config_dict:
            config = config_dict[key]
            #print(f"[ANIM] Pet: {pet.name}, State: {pet.state}, Using animation: {key}")
            sprite.set_animation(config)
        else:
            print(f"[WARN] No animation found for Pet: {pet.name}, State: {pet.state}")

    def rotate_pet_animations(self):
        for pet in self.pets:
            anim_keys = STATE_TO_ANIMATION.get(pet.state, [])
            config_dict = ANIMATION_CONFIGS[pet.species]

            valid_keys = [k for k in anim_keys if k in config_dict]
            if not valid_keys:
                continue

            # Pick a different animation if possible
            current = getattr(pet, "_current_animation_key", None)
            if len(valid_keys) > 1:
                new_choices = [k for k in valid_keys if k != current]
                pet._current_animation_key = random.choice(new_choices)
            else:
                pet._current_animation_key = valid_keys[0]

        self.refresh_pet_scene()

    def show_add_pet_dialog(self):
        dialog = AddPetDialog()
        if dialog.exec():
            name, species, personality, color = dialog.get_pet_info()
            sprite_name = f"AllCats{'' if color == 'BrownWhite' else color}"  # handle default
            new_pet = VirtualPet(name, species, personality, sprite_name)
            self.pets.append(new_pet)
            save_pets(self.pets)
            self.refresh_pet_list()
            self.refresh_pet_scene()


    def edit_selected_pet(self):
        selected = self.pet_list.selectedItems()
        if not selected:
            return
        index = self.pet_list.row(selected[0])
        pet = self.pets[index]
        dialog = EditPetDialog(pet)
        if dialog.exec():
            name, personality = dialog.get_updated_info()
            pet.name = name
            pet.personality = personality
            save_pets(self.pets)
            self.refresh_pet_list()
        

    def delete_selected_pet(self):
        selected = self.pet_list.selectedItems()
        if not selected:
            return

        index = self.pet_list.row(selected[0])
        pet_to_remove = self.pets[index]
        removed_name = pet_to_remove.name

        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Delete Pet",
            f"Are you sure you want to delete {removed_name}? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        # Remove pet
        del self.pets[index]

        # Clean up relationships in remaining pets
        for pet in self.pets:
            if removed_name in pet.relationships:
                del pet.relationships[removed_name]

        save_pets(self.pets)
        self.refresh_pet_list()
        self.refresh_pet_scene()

    def show_pet_context_menu(self, pos: QPoint):
        item = self.pet_list.itemAt(pos)
        if not item:
            return

        # Ensure the clicked item is selected
        self.pet_list.setCurrentItem(item)

        menu = QMenu(self)
        open_profile_action = menu.addAction("Open Profile")
        edit_action = menu.addAction("Edit Pet")
        menu.addSeparator()
        delete_action = menu.addAction("Delete Pet…")

        action = menu.exec_(self.pet_list.mapToGlobal(pos))
        if action == open_profile_action:
            self.open_pet_profile(item)
        elif action == edit_action:
            self.edit_selected_pet()
        elif action == delete_action:
            self.delete_selected_pet()

    def open_pet_profile(self, item):
        index = self.pet_list.row(item)
        pet = self.pets[index]
        self.pet_list.setCurrentRow(index)
        self.profile_window = PetProfileWindow(pet, self.pets, on_stats_changed=self.handle_pet_stats_changed)
        self.profile_window.show()

    def open_pet_profile_from_sprite(self, pet):
        if pet not in self.pets:
            return
        index = self.pets.index(pet)
        self.pet_list.setCurrentRow(index)
        self.profile_window = PetProfileWindow(pet, self.pets, on_stats_changed=self.handle_pet_stats_changed)
        self.profile_window.show()

    def handle_pet_stats_changed(self):
        self.refresh_pet_list()
        self.refresh_pet_scene()

    def random_pet_interaction(self):
        if len(self.pets) < 2:
            return
        p1, p2 = random.sample(self.pets, 2)
        msg = process_interaction(p1, p2)
        self.log_box.append(msg)

        # Change state based on message content (simple keyword rule for now)
        if "cuddled" in msg:
            p1.state = "idle"
            p2.state = "idle"
        elif "tried to play" in msg:
            p1.state = "playing"
            p2.state = "idle"
        elif "shied away" in msg:
            p2.state = "collapsed"

        # Force re-render immediately after state change
        self.refresh_pet_scene()
        self.refresh_pet_list()

        save_pets(self.pets)

    def auto_decay_stats(self):
        for pet in self.pets:
            pet.adjust_stat("hunger", +2)
            pet.adjust_stat("happiness", -2)
            pet.adjust_stat("energy", -1)

            # Simple threshold logic to update state without overwriting playful states
            if pet.energy < 20:
                pet.state = "sleeping"
            elif pet.hunger > 80:
                pet.state = "collapsed"
            elif pet.happiness < 30 and pet.state not in ("sleeping", "collapsed"):
                pet.state = "idle"
            # Otherwise, keep the current state (e.g., playing or idle)

        save_pets(self.pets)
        self.refresh_pet_scene()
        self.refresh_pet_list()


    def closeEvent(self, event):
        save_pets(self.pets)
        event.accept()
