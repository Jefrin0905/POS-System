from billing import BillingWindow
from data_store import menu_items  # use only this, remove menu_items = []
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
from revenue_dashboard import RevenueDashboard


class MenuManagementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hotel POS - Menu Management")
        self.setGeometry(300, 100, 600, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.init_ui()
        self.load_menu_items()

    def init_ui(self):
        # Input fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Item Name")

        self.category_input = QComboBox()
        self.category_input.addItems(["food", "drink", "other"])

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price")

        self.tax_input = QLineEdit()
        self.tax_input.setPlaceholderText("Tax %")

        add_button = QPushButton("Add / Update")
        add_button.clicked.connect(self.add_item)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.category_input)
        input_layout.addWidget(self.price_input)
        input_layout.addWidget(self.tax_input)
        input_layout.addWidget(add_button)

        self.layout.addLayout(input_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Category", "Price", "Tax %", "Delete"])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 80)
        self.table.cellClicked.connect(self.handle_table_click)

        self.layout.addWidget(self.table)
        
        billing_btn = QPushButton("Go to Billing")
        billing_btn.clicked.connect(self.open_billing)
        self.layout.addWidget(billing_btn)
        
        revenue_btn = QPushButton("Revenue Dashboard")
        revenue_btn.clicked.connect(self.open_revenue_dashboard)
        self.layout.addWidget(revenue_btn)

    def load_menu_items(self):
        self.table.setRowCount(len(menu_items))
        for row, item in enumerate(menu_items):
            self.table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.table.setItem(row, 1, QTableWidgetItem(item['category']))
            self.table.setItem(row, 2, QTableWidgetItem(str(item['price'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(item['tax_percent'])))

            delete_btn = QPushButton("❌")
            delete_btn.clicked.connect(lambda _, r=row: self.delete_item(r))
            self.table.setCellWidget(row, 4, delete_btn)

    def add_item(self):
        name = self.name_input.text().strip()
        category = self.category_input.currentText()
        try:
            price = float(self.price_input.text())
            tax_percent = float(self.tax_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Enter valid price and tax values.")
            return

        existing = next((item for item in menu_items if item['name'] == name), None)
        if existing:
            # Update
            existing['category'] = category
            existing['price'] = price
            existing['tax_percent'] = tax_percent
            QMessageBox.information(self, "Updated", f"{name} updated!")
        else:
            menu_items.append({
                'name': name,
                'category': category,
                'price': price,
                'tax_percent': tax_percent
            })
            QMessageBox.information(self, "Added", f"{name} added!")

        self.clear_inputs()
        self.load_menu_items()

    def clear_inputs(self):
        self.name_input.clear()
        self.price_input.clear()
        self.tax_input.clear()

    def delete_item(self, index):
        del menu_items[index]
        self.load_menu_items()

    def handle_table_click(self, row, column):
        if column != 4:
            item = menu_items[row]
            self.name_input.setText(item['name'])
            self.price_input.setText(str(item['price']))
            self.tax_input.setText(str(item['tax_percent']))
            self.category_input.setCurrentText(item['category'])
            
    def open_billing(self):
        self.billing_window = BillingWindow()
        self.billing_window.show()
        self.hide()

    def open_revenue_dashboard(self):
        self.revenue_window = RevenueDashboard()
        self.revenue_window.show()
