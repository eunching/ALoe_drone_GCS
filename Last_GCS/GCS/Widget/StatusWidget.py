# -*- coding: utf-8 -*-

from GCS.Util.Util import *
from PyQt5.QtWidgets import QVBoxLayout
from GCS.Module.GpsModule import GpsModule
from GCS.Widget.BaseWidget import BaseWidget
from GCS.Module.HudModule import FlightModule
from GCS.Module.StatusModule import StatusModule
from GCS.Module.LogModule import LogModule

class StatusWidget(BaseWidget):

    def __init__(self):
        super(StatusWidget, self).__init__(STATUS_WIDTH, CONTENTS_HEIGHT, BACKGROUNG_WIDGET_COLOR)

        # 위젯들(허드 , 상태로그 ) > 레이아웃
        self.status_layout = QVBoxLayout(self.widget)

        # HUD, Status
        self.hud = FlightModule()
        self.log = LogModule()

        # UI 설정
        self.init_widget();

    def init_widget(self):

        # 레이아웃 옵션 설정
        self.status_layout.setSpacing(0)
        self.status_layout.setContentsMargins(0, 0, 0, 0)

        # 위젯 인스턴스 > 레이아웃
        self.status_layout.addWidget(self.hud)
        self.status_layout.addWidget(self.status_log)
        self.status_layout.addWidget(self.log)