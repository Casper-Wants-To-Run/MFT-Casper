#!/usr/bin/env python3

try:
    from analyzemft import mftsession
except:
    from .analyzemft import mftsession

import sys
from PyQt6.QtWidgets import *
from PyQt6 import uic

# UI 파일 연결
form_class = uic.loadUiType("Qt/form.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # layout = QVBoxLayout()

        self.pushButton_MFT_location.clicked.connect(self.buttonMFTFunction)
        self.pushButton_Report_location.clicked.connect(self.buttonMFTFunction)

    def buttonMFTFunction(self):
        print("MFT Clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec()
