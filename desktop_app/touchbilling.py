# desktop_app/billing.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class BillingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        label = QLabel("Welcome to the Billing Section")
        layout.addWidget(label)

        self.setLayout(layout)
