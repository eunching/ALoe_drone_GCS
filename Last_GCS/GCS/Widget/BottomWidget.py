# -*- coding: utf-8 -*-

from GCS.Util.Util import *
from PyQt5.QtWidgets import QHBoxLayout
from GCS.Widget.BaseWidget import BaseWidget
from GCS.Module.LogModule import LogModule
from GCS.Module.GpsModule import GpsModule
from GCS.Module.HudModule import FlightModule



class BottomWidget(BaseWidget):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self):
        super(BottomWidget, self).__init__(MAP_WIDTH, TEXT_HEIGHT, BACKGROUNG_WIDGET_COLOR)

        # 위젯들(컨트롤,맵,허드 및 로그) > 레이아웃
        self.bottom_layout = QHBoxLayout(self.widget)

        # 위젯(컨트롤, 맵, 로그) 인스턴스 생성
        self.text_log_widget = LogModule()
        self.gps_widget = GpsModule()
        self.hud_widget = FlightModule()

        # UI 설정
        self.init_widget()

    # #########################################################################################
    #  Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):

        # 레이아웃 옵션 설정
        self.bottom_layout.setSpacing(0)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)

        # 위젯 인스턴스 > 레이아웃
        self.bottom_layout.addWidget(self.text_log_widget)
        self.bottom_layout.addWidget(self.gps_widget)
        self.bottom_layout.addWidget(self.hud_widget)



