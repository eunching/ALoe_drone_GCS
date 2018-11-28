# -*- coding: utf-8 -*-

import sys
from GCS.Util.Util import *
from PyQt5.QtGui import QPixmap, QIcon
from GCS.Widget.BaseWidget import BaseWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QLineEdit
from GCS.Common.CustomButton import CustomButton
from GCS.Common.CustomImgButton import CustomImgButton
from GCS.Common.CustomComboBox import CustomComboBox
from GCS.Serial.SerialConfig import SerialConfig


# 해당 OS 추출
__platform__ = sys.platform


class TopWidget(BaseWidget):

    def __init__(self):

        super(TopWidget, self).__init__(WIN_WIDTH, LOGO_HEIGHT, BACKGROUNG_WIDGET_COLOR)

        # 위젯들(로고,포트,보드레이트,접속버튼) > 레이아웃
        self.top_layout = QHBoxLayout(self.widget)

        # 로고 위젯
        self.logo = QLabel(self.widget)

        # text 박스
        self.textbox = QLineEdit(self.widget)

        # 접속 포트 콤보박스
        self.port_name = CustomComboBox(self.widget, 300, 35)

        # 접속 보드레이트 콤보박스
        self.baud_rate = CustomComboBox(self.widget, 200, 35)

        # 시리얼 접속 버튼 위젯
        self.btn_connect = CustomButton(self.widget, 130, 35, "Connect")

        # PORT 새로고침 버튼 위젯
        self.btn_refresh = CustomButton(self.widget, 130, 35, "ReFresh")

        # UI 설정
        self.init_widget()

    def init_widget(self):

        # 로고 이미지 설정 옵션
        self.logo.setPixmap(QPixmap(IMG_PATH + "logo.png"))

        # 포트,보드레이트,접속 버튼 데이터(콤보박스) 설정
        self._fill_serial_info()

        ## 위젯 배치(로고,포트,보드레이트,접속버튼)
        self.top_layout.addWidget(self.logo)
        self.top_layout.addWidget(self.textbox)
        self.top_layout.addWidget(self.port_name)
        self.top_layout.addWidget(self.baud_rate)
        self.top_layout.addWidget(self.btn_connect)
        self.top_layout.addWidget(self.btn_refresh)

        # Connect 클릭 이벤트 처리
        self.btn_connect.clicked.connect(self.btn_connect_clicked)

        # refresh 클릭 이벤트 처리
        self.btn_refresh.clicked.connect(self.btn_refresh_clicked)

        # save ip 클릭 이벤트 처리
        self.btn_text.clicked.connect(self.btn_text_clicked)

    # 시리얼 상수 값들을 포트, 보드레이트에 값을 넣고 접속 버튼은 시그널 처리
    def _fill_serial_info(self):

        # 시리얼 포트 및 보드레이터 초기화
        self.port_name.clear()
        self.baud_rate.clear()

        # 포트 및 보드레이터 설정
        self.port_name.insertItems(0, self._get_available_port())
        self.baud_rate.insertItems(0, [str(x) for x in SerialConfig.BAUDRATES])

        # port 맨 마지막 인덱스로 설정
        self.port_name.setCurrentIndex(self.port_name.count() - 1)

        # default boud rate 설정(57600)
        self.baud_rate.setCurrentIndex(6)

    # 사용가능한 포트 조회
    def _get_available_port(self):
        result = []

        for port in QSerialPortInfo().availablePorts():

            result.append(port.portName() if __platform__.startswith('win') else "/dev/" + port.portName())

        return result

    ## 시리얼 connect 버튼 클릭 이벤트
    @pyqtSlot()
    def btn_connect_clicked(self):

        ip_address = self.textbox.text()

        is_open = self.serial_manager.serial.isOpen()
        connect_flag = "open"

        if is_open:
            connect_flag = "close"

        connect_data = (
            "serial",
            (self.port_name.currentText(), int(self.baud_rate.currentText()), ip_address, connect_flag)
        )

        # 접속 정보 전달 >> SerialManager
        self.serial_manager.btn_clicked(connect_data)

        self.btn_connect.setText({False: 'Connect', True: 'Disconnect'}[self.serial_manager.serial.isOpen()])

    # refresh 버튼 클릭 이벤트
    @pyqtSlot()
    def btn_refresh_clicked(self):

        # 새로운 시리얼 포트 및 보드레이트 추가
        self._fill_serial_info()
        self.textbox.clear()
