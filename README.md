# MFT-Casper


[analyzeMFT](https://github.com/dkovar/analyzeMFT) 도구를 기반으로 하여 제작된 MFT 도구입니다.

해당 도구의 코드를 기반으로 아래와 같은 기능을 추가하고자 하고 있습니다.

## 진행상황 
- [X] analyzeMFT 도구 분석
- [X] CLI -> GUI 
- [X] json 기능 개선

<br/>

## 추후 작업 내용 
추후 작업이 진행될 내용입니다. 

- [ ] LaTex 보고서 기능 추가
- [ ] $MFT 결과 / 검색 기능 추가
- [ ] $ATTRIBUTE_LIST 개선 / [개선 필요점](https://github.com/dkovar/analyzeMFT/issues/56)

<br/>

## 사용 방법

### 초기 설정
- pip install -r requirements.txt
- python mftCasper-CLI.py 
  - CLI 환경 기준
- python mftCasper-GUI.py
  - GUI 환경 기준 

(+) 추후 .exe 파일 제공 예정. 

### CLI
CLI에서 제공하는 옵션은 아래와 같습니다. (analyzeMFT와 동일합니다.)

-f 옵션은 필수 옵션이며, 나머지 옵션은 필요에 따라 사용하시면 됩니다. 


        "-v", "--version", action="store_true", dest="version",
                          help="report version and exit"  

        "-f", "--file", dest="filename",
                          help="read MFT from FILE", metavar="FILE"  

         "-j", "--json",
                          dest="json",
                          help="File paths should use the windows path separator instead of linux"          

         "-o", "--output", dest="output",
                          help="write results to FILE", metavar="FILE"  

         "-a", "--anomaly",
                          action="store_true", dest="anomaly",
                          help="turn on anomaly detection"  

         "-e", "--excel",
                          action="store_true", dest="excel",
                          help="print date/time in Excel friendly format"  

         "-b", "--bodyfile", dest="bodyfile",
                          help="write MAC information to bodyfile", metavar="FILE"  

         "--bodystd", action="store_true", dest="bodystd",
                          help="Use STD_INFO timestamps for body file rather than FN timestamps"  

         "--bodyfull", action="store_true", dest="bodyfull",
                          help="Use full path name + filename rather than just filename"  

         "-c", "--csvtimefile", dest="csvtimefile",
                          help="write CSV format timeline file", metavar="FILE"  

         "-l", "--localtz",
                          action="store_true", dest="localtz",
                          help="report times using local timezone"  

         "-d", "--debug",
                          action="store_true", dest="debug",
                          help="turn on debugging output"  

         "-s", "--saveinmemory",
                          action="store_true", dest="inmemory",
                          help="Save a copy of the decoded MFT in memory. Do not use for very large MFTs"  

         "-p", "--progress",
                          action="store_true", dest="progress",
                          help="Show systematic progress reports."  

         "-w", "--windows-path",
                          action="store_true", dest="winpath",
                          help="File paths should use the windows path separator instead of linux"  


### GUI 
현재 CSV, JSON, LaTex, Debug 옵션을 제공하고 있습니다. (LaTex 미완성.)

- CSV - 보고서 : CSV 파일 형태로 보고서 제작 
- JSON - 보고서 : JSON 파일 형태로 보고서 제작 
- LaTex - 보고서 : 미완성 (LaTex 파일 형태로 보고서 제작)
- Debug : analyzeMFT 및 MFT-Casper 로그 / .txt 파일로 저장

사용시, MFT 파일 경로를 지정한 뒤, 보고서 옵션 1개 이상 선택 이후 구동하시면 됩니다.


(보고서 파일 경로 미 지정시, 프로그램 디렉토리 내 생성됩니다.)

<br/>

## 시연 영상 

### GUI
Python 3.11.5 / MacOS Sonoma 

![MFT-Casper-GUI-img.gif](Doc%2FMFT-Casper-GUI-img.gif)


## 관련 보고서

해당 도구를 제작하는 과정에서 작성된 보고서의 경우, 하단의 저장소에서 확인할 수 있습니다. 

https://github.com/Casper-Wants-To-Run/FileSystem-Report
