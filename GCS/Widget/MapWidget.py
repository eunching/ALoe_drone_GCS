# -*- coding: utf-8 -*-


from GCS.Util.Util import *
from PyQt5 import QtCore
from PyQt5.QtWebChannel import *
from PyQt5.QtWebEngineWidgets import *
from GCS.Widget.BaseWidget import BaseWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
import geocoder

class MapWidget(BaseWidget):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self):
        super(MapWidget, self).__init__(MAP_WIDTH, CONTENTS_HEIGHT, None)

        # 레이아웃(구글맵)
        self.map_layout = QVBoxLayout(self.widget)

        # 웹 엔진
        self.engine_view = QWebEngineView()

        # 웹채널(웹페이지 뷰기능)
        self.web_channel = QWebChannel(self.engine_view.page())

        # 구글 맵 인스턴스 생성
        self.google = GoogleObject(self)

        # UI 설정
        self.init_widget()

        # 맵마커 경로 설정
        self.marker_values = str()

        # 구글 인스턴스를 통한 시그널 발생 시 함수 호출
        # self.google.way_point_data.connect(lambda v: self.set_marker_value(v))
        self.google.way_point_data.connect(self.set_marker_value)

        # Wap-Point 설정 정보 슬롯 연결
        self.serial_manager.send_way_point_to_map.connect(self.get_way_point_to_map)

        # GPS_RAW_INTM, VFR_HUD, MISSION_ITEM_INT(seq=0) 를 통한 drone 위치 및 home data 슬롯 연결
        self.serial_manager.send_map_data.connect(self.get_map_data)
        # UI 초기화
        self.serial_manager.send_ui_init.connect(self.get_ui_init)

        self.currentDrone = [0,0,0]

    # #########################################################################################
    #   Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):

        # 현재 디렉토리 패스
        map_path = HTML_PATH+"map.Html"

        # 레이아웃 옵션 설정
        self.map_layout.setSpacing(0)
        self.map_layout.setContentsMargins(0, 0, 0, 0)

        # 웹뷰 > 웹엔진
        self.engine_view.page().setWebChannel(self.web_channel)

        # 구글맵 웹 페이지(js) 연결 오브젝트
        self.web_channel.registerObject("map_info", self.google)

        # 엔진뷰 구글맵 페이지 로드 처리
        self.engine_view.load((QtCore.QUrl.fromLocalFile(map_path)))

        # 엔진뷰 > 레이아웃
        self.map_layout.addWidget(self.engine_view)


    # #########################################################################################
    #  WayPoint widget 으로 마커 위치 전달
    # #########################################################################################
    @pyqtSlot(str)
    def set_marker_value(self, map_data: str):

        self.serial_manager.send_map_to_way_point.emit(map_data)

    # #########################################################################################
    #   Way-Point Widget > Map Widget 클릭 이벤트 전달
    # #########################################################################################
    @pyqtSlot(str)
    def get_way_point_to_map(self, data):

        if data.startswith("init"):
            # 모든 데이터 초기화
            self.engine_view.page().runJavaScript("mapReset(true)")
            # 마커 선택 disable
            self.engine_view.page().runJavaScript("toggleSetYn(false)")

        elif data.startswith("insert"):
            # 마커 선택 Enable
            self.engine_view.page().runJavaScript("toggleSetYn(true)")

        elif data.startswith("delete") or data.startswith("save"):

            # 삭제 및 저장 처리하는 시점 WayPoint 설정 상태를 임시로 해제 시킨다.(JS: autoDrawing() 을 호출하기 위함)
            # 마커 선택 disable
            self.engine_view.page().runJavaScript("toggleSetYn(false)")

            # 최종 way_point 를 추출한다.
            way_point = data.split("-")[1]
            self.engine_view.page().runJavaScript("setWayPoint('"+way_point+"')")

            # 삭제 처리 하는 경우만 setYn = true 로 설정해서 wayPoint 상태로 유지 한다.
            if data.startswith("delete"):
                # 마커 선택 enable
                self.engine_view.page().runJavaScript("toggleSetYn(true)")
        elif data.startswith("Drone"):

            data = data.split("-")[1]
            data = data.split(",")
            self.currentDrone[0] = data[0] if data[0] != "" else self.currentDrone[0]
            self.currentDrone[1] = data[1] if data[1] != "" else self.currentDrone[1]
            self.currentDrone[2] =  data[2] if data[2] != "" else self.currentDrone[2]

            send_data = "myDrone01," + str(0) + "," + str(self.currentDrone[0]) + "," + str(self.currentDrone[1]) + "," + str(0) + "," + str(self.currentDrone[2]) + "," + "d" + "/"
            # 기본적으로 하나의 데이터 필드밖에 없기 때문에 그대로 set

            self.engine_view.page().runJavaScript("setDroneMarker('" + send_data + "')")

        elif data.startswith("Home"):
            data = data.split("-")[1]
            self.engine_view.page().runJavaScript("setHomeMarker('" + data + "')")

    # #########################################################################################
    #   드론 현재 위치 및 Home 위치 google map 에 설정
    # #########################################################################################
    @pyqtSlot(dict)
    def get_map_data(self, map_data):
        # map_data 에서 type , lat,lon,head 가져오기

        type = str(map_data.pop("type"))
        lat = str(map_data.pop("lat"))
        lon = str(map_data.pop("lon"))
        head = str(map_data.pop("heading"))

        # 현재 드론 위치 가져올시 실행되는 루틴.
        # 단 GPS_RAW_INT(#24), VFR_HUD(#74) 두 위치에서 데이터를 각각 가져오기 때문에 전역 변수를 계속 덮어 씌우며 사용한다.
        if type == "drone":
            self.currentDrone[0] = lat if lat != "" else self.currentDrone[0]
            self.currentDrone[1] = lon if lon != "" else self.currentDrone[1]
            self.currentDrone[2] = head if head != "" else self.currentDrone[2]

            # javascript에 전송할 데이터 셋 생성
            send_data = "myDrone01," + str(0) + "," + str(self.currentDrone[0]) + "," + str(self.currentDrone[1]) + "," + str(0) + "," + str(self.currentDrone[2])  + "," + "d" + "/"

            # 기본적으로 하나의 데이터 필드밖에 없기 때문에 그대로 set
            self.engine_view.page().runJavaScript("setDroneMarker('" + send_data + "')")
        elif type == "home":

            send_data = lat + "," + lon
            self.engine_view.page().runJavaScript("setHomeMarker('" + send_data + "')")
    # #########################################################################################
    #  시리얼 접속 해제로 인한 UI 초기화
    # #########################################################################################
    @pyqtSlot(str)
    def get_ui_init(self, connect):

        # 모든 데이터 초기화
        self.engine_view.page().runJavaScript("mapReset(true)")


# #########################################################################################
#  구글맵 연동 Class
# #########################################################################################
class GoogleObject(QObject):

    # 구글 맵 클릭 시 시그널 발생
    way_point_data = pyqtSignal(str)

    @pyqtSlot(str)
    def location_changed(self, string):
        self.way_point_data.emit(string)

    @pyqtSlot()
    def getCenter(self):
        data = geocoder.ip('me').latlng
