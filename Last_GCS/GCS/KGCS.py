# -*- coding: utf-8 -*-

import sys

from GCS.Util.Util import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from GCS.Widget.TopWidget import TopWidget
from GCS.Widget.ContentsWidget import ContentsWidget


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        # TOP - CONTENTS 위젯 > 레이아웃
        self.main_layout = QVBoxLayout(self)

        # 로고 및 시리얼 연결 객체
        self.top_widget = TopWidget()

        # 컨트롤러, 맵, 상태 모니터링 객체
        self.content_widget = ContentsWidget()

        # UI 설정
        self.init_widget()

    def init_widget(self):

        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)

        # TopWidget - ContentWidget > 레이아웃
        self.main_layout.addWidget(self.top_widget)
        self.main_layout.addWidget(self.content_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
