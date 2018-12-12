
from PyQt5.QtWidgets import *
from GCS.Widget.BaseWidget import BaseWidget
from GCS.Common.CustomLabel import *
from GCS.Common.CustomTextEdit import *
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel
import cv2



class CameraModule(BaseWidget):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self):
        super(CameraModule, self).__init__(CONTROL_WIDTH, TEXT_HEIGHT, None)

        # 텍스트 레이아웃(라벨, 상태로그)
        self.camera_layout = QVBoxLayout(self.widget)

        # 라벨(타이틀) 생성
        self.title = CustomLabel(self.widget, width=CONTROL_WIDTH, name="  ▶  FLIR CAMERA", color="B")
        self.setStyleSheet(FONT_STYLE)

        self.flir_image = QLabel(self.widget)
        self.flir_image.setStyleSheet(LABEL_BLACK)
        self.flir_image.setAlignment(Qt.AlignCenter)

        # UI 초기화
        self.serial_manager.send_ui_init.connect(self.get_ui_init)

        # UI 설정
        self.init_widget()

    # #########################################################################################
    #  Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):
        # 레이아웃(self) 옵션 설정
        camera_path = HTML_PATH + "media.Html"
        self.camera_layout.setContentsMargins(0, 0, 0, 0)

        # 위젯(타이틀 라벨, 텍스트 위젯) > 레이아웃
        self.camera_layout.addWidget(self.title)
        self.camera_layout.addWidget( self.flir_image)
        self.camera_layout.setSpacing(0)
        self.camera_layout.setContentsMargins(0, 0, 0, 0)

        capture = CaptureThread(self)
        capture.set_change_image.connect(self.get_change_image)
        capture.start()

    # #########################################################################################
    #  시리얼 접속 해제로 인한 UI 초기화
    # #########################################################################################
    @pyqtSlot(str)
    def get_ui_init(self, connect):

        if connect == "on":
            pass
        else:
            # Log edit 초기화
            pass

    # #########################################################################################
    #  캡쳐한 이미지를 라벨에다 추가
    # #########################################################################################
    @pyqtSlot(QImage)
    def get_change_image(self, image):
        self.flir_image.setPixmap(QPixmap.fromImage(image))


class CaptureThread(QThread):

    set_change_image = pyqtSignal(QImage)

    def run(self):

        url = "http://192.168.200.5:8080"
        cap = cv2.VideoCapture(url)
        count_plus = 1
        path = './FLIR_image/'

        while True:

            try:
                ret, frame = cap.read()

                if ret:
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    convert_to_format = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)

                    p = convert_to_format.scaled(570, 300, Qt.KeepAspectRatio)
                    self.set_change_image.emit(p)

                    count = str(count_plus)
                    filename = path + count + '.jpg'
                    cv2.imwrite(filename, frame,  params=[cv2.IMWRITE_PNG_COMPRESSION, 0])
                    count_plus += 1

            except Exception as exp:
                print(exp)

