import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
import os

class WebApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and icon
        self.setWindowTitle("PomSync")
        script_dir = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(script_dir, "favicon.svg")
        self.setWindowIcon(QIcon(icon_path))
        self.resize(480, 380)

        # Create a stacked widget to hold the loading screen and the web view
        self.stack = QStackedWidget()

        # Create the loading screen widget
        self.loadingWidget = QWidget()
        loadingLayout = QVBoxLayout()
        self.loadingLabel = QLabel("Starting.....")
        self.loadingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loadingLayout.addWidget(self.loadingLabel)
        self.loadingWidget.setLayout(loadingLayout)

        # Create the web browser widget
        self.browser = QWebEngineView()
        # Wrap the URL string with QUrl
        self.browser.setUrl(QUrl("https://pomsync.onrender.com/"))
        # When the page is loaded, call onLoadFinished
        self.browser.loadFinished.connect(self.onLoadFinished)

        # Add both widgets to the stack: index 0 for loading, index 1 for the website
        self.stack.addWidget(self.loadingWidget)
        self.stack.addWidget(self.browser)

        # Set the stacked widget as the central widget and show the loading screen first
        self.setCentralWidget(self.stack)
        self.stack.setCurrentIndex(0)

    def onLoadFinished(self, ok):
        if ok:
            # Switch to the web browser view when loading is finished
            self.stack.setCurrentIndex(1)
        else:
            self.loadingLabel.setText("Failed to load website.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebApp()
    window.show()
    sys.exit(app.exec())

# For windows: pyinstaller --onefile --windowed --name=PomSync --icon=favicon.ico --add-data "favicon.svg;." webview.py
# For linux: pyinstaller --onefile --windowed --name=PomSync --icon=favicon.ico --add-data "favicon.svg:." webview.py

