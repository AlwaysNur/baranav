import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QSizePolicy,
    QScrollArea,
)


class ResultsContainer(QWidget):
    def __init__(self, items, max_height=240):
        """
        items: list of [img_path, text, subtext]
        max_height: maximum height of the results area before scrolling
        """
        super().__init__()

        # overall background for the widget (behind the scroll area)
        self.setStyleSheet("background-color: #1e1e2e;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(0)

        # Scroll area so results don't grow indefinitely
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        # make scroll background match parent (so only the rows' backgrounds show)
        scroll.setStyleSheet("background-color: transparent; border: none;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Keep the vertical scrollbar functional but visually hidden:
        # - setting policy to AlwaysOn ensures the scrollbar exists (so wheel/keyboard scrolling works),
        # - then we set the scrollbar stylesheet to zero width / transparent so it doesn't appear.
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.verticalScrollBar().setStyleSheet(
            """
            QScrollBar:vertical {
                background: transparent;
                width: 0px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: transparent;
                min-height: 20px;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                height: 0px;
            }
            """
        )

        # Content widget that holds the rows
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)

        for item in items:
            img_path = item[0] if len(item) > 0 else ""
            text = str(item[1]) if len(item) > 1 else ""
            subtext = str(item[2]) if len(item) > 2 else ""

            # Row widget: background (gray) applies to the whole row
            row_widget = QWidget()
            row_widget.setStyleSheet(
                "background-color: #313244; color: #cdd6f4; border-radius: 6px;"
            )
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(8, 6, 8, 6)
            row_layout.setSpacing(8)

            # Image label
            image_label = QLabel()
            pixmap = QPixmap(img_path) if img_path and os.path.exists(img_path) else QPixmap()
            if pixmap.isNull():
                # create a simple gray placeholder pixmap so the row doesn't collapse
                placeholder = QPixmap(40, 40)
                placeholder.fill(Qt.gray)
                pixmap = placeholder
            pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
            image_label.setFixedSize(40, 40)
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

            # Add the row widget to the content layout
            content_layout.addWidget(row_widget)

        # Add a stretch at the end so rows hug the top
        content_layout.addStretch()

        scroll.setWidget(content_widget)

        # Limit height so the scroll bar appears when needed
        scroll.setMaximumHeight(max_height)

        main_layout.addWidget(scroll)
        self.setLayout(main_layout)