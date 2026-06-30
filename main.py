import sys

from PySide6.QtWidgets import QApplication

from core.config import ensure_settings_file
from ui.main_window import MainWindow


def main() -> int:
    ensure_settings_file()
    app = QApplication(sys.argv)
    app.setApplicationName("LohnMail")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
