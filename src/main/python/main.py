from fbs_runtime.application_context.PyQt5 import ApplicationContext
from widgets import AppView
from models import App
from api import Api
from argparse import ArgumentParser
import os
import logging
import sys
    
def main():
    parser = ArgumentParser()
    parser.add_argument("--rootdir", default="F:/TV Shows/")
    parser.add_argument("--cred", default="credentials.json")
    args = parser.parse_args()

    logging.basicConfig(filename='history.log',level=logging.INFO)

    qctx = ApplicationContext()       # 1. Instantiate ApplicationContext
    qctx.app.setStyle("Fusion")

    api = Api.load_api(args.cred)
    app = App(api)
    app_view = AppView(app)
    app.set_root_dir(args.rootdir)

    app_view.setWindowTitle("Torrent Renamer")
    app_view.show()

    return qctx.app.exec_()

if __name__ == '__main__':
    sys.exit(main())