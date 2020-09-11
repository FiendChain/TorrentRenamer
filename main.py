from PyQt5.QtWidgets import QApplication
from src.widgets import AppView
from src.models import App
from src.api import Api
from argparse import ArgumentParser
import os
    
def main():
    parser = ArgumentParser()
    parser.add_argument("--rootdir", default="F:/TV Shows/")
    parser.add_argument("--cred", default="credentials.json")
    args = parser.parse_args()

    qapp = QApplication([])
    qapp.setStyle("Fusion")

    api = Api.load_api(args.cred)
    app = App(api)
    app_view = AppView(app)
    app.set_root_dir(args.rootdir)

    app_view.show()

    qapp.exec_()

if __name__ == '__main__':
    main()