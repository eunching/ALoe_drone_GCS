
from GCS.Util.Util import *
from PyQt5.QtWidgets import *
from GCS.Widget.BaseWidget import BaseWidget
from GCS.Common.CustomLabel import *
from GCS.Common.CustomTextEdit import *
from PyQt5.QtCore import pyqtSlot


class LogModule(BaseWidget):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self):
        super(LogModule, self).__init__(TEXT_WIDTH, TEXT_HEIGHT, None)

        # 텍스트 레이아웃(라벨, 상태로그)
        self.text_layout = QVBoxLayout(self.widget)

        # 라벨(타이틀) 생성
        self.title = CustomLabel(self.widget, width=TEXT_WIDTH, name="  ▶  LOG LIST", color="G")

        # 텍스트 로그 위젯
        self.text_log_widget = QWidget(self)

        # 텍스트 로그 레이아웃
        self.text_log_layout = QVBoxLayout(self.text_log_widget)

        # 로그 텍스트 에디터
        self.text_edit = CustomTextEdit(self.text_log_widget)

        # 시리얼 Read(STATUSTEXT + COMMAND_ACK) 정보 스롯 연결
        self.serial_manager.send_log_data.connect(self.get_log_data)

        # UI 초기화
        self.serial_manager.send_ui_init.connect(self.get_ui_init)

        # UI 설정
        self.init_widget()

    # #########################################################################################
    #  Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):
        # 레이아웃(self) 옵션 설정
        self.text_log_layout.setContentsMargins(0, 0, 0, 0)
        self.text_log_layout.addWidget(self.text_edit)

        # 위젯(타이틀 라벨, 텍스트 위젯) > 레이아웃
        self.text_layout.addWidget(self.title)
        self.text_layout.addWidget(self.text_log_widget)
        self.text_layout.setSpacing(0)
        self.text_layout.setContentsMargins(0, 0, 0, 0)

        self.text_edit.setReadOnly(True)

    # #########################################################################################
    #  Log 데이터 등록 처리
    # #########################################################################################
    @pyqtSlot(str)
    def get_log_data(self, message):

        self.text_edit.append(message)

    # #########################################################################################
    #  시리얼 접속 해제로 인한 UI 초기화
    # #########################################################################################
    @pyqtSlot(str)
    def get_ui_init(self, connect):

        if connect == "on":
            pass
        else:
            # Log edit 초기화
            self.text_edit.clear()
