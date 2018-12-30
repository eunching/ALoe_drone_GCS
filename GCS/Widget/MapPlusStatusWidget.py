# -*- coding: utf-8 -*-

from GCS.Util.Util import *
from PyQt5.QtWidgets import QVBoxLayout
from GCS.Widget.BaseWidget import BaseWidget
from GCS.Module.LogModule import LogModule
from GCS.Module.CameraModule import CameraModule
from GCS.Widget.MapWidget import MapWidget
from GCS.Widget.StatusWidget import StatusWidget

class MapPlusStatusWidget(BaseWidget):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self):
        super(MapPlusStatusWidget, self).__init__(MAP_WIDTH, 954, None)

        # 위젯들(컨트롤,맵,허드 및 로그) > 레이아웃
        self.map_plus_status_layout = QVBoxLayout(self.widget)

        # 위젯(컨트롤, 맵, 로그) 인스턴스 생성
        self.map_widget = MapWidget()
        self.status_widget = StatusWidget()

        # UI 설정
        self.init_widget()

    # #########################################################################################
    #  Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):

        # 레이아웃 옵션 설정
        self.map_plus_status_layout.setSpacing(0)
        self.map_plus_status_layout.setContentsMargins(0, 0, 0, 0)

        # 위젯 인스턴스 > 레이아웃
        self.map_plus_status_layout.addWidget(self.map_widget)
        self.map_plus_status_layout.addWidget(self.status_widget)
