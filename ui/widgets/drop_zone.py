from pathlib import Path

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout


class LMDropZone(QFrame):
    """Small drag & drop target used by the processing workflow.

    The widget keeps the selected path visible and emits ``path_dropped`` when the
    user drops a file/folder from Finder/Explorer. It does not own validation; the
    existing legacy validation remains the source of truth.
    """

    path_dropped = Signal(str)
    browse_requested = Signal()

    def __init__(self, title: str, helper: str, button_text: str, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setObjectName("dropZone")
        self._empty_text = "Noch nicht ausgewählt"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        head = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setObjectName("sectionTitle")
        head.addWidget(title_label)
        head.addStretch(1)
        self.browse_button = QPushButton(button_text)
        self.browse_button.clicked.connect(self.browse_requested.emit)
        head.addWidget(self.browse_button)
        layout.addLayout(head)

        helper_label = QLabel(helper)
        helper_label.setObjectName("muted")
        helper_label.setWordWrap(True)
        layout.addWidget(helper_label)

        self.path_label = QLabel(self._empty_text)
        self.path_label.setObjectName("dropPath")
        self.path_label.setWordWrap(True)
        layout.addWidget(self.path_label)

    def set_path(self, value: str) -> None:
        text = str(value or "").strip()
        self.path_label.setText(text if text else self._empty_text)
        self.setProperty("hasPath", "true" if text else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def set_button_text(self, text: str) -> None:
        self.browse_button.setText(text)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("dragging", "true")
            self.style().unpolish(self)
            self.style().polish(self)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setProperty("dragging", "false")
        self.style().unpolish(self)
        self.style().polish(self)
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        self.setProperty("dragging", "false")
        self.style().unpolish(self)
        self.style().polish(self)
        urls = event.mimeData().urls()
        if not urls:
            event.ignore()
            return
        path = urls[0].toLocalFile()
        if path:
            self.path_dropped.emit(str(Path(path)))
            event.acceptProposedAction()
        else:
            event.ignore()
