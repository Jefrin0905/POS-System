# admin_panel.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox
)
from data_store import menu_items, save_menu


ADMIN_PASSWORD = "admin123"  # change this as you want


class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()

        if not self.check_password():
            self.close()
            return

        self.setWindowTitle("Admin Panel")
        self.setGeometry(100, 100, 600, 500)

        self.layout = QVBoxLayout()

        # Sorting
        sort_layout = QHBoxLayout()
        sort_label = QLabel("Sort by:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Name (A-Z)", "Price (Low to High)", "Price (High to Low)"])
        self.sort_combo.currentIndexChanged.connect(self.sort_menu)
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_combo)
        self.layout.addLayout(sort_layout)

        # Table to show menu items
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Price", "Tax %"])
        self.table.itemChanged.connect(self.edit_item)
        self.layout.addWidget(self.table)
        self.load_menu_table()

        # Input fields
        input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Item Name")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price")
        self.tax_input = QLineEdit()
        self.tax_input.setPlaceholderText("Tax %")

        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.price_input)
        input_layout.addWidget(self.tax_input)

        self.layout.addLayout(input_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Item")
        add_btn.clicked.connect(self.add_item)

        del_btn = QPushButton("Delete Selected")
        del_btn.clicked.connect(self.delete_selected)

        save_btn = QPushButton("Save Menu")
        save_btn.clicked.connect(self.save_menu)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        btn_layout.addWidget(save_btn)

        self.layout.addLayout(btn_layout)

        self.setLayout(self.layout)

    def check_password(self):
        from PyQt5.QtWidgets import QInputDialog

        pwd, ok = QInputDialog.getText(self, "Admin Login", "Enter Admin Password:", echo=QLineEdit.Password)
        if ok and pwd == ADMIN_PASSWORD:
            return True
        QMessageBox.critical(self, "Access Denied", "Incorrect password.")
        return False

    def load_menu_table(self):
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        for item in menu_items:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.table.setItem(row, 1, QTableWidgetItem(str(item['price'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(item['tax_percent'])))
        self.table.blockSignals(False)

    def sort_menu(self):
        option = self.sort_combo.currentText()
        if option == "Name (A-Z)":
            menu_items.sort(key=lambda x: x['name'].lower())
        elif option == "Price (Low to High)":
            menu_items.sort(key=lambda x: x['price'])
        elif option == "Price (High to Low)":
            menu_items.sort(key=lambda x: x['price'], reverse=True)
        self.load_menu_table()

    def add_item(self):
        name = self.name_input.text().strip()
        try:
            price = float(self.price_input.text())
            tax = float(self.tax_input.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid input", "Price and Tax must be numbers.")
            return

        if not name:
            QMessageBox.warning(self, "Missing name", "Item name cannot be empty.")
            return

        menu_items.append({
            "name": name,
            "price": price,
            "tax_percent": tax
        })

        self.name_input.clear()
        self.price_input.clear()
        self.tax_input.clear()
        self.sort_menu()

    def delete_selected(self):
        selected = self.table.currentRow()
        if selected >= 0:
            del menu_items[selected]
            self.load_menu_table()
        else:
            QMessageBox.warning(self, "No selection", "Please select a row to delete.")

    def save_menu(self):
        save_menu(menu_items)
        QMessageBox.information(self, "Saved", "Menu saved successfully.")

    def edit_item(self, item):
        row = item.row()
        col = item.column()
        value = item.text()

        try:
            if col == 0:
                menu_items[row]['name'] = value
            elif col == 1:
                menu_items[row]['price'] = float(value)
            elif col == 2:
                menu_items[row]['tax_percent'] = float(value)
        except ValueError:
            QMessageBox.warning(self, "Error", "Price and Tax must be numbers.")
            self.load_menu_table()
