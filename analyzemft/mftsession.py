#!/usr/bin/env python3

# Author: David Kovar [dkovar <at> gmail [dot] com]
# Name: mftsession.py
#
# Copyright (c) 2010 David Kovar. All rights reserved.
# This software is distributed under the Common Public License 1.0
#
# Date: May 2013
#

# analyzemft 버전값
VERSION = "v3.0.1"


import csv
import json
import os
import sys
import time

from optparse import OptionParser
from analyzemft import mft
from pylatex import Document, Section, Subsection, Command, NoEscape


SIAttributeSizeXP = 72
SIAttributeSizeNT = 48

class Options:
    # self.options Value
    def __init__(self):
        self.inmemory = False
        self.debug = False
        self.UseLocalTimezone = False
        self.UseGUI = False
        self.version = None
        self.filename = None
        self.json = None
        self.output = None
        self.anomaly = None
        self.excel = None
        self.bodyfile = None
        self.bodystd = None
        self.bodyfull = None
        self.csvtimefile = None
        self.localtz = None
        self.progress = None
        self.winpath = None
        self.Latex = None

class MftSession:
    """Class to describe an entire MFT processing session"""

    @staticmethod
    def fmt_excel(date_str):
        return '="{}"'.format(date_str)

    @staticmethod
    def fmt_norm(date_str):
        return date_str


    def __init__(self):
        self.mft = {}
        self.fullmft = {}
        self.folders = {}
        self.debug = False
        self.mftsize = 0

    # fot GUI
    def mft_option_gui(self, mft_filename, mft_debug, mft_csv, mft_Latex, mft_json, mft_report_name):
        print("mft_option_gui Run..")

        self.options = Options()

        if(mft_filename != ''):
            self.options.filename = mft_filename
        else:
            print("Unable to open file: %s" % self.options.filename)
            sys.exit()

        # 파일 이름 -> date 값 기준 / 동작 시간
        # filename
        report_name = time.strftime("%Y%m%d-%H%M%S")

        # report dir
        if (mft_report_name != ''):
            report_dir = mft_report_name
        else:
            report_dir = ''

        # DEBUG
        if(mft_debug == True):
            self.options.debug = True

        # csv
        if(mft_csv == True):
            self.options.output = report_name + ".csv"
            self.options.output = os.path.join(report_dir, self.options.output)
        # json
        if(mft_json == True):
            self.options.json = report_name + ".json"
            self.options.json = os.path.join(report_dir, self.options.json)

        # Latex  / 연결 Only
        if (mft_Latex == True):
            self.options.Latex = report_name
            self.options.Latex = os.path.join(report_dir, self.options.Latex)

        # DEBUG
        #print(mft_csv, mft_json, mft_Latex)
        #print(self.options.output)
        #print(self.options.json)
        #print(self.options.Latex)

        # (options, args) = parser.parse_args()
        self.path_sep = '\\' if self.options.winpath else '/'

        # ~~
        if self.options.excel:
            self.options.date_formatter = MftSession.fmt_excel
        else:
            self.options.date_formatter = MftSession.fmt_norm


    # 도구 옵션 값 정의
    def mft_options(self):
        parser = OptionParser()
        parser.set_defaults(inmemory=False, debug=False, UseLocalTimezone=False, UseGUI=False)

        parser.add_option("-v", "--version", action="store_true", dest="version",
                          help="report version and exit")

        parser.add_option("-f", "--file", dest="filename",
                          help="read MFT from FILE", metavar="FILE")

        # json
        parser.add_option("-j", "--json",
                          dest="json",
                          help="File paths should use the windows path separator instead of linux")        

        # CSV
        parser.add_option("-o", "--output", dest="output",
                          help="write results to FILE", metavar="FILE")

        parser.add_option("-a", "--anomaly",
                          action="store_true", dest="anomaly",
                          help="turn on anomaly detection")

        parser.add_option("-e", "--excel",
                          action="store_true", dest="excel",
                          help="print date/time in Excel friendly format")

        parser.add_option("-b", "--bodyfile", dest="bodyfile",
                          help="write MAC information to bodyfile", metavar="FILE")

        parser.add_option("--bodystd", action="store_true", dest="bodystd",
                          help="Use STD_INFO timestamps for body file rather than FN timestamps")

        parser.add_option("--bodyfull", action="store_true", dest="bodyfull",
                          help="Use full path name + filename rather than just filename")

        # csvtimefile
        parser.add_option("-c", "--csvtimefile", dest="csvtimefile",
                          help="write CSV format timeline file", metavar="FILE")

        parser.add_option("-l", "--localtz",
                          action="store_true", dest="localtz",
                          help="report times using local timezone")

        parser.add_option("-d", "--debug",
                          action="store_true", dest="debug",
                          help="turn on debugging output")

        parser.add_option("-s", "--saveinmemory",
                          action="store_true", dest="inmemory",
                          help="Save a copy of the decoded MFT in memory. Do not use for very large MFTs")

        parser.add_option("-p", "--progress",
                          action="store_true", dest="progress",
                          help="Show systematic progress reports.")

        parser.add_option("-w", "--windows-path",
                          action="store_true", dest="winpath",
                          help="File paths should use the windows path separator instead of linux")

        ### Latex 추가 예정
        #parser.add_option("-w", "--windows-path",
        #                  action="store_true", dest="winpath",
        #                  help="File paths should use the windows path separator instead of linux")

        (self.options, args) = parser.parse_args()

        # DEBUG
        # print(self.options)

        # ~~
        self.path_sep = '\\' if self.options.winpath else '/'

        # ~~
        if self.options.excel:
            self.options.date_formatter = MftSession.fmt_excel
        else:
            self.options.date_formatter = MftSession.fmt_norm


