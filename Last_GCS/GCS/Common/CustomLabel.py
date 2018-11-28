# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel


class CustomLabel(QLabel):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self, parent=None, width=0, height=40, name="", color="B"):
        super(CustomLabel, self).__init__(parent)

        self.width = width
        self.height = height
        self.name = name

        # Label 크기 강제 지정
        self.resize(self.width, self.height)
        self.setFixedSize(self.width, self.height)

        # set Label Text
        self.setText(name)

        # Label style sheet
        if color == "B":
            self.setStyleSheet("QLabel { background-color:rgb(192,108,132); color : white; border: none; }")
            pass
        else:
            # self.setStyleSheet("QLabel { background-color:rgb(89, 178, 186); color : white; border: none; }")
            # self.setStyleSheet("QLabel { background-color:rgb(130, 140, 100); color : white; border: none; }")
            self.setStyleSheet("QLabel { background-color:rgb(53,92,125); color : white; border: none; }")
