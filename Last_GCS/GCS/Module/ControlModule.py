# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from GCS.Common.CustomImgButton import CustomImgButton
from GCS.Widget.BaseWidget import BaseWidget
from PyQt5.QtCore import pyqtSlot, QPropertyAnimation, QSize
from GCS.Common.CustomLabel import *
from GCS.Util.Util import *


class ControlModule(BaseWidget):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self):

        super(ControlModule, self).__init__(CONTROL_WIDTH, CONTROL_HEIGHT, BACKGROUNG_WIDGET_COLOR)

        # 상태 레이아웃(라벨,버튼 위젯)get_log_data
        self.control_layout = QVBoxLayout(self.widget)

        # 라벨(타이틀) 생성
        self.title = CustomLabel(self.widget, width=CONTROL_WIDTH, name="  ▶  CONTROLLER", color="B")
        self.setStyleSheet('font-size : 10pt; font-family : HY그래픽M;')

        # 컨트롤 위젯
        self.control_btn_widget = QWidget(self)

        # 컨트롤 레이아웃
        self.control_btn_layout = QGridLayout(self.control_btn_widget)

        # 버튼 이미지 설정
        take_off = IMG_PATH + "drone_btn_1.png"
        landing = IMG_PATH + "drone_btn_5.png"
        flight_start = IMG_PATH + "drone_btn_7.png"
        rtl = IMG_PATH + "drone_btn_6.png"
        arming = IMG_PATH + "drone_btn_2.png"
        dis_arming = IMG_PATH + "drone_btn_3.png"
        spray = IMG_PATH + "drone_btn_9.png"
        #buzzer = IMG_PATH + "drone_btn_10.png"

        # 컨트롤 버튼 생성
        self.btn_take_off = CustomImgButton(self.control_btn_widget, 171, 41, "Take Off", take_off)
        self.btn_landing = CustomImgButton(self.control_btn_widget, 171, 41, "   Landing     ", landing)
        self.btn_flight_start = CustomImgButton(self.control_btn_widget, 171, 41, " Flight Start ", flight_start)
        self.btn_rtl = CustomImgButton(self.control_btn_widget, 171, 41, "Return Home", rtl)
        self.btn_arming = CustomImgButton(self.control_btn_widget, 171, 41, "Arming", arming)
        self.btn_dis_arming = CustomImgButton(self.control_btn_widget, 171, 41, "  DisArming  ", dis_arming)
        self.btn_spray = CustomImgButton(self.control_btn_widget, 171, 41, "  Spray  ", spray)
        #self.btn_buzzer = CustomImgButton(self.control_btn_widget, 171, 41, "  Buzzer  ", buzzer)

        self.init_widget()

        # UI 초기화
        self.serial_manager.send_ui_init.connect(self.get_ui_init)

    # #########################################################################################
    #  Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):

        # 버튼 위젯 > 레이아웃 배치
        self.control_btn_layout.addWidget(self.btn_take_off, 0, 0)
        self.control_btn_layout.addWidget(self.btn_landing, 0, 1)
        self.control_btn_layout.addWidget(self.btn_flight_start, 1, 0)
        self.control_btn_layout.addWidget(self.btn_rtl, 1, 1)
        self.control_btn_layout.addWidget(self.btn_arming, 2, 0)
        self.control_btn_layout.addWidget(self.btn_dis_arming, 2, 1)
        self.control_btn_layout.addWidget(self.btn_spray, 3, 0)
        #self.control_btn_layout.addWidget(self.btn_buzzer, 3, 1)

        # 버튼 스롯 연결
        self.btn_clicked_bind()

        # 위젯(타이틀, 컨트롤 버튼) > 레이아웃
        self.control_layout.addWidget(self.title)
        self.control_layout.addWidget(self.control_btn_widget)
        self.control_layout.setContentsMargins(0, 0, 0, 0)

        # 접속 전 모든 버튼 비활성화 처리
        self.btn_clicked_display("off")

    # #########################################################################################
    #  버튼 클릭 이벤트 바인딩
    # #########################################################################################
    def btn_clicked_bind(self):

        self.btn_take_off.clicked.connect(lambda: self.btn_clicked('take_off'))
        self.btn_landing.clicked.connect(lambda: self.btn_clicked('landing'))
        self.btn_flight_start.clicked.connect(lambda: self.btn_clicked('flight_start'))
        self.btn_rtl.clicked.connect(lambda: self.btn_clicked('rtl'))
        self.btn_arming.clicked.connect(lambda: self.btn_clicked('arming'))
        self.btn_dis_arming.clicked.connect(lambda: self.btn_clicked('dis_arming'))
        self.btn_spray.clicked.connect(lambda: self.btn_clicked('spray'))
        #self.btn_buzzer.clicked.connect(lambda: self.btn_clicked('buzzer'))

    # #########################################################################################
    #  버튼 클릭 후 스롯 처리
    # #########################################################################################
    @pyqtSlot(str)
    def btn_clicked(self, value):

        click_data = (
            "control", value
        )
        self.serial_manager.btn_clicked(click_data)

    def resizeDialog(self):
        self.animation = QPropertyAnimation(self, "size")
        # self.animation.setDuration(1000) #Default 250ms
        if self.size().width() == 200:
            self.animation.setEndValue(QSize(600, 300))
        else:
            self.animation.setEndValue(QSize(200, 100))
        self.animation.start()

    # #########################################################################################
    #  버튼 별 enable/disable 처리
    # #########################################################################################
    def btn_clicked_display(self, value):

        # 모든 버튼 초기 활성화 설정
        btn_take_off = True
        btn_landing = True
        btn_flight_start = True
        btn_rtl = True
        btn_arming = True
        btn_dis_arming = True
        btn_spray = True
        btn_buzzer = True

        if value == "on":
            pass

        elif value == "off":
            btn_take_off = False
            btn_landing = False
            btn_flight_start = False
            btn_rtl = False
            btn_arming = False
            btn_dis_arming = False
            btn_spray = False
            btn_buzzer = False

        elif value == "take_off":
            pass
        elif value == "landing":
            pass
        elif value == "flight_start":

            btn_take_off = False
            btn_landing = True
            btn_flight_start = True
            btn_rtl = True
            btn_arming = False
            btn_dis_arming = False
            btn_spray = False
            btn_buzzer = False

        elif value == "rtl":
            pass
        elif value == "arming":
            pass
        elif value == "dis_arming":
            pass
        elif value == "spray":
            pass
        elif value == "buzzer":
            pass

        self.btn_take_off.setEnabled(btn_take_off)
        self.btn_landing.setEnabled(btn_landing)
        self.btn_flight_start.setEnabled(btn_flight_start)
        self.btn_rtl.setEnabled(btn_rtl)
        self.btn_arming.setEnabled(btn_arming)
        self.btn_dis_arming.setEnabled(btn_dis_arming)
        self.btn_spray.setEnabled(btn_spray)
        #self.btn_buzzer.setEnabled(btn_buzzer)

    # #########################################################################################
    #  시리얼 접속 해제로 인한 UI 초기화
    # #########################################################################################
    @pyqtSlot(str)
    def get_ui_init(self, connect):

        self.btn_clicked_display(connect)

