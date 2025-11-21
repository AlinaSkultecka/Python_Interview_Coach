# pages/ui/animated_border_button.py

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QColor, QConicalGradient, QBrush


class AnimatedBorderButton(QPushButton):
    """
    QPushButton with an animated pastel border along its own outline
    when loading is True.
    """

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self._loading = False
        self._phase = 0.0

        self._timer = QTimer(self)
        self._timer.setInterval(40)  # animation speed
        self._timer.timeout.connect(self._on_timeout)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def setLoading(self, loading: bool):
        """Turn the animated border on/off."""
        self._loading = loading
        if loading:
            self._phase = 0.0
            self._timer.start()
        else:
            self._timer.stop()
            self._phase = 0.0
            self.update()

    # ------------------------------------------------------------------ #
    # Internal
    # ------------------------------------------------------------------ #
    def _on_timeout(self):
        # Rotate the gradient for motion effect
        self._phase += 2.0
        if self._phase > 1000:
            self._phase = 0.0
        self.update()

    def paintEvent(self, event):
        # First paint normal button (background + text, styled by QSS)
        super().paintEvent(event)

        if not self._loading:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Slightly inside the button rect so the border isn't clipped
        rect = self.rect().adjusted(1, 1, -1, -1)

        # Pastel "rainbow" gradient that rotates with _phase
        grad = QConicalGradient(rect.center(), self._phase * 2.0)
        grad.setColorAt(0.00, QColor(255, 179, 186))  # soft pink
        grad.setColorAt(0.20, QColor(255, 223, 186))  # peach
        grad.setColorAt(0.40, QColor(255, 255, 186))  # light yellow
        grad.setColorAt(0.60, QColor(186, 255, 201))  # mint
        grad.setColorAt(0.80, QColor(186, 225, 255))  # baby blue
        grad.setColorAt(1.00, QColor(221, 186, 255))  # lavender

        brush = QBrush(grad)

        pen = QPen(brush, 3)
        pen.setStyle(Qt.SolidLine)  # full continuous line, no gaps

        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        # Match your QSS border-radius (22)
        painter.drawRoundedRect(rect, 22, 22)