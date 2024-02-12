#!/usr/bin/env python3

try:
    from analyzemft import mftsession
except:
    from .analyzemft import mftsession

import sys
import traceback

from PyQt6.QtWidgets import *
from PyQt6 import uic

# 옵션값
mft_debug = False
mft_csv = False
mft_json = False
mft_Latex = False

# UI 파일 연결
form_class = uic.loadUiType("Qt/form.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.mft_file_name = ""
        self.mft_report_name = ""

        self.mft_file_name = self.pushButton_MFT_location.clicked.connect(self.buttonMft)
        self.mft_report_name = self.pushButton_Report_location.clicked.connect(self.buttonReport)

        self.pushButton_Run.clicked.connect(self.buttonRun)

        self.checkBox_DEBUG.stateChanged.connect(self.chkFunction)
        self.checkBox_CSV.stateChanged.connect(self.chkFunction)
        self.checkBox_JSON.stateChanged.connect(self.chkFunction)
        self.checkBox_LaTex.stateChanged.connect(self.chkFunction)

    def chkFunction(self):
        if self.checkBox_DEBUG.isChecked():
            print("DEBUG Checked")
        if self.checkBox_CSV.isChecked():
            print("CSV Checked")
        if self.checkBox_JSON.isChecked():
            print("JSON Checked")
        if self.checkBox_LaTex.isChecked():
            print("LaTex Checked")

    def buttonMft(self):
        print("MFT Clicked")
        mft_file, check = QFileDialog.getOpenFileName(self, '파일 선택창', "", "All Files (*)")
        if check:
            self.textBrowser_MFT.setText(mft_file)
        print(mft_file)
        return mft_file

    def buttonReport(self):
        print("Report Clicked")
        report_file = QFileDialog.getExistingDirectory(self, '파일 선택창')
        if report_file:
            self.textBrowser_SAVE.setText(report_file)
            mft_report_name = report_file
        print(report_file)
        return report_file

    def buttonRun(self):
        print("Run Clicked")
        if self.checkBox_DEBUG.isChecked():
            mft_debug = True
        if self.checkBox_CSV.isChecked():
            mft_csv = True
        if self.checkBox_JSON.isChecked():
            mft_json = True
        if self.checkBox_LaTex.isChecked():
            mft_Latex = True

        print("MFT NAME")
        print(self.mft_file_name)
        if self.mft_file_name == '':
            self.textBrowser_MFT.setText("mft 파일 경로를 지정해주세요.")
        else:
            # analyzemft Part
            # mft_file_name / mft_report_name
            try:
                session = mftsession.MftSession()

                # 인자 값 확인
                session.mft_option_gui(self.mft_file_name)
                # mft 및 인자 값에 따른 분석 결과 파일 Open
                session.open_files()
                # mft 파일 분석
                session.process_mft_file()
            except Exception as ex:
                self.textBrowser_MFT.setText("치명적인 오류가 발생하였습니다.")
                print("오류 발생!")
                err_msg = traceback.format_exc()
                print(err_msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec()
