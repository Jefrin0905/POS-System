import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QFileDialog,
    QMessageBox, QDateEdit
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton

from generate_bill_pdf import generate_pdf
import menu_editor
import revenue_dashboard


class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel - Hotel POS")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #f8f8f8;")
        
        layout = QVBoxLayout()
        
        header = QLabel("📊 Admin Dashboard")
        header.setFont(QFont("Arial", 20))
        header.setStyleSheet("color: #333;")
        layout.addWidget(header)

        # Date filters
        date_layout = QHBoxLayout()
        self.from_date = QDateEdit()
        self.from_date.setDate(QDate.currentDate().addDays(-30))
        self.to_date = QDateEdit()
        self.to_date.setDate(QDate.currentDate())
        filter_btn = QPushButton("🔍 Filter")
        filter_btn.clicked.connect(self.load_sales_data)

        date_layout.addWidget(QLabel("From:"))
        date_layout.addWidget(self.from_date)
        date_layout.addWidget(QLabel("To:"))
        date_layout.addWidget(self.to_date)
        date_layout.addWidget(filter_btn)

        layout.addLayout(date_layout)

        # Sales Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Bill No", "Customer", "Total ₹", "Actions"])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 300)
        layout.addWidget(self.table)

        # Shortcut buttons
        btn_layout = QHBoxLayout()
        menu_btn = QPushButton("🍽️ Menu Manager")
        menu_btn.clicked.connect(self.open_menu_editor)
        revenue_btn = QPushButton("📈 Revenue Report")
        revenue_btn.clicked.connect(self.open_revenue_dashboard)

        btn_layout.addWidget(menu_btn)
        btn_layout.addWidget(revenue_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_sales_data()

    def load_sales_data(self):
        self.table.setRowCount(0)
        from_date = self.from_date.date().toPyDate()
        to_date = self.to_date.date().toPyDate()

        if not os.path.exists("sales_data.json"):
            return

        with open("sales_data.json", "r") as f:
            all_sales = json.load(f)

        for i, sale in enumerate(all_sales):
            sale_date = QDate.fromString(sale["date"], "yyyy-MM-dd").toPyDate()
            if not (from_date <= sale_date <= to_date):
                continue

            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(sale["date"]))
            self.table.setItem(i, 1, QTableWidgetItem(sale["bill_no"]))
            self.table.setItem(i, 2, QTableWidgetItem(sale["customer_name"]))
            self.table.setItem(i, 3, QTableWidgetItem(f"₹ {sale['total']:.2f}"))

            # Actions
            btn_view = QPushButton("📄 View PDF")
            btn_view.clicked.connect(lambda _, s=sale: self.view_pdf(s))
            btn_delete = QPushButton("🗑️ Delete")
            btn_delete.clicked.connect(lambda _, i=i: self.delete_sale(i))

            action_layout = QHBoxLayout()
            action_layout.addWidget(btn_view)
            action_layout.addWidget(btn_delete)

            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.table.setCellWidget(i, 4, action_widget)

    def view_pdf(self, sale):
        save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", f"{sale['bill_no']}.pdf", "PDF Files (*.pdf)")
        if save_path:
            generate_pdf(sale, save_path)
            QMessageBox.information(self, "Saved", "PDF generated successfully!")

    def delete_sale(self, index):
        confirm = QMessageBox.question(self, "Confirm", "Are you sure you want to delete this bill?", 
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            with open("sales_data.json", "r") as f:
                sales = json.load(f)

            del sales[index]

            with open("sales_data.json", "w") as f:
                json.dump(sales, f, indent=4)

            self.load_sales_data()
            QMessageBox.information(self, "Deleted", "Bill deleted successfully.")

    def open_menu_editor(self):
        self.menu_editor_window = menu_editor.MenuEditor()
        self.menu_editor_window.show()

    def open_revenue_dashboard(self):
        self.revenue_window = revenue_dashboard.RevenueDashboard()
        self.revenue_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminDashboard()
    window.show()
    sys.exit(app.exec())
