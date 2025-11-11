import os

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QSizePolicy,
    QScrollArea,
)


def click(do):
    do()
    QCoreApplication.quit()

class ResultsContainer(QWidget):
    def make_click_handler(self, i: int):
        return lambda event: click(self.items[i][4])

    def __init__(self, items, max_height=240):
        """
        items: list of [img_path, text, subtext]
        max_height: maximum height of the results area before scrolling
        """
        super().__init__()
        self.items = items
        # overall background for the widget (behind the scroll area)
        self.setStyleSheet("background-color: #1e1e2e;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(0)

        # Scroll area so results don't grow indefinitely
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("background-color: transparent; border: none;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # keep scrollbar hidden visually

        # Content widget that holds the rows
        content_widget = QWidget()
        # Add a little bottom margin so the last row doesn't get visually clipped by the parent's rounded corners
        # (This fixes "cut off" appearance.)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 8)  # <-- bottom padding added
        content_layout.setSpacing(8)

        # Styles for rows
        normal_row_style = "background-color: #313244; color: #cdd6f4; border-radius: 6px;"

        for item in range(len(items)):
            img_path = items[item][0] if len(items[item][0]) > 0 else ""
            text = str(items[item][1]) if len(items[item][1]) > 0 else ""
            subtext = str(items[item][2]) if len(items[item][2]) > 0 else ""

            row_widget = QWidget()
            row_widget.setFixedHeight(49)

            row_widget.mousePressEvent = self.make_click_handler(item)

            row_widget.setStyleSheet(normal_row_style)
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(8, 6, 8, 6)
            row_layout.setSpacing(8)

            # Image label
            image_label = QLabel()
            pixmap = QPixmap(img_path) if img_path and os.path.exists(img_path) else QPixmap()
            if pixmap.isNull():
                # create a simple gray placeholder pixmap so the row doesn't collapse
                placeholder = QPixmap(25, 25)
                placeholder.fill(Qt.gray)
                pixmap = placeholder
            pixmap = pixmap.scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
            image_label.setFixedSize(25, 25)
            # noinspection PyTypeChecker
            image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            # Text container: vertical stack for main text and subtext
            text_container = QWidget()
            text_layout = QVBoxLayout(text_container)
            text_layout.setContentsMargins(0, 0, 0, 0)
            text_layout.setSpacing(2)

            # Main text (bigger / bold)
            text_label = QLabel(text)
            text_label.setStyleSheet("color: #cdd6f4; font-weight: 600; font-size: 14px;")
            text_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            text_label.setWordWrap(True)

            # Subtext (smaller, muted color)
            subtext_label = QLabel(subtext)
            subtext_label.setStyleSheet("color: #6c7086; font-size: 12px;")
            subtext_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            subtext_label.setWordWrap(True)

            text_layout.addWidget(text_label)
            text_layout.addWidget(subtext_label)

            # Add to row layout
            row_layout.addWidget(image_label)
            row_layout.addWidget(text_container, 1)
            row_layout.addStretch()

            # noinspection PyTypeChecker
            row_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            # Add the row widget to the content layout
            content_layout.addWidget(row_widget)

        # Add a small spacer at the end instead of a stretch to avoid pushing rows into obscure layout behaviour
        content_layout.addSpacing(4)

        scroll.setWidget(content_widget)

        # Limit height so the scroll area appears when needed
        scroll.setMaximumHeight(max_height)
        # noinspection PyTypeChecker
        scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
