from PySide6.QtWidgets import QLabel

from ui.widgets.card import LMCard
from ui.widgets.badge import LMBadge


class LMMetricCard(LMCard):
    def __init__(self, value: str, label: str, badge: str = "Ready", tone: str = "neutral", parent=None):
        super().__init__(None, parent)
        self.value_label = QLabel(value)
        self.value_label.setObjectName("metricValue")
        self.label = QLabel(label)
        self.label.setObjectName("muted")
        self.badge = LMBadge(badge, tone)
        self.layout.addWidget(self.value_label)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.badge)

    def set_value(self, value: str | int) -> None:
        self.value_label.setText(str(value))
