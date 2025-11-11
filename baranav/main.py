import sys
from PyQt5.QtWidgets import QApplication
from main_gui import OverlayBar

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Baranav")
    baranav = OverlayBar()
    baranav.show()
    sys.exit(app.exec_())