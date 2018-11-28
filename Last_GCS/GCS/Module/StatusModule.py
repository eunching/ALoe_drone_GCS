# -*- coding: utf-8 -*-

from GCS.Util.Util import *
from PyQt5.QtWidgets import *
from GCS.Widget.BaseWidget import BaseWidget
from GCS.Common.CustomLabel import *
from GCS.Common.CustomLabelWhite import *
from PyQt5.QtCore import pyqtSlot


class StatusModule(BaseWidget):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self):
        super(StatusModule, self).__init__(CONTROL_WIDTH, STATUS_TEXT_HEIGHT, None)

        # 상태 레이아웃(라벨, 상태로그)
        self.status_layout = QVBoxLayout(self.widget)

        # 라벨(타이틀) 생성
        #self.title = CustomLabel(self.widget, width=CONTROL_WIDTH, name="  ▶  DRONE STATUS", color="G")

        # 상태로그 위젯
        self.status_log_widget = QWidget(self)

        # 상태로그 레이아웃
        self.status_log_layout = QGridLayout(self.status_log_widget)

        # 타이틀 라벨 생성
        self.mode = CustomLabelWhite(self.status_log_widget, name="Mode")
        self.arming = CustomLabelWhite(self.status_log_widget, name="Arming")
        self.battery_volt = CustomLabelWhite(self.status_log_widget, name="Battery Volt")
        self.battery_remain = CustomLabelWhite(self.status_log_widget, name="Battery Remain")
        self.current_mission = CustomLabelWhite(self.status_log_widget, name="Current Mission")

        # 타이틀 라벨 생성
        self.mode_val = CustomLabelWhite(self.status_log_widget, name="N/A")
        self.arming_val = CustomLabelWhite(self.status_log_widget, name="N/A")
        self.battery_volt_val = CustomLabelWhite(self.status_log_widget, name="N/A")
        self.battery_remain_val = CustomLabelWhite(self.status_log_widget, name="N/A")
        self.current_mission_val = CustomLabelWhite(self.status_log_widget, name="N/A")

        # UI 설정
        self.init_widget()

        # 시리얼 Read(HeartBeat) 슬롯 연결
        self.serial_manager.send_status_data.connect(self.get_status_data)

        # UI 초기화
        self.serial_manager.send_ui_init.connect(self.get_ui_init)

    # #########################################################################################
    #  Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):

        # 레이아웃(self) 옵션 설정
        self.status_log_layout.setContentsMargins(10, 0, 0, 10)

        # Mode 라벨 및 데이터 배치
        self.status_log_layout.addWidget(self.mode, 0, 0)
        self.status_log_layout.addWidget(self.mode_val, 0, 1)

        # Arming 라벨 및 데이터 배치
        self.status_log_layout.addWidget(self.arming, 1, 0)
        self.status_log_layout.addWidget(self.arming_val, 1, 1)

        # Battery Volt 라벨 및 데이터 배치
        self.status_log_layout.addWidget(self.battery_volt, 2, 0)
        self.status_log_layout.addWidget(self.battery_volt_val, 2, 1)

        # Battery remain 라벨 및 데이터 배치
        self.status_log_layout.addWidget(self.battery_remain, 3, 0)
        self.status_log_layout.addWidget(self.battery_remain_val, 3, 1)

        # current Mission 라벨 및 데이터 배치
        self.status_log_layout.addWidget(self.current_mission, 4, 0)
        self.status_log_layout.addWidget(self.current_mission_val, 4, 1)

        # 위젯(타이틀 라벨, 상태로그 위젯) > 레이아웃
        #self.status_layout.addWidget(self.title)
        self.status_layout.addWidget(self.status_log_widget)
        self.status_layout.setContentsMargins(0, 0, 0, 0)

    # #########################################################################################
    #  시리얼 Read(HeartBeat) 데이터 전송
    # #########################################################################################
    @pyqtSlot(dict)
    def get_status_data(self, status_data):

        mode = str(status_data.pop('mode'))
        arming = str(status_data.pop('arming'))
        battery_volt = str(status_data.pop('battery_volt'))
        battery_remain = str(status_data.pop('battery_remain'))
        current_mission = str(status_data.pop('current_mission'))

        mode = self.mode_val.text() if mode == '' else mode
        arming = self.arming_val.text() if arming == '' else arming
        battery_volt = self.battery_volt_val.text() if battery_volt == '' else battery_volt
        battery_remain = self.battery_remain_val.text() if battery_remain == '' else battery_remain
        current_mission = self.current_mission_val.text() if current_mission == '' else current_mission

        self.mode_val.setText(mode)
        self.arming_val.setText(arming)
        self.battery_volt_val.setText(battery_volt)
        self.battery_remain_val.setText(battery_remain)
        self.current_mission_val.setText(current_mission)

    # #########################################################################################
    #  시리얼 접속 해제로 인한 UI 초기화
    # #########################################################################################
    @pyqtSlot(str)
    def get_ui_init(self, connect):

        if connect == "on":
            pass
        else:
            self.mode_val.setText("N/A")
            self.arming_val.setText("N/A")
            self.battery_volt_val.setText("N/A")
            self.battery_remain_val.setText("N/A")
            self.current_mission_val.setText("N/A")