from PySide6.QtWidgets import QTextEdit


class LMLogView(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setMinimumHeight(240)
        self.setPlaceholderText("Operationen erscheinen hier…")

    def append_entry(self, text: str) -> None:
        self.append(text)
