# desktop_app/login.py

from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel
from dashboard import Dashboard  # Make sure dashboard.py exists with Dashboard class

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)

        # Set up layout
        layout = QVBoxLayout()

        # Username field
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username)

        # Password field
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)  # Simplified line
        layout.addWidget(self.password)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        # Message label
        self.message = QLabel("")
        layout.addWidget(self.message)

        # Finalize layout
        self.setLayout(layout)

    def check_login(self):
        user = self.username.text()
        pwd = self.password.text()

        # Very basic login validation
        if user == "admin" and pwd == "admin":
            self.message.setText("Login successful!")
            self.open_dashboard()
        else:
            self.message.setText("Invalid credentials")

    def open_dashboard(self):
        self.dashboard = Dashboard()
        self.dashboard.show()
        self.close()
