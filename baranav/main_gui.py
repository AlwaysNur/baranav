from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QWidget,
    QVBoxLayout,
)
from PyQt5.QtWidgets import QShortcut

from results import hii
from results_gui import ResultsContainer


class OverlayBar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Baranav")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setStyleSheet("background-color: #181825; border-radius: 12px;")
        self.setFixedWidth(400)

        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            self.move(geo.center().x() - self.width() // 2, geo.center().y() - 60)

        QShortcut(QKeySequence("Esc"), self).activated.connect(QCoreApplication.quit)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Search, Calculate, and so much more!")
        self.line_edit.setStyleSheet(
            "background: #181825; color: #cdd6f4; padding: 10px; font-size: 14px; "
            "border-top-left-radius: 8px; border-top-right-radius: 8px;"
        )
        self.line_edit.setFixedHeight(40)
        layout.addWidget(self.line_edit)

        # results area with each row as its own QWidget (so background + radius apply cleanly)
        self.results = ResultsContainer(hii)
        layout.addWidget(self.results)

        self.setLayout(layout)
        self.line_edit.setFocus()
        self.line_edit.textChanged.connect(self.on_text_changed)

    def on_text_changed(self, text):
        # placeholder for filtering
        print(text)
