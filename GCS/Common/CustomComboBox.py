# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *


class CustomComboBox(QComboBox):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self,parent=None, width=145, height=170):
        super(CustomComboBox, self).__init__(parent)
        self.width = width;
        self.height = height;
        self.init_widget()

    # #########################################################################################
    #  Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):

        self.setStyleSheet("QComboBox {background-color:rgb(46, 88 ,127); color : white; border: none;}")
        self.resize(self.width, self.height)
        self.setFixedSize(self.width,self.height)
