import os
from pathlib import Path

from PySide6.QtWidgets import (
    QPushButton, QHBoxLayout, QVBoxLayout, QLabel
)
from PySide6.QtGui import QPainter, QBrush, QLinearGradient, QColor, QPixmap
from PySide6.QtCore import Qt, QRectF


class GradientCardButton(QPushButton):
    """
    A large, card-like button with:
      - gradient background
      - level text (small, e.g. "Level 1")
      - main text (big, e.g. "Play a Quiz")
      - optional right-aligned icon

    Used on the main menu as a primary navigation card.
    """

    def __init__(
        self,
        level_text: str,
        main_text: str,
        color1: str,
        color2: str,
        image_path: str | None = None,
        parent=None,
    ):
        super().__init__(parent)

        self.level_text = level_text
        self.main_text = main_text
        self.color1 = color1
        self.color2 = color2
        self.image_path = image_path

        self._configure_button()
        self._build_ui()
        if self.image_path:
            self._add_icon(self.image_path)

    # ======================================================================
    # SETUP
    # ======================================================================

    def _configure_button(self):
        """Basic button appearance and behavior."""
        self.setFixedHeight(130)
        self.setCursor(Qt.PointingHandCursor)

        # We draw the background ourselves in paintEvent -> border: none
        self.setStyleSheet(
            "border: none; border-radius: 20px; text-align: left;"
        )

    def _build_ui(self):
        """Create internal layout and text labels."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)  # L T R B
        layout.setSpacing(12)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)

        level_label = QLabel(self.level_text)
        level_label.setStyleSheet(
            "font-size: 18px; color: white; font-weight: 500; background: transparent;"
        )

        main_label = QLabel(self.main_text)
        main_label.setStyleSheet(
            "font-size: 28px; color: white; font-weight: 800; background: transparent;"
        )

        text_layout.addWidget(level_label)
        text_layout.addWidget(main_label)

        layout.addLayout(text_layout)
        layout.addStretch()  # pushes icon to the far right

        self._main_layout = layout  # store if we need to add icon later

    # ======================================================================
    # ICON HANDLING
    # ======================================================================

    def _add_icon(self, image_path: str):
        """Optional small icon on the right side of the card."""
        img_label = QLabel()
        img_label.setStyleSheet("background: transparent;")
        img_label.setFixedSize(60, 60)
        img_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        full_path = self._resolve_image_path(image_path)
        pix = QPixmap(full_path)

        if pix.isNull():
            # fallback: try original path directly
            pix = QPixmap(image_path)

        if pix.isNull():
            # Debug info only, doesn't crash UI
            print(
                f"[GradientCardButton] Image NOT found: tried '{full_path}' and '{image_path}'"
            )
            return

        pix = pix.scaled(
            img_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        img_label.setPixmap(pix)

        # Hug the right/top edge
        self._main_layout.addWidget(
            img_label,
            0,
            Qt.AlignRight | Qt.AlignTop
        )

    def _resolve_image_path(self, image_path: str) -> str:
        """
        Try to robustly resolve an image path.

        Priority:
          1. Absolute path that exists
          2. <this_file>/data/images/<image_path>
          3. Walk up parents to find 'data/images/<image_path>'
          4. CWD/data/images/<image_path>
          5. Fallback: <this_file>/data/images/<image_path> (even if missing)
        """
        p = Path(image_path)

        # 1) Absolute path
        if p.is_absolute() and p.exists():
            return str(p)

        here = Path(__file__).resolve().parent

        # 2) data/images next to this file
        candidate = here / "data" / "images" / image_path
        if candidate.exists():
            return str(candidate)

        # 3) Walk up parents to find data/images
        for parent in here.parents:
            candidate = parent / "data" / "images" / image_path
            if candidate.exists():
                return str(candidate)

        # 4) CWD/data/images
        candidate = Path.cwd() / "data" / "images" / image_path
        if candidate.exists():
            return str(candidate)

        # 5) Last resort (probably missing, but QPixmap will handle it)
        return str(here / "data" / "images" / image_path)

    # ======================================================================
    # CUSTOM PAINTING
    # ======================================================================

    def paintEvent(self, event):
        """Draw gradient background and then let QPushButton paint its contents."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(self.color1))
        gradient.setColorAt(1, QColor(self.color2))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRectF(self.rect()), 20, 20)

        # Let QPushButton handle text/child widgets
        super().paintEvent(event)


