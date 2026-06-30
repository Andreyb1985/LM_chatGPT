from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QProgressBar

from ui.widgets.badge import LMBadge
from ui.widgets.card import LMCard
from ui.widgets.metric_card import LMMetricCard


class DashboardPage(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(24)
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Überblick über Verarbeitung, Versand und Systemstatus.")
        subtitle.setObjectName("muted")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch(1)
        new_btn = QPushButton("New Processing")
        new_btn.setObjectName("primary")
        if parent_window:
            new_btn.clicked.connect(lambda: parent_window.navigate("processing"))
        header.addWidget(new_btn)
        root.addLayout(header)

        kpi = QGridLayout()
        kpi.setSpacing(16)
        self.cards = {}
        for i, (key, value, label, tone) in enumerate([
            ("employees", "0", "Employees processed", "primary"),
            ("sent", "0", "Emails sent", "success"),
            ("missing", "0", "Missing emails", "warning"),
            ("errors", "0", "Errors", "error"),
        ]):
            card = LMMetricCard(value, label, "Ready", tone)
            self.cards[key] = card
            kpi.addWidget(card, 0, i)
        root.addLayout(kpi)

        mid = QGridLayout()
        mid.setSpacing(18)
        health = LMCard("System Health")
        for text, tone in [
            ("SMTP Ready", "success"),
            ("License Active", "success"),
            ("PDF Engine OK", "success"),
            ("Excel Engine OK", "success"),
        ]:
            health.layout.addWidget(LMBadge(text, tone))
        mid.addWidget(health, 0, 0)

        activity = LMCard("Activity Timeline")
        self.activity_label = QLabel("Noch keine Verarbeitung gestartet.\nWähle PDF und Excel in Verarbeitung.")
        self.activity_label.setObjectName("muted")
        activity.layout.addWidget(self.activity_label)
        mid.addWidget(activity, 0, 1)

        reports = LMCard("Recent Reports")
        self.report_buttons = []
        if parent_window:
            for label, callback in [
                ("audit_check.xlsx", parent_window.open_audit_file),
                ("ohne_email_gesamt.pdf", parent_window.open_missing_pdf_file),
                ("send_report.xlsx", parent_window.open_send_report_file),
            ]:
                btn = QPushButton(label)
                btn.clicked.connect(callback)
                btn.setEnabled(False)
                reports.layout.addWidget(btn)
                self.report_buttons.append(btn)
        mid.addWidget(reports, 0, 2)

        pipeline = LMCard("Processing Overview")
        self.pipeline_labels = []
        for step in ["PDF", "Excel", "Prüfung", "Verarbeitung", "Versand", "Berichte"]:
            label = QLabel(f"○ {step}")
            self.pipeline_labels.append(label)
            pipeline.layout.addWidget(label)
        self.pipeline_bar = QProgressBar()
        self.pipeline_bar.setValue(0)
        pipeline.layout.addWidget(self.pipeline_bar)
        mid.addWidget(pipeline, 1, 0, 1, 3)
        root.addLayout(mid)
        root.addStretch(1)

    def update_from_result(self, result: dict) -> None:
        rows = result.get("table_rows", []) or []
        summary = result.get("summary", {}) or {}
        total = len(rows)
        missing = sum(1 for r in rows if "keine e-mail" in str(r.get("Status", "")).lower())
        errors = sum(1 for r in rows if str(r.get("Error", "") or "").strip() or "fehler" in str(r.get("Status", "")).lower())
        sent = sum(1 for r in rows if "gesendet" in str(r.get("Status", "")).lower())
        self.cards["employees"].set_value(total or summary.get("total", 0) or 0)
        self.cards["sent"].set_value(sent or summary.get("sent", 0) or 0)
        self.cards["missing"].set_value(missing)
        self.cards["errors"].set_value(errors)
        self.activity_label.setText("Letzter Lauf abgeschlossen.\nReports und Prüftabelle wurden aktualisiert.")
        self.pipeline_bar.setValue(100)
        for label in self.pipeline_labels:
            label.setText(label.text().replace("○", "✓"))
        for button in self.report_buttons:
            button.setEnabled(True)
