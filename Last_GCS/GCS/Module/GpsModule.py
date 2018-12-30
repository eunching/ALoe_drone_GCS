# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from GCS.Util.Util import *
from PyQt5.QtCore import pyqtSlot
from GCS.Common.CustomLabel import *
from GCS.Common.CustomLabelWhite import *
from GCS.Widget.BaseWidget import BaseWidget

class GpsModule(BaseWidget):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self):
        super(GpsModule, self).__init__(TEXT_WIDTH, GPS_HEIGHT, BACKGROUND_COLOR_1)

        # 상태 레이아웃(라벨, 상태로그)
        self.status_layout = QVBoxLayout(self.widget)

        # 라벨(타이틀) 생성
        self.title = CustomLabel(self.widget, width=TEXT_WIDTH, name=" ▶  DRONE STATUS", color="B")

        # 상태로그 위젯
        self.gps_widget = QWidget(self)

        # 상태로그 레이아웃
        self.gps_layout = QGridLayout(self.gps_widget)

        # 타이틀 라벨 생성
        self.fix = CustomLabelWhite(self.gps_widget, name="Fix")
        self.count = CustomLabelWhite(self.gps_widget, name="Count")
        self.alt = CustomLabelWhite(self.gps_widget, name="Altitude")
        self.lat = CustomLabelWhite(self.gps_widget, name="Latitude")
        self.lng = CustomLabelWhite(self.gps_widget, name="Longitude")
        # self.h_dop = CustomLabelWhite(self.gps_widget, name="HDOP")
        # self.v_dop = CustomLabelWhite(self.gps_widget, name="VDOP")

        # 타이틀 라벨 생성
        self.fix_val = CustomLabelWhite(self.gps_widget, name="N/A")
        self.count_val = CustomLabelWhite(self.gps_widget, name="N/A")
        self.lat_val = CustomLabelWhite(self.gps_widget, name="N/A")
        self.alt_val = CustomLabelWhite(self.gps_widget, name="N/A")
        self.lng_val = CustomLabelWhite(self.gps_widget, name="N/A")
        # self.h_dop_val = CustomLabelWhite(self.gps_widget, name="N/A")
        # self.v_dop_val = CustomLabelWhite(self.gps_widget, name="N/A")

        # status module
        self.mode = CustomLabelWhite(self.gps_widget, name="Mode")
        self.arming = CustomLabelWhite(self.gps_widget, name="Arming")
        self.battery_volt = CustomLabelWhite(self.gps_widget, name="Battery Volt")
        self.battery_remain = CustomLabelWhite(self.gps_widget, name="Battery Remain")
        self.current_mission = CustomLabelWhite(self.gps_widget, name="Current Mission")

        # 타이틀 라벨 생성
        self.mode_val = CustomLabelWhite(self.gps_widget, name="N/A")
        self.arming_val = CustomLabelWhite(self.gps_widget, name="N/A")
        self.battery_volt_val = CustomLabelWhite(self.gps_widget, name="N/A")
        self.battery_remain_val = CustomLabelWhite(self.gps_widget, name="N/A")
        self.current_mission_val = CustomLabelWhite(self.gps_widget, name="N/A")

        # UI 설정
        self.init_widget()

        # 시리얼 Read(GPS) 정보 스롯 연결
        self.serial_manager.send_gps_data.connect(self.get_gps_data)

        # UI 초기화
        self.serial_manager.send_ui_init.connect(self.get_ui_init)

    # #########################################################################################
    #  Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):

        # 레이아웃(self) 옵션 설정
        self.gps_layout.setContentsMargins(10, 0, 0, 10)

        # Fix 라벨 및 데이터 배치
        self.gps_layout.addWidget(self.fix, 0, 0)
        self.gps_layout.addWidget(self.fix_val, 0, 1)

        # Count 라벨 및 데이터 배치
        self.gps_layout.addWidget(self.count, 1, 0)
        self.gps_layout.addWidget(self.count_val, 1, 1)

        # Alt 라벨 및 데이터 배치
        self.gps_layout.addWidget(self.alt, 2, 0)
        self.gps_layout.addWidget(self.alt_val, 2, 1)

        # Lat 라벨 및 데이터 배치
        self.gps_layout.addWidget(self.lat, 3, 0)
        self.gps_layout.addWidget(self.lat_val, 3, 1)

        # Lng 라벨 및 데이터 배치
        self.gps_layout.addWidget(self.lng, 4, 0)
        self.gps_layout.addWidget(self.lng_val, 4, 1)

        # H-dop 라벨 및 데이터 배치
        # self.gps_layout.addWidget(self.h_dop, 5, 0)
        # self.gps_layout.addWidget(self.h_dop_val, 5, 1)
        #
        # V-dop 라벨 및 데이터 배치
        # self.gps_layout.addWidget(self.v_dop, 6, 0)
        # self.gps_layout.addWidget(self.v_dop_val, 6, 1)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~status
        self.gps_layout.addWidget(self.mode, 0, 2)
        self.gps_layout.addWidget(self.mode_val, 0, 3)

        # Arming 라벨 및 데이터 배치
        self.gps_layout.addWidget(self.arming, 1, 2)
        self.gps_layout.addWidget(self.arming_val, 1, 3)

        # Battery Volt 라벨 및 데이터 배치
        self.gps_layout.addWidget(self.battery_volt, 2, 2)
        self.gps_layout.addWidget(self.battery_volt_val, 2 ,3)

        # Battery remain 라벨 및 데이터 배치
        self.gps_layout.addWidget(self.battery_remain, 3, 2)
        self.gps_layout.addWidget(self.battery_remain_val, 3, 3)

        # current Mission 라벨 및 데이터 배치
        self.gps_layout.addWidget(self.current_mission, 4, 2)
        self.gps_layout.addWidget(self.current_mission_val, 4, 3)

        # 위젯(타이틀 라벨, 상태로그 위젯) > 레이아웃
        self.status_layout.addWidget(self.title)
        self.status_layout.addWidget(self.gps_widget)
        self.status_layout.setSpacing(0)
        self.status_layout.setContentsMargins(0, 0, 0, 0)

    # #########################################################################################
    #  시리얼 Read(HeartBeat) 데이터 전송
    # #########################################################################################
    @pyqtSlot(dict)
    def get_gps_data(self, gps_data):

        fix = str(gps_data.pop('fix'))
        count = str(gps_data.pop('count'))
        alt = str(gps_data.pop('alt'))
        lat = str(gps_data.pop('lat'))
        lng = str(gps_data.pop('lng'))
        # hdop = str(gps_data.pop('hdop'))
        # vdop = str(gps_data.pop('vdop'))

        fix = self.fix_val.text() if fix == '' else fix
        count = self.count_val.text() if count == '' else count
        alt = self.alt_val.text() if alt == '' else alt
        lat = self.lat_val.text() if lat == '' else lat
        lng = self.lng_val.text() if lng == '' else lng
        # hdop = self.h_dop_val.text() if hdop == '' else hdop
        # vdop = self.v_dop_val.text() if vdop == '' else vdop

        self.fix_val.setText(fix)
        self.count_val.setText(count)
        self.alt_val.setText(alt)
        self.lat_val.setText(lat)
        self.lng_val.setText(lng)
        # self.h_dop_val.setText(hdop)
        # self.v_dop_val.setText(vdop)

    # #########################################################################################
    #  시리얼 접속 해제로 인한 UI 초기화
    # #########################################################################################
    @pyqtSlot(str)
    def get_ui_init(self, connect):

        if connect == "on":
            pass
        else:
            self.fix_val.setText("N/A")
            self.count_val.setText("N/A")
            self.alt_val.setText("N/A")
            self.lat_val.setText("N/A")
            self.lng_val.setText("N/A")
            self.h_dop_val.setText("N/A")
            self.v_dop_val.setText("N/A")
