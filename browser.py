import sys
import random
import re
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTabWidget, QInputDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.favorite_buttons = [] 

        self.setWindowTitle("Browser")
        self.setGeometry(100, 100, 800, 600)

        self.home_url = "https://www.google.com"  # Set your home URL here

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()  # Vertical layout
        self.central_widget.setLayout(self.layout)

        # Create a QHBoxLayout for the address bar and buttons
        self.top_layout = QHBoxLayout()
        self.layout.addLayout(self.top_layout)

        # Add the address bar to the top layout
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.load_url)
        self.address_bar.setStyleSheet("border-radius: 10px;")
        self.address_bar.setMinimumWidth(300)
        self.top_layout.addWidget(self.address_bar)

        # Add the "+" button to create a new tab
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.clicked.connect(self.add_new_tab)
        self.add_tab_button.setStyleSheet("border-radius: 5px; font-size: 40px;")
        self.add_tab_button.setMinimumWidth(70)
        self.add_tab_button.setMinimumHeight(70)
        self.top_layout.addWidget(self.add_tab_button)

        self.remove_tab_button = QPushButton("-")
        self.remove_tab_button.clicked.connect(self.remove_tab)
        self.remove_tab_button.setStyleSheet("border-radius: 5px; font-size: 75px;")
        self.remove_tab_button.setMinimumWidth(70)
        self.remove_tab_button.setMinimumHeight(70)
        self.top_layout.addWidget(self.remove_tab_button)

        self.favorite_button = QPushButton("Favorite")
        self.favorite_button.clicked.connect(self.save_favorite)
        self.top_layout.addWidget(self.favorite_button)

        # Add the search button to the top layout
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_query)
        self.top_layout.addWidget(self.search_button)

        # Add the web view below the top layout
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.favorite_layout = QHBoxLayout()
        self.layout.addLayout(self.favorite_layout)

        self.history = []

        # Add the first tab
        self.add_new_tab()

        self.load_favorites()

    def add_new_tab(self):
        new_webview = QWebEngineView()
        new_webview.loadStarted.connect(self.load_started)
        new_webview.loadFinished.connect(self.load_finished)

        tab_index = self.tab_widget.addTab(new_webview, "New Tab")
        self.tab_widget.setCurrentIndex(tab_index)
        self.tab_widget.tabBar().setTabText(tab_index, "New Tab")  # Set the text next to the new tab

    def remove_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index != 0:
            self.tab_widget.removeTab(current_index)

    def load_url(self):
        url = self.address_bar.text()
        if url:
            if url.startswith("http://") or url.startswith("https://"):
                # If it starts with "http://" or "https://", treat it as a valid URL
                print("Loading URL directly:", url)
                self.current_webview().setUrl(QUrl(url))
                self.history.append(url)
            elif re.search(r'\..{2,}$', url):
                # If it looks like a domain without a protocol, add "https://" and load
                new_url = "https://" + url
                print("Loading URL with 'https://':", new_url)
                self.current_webview().setUrl(QUrl(new_url))
                self.history.append(new_url)
            else:
                # If it doesn't start with "http://" or "https://", treat it as a search query
                search_query = "+".join(url.split())  # Convert spaces to "+" for the search query
                google_search_url = f"https://www.google.com/search?q={search_query}"
                print("Loading Google search:", google_search_url)
                self.current_webview().setUrl(QUrl(google_search_url))
                self.history.append(google_search_url)

    def search_query(self):
        # Load the search query in the current tab
        self.load_url()

    def current_webview(self):
        # Get the web view of the current tab
        return self.tab_widget.currentWidget()

    def load_started(self):
        webview = self.sender()
        self.setWindowTitle(webview.title())

    def load_finished(self):
        webview = self.sender()
        self.setWindowTitle(webview.title() + " | " + webview.url().toString())
      
        index = self.tab_widget.indexOf(webview)
        self.tab_widget.setTabText(index, webview.title())

    def navigate_back(self):
        webview = self.current_webview()
        if webview:
            webview.back()

    def navigate_forward(self):
        webview = self.current_webview()
        if webview:
            webview.forward()
    
    def save_favorite(self):
        current_url = self.current_webview().url().toString()
        if current_url != "":
            # Implement your logic to save the favorite URL
            with open("favorites.txt", "a") as f:
                f.write(current_url + "\n")
            print("Favorite saved:", current_url)
            self.load_favorites()


    def add_new_favorite_tab(self, url):
        new_webview = QWebEngineView()
        new_webview.loadStarted.connect(self.load_started)
        new_webview.loadFinished.connect(self.load_finished)
        new_webview.setUrl(QUrl(url))

        title = QUrl(url).host()
        tab_index = self.tab_widget.addTab(new_webview, title)
        self.tab_widget.setCurrentIndex(tab_index)
        self.tab_widget.tabBar().setTabText(tab_index, title)

    def add_favorite_button(self, url):
        clean_url = url.replace("https://", "").replace("http://", "").replace("www.", "")
        favorite_button = QPushButton(clean_url)
        favorite_button.clicked.connect(lambda: self.open_favorite_url(url))

        self.favorite_layout.addWidget(favorite_button)
        self.favorite_buttons.append(favorite_button)
        
        # Add remove button for each favorite
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.remove_favorite(url))
        
        # Add both buttons to a horizontal layout
        layout = QHBoxLayout()
        layout.addWidget(favorite_button)
        layout.addWidget(remove_button)
        
        # Add the layout to the favorite layout
        self.favorite_layout.addLayout(layout)

    def remove_favorite(self, url):
        with open("favorites.txt", "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if line.strip() != url:
                    f.write(line)
            f.truncate()
        
        # Reload favorites after removing one
        self.load_favorites()


    def open_favorite_url(self, url):
        new_webview = QWebEngineView()
        new_webview.loadStarted.connect(self.load_started)
        new_webview.loadFinished.connect(self.load_finished)
        new_webview.setUrl(QUrl(url))

        title = QUrl(url).host()
        tab_index = self.tab_widget.addTab(new_webview, title)
        self.tab_widget.setCurrentIndex(tab_index)
        self.tab_widget.tabBar().setTabText(tab_index, title)

    def load_favorites(self):
        # Clear the layout containing favorite buttons
        for button in self.favorite_buttons:
            button.setParent(None)
        self.favorite_buttons = []  # Clear the list of favorite buttons
        if not self.favorite_buttons:
            self.remove_tab_button.setParent(None)


        # Load favorites from file and add them as new buttons
        try:
            with open("favorites.txt", "r") as f:
                for line in f:
                    self.add_favorite_button(line.strip())
        except FileNotFoundError:
            pass  # No favorites file found, do nothing


if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = WebBrowser()
    browser.show()
    sys.exit(app.exec_())
