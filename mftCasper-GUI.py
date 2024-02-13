#!/usr/bin/env python3

try:
    from analyzemft import mftsession
except:
    from .analyzemft import mftsession

import sys
import traceback

from PyQt6.QtWidgets import *
from PyQt6 import uic

# UI 파일 연결
form_class = uic.loadUiType("Qt/form.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 설정 값 (초기 값)
        self.mft_debug = False
        self.mft_csv = False
        self.mft_Latex = False
        self.mft_json = False

        self.mft_file_name = ""
        self.mft_report_name = ""

        # GUI -> 버튼 및 체크박스 연결
        self.pushButton_MFT_location.clicked.connect(self.buttonMft)
        self.pushButton_Report_location.clicked.connect(self.buttonReport)

        self.pushButton_Run.clicked.connect(self.buttonRun)

        self.mft_debug = self.checkBox_DEBUG.stateChanged.connect(self.chkFunction)
        self.mft_csv = self.checkBox_CSV.stateChanged.connect(self.chkFunction)
        self.mft_Latex = self.checkBox_JSON.stateChanged.connect(self.chkFunction)
        self.mft_json = self.checkBox_LaTex.stateChanged.connect(self.chkFunction)

    def chkFunction(self):
        '''
        if self.checkBox_DEBUG.isChecked():
            print("DEBUG Checked")
        if self.checkBox_CSV.isChecked():
            print("CSV Checked")
        if self.checkBox_JSON.isChecked():
            print("JSON Checked")
        if self.checkBox_LaTex.isChecked():
            print("LaTex Checked")
        '''

        if self.checkBox_DEBUG.isChecked():
            self.mft_debug = True
        else:
            self.mft_debug = False

        if self.checkBox_CSV.isChecked():
            self.mft_csv = True
        else:
            self.mft_csv = False

        if self.checkBox_JSON.isChecked():
            self.mft_json = True
        else:
            self.mft_json = False

        if self.checkBox_LaTex.isChecked():
            self.mft_Latex = True
        else:
            self.mft_Latex = False

    def buttonMft(self):
        print("MFT Clicked")
        mft_file, check = QFileDialog.getOpenFileName(self, '파일 선택창', "", "All Files (*)")
        if check:
            self.textBrowser_MFT.setText(mft_file)
            self.mft_file_name = mft_file

        print(self.mft_file_name)

    def buttonReport(self):
        print("Report Clicked")
        report_file = QFileDialog.getExistingDirectory(self, '파일 선택창')
        if report_file:
            self.textBrowser_SAVE.setText(report_file)
            self.mft_report_name = report_file

        print(self.mft_report_name)

    def buttonRun(self):
        print("Run Clicked")

        if self.mft_debug == False and self.mft_csv == False and self.mft_json == False:
            self.textBrowser_MFT.setText("최소 하나의 보고서를 설정해주세요.")
        else:
            if self.mft_file_name == '':
                self.textBrowser_MFT.setText("mft 파일 경로를 지정해주세요.")
            else:
                # analyzemft Part
                # mft_file_name / mft_report_name
                try:
                    session = mftsession.MftSession()

                    # 인자 값 확인
                    session.mft_option_gui(self.mft_file_name, self.mft_debug, self.mft_csv, self.mft_Latex, self.mft_json, self.mft_report_name)

                    # mft 및 인자 값에 따른 분석 결과 파일 Open
                    session.open_files()

                    # mft 파일 분석
                    session.process_mft_file()
                except Exception as ex:
                    self.textBrowser_MFT.setText("치명적인 오류가 발생하였습니다.")
                    print("오류 발생!")
                    err_msg = traceback.format_exc()
                    print(err_msg)
            self.textBrowser_MFT.setText("작업 완료! 보고서 파일을 확인해주세요.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec()
