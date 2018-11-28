
from GCS.Widget.BaseWidget import BaseWidget
from PyQt5.QtWidgets import QWidget,QVBoxLayout
from GCS.Util.Util import *
from GCS.Module.ControlModule import ControlModule
from GCS.Module.CameraModule import CameraModule
from GCS.Module.WaypointModule import WaypointModule
from GCS.Module.StatusModule import StatusModule


class ControlWidget(BaseWidget):

    def __init__(self):

        super(ControlWidget, self).__init__(CONTROL_WIDTH, CONTENTS_HEIGHT, BACKGROUNG_WIDGET_COLOR)

        # 위젯들(버튼컨트롤, 접속정보, Waypoint) > 레이아웃
        self.control_layout = QVBoxLayout(self.widget)

        self.control_module = ControlModule()
        self.way_point_module = WaypointModule()
        self.camera_module = CameraModule()

        # UI 설정
        self.init_widget()

    # #########################################################################################
    #  Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):

        # 레이아웃 옵션 설정
        self.control_layout.setSpacing(0)
        self.control_layout.setContentsMargins(0, 0, 0, 0)

        # 위젯 인스턴스 > 레이아웃
        self.control_layout.addWidget(self.control_module)
        self.control_layout.addWidget(self.way_point_module)
        self.control_layout.addWidget(self.camera_module)

