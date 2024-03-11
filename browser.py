import sys
import os
import random
import re
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

patron = r'\..{2,}$'

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        

        self.setWindowTitle("Timmy's Professional Web Browser")
        self.setGeometry(100, 100, 800, 600)

        self.home_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Set your home URL here

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()  # Vertical layout
        self.central_widget.setLayout(self.layout)

        # Create a QHBoxLayout for the address bar and buttons
        self.top_layout = QHBoxLayout()
        self.layout.addLayout(self.top_layout)

        # Add the back button to the top layout
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.navigate_back)
        self.top_layout.addWidget(self.back_button)

        # Add the address bar to the top layout
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.load_url)
        self.address_bar.setStyleSheet("border-radius: 10px;")
        self.top_layout.addWidget(self.address_bar)

        # Add the web view below the top layout
        self.webview = QWebEngineView()
        self.layout.addWidget(self.webview)

        self.history = []

    def load_url(self):
        url = self.address_bar.text()
        chance = random.randint(1, 3)  # Increase the range for more random redirects and pop-ups
        if chance == 1:
            # Randomly trigger an annoying pop-up
            self.show_annoying_popup()
        elif chance == 2:
            # Randomly redirect to a funny or unexpected URL
            self.redirect_to_another_site()
        else:
            print("Input URL:", url)
            if url:
                if url.startswith("http://") or url.startswith("https://"):
                    # If it starts with "http://" or "https://", treat it as a valid URL
                    print("Loading URL directly:", url)
                    self.webview.setUrl(QUrl(url))
                    self.history.append(url)
                elif re.search(patron, url):
                    # If it looks like a domain without a protocol, add "https://" and load
                    new_url = "https://" + url
                    print("Loading URL with 'https://':", new_url)
                    self.webview.setUrl(QUrl(new_url))
                    self.history.append(new_url)
                else:
                    # If it doesn't start with "http://" or "https://", treat it as a search query
                    search_query = "+".join(url.split())  # Convert spaces to "+" for the search query
                    google_search_url = f"https://www.google.com/search?q={search_query}"
                    print("Loading Google search:", google_search_url)
                    self.webview.setUrl(QUrl(google_search_url))
                    self.history.append(google_search_url)

                # Configure web view settings
                self.webview.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
                settings = self.webview.settings()
                settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
                settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)

    def show_annoying_popup(self):
        # Show an annoying pop-up with a random message
        messages = [
            "Timmy is crying, go help him",
            "Bomb sent to destination.",
            "This browser is property of Timmy, pay your 100.000 € fine now!"
        ]
        message = random.choice(messages)
        QMessageBox.warning(self, "Ball tickler", message)

    def redirect_to_another_site(self):
        # Randomly redirect to a funny or unexpected URL
        redirect_url = random.choice(["https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
                                      "https://www.youtube.com/watch?v=R-c2cYCNLQo",  
                                      "https://www.youtube.com/watch?v=hjQCSLb9OXU"])  
        print("Redirecting to:", redirect_url)
        self.webview.setUrl(QUrl(redirect_url))

    def navigate_back(self):
        if len(self.history) > 1:
            previous_url = self.history[-2]  # Get the previous URL from history
            self.history.pop()  # Remove the current URL from history
            self.webview.setUrl(QUrl(previous_url))  # Load the previous URL
        else:
            self.webview.setUrl(QUrl(self.home_url))  # Load the home URL

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = WebBrowser()
    browser.show()
    sys.exit(app.exec_())