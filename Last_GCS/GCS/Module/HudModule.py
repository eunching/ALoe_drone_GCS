# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from GCS.Util.Util import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtCore import pyqtSlot, Qt
from GCS.Common.CustomLabel import *
from PyQt5.QtWebEngineWidgets import *
from GCS.Widget.BaseWidget import BaseWidget


class FlightModule(BaseWidget):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self):

        super(FlightModule, self).__init__(TEXT_WIDTH, TEXT_HEIGHT, BACKGROUNG_WIDGET_COLOR)

        # 허드 레이아웃
        self.flight_layout = QVBoxLayout(self.widget)

        # 라벨(타이틀) 생성
        self.title = CustomLabel(self.widget, width=TEXT_WIDTH, name="  ▶  HUD", color="G")
        self.setStyleSheet(FONT_STYLE)

        # 웹 엔진
        self.hud_view = QWebEngineView(self)

        # 웹채널
        self.web_channel = QWebChannel(self.hud_view.page())

        # UI 설정
        self.init_widget()

        # 시리얼 접속 후 비행 상태 변경 정보(roll,pitch,heading) 스롯 연결
        self.serial_manager.send_hud_data.connect(self.get_hud_data)

        # UI 초기화
        self.serial_manager.send_ui_init.connect(self.get_ui_init)

    # #########################################################################################
    #  Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):

        # 로컬 경로 패스
        hud_path = HUD_HTML_PATH + "hud.Html"

        # 레이아웃 옵션
        self.flight_layout.setSpacing(35)
        #self.flight_layout.setAlignment(Qt.AlignCenter)
        self.flight_layout.setContentsMargins(0, 0, 0, 0)

        # HUD 웹 페이지 설정 및 호출
        self.hud_view.page().setWebChannel(self.web_channel)
        self.hud_view.load(QtCore.QUrl.fromLocalFile(hud_path))

        # 웹페이지(허드) > 레이아웃(self)
        self.flight_layout.addWidget(self.title)
        self.flight_layout.addWidget(self.hud_view)

    # #########################################################################################
    #  시리얼 Read(HeartBeat) 데이터 전송
    # #########################################################################################
    @pyqtSlot(dict)
    def get_hud_data(self, hud_data):

        roll = str(hud_data.pop('roll'))
        pitch = str(hud_data.pop('pitch'))
        heading = str(hud_data.pop('heading'))

        if roll != '' and pitch != '':
            self.hud_view.page().runJavaScript("changeAlt(" + str(roll) + "," + str(pitch) + ")")

        if heading != '':
            self.hud_view.page().runJavaScript("changeHead(" + str(heading) + ")")

    # #########################################################################################
    #  시리얼 접속 해제로 인한 UI 초기화
    # #########################################################################################
    @pyqtSlot(str)
    def get_ui_init(self, connect):

        if connect == "on":
            self.hud_view.page().runJavaScript("changeHead(" + str(90) + ")")
            self.hud_view.page().runJavaScript("changeAlt(" + str(60) + ","+str(80)+")")
            pass

        else:
            self.hud_view.page().runJavaScript("changeHead(" + str(0) + ")")
            self.hud_view.page().runJavaScript("changeAlt(" + str(0) + "," + str(0) + ")")
