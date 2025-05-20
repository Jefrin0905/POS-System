# desktop_app/dashboard.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from admin_panel import AdminPanel
from billing import BillingWindow

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # 🧾 Billing Button
        billing_btn = QPushButton("🧾 Billing")
        billing_btn.clicked.connect(self.open_billing)
        layout.addWidget(billing_btn)

        # ⚙️ Admin Panel Button
        admin_btn = QPushButton("⚙️ Admin Panel")
        admin_btn.clicked.connect(self.open_admin_panel)
        layout.addWidget(admin_btn)

        self.setLayout(layout)

    def open_billing(self):
        self.billing_window = BillingWindow()
        self.billing_window.show()


    def open_admin_panel(self):
        self.admin_window = AdminPanel()
        self.admin_window.show()
    
    