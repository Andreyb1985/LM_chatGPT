from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.widgets.badge import LMBadge
from ui.widgets.card import LMCard
from ui.widgets.drop_zone import LMDropZone
from ui.widgets.log_view import LMLogView
from ui.widgets.progress_card import LMProgressCard


class ProcessingPage(QWidget):
    """Primary workflow page for PDF/Excel selection and job execution."""

    def __init__(self, window):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(22)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("Verarbeitung")
        title.setObjectName("pageTitle")
        subtitle = QLabel("PDF und Excel laden, prüfen und anschließend sicher verarbeiten.")
        subtitle.setObjectName("muted")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch(1)
        window.btn_check = QPushButton("Prüfen")
        window.btn_check.setObjectName("primary")
        window.btn_send = QPushButton("Verarbeiten & Versand vorbereiten")
        window.btn_send_selected = QPushButton("Nur ausgewählte senden")
        header.addWidget(window.btn_check)
        header.addWidget(window.btn_send)
        header.addWidget(window.btn_send_selected)
        root.addLayout(header)

        grid = QGridLayout()
        grid.setSpacing(18)

        workspace = LMCard("Smart Workspace")
        workspace.layout.addWidget(LMBadge("Lokale Verarbeitung", "primary"))
        form = QFormLayout()
        form.setSpacing(12)

        window.input_mode_combo = QComboBox()
        window.input_mode_combo.addItem("PDF-Ordner mit fertigen Dateien", "folder")
        window.input_mode_combo.addItem("Eine Gesamt-PDF zum Aufteilen", "single_pdf")
        saved_input_mode = str(window.settings.get("ui", {}).get("last_pdf_input_mode", "folder") or "folder")
        idx = window.input_mode_combo.findData(saved_input_mode)
        if idx >= 0:
            window.input_mode_combo.setCurrentIndex(idx)

        window.company_combo = QComboBox()
        window.active_company_label = QLabel()
        window.active_company_label.setObjectName("muted")
        window.dry_run_checkbox = QCheckBox("Dry-Run: PDF erstellen, aber keine E-Mails senden")
        window.dry_run_checkbox.setChecked(bool(window.settings.get("ui", {}).get("dry_run_default", True)))

        form.addRow("Eingabemodus", window.input_mode_combo)
        form.addRow("Unternehmen", window.company_combo)
        form.addRow("Aktive Firma", window.active_company_label)
        form.addRow("Sicherheit", window.dry_run_checkbox)
        workspace.layout.addLayout(form)
        grid.addWidget(workspace, 0, 0)

        files = LMCard("Import Workflow")
        window.pdf_input_edit = QLineEdit(window.settings.get("ui", {}).get("last_pdf_dir", ""))
        window.pdf_input_edit.setObjectName("pathMirror")
        window.pdf_input_edit.setReadOnly(True)
        window.excel_file_edit = QLineEdit(window._current_company_email_excel_file(window.settings.get("selected_company_id")))
        window.excel_file_edit.setObjectName("pathMirror")
        window.excel_file_edit.setReadOnly(True)

        window.pdf_drop_zone = LMDropZone(
            "① PDF laden",
            "Ordner mit fertigen Abrechnungen oder eine Gesamt-PDF per Drag & Drop ablegen.",
            "Ordner wählen",
        )
        window.excel_drop_zone = LMDropZone(
            "② Excel laden",
            "Personalnummern und E-Mail-Adressen aus der Zuordnungstabelle laden.",
            "Datei wählen",
        )
        window.pdf_drop_zone.set_path(window.pdf_input_edit.text())
        window.excel_drop_zone.set_path(window.excel_file_edit.text())

        files.layout.addWidget(window.pdf_drop_zone)
        files.layout.addWidget(window.pdf_input_edit)
        files.layout.addWidget(window.excel_drop_zone)
        files.layout.addWidget(window.excel_file_edit)
        grid.addWidget(files, 0, 1, 2, 1)

        pipeline = LMCard("Workflow Status")
        for step, tone in [
            ("① PDF", "neutral"),
            ("② Excel", "neutral"),
            ("③ Prüfung", "info"),
            ("④ Verarbeitung", "primary"),
            ("⑤ Versand", "neutral"),
            ("⑥ Berichte", "neutral"),
        ]:
            pipeline.layout.addWidget(LMBadge(step, tone))
        hint = QLabel("Empfohlen: zuerst prüfen. Erst nach Kontrolle in Prüfung/Versand senden.")
        hint.setObjectName("muted")
        hint.setWordWrap(True)
        pipeline.layout.addWidget(hint)
        grid.addWidget(pipeline, 1, 0)

        window.processing_progress = LMProgressCard("Live Processing")
        grid.addWidget(window.processing_progress, 2, 0)

        log_card = LMCard("Operation Journal")
        window.log = LMLogView()
        log_card.layout.addWidget(window.log)
        grid.addWidget(log_card, 2, 1)

        root.addLayout(grid)
        root.addStretch(1)

        # Legacy-compatible actions and path mirrors.
        window.btn_pdf_select = window.pdf_drop_zone.browse_button
        window.pdf_drop_zone.browse_requested.connect(window.choose_pdf_input)
        window.excel_drop_zone.browse_requested.connect(window.choose_excel_file)
        window.pdf_drop_zone.path_dropped.connect(self._set_pdf_path)
        window.excel_drop_zone.path_dropped.connect(self._set_excel_path)
        window.pdf_input_edit.textChanged.connect(window.pdf_drop_zone.set_path)
        window.excel_file_edit.textChanged.connect(window.excel_drop_zone.set_path)

    def _set_pdf_path(self, path: str) -> None:
        window = self.window()
        window.pdf_input_edit.setText(path)
        window._remember_ui_path(pdf_dir=path)

    def _set_excel_path(self, path: str) -> None:
        window = self.window()
        window.excel_file_edit.setText(path)
        window._remember_ui_path(excel_file=path)
