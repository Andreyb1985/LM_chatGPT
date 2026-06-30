from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from ui.widgets.badge import LMBadge
from ui.widgets.card import LMCard


class ValidationPage(QWidget):
    def __init__(self, window):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(18)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("Prüfung")
        title.setObjectName("pageTitle")
        subtitle = QLabel("PersNr, E-Mail, Anhänge, Warnungen und Fehler vor dem Versand prüfen.")
        subtitle.setObjectName("muted")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch(1)
        export_btn = QPushButton("Audit öffnen")
        export_btn.clicked.connect(window.open_audit_file)
        header.addWidget(export_btn)
        root.addLayout(header)

        summary = QGridLayout()
        summary.setSpacing(14)
        window.validation_total_badge = LMBadge("0 Mitarbeiter", "neutral")
        window.validation_ready_badge = LMBadge("0 OK", "success")
        window.validation_missing_badge = LMBadge("0 ohne E-Mail", "warning")
        window.validation_error_badge = LMBadge("0 Fehler", "error")
        for i, badge in enumerate([
            window.validation_total_badge,
            window.validation_ready_badge,
            window.validation_missing_badge,
            window.validation_error_badge,
        ]):
            card = LMCard()
            card.layout.addWidget(badge)
            summary.addWidget(card, 0, i)
        root.addLayout(summary)

        filters = LMCard("Filter & Ergebnisse")
        row = QHBoxLayout()
        window.search_persnr_edit = QLineEdit()
        window.search_persnr_edit.setPlaceholderText("Suche PersNr")
        window.search_email_edit = QLineEdit()
        window.search_email_edit.setPlaceholderText("Suche E-Mail")
        window.status_filter_combo = QComboBox()
        window.status_filter_combo.addItems(["Alle", "OK", "Keine E-Mail", "Keine Dateien", "Fehler", "Dry-Run", "Gesendet"])
        window.btn_select_all = QPushButton("Alle markieren")
        window.btn_select_none = QPushButton("Alle abwählen")
        window.btn_clear_filters = QPushButton("Filter zurücksetzen")
        for w in [
            QLabel("PersNr"),
            window.search_persnr_edit,
            QLabel("E-Mail"),
            window.search_email_edit,
            QLabel("Status"),
            window.status_filter_combo,
            window.btn_select_all,
            window.btn_select_none,
            window.btn_clear_filters,
        ]:
            row.addWidget(w)
        filters.layout.addLayout(row)
        root.addWidget(filters)

        window.table = QTableWidget(0, 10)
        window.table.setAlternatingRowColors(True)
        window.table.setHorizontalHeaderLabels([
            "Auswahl",
            "PersNr",
            "Name, Vorname",
            "E-Mail",
            "Dateien",
            "Anzahl",
            "Status",
            "Anhang",
            "Passwort",
            "Fehler",
        ])
        window.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        window.table.verticalHeader().setVisible(False)
        root.addWidget(window.table, 1)
