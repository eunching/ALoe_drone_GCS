# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from GCS.Serial.SerialManager import SerialManager


class BaseWidget(QWidget):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self, width: int, height: int, color: str):
        super(BaseWidget, self).__init__()

        # 시러얼 singleton 클래스
        self.serial_manager = SerialManager.instance()

        # 각각 클래스 내에 위젯 선언
        self.widget = QWidget(self)
        self.widget.setMinimumSize(width, height)
        self.widget.setMaximumSize(width, height)

        # 위젯 컬러가 존재 한 경우
        if color is not None:
            self.widget.setStyleSheet(color)

        # 각각 클래스 내에 레이아웃 공통 처리
        self.box = QVBoxLayout()
        self.box.setContentsMargins(0, 0, 0, 0)

        # 하위 클래스 모든 위젯들은 self.widget 상속 받은 후 하위 위젯들을 주입 시킨다.
        self.box.addWidget(self.widget)

        # 자식 클래스들 레이아웃에 설정
        self.setLayout(self.box)

    # #########################################################################################
    #   공통 메시지 박스
    # #########################################################################################
    @staticmethod
    def show_message(title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
