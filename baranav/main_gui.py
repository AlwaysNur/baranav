import sys
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QWidget,
    QVBoxLayout,
)
from PyQt5.QtWidgets import QShortcut

from results import get_results
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

        self.lay = QVBoxLayout()
        self.lay.setContentsMargins(10, 10, 10, 10)
        self.lay.setSpacing(8)
        self.setLayout(self.lay)

        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Search, Calculate, and so much more!")
        self.line_edit.setStyleSheet(
            "background: #181825; color: #cdd6f4; padding: 10px; font-size: 14px; "
            "border-top-left-radius: 8px; border-top-right-radius: 8px;"
        )
        self.line_edit.setFixedHeight(40)
        self.lay.addWidget(self.line_edit)
        self.line_edit.setFocus()

        self.results = QWidget().setFixedHeight(1)

        self.lay.addWidget(self.results)

        self.line_edit.textChanged.connect(self.on_text_changed)

    def on_text_changed(self, text):
        results_list = get_results(text)

        # Create a new ResultsContainer with the updated results
        new_results_widget = ResultsContainer(results_list,280)

        # Find index of current results widget in the layout
        index = self.lay.indexOf(self.results)
        if index == -1:
            # fallback: append
            self.lay.addWidget(new_results_widget)
        else:
            # remove the old widget from the layout and delete it
            old = self.results
            self.lay.takeAt(index)  # remove the layout item
            old.setParent(None)
            old.deleteLater()

            # insert the new widget at the same position
            self.lay.insertWidget(index, new_results_widget)

        # keep reference to the current results widget
        self.results = new_results_widget
