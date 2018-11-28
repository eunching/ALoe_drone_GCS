# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel
from GCS.Util.Util import *


class CustomLabelWhite(QLabel):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self, parent=None, name=""):
        super(CustomLabelWhite, self).__init__(parent)

        # set Label Text
        self.setText(name)
        self.setStyleSheet(FONT_WHITE)
