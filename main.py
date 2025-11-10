import sys
from PySide6.QtWidgets import QApplication
from pages.entrance_window import EntranceWindow
from pages.main_menu_view import MainMenuView

def main():
    app = QApplication(sys.argv)

    # Show the entrance window first
    entrance = EntranceWindow()
    entrance.show()

    # When the user clicks "Continue", show the main menu and pass the username
    def on_continue():
        username = entrance.name_input.text().strip() or "user"
        # Keep a reference to the main menu so it doesn't get garbage collected
        app.main_menu = MainMenuView(username=username)
        app.main_menu.show()
        entrance.close()

    entrance.btn_continue.clicked.connect(on_continue)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()