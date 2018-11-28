# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTextEdit
from GCS.Util.Util import *


class CustomTextEdit(QTextEdit):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self, parent=None, name=""):
        super(CustomTextEdit, self).__init__(parent)

        self.setStyleSheet(TEXT_WHITE)
        #self.setReadOnly(True)

