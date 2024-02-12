#!/usr/bin/env python3

try:
    from analyzemft import mftsession
except:
    from .analyzemft import mftsession

if __name__ == "__main__":

    # analyzemft Part
    session = mftsession.MftSession()

    # 인자 값 확인
    session.mft_options()
    # mft 및 인자 값에 따른 분석 결과 파일 Open
    session.open_files()
    # mft 파일 분석
    session.process_mft_file()
