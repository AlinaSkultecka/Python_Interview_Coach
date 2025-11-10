import os
from pathlib import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtGui import QPainter, QBrush, QLinearGradient, QColor, QPixmap
from PySide6.QtCore import Qt, QRectF


class GradientCardButton(QPushButton):
    def __init__(self, level_text, main_text, color1, color2, image_path=None, parent=None):
        super().__init__(parent)
        self.level_text = level_text
        self.main_text = main_text
        self.color1 = color1
        self.color2 = color2
        self.image_path = image_path  # can be just "suitcase.png" or an absolute path

        self.setFixedHeight(130)
        self.setCursor(Qt.PointingHandCursor)
        # keep text left-aligned; no borders (we draw bg ourselves)
        self.setStyleSheet("border: none; border-radius: 20px; text-align: left;")

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)  # L T R B
        layout.setSpacing(12)

        # Text area
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)

        label1 = QLabel(level_text)
        label1.setStyleSheet("font-size: 18px; color: white; font-weight: 500; background: transparent;")
        label2 = QLabel(main_text)
        label2.setStyleSheet("font-size: 28px; color: white; font-weight: 800; background: transparent;")

        text_layout.addWidget(label1)
        text_layout.addWidget(label2)

        layout.addLayout(text_layout)
        layout.addStretch()  # push image to the far right

        # Optional image on the right
        if image_path:
            img_label = QLabel()
            img_label.setStyleSheet("background: transparent;")
            # size similar to reference; tweak 68–80 if you want larger
            img_label.setFixedSize(60, 60)
            img_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

            full_path = self._resolve_image_path(image_path)
            pix = QPixmap(full_path)
            if pix.isNull():
                # fallback: try raw path directly (maybe already absolute)
                pix = QPixmap(image_path)

            if pix.isNull():
                print(f"[GradientCardButton] Image NOT found: tried '{full_path}' and '{image_path}'")
            else:
                pix = pix.scaled(img_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                img_label.setPixmap(pix)

            # ensure it hugs the right edge like the reference
            layout.addWidget(img_label, 0, Qt.AlignRight | Qt.AlignTop)

    def _resolve_image_path(self, image_path: str) -> str:
        """
        Resolve image_path robustly:
        - If absolute and exists -> use it
        - Try <this_file>/data/images/<image_path>
        - Walk up parents to find a 'data/images' folder
        - Try CWD/data/images/<image_path>
        """
        p = Path(image_path)
        if p.is_absolute() and p.exists():
            return str(p)

        # 1) next to this file
        here = Path(__file__).resolve().parent
        candidate = here / "data" / "images" / image_path
        if candidate.exists():
            return str(candidate)

        # 2) walk up to find 'data/images'
        for parent in here.parents:
            candidate = parent / "data" / "images" / image_path
            if candidate.exists():
                return str(candidate)

        # 3) current working directory
        candidate = Path.cwd() / "data" / "images" / image_path
        if candidate.exists():
            return str(candidate)

        # last resort: return joined path even if it doesn't exist (QPixmap will fail gracefully)
        return str(here / "data" / "images" / image_path)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(self.color1))
        gradient.setColorAt(1, QColor(self.color2))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRectF(self.rect()), 20, 20)

        super().paintEvent(event)


