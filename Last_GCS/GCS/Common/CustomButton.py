# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *


class CustomButton(QPushButton):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self, parent=None, width=145, height=170, name='button'):
        super(CustomButton, self).__init__(parent)
        self.width = width
        self.height = height
        self.name = name

        self.init_widget()

    # #########################################################################################
    #  버튼 위젯 처리
    # #########################################################################################
    def init_widget(self):
        self.setStyleSheet("QPushButton { background-color:rgb(85, 94, 110); color : white; border: none;}\n"
                           "QPushButton:hover{ background-color: rgb(73, 101, 128); }\n"
                           "QPushButton:pressed{ background-color: rgb(65, 168, 167);}\n"
                           "QPushButton:disabled{ background-color:#9fa7b5}")
        self.resize(self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setText(self.name)
