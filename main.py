import sys
from PySide6.QtWidgets import QApplication

from pages.entrance_window import EntranceWindow
from pages.main_menu_view import MainMenuView


def main():
    """
    Application entry point.
    Shows EntranceWindow first, then launches MainMenuView after the user enters a name.
    """
    app = QApplication(sys.argv)

    entrance = EntranceWindow()
    entrance.show()

    def on_continue():
        """Move from entrance screen → main menu."""
        username = entrance.name_input.text().strip() or "User"

        # Keep a strong reference to prevent garbage collection
        app.main_menu = MainMenuView(username=username)
        app.main_menu.show()

        entrance.close()

    # Connect continue button
    entrance.btn_continue.clicked.connect(on_continue)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()