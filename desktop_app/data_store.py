# data_store.py
import json
import os

MENU_FILE = os.path.join(os.getcwd(), "menu.json")

def load_menu():
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, 'r') as f:
            return json.load(f)
    return []

def save_menu(menu_items):
    with open(MENU_FILE, 'w') as f:
        json.dump(menu_items, f, indent=4)

menu_items = load_menu()
