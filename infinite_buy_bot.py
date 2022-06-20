import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from PyQt5 import uic
import threading
from inf_mod import *


form_starting = uic.loadUiType("starting_screen.ui")[0]
form_running = uic.loadUiType("running_screen.ui")[0]


class WindowClass(QMainWindow):
    def __init__(self):
        super( ).__init__( )
        self.initUI()
        self.initStackedWidget()

    def initUI(self):
        self.setWindowTitle('BTC ETH Infinite buy bot')     # window title
        self.setWindowIcon(QIcon('window_icon.png'))        # window icon
        self.setGeometry(300, 200, 700, 400)    #window start position & size

    def initStackedWidget(self):
        #StackedWidget 만들기
        # QStackedWidget 생성
        self.stack = QStackedWidget(self)                   # QStackedWidget 생성
        self.stack.setGeometry(0,0,700,400)                 # 위치 및 크기 지정
        # self.stack.setFrameShape(QFrame.Box)                # 테두리 설정(보기 쉽게)

        # 입력할 page를 QWidget으로 생성
        page_1 = StartingWindow()                         # page_1 생성
        page_2 = RunningWindow()                         # page_2 생성

        # 내용입력이 완료된 페이지를 QStackedWidget객체에 추가
        self.stack.addWidget(page_1)                   # stack에 page_1 추가
        self.stack.addWidget(page_2)                   # stack에 page_2 추가

        page_1.startButton.clicked.connect(self.startBot)
        page_2.stopButton.clicked.connect(self.stopBot)

    def startBot(self):
        self.stack.setCurrentIndex(1)
        t = threading.Thread(target=run, args=())
        t.daemon = True
        t.start()

    def stopBot(self):
        self.close()

class StartingWindow(QMainWindow, form_starting):

    def __init__(self):
        super().__init__()
        self.binding()

    def binding(self):
        self.setupUi(self)


class RunningWindow(QMainWindow, form_running):

    def __init__(self):
        super().__init__()
        self.binding()

    def binding(self):
        self.setupUi(self)


if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()