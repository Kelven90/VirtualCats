from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt, QTimer, QRect, Signal


class PetSprite(QWidget):
    clicked = Signal(object)

    def __init__(
        self,
        sprite_path,
        species,
        animation_config,
        state,
        frame_width=64,
        frame_height=64,
        parent=None,
        pet=None,
    ):
        super().__init__(parent)

        self.sprite_sheet = QPixmap(sprite_path)
        self.species = species
        self.animation_config = animation_config
        self.state = state
        self.pet = pet
        self.frame_width = frame_width
        self.frame_height = frame_height

        self.setFixedSize(96, 96)
        self.current_pixmap = QPixmap(self.frame_width, self.frame_height)
        self.current_pixmap.fill(Qt.transparent)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)

        self.multi_row_frames = []
        self.multi_row_index = 0
        self.loop = True

    def set_animation(self, config):
        self.multi_row_frames = []
        self.multi_row_index = 0

        if isinstance(config[0], tuple) and isinstance(config[1], tuple):
            # Multi-row animation
            frame_ranges = config[:-2]
            self.loop = config[-2]
            interval = config[-1]
            for row, start, end in frame_ranges:
                for col in range(start, end):
                    self.multi_row_frames.append((row, col))
        else:
            # Single-row animation
            row, start, end, self.loop, interval = config
            for col in range(start, end):
                self.multi_row_frames.append((row, col))

        self.timer.stop()
        self.timer.start(interval)
        self.update_animation()

    def update_animation(self):
        if not self.multi_row_frames:
            return

        row, col = self.multi_row_frames[self.multi_row_index]
        x = col * self.frame_width
        y = row * self.frame_height

        if (
            x + self.frame_width <= self.sprite_sheet.width()
            and y + self.frame_height <= self.sprite_sheet.height()
        ):
            cropped = self.sprite_sheet.copy(
                QRect(x, y, self.frame_width, self.frame_height)
            )
            self.current_pixmap = cropped

        self.multi_row_index += 1
        if self.multi_row_index >= len(self.multi_row_frames):
            if self.loop:
                self.multi_row_index = 0
            else:
                self.multi_row_index -= 1  # stay at last frame
                self.timer.stop()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled = self.current_pixmap.scaled(
            self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        x_offset = (self.width() - scaled.width()) // 2
        y_offset = (self.height() - scaled.height()) // 2
        painter.drawPixmap(x_offset, y_offset, scaled)
        painter.end()

    def reset_animation_frame(self):
        self.multi_row_index = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.pet)
        super().mousePressEvent(event)
