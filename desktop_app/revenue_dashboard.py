import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QDateEdit, QHBoxLayout
)
from PyQt5.QtCore import QDate
from datetime import datetime, timedelta

class RevenueDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Revenue Dashboard")
        self.setGeometry(300, 100, 500, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.filter_type = QComboBox()
        self.filter_type.addItems(["Today", "This Week", "This Month", "Custom Range"])
        self.filter_type.currentIndexChanged.connect(self.toggle_date_inputs)

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate())

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())

        self.load_button = QPushButton("Load Report")
        self.load_button.clicked.connect(self.load_report)

        self.result_label = QLabel("")

        # Layouts
        top = QHBoxLayout()
        top.addWidget(self.filter_type)
        top.addWidget(self.date_from)
        top.addWidget(self.date_to)
        top.addWidget(self.load_button)

        self.layout.addLayout(top)
        self.layout.addWidget(self.result_label)

        self.toggle_date_inputs()  # Default

    def toggle_date_inputs(self):
        is_custom = self.filter_type.currentText() == "Custom Range"
        self.date_from.setEnabled(is_custom)
        self.date_to.setEnabled(is_custom)

    def load_report(self):
        path = os.path.join(os.getcwd(), "sales_data.json")
        if not os.path.exists(path):
            self.result_label.setText("No sales data found.")
            return

        with open(path, 'r') as f:
            try:
                sales = json.load(f)
            except json.JSONDecodeError:
                self.result_label.setText("Invalid data file.")
                return

        now = datetime.now()
        if self.filter_type.currentText() == "Today":
            start = datetime(now.year, now.month, now.day)
            end = start + timedelta(days=1)
        elif self.filter_type.currentText() == "This Week":
            start = now - timedelta(days=now.weekday())
            end = start + timedelta(days=7)
        elif self.filter_type.currentText() == "This Month":
            start = datetime(now.year, now.month, 1)
            end = datetime(now.year, now.month + 1, 1) if now.month < 12 else datetime(now.year + 1, 1, 1)
        else:
            start = datetime.strptime(self.date_from.date().toString("yyyy-MM-dd"), "%Y-%m-%d")
            end = datetime.strptime(self.date_to.date().toString("yyyy-MM-dd"), "%Y-%m-%d") + timedelta(days=1)

        filtered_sales = []
        for entry in sales:
            entry_time = datetime.strptime(entry['timestamp'], '%Y-%m-%d %H:%M:%S')
            if start <= entry_time < end:
                filtered_sales.append(entry)

        total_orders = len(filtered_sales)
        total_revenue = sum(sale['total'] for sale in filtered_sales)

        self.result_label.setText(f"Orders: {total_orders}\nTotal Revenue: ₹{total_revenue:.2f}")
