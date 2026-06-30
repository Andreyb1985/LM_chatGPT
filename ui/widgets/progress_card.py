from PySide6.QtWidgets import QLabel, QProgressBar

from ui.widgets.card import LMCard


class LMProgressCard(LMCard):
    def __init__(self, title: str = "Live Progress", parent=None):
        super().__init__(title, parent)
        self.status = QLabel("Bereit")
        self.status.setObjectName("muted")
        self.current = QLabel("Noch kein Vorgang gestartet.")
        self.current.setWordWrap(True)
        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setValue(0)
        self.layout.addWidget(self.status)
        self.layout.addWidget(self.bar)
        self.layout.addWidget(self.current)

    def set_busy(self, busy: bool) -> None:
        if busy:
            self.status.setText("Vorgang läuft…")
            self.bar.setRange(0, 0)
        else:
            self.status.setText("Bereit")
            self.bar.setRange(0, 100)
            if self.bar.value() == 0:
                self.current.setText("Noch kein Vorgang gestartet.")

    def set_completed(self, message: str = "Vorgang abgeschlossen.") -> None:
        self.status.setText("Abgeschlossen")
        self.bar.setRange(0, 100)
        self.bar.setValue(100)
        self.current.setText(message)

    def set_error(self, message: str) -> None:
        self.status.setText("Fehler")
        self.bar.setRange(0, 100)
        self.bar.setValue(0)
        self.current.setText(message)