# mft 파일 및 분석 결과 파일 Open
    def open_files(self):

        if self.options.version:
            print(("Version is: %s" % VERSION))
            sys.exit()

        if self.options.filename is None:
            print("-f <filename> required.")
            sys.exit()

        # if self.options.output == None and self.options.bodyfile == None and self.options.csvtimefile == None:
        #     print "-o <filename> or -b <filename> or -c <filename> required."
        #     sys.exit()

        try:
            self.file_mft = open(self.options.filename, 'rb')
        except:
            print("Unable to open file: %s" % self.options.filename)
            sys.exit()

        if self.options.output is not None:
            try:
                self.file_csv = csv.writer(open(self.options.output, 'w'), dialect=csv.excel, quoting=1)
            except (IOError, TypeError):
                print("Unable to open file: %s" % self.options.output)
                sys.exit()
        
        if self.options.bodyfile is not None:
            try:
                self.file_body = open(self.options.bodyfile, 'w')
            except:
                print("Unable to open file: %s" % self.options.bodyfile)
                sys.exit()

        if self.options.csvtimefile is not None:
            try:
                self.file_csv_time = open(self.options.csvtimefile, 'w')
            except (IOError, TypeError):
                print("Unable to open file: %s" % self.options.csvtimefile)
                sys.exit()

    # Provides a very rudimentary check to see if it's possible to store the entire MFT in memory
    # Not foolproof by any means, but could stop you from wasting time on a doomed to failure run.

    # sizecheck 및 메모리 부족으로 발생할 수 있는 문제 방지

    def sizecheck(self):

        # The number of records in the MFT is the size of the MFT / 1024
        self.mftsize = int(os.path.getsize(self.options.filename)) / 1024

        if self.options.debug:
            print('There are %d records in the MFT' % self.mftsize)

        if not self.options.inmemory:
            return

        # The size of the full MFT is approximately the number of records * the avg record size
        # Avg record size was determined empirically using some test data
        sizeinbytes = self.mftsize * 4500

        if self.options.debug:
            print('Need %d bytes of memory to save into memory' % sizeinbytes)

        try:
            arr = []
            for i in range(0, sizeinbytes / 10):
                arr.append(1)

        except MemoryError:
            print('Error: Not enough memory to store MFT in memory. Try running again without -s option')
            sys.exit()

    # mft file - Process / 핵심
    def process_mft_file(self):

        # sizecheck / Memory Error 방지
        self.sizecheck()

        # file 경로 값 확인? (체크)
        self.build_filepaths()

        #
        # reset the file reading
        self.num_records = 0
        self.file_mft.seek(0)
        raw_record = self.file_mft.read(1024)

        if self.options.output is not None:
            self.file_csv.writerow(mft.mft_to_csv(None, True, self.options))

        while raw_record != b"":
            record = mft.parse_record(raw_record, self.options)
            if self.options.debug:
                print(record)

            record['filename'] = self.mft[self.num_records]['filename']

            self.do_output(record)

            self.num_records += 1

            if record['ads'] > 0:
                for i in range(0, record['ads']):
                    #                         print "ADS: %s" % (record['data_name', i])
                    record_ads = record.copy()
                    record_ads['filename'] = record['filename'] + ':' + record['data_name', i].decode()
                    self.do_output(record_ads)

            raw_record = self.file_mft.read(1024)

    # output -> 분석 결과 작성
    def do_output(self, record):

        if self.options.inmemory:
            self.fullmft[self.num_records] = record

        if self.options.output is not None:
            self.file_csv.writerow(mft.mft_to_csv(record, False, self.options))
        
        if self.options.json is not None:    
            with open(self.options.json, 'a') as outfile:
                json.dump(mft.mft_to_json(record), outfile)
                outfile.write('\n')
            
        if self.options.csvtimefile is not None:
            self.file_csv_time.write(mft.mft_to_l2t(record))

        if self.options.bodyfile is not None:
            self.file_body.write(mft.mft_to_body(record, self.options.bodyfull, self.options.bodystd))

        if self.options.progress:
            if self.num_records % (self.mftsize / 5) == 0 and self.num_records > 0:
                print('Building MFT: {0:.0f}'.format(100.0 * self.num_records / self.mftsize) + '%')

        # Latex / 구현 중...
        if self.options.Latex is not None:
            # LaTeX 문서 생성
            doc = Document()

            # 제목 추가
            doc.preamble.append(Command('title', 'My Document'))
            doc.preamble.append(Command('author', 'John Doe'))
            doc.preamble.append(Command('date', ''))
            doc.append(NoEscape(r'\maketitle'))

            # 섹션 및 하위 섹션 추가
            with doc.create(Section('Section 1')):
                doc.append('Content of section 1')
                with doc.create(Subsection('Subsection 1')):
                    doc.append('Content of subsection 1')
                with doc.create(Subsection('Subsection 2')):
                    doc.append('Content of subsection 2')

            # LaTex 문서 저장
            doc.generate_tex(self.options.Latex)

    # plaso 연계 / 미완성 (추측)
    def plaso_process_mft_file(self):

        # TODO - Add ADS support ....

        self.build_filepaths()

        # reset the file reading
        self.num_records = 0
        self.file_mft.seek(0)
        raw_record = self.file_mft.read(1024)

        while raw_record != b"":
            record = mft.parse_record(raw_record, self.options)
            if self.options.debug:
                print(record)

            record['filename'] = self.mft[self.num_records]['filename']

            self.fullmft[self.num_records] = record

            self.num_records += 1

            raw_record = self.file_mft.read(1024)

    ##################################
    # MFT 파일 내에서 파일 경로 추출시 활용
    def build_filepaths(self):
        # reset the file reading
        self.file_mft.seek(0)

        self.num_records = 0

        # 1024 is valid for current version of Windows but should really get this value from somewhere

        # 1024 바이트 읽은 후 raw_recrods 초기화
        raw_record = self.file_mft.read(1024)
        while raw_record != b"": # raw_record 빈 문자열이 아닌 경우 계속 루프
            minirec = {}

            # mft 레코드 값 파싱
            record = mft.parse_record(raw_record, self.options)
            if self.options.debug:
                print(record)

            # 앞 parse_record에서 파싱한 값에서 file 관련(file name, fncnt)만 minirec 저장
            minirec['filename'] = record['filename']
            minirec['fncnt'] = record['fncnt']

            # fncnt 1인 경우, par_ref 및 이름 추출하여 저장
            if record['fncnt'] == 1:
                minirec['par_ref'] = record['fn', 0]['par_ref']
                minirec['name'] = record['fn', 0]['name']
            # fncnt 2 이상인 경우,
            if record['fncnt'] > 1:
                minirec['par_ref'] = record['fn', 0]['par_ref']
                for i in (0, record['fncnt'] - 1):
                    # print record['fn',i]
                    # 유니코드 nspace -> 0x1, 0x3인 경우만 파일 이름 추출 -> 저장
                    if record['fn', i]['nspace'] == 0x1 or record['fn', i]['nspace'] == 0x3:
                        minirec['name'] = record['fn', i]['name']
                # name 값이 없는 경우, 마지막 파일 이름(name) 추출, 저장
                if minirec.get('name') is None:
                    minirec['name'] = record['fn', record['fncnt'] - 1]['name']

            self.mft[self.num_records] = minirec

            if self.options.progress:
                if self.num_records % (self.mftsize / 5) == 0 and self.num_records > 0:
                    print('Building Filepaths: {0:.0f}'.format(100.0 * self.num_records / self.mftsize) + '%')

            self.num_records += 1

            raw_record = self.file_mft.read(1024)

        self.gen_filepaths()

    # fncnt 값이 0보다 큰 경우, 전체 경로 확보를 위한 함수
    def get_folder_path(self, seqnum):
        if self.debug:
            print("Building Folder For Record Number (%d)" % seqnum)

        # 주어진 순번에 해당하는 레코드 -> mft 내에 없다면, Orphan 반환
        if seqnum not in self.mft:
            return 'Orphan'

        # If we've already figured out the path name, just return it
        # 이미 폴더 경로가 확인된 경우, 해당 경로 반환
        if (self.mft[seqnum]['filename']) != '':
            return self.mft[seqnum]['filename']

        try:
            # if (self.mft[seqnum]['fn',0]['par_ref'] == 0) or
            # (self.mft[seqnum]['fn',0]['par_ref'] == 5):  # There should be no seq
            # number 0, not sure why I had that check in place.
            # 루트 디렉토리인 경우 (5) / 루트 디렉토리에 해댕되는 경로, 파일 이름 결합 -> 반환
            if self.mft[seqnum]['par_ref'] == 5:  # Seq number 5 is "/", root of the directory
                self.mft[seqnum]['filename'] = self.path_sep + self.mft[seqnum]['name'].decode()
                return self.mft[seqnum]['filename']
        except:  # If there was an error getting the parent's sequence number, then there is no FN record
            self.mft[seqnum]['filename'] = 'NoFNRecord'
            return self.mft[seqnum]['filename']

        # Self referential parent sequence number. The filename becomes a NoFNRecord note
        if (self.mft[seqnum]['par_ref']) == seqnum:
            if self.debug:
                print("Error, self-referential, while trying to determine path for seqnum %s" % seqnum)
            self.mft[seqnum]['filename'] = 'ORPHAN' + self.path_sep + self.mft[seqnum]['name'].decode()
            return self.mft[seqnum]['filename']

        # We're not at the top of the tree and we've not hit an error
        # 위 조건 미 만족시, 부모 레코드 시퀸스 번호 활용 / 부모 폴더의 경로 확보
        parentpath = self.get_folder_path((self.mft[seqnum]['par_ref']))
        self.mft[seqnum]['filename'] = parentpath + self.path_sep + self.mft[seqnum]['name'].decode()

        return self.mft[seqnum]['filename']

    def gen_filepaths(self):

        # mft 레코드 반복
        for i in self.mft:

            #            if filename starts with / or ORPHAN, we're done.
            #            else get filename of parent, add it to ours, and we're done.

            # If we've not already calculated the full path ....

            # filename 레코드가 비어있는 경우 작업 진행
            if (self.mft[i]['filename']) == '':
                # fncnt 값이 0보다 큰 경우, get_folder_path -> 전체 경로 생성
                if self.mft[i]['fncnt'] > 0:
                    self.get_folder_path(i)
                    # self.mft[i]['filename'] = self.mft[i]['filename'] + '/' +
                    #   self.mft[i]['fn',self.mft[i]['fncnt']-1]['name']
                    # self.mft[i]['filename'] = self.mft[i]['filename'].replace('//','/')
                    if self.debug:
                        print("Filename (with path): %s" % self.mft[i]['filename'])
                else:
                    self.mft[i]['filename'] = 'NoFNRecord'
