from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime
import os
import json

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt
from data_store import menu_items


class BillingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing")
        self.setGeometry(100, 100, 800, 600)
        self.cart = []

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        # Top input section
        top_layout = QHBoxLayout()

        self.item_select = QComboBox()
        self.update_menu_items()

        self.qty_input = QLineEdit()
        self.qty_input.setPlaceholderText("Qty")

        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_to_cart)

        top_layout.addWidget(QLabel("Item:"))
        top_layout.addWidget(self.item_select)
        top_layout.addWidget(QLabel("Qty:"))
        top_layout.addWidget(self.qty_input)
        top_layout.addWidget(add_btn)

        self.layout.addLayout(top_layout)

        # Cart table
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["Item", "Price", "Qty", "Tax%", "Total"])
        self.layout.addWidget(self.cart_table)

        # Totals and action buttons
        self.total_label = QLabel("Total: ₹0.00")
        self.layout.addWidget(self.total_label)

        save_btn = QPushButton("Save Bill")
        save_btn.clicked.connect(self.save_bill)
        self.layout.addWidget(save_btn)

        print_btn = QPushButton("Print PDF")
        print_btn.clicked.connect(self.print_pdf)
        self.layout.addWidget(print_btn)

    def update_menu_items(self):
        self.item_select.clear()
        for item in menu_items:
            self.item_select.addItem(item['name'])

    def add_to_cart(self):
        item_name = self.item_select.currentText()
        try:
            qty = int(self.qty_input.text())
            if qty <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Enter a valid quantity.")
            return

        item = next((i for i in menu_items if i['name'] == item_name), None)
        if item:
            total = (item['price'] * qty) * (1 + item['tax_percent'] / 100)
            self.cart.append({
                'name': item['name'],
                'price': item['price'],
                'qty': qty,
                'tax': item['tax_percent'],
                'total': total
            })
            self.update_cart_table()
            self.qty_input.clear()

    def update_cart_table(self):
        self.cart_table.setRowCount(len(self.cart))
        grand_total = 0
        for row, item in enumerate(self.cart):
            self.cart_table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.cart_table.setItem(row, 1, QTableWidgetItem(str(item['price'])))
            self.cart_table.setItem(row, 2, QTableWidgetItem(str(item['qty'])))
            self.cart_table.setItem(row, 3, QTableWidgetItem(str(item['tax'])))
            self.cart_table.setItem(row, 4, QTableWidgetItem("₹{:.2f}".format(item['total'])))
            grand_total += item['total']
        self.total_label.setText("Total: ₹{:.2f}".format(grand_total))

    def save_bill(self):
        if not self.cart:
            QMessageBox.warning(self, "Error", "Cart is empty.")
            return

        now = datetime.datetime.now()
        bill_data = {
            "timestamp": now.strftime('%Y-%m-%d %H:%M:%S'),
            "items": self.cart,
            "total": sum(item['total'] for item in self.cart)
        }

        file_path = os.path.join(os.getcwd(), "sales_data.json")
        sales = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    sales = json.load(f)
                except json.JSONDecodeError:
                    pass

        sales.append(bill_data)
        with open(file_path, 'w') as f:
            json.dump(sales, f, indent=4)

        QMessageBox.information(self, "Saved", "Bill saved and recorded.")
        self.cart = []
        self.update_cart_table()
        self.total_label.setText("Total: ₹0.00")

    def print_pdf(self):
        if not self.cart:
            QMessageBox.warning(self, "Error", "Cart is empty. Cannot print.")
            return

        now = datetime.datetime.now()
        file_name = f"receipt_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = os.path.join(os.getcwd(), file_name)

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, height - 50, "Hotel POS - Invoice")

        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Date: {now.strftime('%Y-%m-%d %H:%M:%S')}")

        y = height - 120
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Item")
        c.drawString(200, y, "Price")
        c.drawString(300, y, "Qty")
        c.drawString(350, y, "Tax")
        c.drawString(420, y, "Total")

        y -= 20
        c.setFont("Helvetica", 12)
        grand_total = 0
        for item in self.cart:
            c.drawString(50, y, item['name'])
            c.drawString(200, y, f"₹{item['price']}")
            c.drawString(300, y, str(item['qty']))
            c.drawString(350, y, f"{item['tax']}%")
            c.drawString(420, y, f"₹{item['total']:.2f}")
            grand_total += item['total']
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 50

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y - 10, f"Grand Total: ₹{grand_total:.2f}")
        c.save()

        QMessageBox.information(self, "PDF Created", f"Invoice saved as:\n{file_name}")
