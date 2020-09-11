from PyQt5.QtWidgets import QApplication
from src.widgets import AppView
from src.models import App
from argparse import ArgumentParser
import os

    
def main():
    qapp = QApplication([])
    qapp.setStyle("Fusion")

    app = App()
    app_view = AppView()
    app_view.set_app(app)

    app.set_root_dir("F:/TV Shows/")

    app_view.show()

    qapp.exec_()

if __name__ == '__main__':
    main()