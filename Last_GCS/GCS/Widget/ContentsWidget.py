# -*- coding: utf-8 -*-

from GCS.Util.Util import *
from PyQt5.QtWidgets import QHBoxLayout
from GCS.Widget.MapWidget import MapWidget
from GCS.Widget.BaseWidget import BaseWidget
from GCS.Widget.StatusWidget import StatusWidget
from GCS.Widget.ControlWidget import ControlWidget
from GCS.Widget.RightWidget import RightWidget


class ContentsWidget(BaseWidget):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self):
        super(ContentsWidget, self).__init__(WIN_WIDTH, CONTENTS_HEIGHT, None)

        # 위젯들(컨트롤,맵,허드 및 로그) > 레이아웃
        self.contents_layout = QHBoxLayout(self.widget)

        # 위젯(컨트롤, 맵, 로그) 인스턴스 생성
        self.control_widget = ControlWidget()
        self.right_widget = RightWidget()

        # UI 설정
        self.init_widget()

    # #########################################################################################
    #  Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):

        # 레이아웃 옵션 설정
        self.contents_layout.setSpacing(0)
        self.contents_layout.setContentsMargins(0, 0, 0, 0)

        # 위젯 인스턴스 > 레이아웃
        self.contents_layout.addWidget(self.control_widget)
        self.contents_layout.addWidget(self.right_widget)
        #self.contents_layout.addWidget(self.map_widget)
        #self.contents_layout.addWidget(self.status_widget)
