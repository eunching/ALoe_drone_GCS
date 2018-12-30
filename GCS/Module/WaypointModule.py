# -*- coding: utf-8 -*-

from math import floor
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from GCS.Util.Util import *
from GCS.Common.CustomLabel import *
from PyQt5.QtCore import pyqtSlot
from GCS.Widget.BaseWidget import BaseWidget
from GCS.Common.CustomButton import CustomButton
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QVBoxLayout, QWidget, QHBoxLayout, QAbstractItemView


class WaypointModule(BaseWidget):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self):
        super(WaypointModule, self).__init__(CONTROL_WIDTH, WAYPOINT_HEIGHT, WAYPOINT_WIDGET_COLOR)

        # 상태 레이아웃(라벨, 버튼, 테이블)
        self.waypoint_layout = QVBoxLayout(self.widget)

        # 라벨(타이틀) 생성
        self.title = CustomLabel(self.widget, width=CONTROL_WIDTH, name="  ▶  DRONE FLIGHT WAY POINT", color="B")

        # way point 관련 버튼 모음 위젯
        self.waypoint_btn_widget = QWidget(self)

        # way point 관련 버튼 모음 레이아웃
        self.waypoint_btn_layout = QHBoxLayout(self.waypoint_btn_widget)

        # table 관련 버튼 모음 위젯
        self.table_btn_widget = QWidget(self)

        # way point 관련 버튼 모음 레이아웃
        self.table_btn_layout = QHBoxLayout(self.table_btn_widget)

        # way point 관련 버튼 생성
        self.btn_read = CustomButton(self.waypoint_btn_widget, 170, 30, "READ")
        self.btn_mission = CustomButton(self.waypoint_btn_widget, 170, 30, "MISSION")

        # Table 관련 버튼 생성
        self.btn_init = CustomButton(self.table_btn_widget, 90, 30, "INIT")
        self.btn_insert = CustomButton(self.table_btn_widget, 90, 30, "INSERT")
        self.btn_delete = CustomButton(self.table_btn_widget, 90, 30, "DELETE")
        self.btn_save = CustomButton(self.table_btn_widget, 90, 30, "SAVE")

        # 하단 테이블 위젯 생성
        self.way_point_list = QTableWidget(self.widget)

        # UI 설정
        self.init_widget()

        # Map Widget(마커) 설정 정보 슬롯 연결
        self.serial_manager.send_map_to_way_point.connect(self.get_map_to_way_point)

        # Read 클릭 후 미션 카운트 및 미션 로우별 데이터 전송됨
        self.serial_manager.send_mission_data.connect(self.get_mission_data)
    # #########################################################################################
    #  Widget 초기화 및 설정
    # #########################################################################################
    def init_widget(self):

        # 버튼 이벤트 설정
        self.btn_read.clicked.connect(lambda: self.btn_clicked('read'))
        self.btn_init.clicked.connect(lambda: self.btn_clicked('init'))
        self.btn_insert.clicked.connect(lambda: self.btn_clicked('insert'))
        self.btn_delete.clicked.connect(lambda: self.btn_clicked('delete'))
        self.btn_save.clicked.connect(lambda: self.btn_clicked('save'))
        self.btn_mission.clicked.connect(lambda: self.btn_clicked('mission'))

        # Waypoint 관련 버튼 > 레이아웃 | 위젯-레이아웃 사이즈 옵션 설정
        self.waypoint_btn_layout.addWidget(self.btn_read)
        self.waypoint_btn_layout.addWidget(self.btn_mission)
        self.waypoint_btn_widget.setFixedSize(CONTROL_WIDTH, 30)
        self.waypoint_btn_layout.setContentsMargins(0, 0, 0, 0)

        # Table 관련 버튼 > 레이아웃 | 위젯-레이아웃 사이즈 옵션 설정
        self.table_btn_layout.addWidget(self.btn_init)
        self.table_btn_layout.addWidget(self.btn_insert)
        self.table_btn_layout.addWidget(self.btn_delete)
        self.table_btn_layout.addWidget(self.btn_save)
        self.table_btn_widget.setFixedSize(CONTROL_WIDTH, 30)
        self.table_btn_layout.setContentsMargins(0, 0, 0, 0)

        # 테이블 위젯 생성
        self.init_table_widget()

        # 위젯(타이틀, 컨트롤 버튼) > 레이아웃
        self.waypoint_layout.addWidget(self.title)
        self.waypoint_layout.addWidget(self.waypoint_btn_widget)
        self.waypoint_layout.addWidget(self.table_btn_widget)
        self.waypoint_layout.addWidget(self.way_point_list)
        self.waypoint_layout.setContentsMargins(0, 0, 0, 0)

        # 버튼 초기화 셋팅
        self.btn_setting("off")

        # UI 초기화
        self.serial_manager.send_ui_init.connect(self.get_ui_init)

    # #########################################################################################
    #  테이블 옵션 처리
    # #########################################################################################
    def init_table_widget(self):

        # row 단위로 선택 가능
        self.way_point_list.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Table Widget Read Only 설정
        # self.way_point_list.setEditTriggers(QTableWidget.NoEditTriggers)

        # 테이블 위젯 배경색 및 테두리 두께 지정
        self.way_point_list.setStyleSheet("background-color:rgb(255, 255, 255); border: 0.5px solid gray;")

        # 세로 스크롤바 항상 ON
        self.way_point_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 가로 스크롤바 항상 OFF
        self.way_point_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 각 테이블 요소 간 경계선 View
        self.way_point_list.setShowGrid(True)

        # 초기 row 개수
        self.way_point_list.setRowCount(0)

        # 초기 Column 개수
        self.way_point_list.setColumnCount(5)

        # 테이블 헤더 이름 설정
        table_header = ["NO", "LAT", "LON", "ALT", "HOLD"]

        # 테이블 위젯 수평 헤더 추가
        for i in range(5):
            item = QTableWidgetItem()
            item.setText(table_header[i])
            item.setFlags(Qt.ItemIsEditable)
            self.way_point_list.setHorizontalHeaderItem(i, item)

        # 테이블 위젯 수직 헤더 옵션 설정
        self.way_point_list.verticalHeader().setVisible(False)

        # 컬럼 사이즈 설정
        self.way_point_list.setColumnWidth(0, 30)
        self.way_point_list.setColumnWidth(1, 121)
        self.way_point_list.setColumnWidth(2, 121)
        self.way_point_list.setColumnWidth(3, 78)
        self.way_point_list.setColumnWidth(4, 78)

        # 테이블 로우 컬러 처리
        palette = QPalette()
        palette.setColor(QPalette.Highlight, Qt.darkBlue)
        palette.setColor(QPalette.HighlightedText, Qt.white)
        self.way_point_list.setPalette(palette)

    # #########################################################################################
    #  시그널 및 테이블 버튼 처리
    # #########################################################################################
    @pyqtSlot(str)
    def btn_clicked(self, value):

        # WayPoint Row Count
        row_cnt = self.way_point_list.rowCount()

        # read / mission 인 경우만 시그널 처리
        if value == "read" or value == "mission":

            if value == "read":

                click_data = (
                    "way_point", value
                )

                # 테이블 로우 초기화
                self.way_point_list.setRowCount(0)
                # WayPoint > Map Widget Send Data
                self.serial_manager.send_way_point_to_map.emit("init")

            elif value == "mission":

                # 카운트 체크 후 미설정인 경우 알림 공지
                if row_cnt < 1:

                    self.show_message("[설정오류]", "Way Point 설정 후 다시 시도하세요")
                    return False

                # 데이터 설정( "mission", "전체카운트", "웨이포인트 데이터")
                # WayPoint 설정 방법
                # 맵데이터 클릭 포인트 + 홈포인트 지정
                # (1 ~ 4)번 포인트 지정을 한 경우 홈포인트는 첫번째 포인트에 ALT: 10 으로 데이터를 만들어서 idx = 0 번으로 설정한다.
                # 그 이후에는 사용자가 선택한 WayPoint 를 순차적으로 설정한다.

                # 홈 위치 추가로 인해 전체 카운트 + 1 처리
                row_cnt = row_cnt + 1

                # 첫번째 WayPoint 값에 lat , lng 값을 가져와서 홈 포지션을 만든다.
                lat = self.way_point_list.item(0, 1).text()
                lng = self.way_point_list.item(0, 2).text()
                way_point_data = "myDrone01,0," + lat + "," + lng + ",10,0,w/" + self.get_table_column_data()

                # 데이터 셋 생성
                mission_data_set = (value, row_cnt, way_point_data)

                click_data = (
                    "way_point", mission_data_set
                )

            self.serial_manager.btn_clicked(click_data)

        else:

            send_data = value

            if value == "init":

                # 테이블 로우 초기화
                self.way_point_list.setRowCount(0)

                # 수정가능
                self.way_point_list.setEditTriggers(QAbstractItemView.AllEditTriggers)
            elif value == "delete":

                # 전체 로우 카운트 체크
                if row_cnt == 0:
                    self.show_message("[삭제오류]", "Way Point 를 먼저 설정 하셔야 합니다.")
                    return False

                # 클릭된 로우를 찾는다(currentRow 가 마지막 로우로 설정되어 사용불가)
                if len(self.way_point_list.selectedItems()) < 1:
                    self.show_message("[삭제오류]", "삭제할 로우를 선택하세요")
                    return

                # 선택된 로우 찾기
                current_row = self.way_point_list.currentRow()

                # 화면에서 로우 삭제 처리
                self.way_point_list.removeRow(current_row)

                # 첫번째 로우가 첫번째로 아닌 경우 삭제 로우 - 1 번째로 보내진다.
                selected_row = 0 if current_row == 0 else current_row - 1

                # Numbering 재정의
                for i in range(row_cnt-1):
                    self.way_point_list.selectRow(selected_row)
                    self.way_point_list.setItem(i, 0, QTableWidgetItem(str(1+i)))

                # 테이블에 컬럼별 데이터 추출
                send_data += "-"+self.get_table_column_data()

            elif value == "save":

                # 테이블에 컬럼별 데이터 추출
                send_data += "-"+self.get_table_column_data()

                # 저장 가능 여부 판단.
                if send_data.split("-")[1] == "empty":
                    self.show_message("[저장오류]", "저장할 값이 존재 하지 않습니다.")
                    return

                # 수정불가
                self.way_point_list.setEditTriggers(QTableWidget.NoEditTriggers)

            # WayPoint > Map Widget Send Data
            self.serial_manager.send_way_point_to_map.emit(send_data)

        # 버튼 클릭 시 활성/비활성 처리
        self.btn_setting(value)

    # #########################################################################################
    #  버튼별 클릭 시 활성/비활성 처리
    # #########################################################################################
    def btn_setting(self, btn_type: str):

        if btn_type == "init":

            # Read / Init / Insert 활성화
            self.btn_read.setEnabled(True)
            self.btn_init.setEnabled(True)
            self.btn_insert.setEnabled(True)

            # 나머지 버튼 비활성화
            self.btn_delete.setEnabled(False)
            self.btn_save.setEnabled(False)
            self.btn_mission.setEnabled(False)

        elif btn_type == "insert":

            # Delete / Save 활성화
            self.btn_delete.setEnabled(True)
            self.btn_save.setEnabled(True)

            # 나머지 버튼 비활성화
            self.btn_insert.setEnabled(False)
            self.btn_read.setEnabled(False)
            self.btn_mission.setEnabled(False)

        elif btn_type == "save":

            # Mission 활성화
            self.btn_mission.setEnabled(True)

            # 나머지 버튼 비활성화
            self.btn_read.setEnabled(False)
            self.btn_insert.setEnabled(False)
            self.btn_delete.setEnabled(False)
            self.btn_save.setEnabled(False)

        elif btn_type == "read":

            # 모든 버튼 비활성화
            self.btn_read.setEnabled(True)
            self.btn_insert.setEnabled(False)
            self.btn_delete.setEnabled(False)
            self.btn_save.setEnabled(False)
            self.btn_mission.setEnabled(False)

        elif btn_type == "mission" or btn_type == "off":

            # 모든 버튼 비활성화
            self.btn_init.setEnabled(False)
            self.btn_read.setEnabled(False)
            self.btn_insert.setEnabled(False)
            self.btn_delete.setEnabled(False)
            self.btn_save.setEnabled(False)
            self.btn_mission.setEnabled(False)

    # #########################################################################################
    #  Map > Way-Point Widget 마커 데이터 전송
    # (myDrone01,0,37.386403, 126.795233,5,0,w)
    # #########################################################################################
    @pyqtSlot(str)
    def get_map_to_way_point(self, data):

        total_row = self.way_point_list.rowCount()

        map_datas = data.split(",")

        self.way_point_list.insertRow(total_row)
        self.way_point_list.setItem(total_row, 0, QTableWidgetItem(str(map_datas[1])))
        self.way_point_list.setItem(total_row, 1, QTableWidgetItem(str(map_datas[2])))
        self.way_point_list.setItem(total_row, 2, QTableWidgetItem(str(map_datas[3])))
        self.way_point_list.setItem(total_row, 3, QTableWidgetItem(str(map_datas[4])))
        self.way_point_list.setItem(total_row, 4, QTableWidgetItem(str(map_datas[5])))

        # 현재로우 selected 처리
        self.way_point_list.selectRow(int(map_datas[1]) - 1)

        # WayPoint 추가 시점에 NO/LAT/LNG 비활성화 시킨다.(수정불가처리)
        # 수정가능[item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled )]
        # 수정불가[item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled )]
        self.way_point_list.item(total_row, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.way_point_list.item(total_row, 1).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.way_point_list.item(total_row, 2).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    # #########################################################################################
    #  테이블 로우별 컬럼 데이터 수집
    # #########################################################################################
    def get_table_column_data(self):

        # 로우별 데이터 수집
        way_points = str()

        if self.way_point_list.rowCount() > 0:

            for i in range(self.way_point_list.rowCount()):

                # 컬럼별 Value 가져오기
                no = self.way_point_list.item(i, 0).text()
                lat = self.way_point_list.item(i, 1).text()
                lng = self.way_point_list.item(i, 2).text()
                alt = floor(float(self.way_point_list.item(i, 3).text()))
                hold = floor(float(self.way_point_list.item(i, 4).text()))

                way_points += "myDrone01," + no + "," + lat + "," + lng + "," + str(alt) + "," + str(hold) + "," + "w" + "/"

            return way_points
        else:
            return "empty"

    # #########################################################################################
    #  시리얼 접속 해제로 인한 UI 초기화
    # #########################################################################################
    @pyqtSlot(str)
    def get_ui_init(self, connect):

        if connect == "on":
            # 버튼 초기화 셋팅
            self.btn_setting("init")
        else:
            # 버튼 초기화 셋팅
            self.btn_setting("off")
            # 테이블 로우 초기화
            self.way_point_list.setRowCount(0)

    # #########################################################################################
    #  Mission 카운트 및 미션 데이터 전달
    #  데이터 포맷(Read 클릭 후)
    #  미션이 없는 경우 = (0, )
    #  미션이 있는 경우 = (0, lat , lon , alt, hold)
    #  미션 업로드 성공 = (100,)
    # #########################################################################################
    @pyqtSlot(tuple)
    def get_mission_data(self, mission):

        if len(mission) < 5:

            if mission[0] == 0:
                # 미션이 없거나 미션 완료인 경우
                self.btn_setting("init")

            if mission[0] == 100:
                self.btn_read.setEnabled(True)
                self.btn_init.setEnabled(True)
        else:

            # idx = 0 인 경우는 홈 또는 take-off 로 강제 셋팅이 된다.
            # 실제 way-point 설정은 1번 포인트 부터 설정됨.
            if mission[0] > 0:

                mission_data = ("myDrone01", mission[0], mission[1], mission[2], mission[3], mission[4])
                # 데이터가 존재 하는 경우 테이블 Append 시킨다.
                self.get_map_to_way_point(",".join(map(str, mission_data)))

                # Map 에 표시 한다.
                send_data = "save-" + self.get_table_column_data()
                # WayPoint > Map Widget Send Data
                self.serial_manager.send_way_point_to_map.emit(send_data)
