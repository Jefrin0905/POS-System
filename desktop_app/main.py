import sys
from PyQt5.QtWidgets import QApplication
from admin_panel import AdminPanel  # this is your AdminPanel code

def main():
    app = QApplication(sys.argv)     # create the app
    panel = AdminPanel()             # create AdminPanel window
    panel.show()                    # show the window
    sys.exit(app.exec_())            # start the app

if __name__ == "__main__":
    main()
