# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from GCS.Widget.BaseWidget import QWidget, BaseWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from GCS.Common.CustomLabel import *
from GCS.Common.CustomLabelWhite import *
from PyQt5.QtCore import pyqtSlot
from GCS.Util.Util import *


class DroneModule(BaseWidget):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self,):

        super(DroneModule, self).__init__(CONTROL_WIDTH, DRONE_HEIGHT, None)

        # 상태 레이아웃(라벨, 드론 및 접속 정보)
        self.drone_layout = QVBoxLayout(self.widget)

        # 라벨(타이틀) 생성
        self.title = CustomLabel(self.widget, width=CONTROL_WIDTH, name="  ▶  DRONE", color="B")

        # 드론 및 접속정보 위젯
        self.drone_widget = QWidget()

        # 드론 이미지
        self.drone_img = QLabel(self.widget)

        # 드론 및 접속정보 merge 레이아웃
        self.drone_info_layout = QHBoxLayout(self.drone_widget)

        # 접속정보 레이아웃
        self.info_layout = QGridLayout()

        # 타이틀 라벨 생성
        self.flight_control = CustomLabelWhite(self.widget, name="Flight Controller")
        self.flight_type = CustomLabelWhite(self.widget, name="Flight Type")
        self.flight_status = CustomLabelWhite(self.widget, name="Flight Status")
        self.connected_port = CustomLabelWhite(self.widget, name="Connected Port")
        self.connected_baud = CustomLabelWhite(self.widget, name="Connected BaudRate")

        # 데이터 라벨 생성
        self.flight_control_val = CustomLabelWhite(self.widget, name="N/A")
        self.flight_type_val = CustomLabelWhite(self.widget, name="N/A")
        self.flight_status_val = CustomLabelWhite(self.widget, name="N/A")
        self.connected_port_val = CustomLabelWhite(self.widget, name="N/A")
        self.connected_baud_val = CustomLabelWhite(self.widget, name="N/A")

        # UI 설정
        self.init_widget()

        # 시리얼 접속 후 드론 상태 변경 및 접속 정보 스롯 연결
        self.serial_manager.send_drone_data.connect(self.get_drone_data)

        # UI 초기화
        self.serial_manager.send_ui_init.connect(self.get_ui_init)

    # #########################################################################################
    #  Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):

        # 드론 이미지 설정 및 위치 지정
        self.drone_img.setPixmap(QtGui.QPixmap(IMG_PATH+"drone_off.png"))
        self.drone_img.setGeometry(QtCore.QRect(20, 80, 141, 81))

        # flight_control 라벨 및 데이터 배치
        self.info_layout.addWidget(self.flight_control, 0, 0)
        self.info_layout.addWidget(self.flight_control_val, 0, 1)

        # flight_speed 라벨 및 데이터 배치
        self.info_layout.addWidget(self.flight_type, 1, 0)
        self.info_layout.addWidget(self.flight_type_val, 1, 1)

        # flight_status 라벨 및 데이터 배치
        self.info_layout.addWidget(self.flight_status, 2, 0)
        self.info_layout.addWidget(self.flight_status_val, 2, 1)

        # drone_serial 라벨 및 데이터 배치
        self.info_layout.addWidget(self.connected_port, 3, 0)
        self.info_layout.addWidget(self.connected_port_val, 3, 1)

        # drone_port 라벨 및 데이터 배치
        self.info_layout.addWidget(self.connected_baud, 4, 0)
        self.info_layout.addWidget(self.connected_baud_val, 4, 1)

        # 드론 이미지 및 접속 정보 레이아웃 > Merge 레이아웃
        self.drone_info_layout.addWidget(self.drone_img)
        self.drone_info_layout.setStretchFactor(self.drone_img, 30)
        self.drone_info_layout.addLayout(self.info_layout)
        self.drone_info_layout.setStretchFactor(self.info_layout, 70)

        # 위젯(타이틀 라벨, 드론 및 접속 정보 위젯) > 레이아웃
        self.drone_layout.addWidget(self.title)
        self.drone_layout.addWidget(self.drone_widget)
        self.drone_layout.setContentsMargins(0, 0, 0, 0)

    # #########################################################################################
    #  시리얼 접속 후 드론 이미지 변경 처리
    #  1. Flight 데이터 : HeartBeat
    #  2. Drone 접속 정보: 시리얼 접속
    # #########################################################################################
    @pyqtSlot(dict)
    def get_drone_data(self, status_data):

        controller = str(status_data.pop('controller'))
        type = str(status_data.pop('type'))
        status = str(status_data.pop('status'))
        port = str(status_data.pop('port'))
        baud = str(status_data.pop('baud'))

        controller = self.flight_control_val.text() if controller == '' else controller
        status = self.flight_status_val.text() if status == '' else status
        type = self.flight_type_val.text() if type == '' else type
        port = self.connected_port_val.text() if port == '' else port
        baud = self.connected_baud_val.text() if baud == '' else baud

        self.flight_control_val.setText(controller)
        self.flight_type_val.setText(type)
        self.flight_status_val.setText(status)
        self.connected_port_val.setText(port)
        self.connected_baud_val.setText(baud)

        if status_data.pop("icon") == "ON":
            self.drone_img.setPixmap(QtGui.QPixmap(IMG_PATH + "drone_on.png"))

    # #########################################################################################
    #  시리얼 접속 해제로 인한 UI 초기화
    # #########################################################################################
    @pyqtSlot(str)
    def get_ui_init(self, connect):

        if connect == "on":
            # 접속 하고나면 get_drone_data()를 통해 접속 정보를 전달한다.
            pass
        else:
            self.flight_control_val.setText("N/A")
            self.flight_type_val.setText("N/A")
            self.flight_status_val.setText("N/A")
            self.connected_port_val.setText("N/A")
            self.connected_baud_val.setText("N/A")

            # 드론 이미지 설정 및 위치 지정
            self.drone_img.setPixmap(QtGui.QPixmap(IMG_PATH + "drone_off.png"))
