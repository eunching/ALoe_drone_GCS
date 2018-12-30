# -*- coding: utf-8 -*-

import serial as pyserial
import threading
from PyQt5.QtCore import pyqtSlot, QObject
from GCS.Serial.SerialReadThread import *
from GCS.Serial.SerialWriteThread import *
from GCS.Serial.SerialConfig import SerialConfig
from GCS.Serial.SerialMessage import *


class SerialManager(QObject):

    # #########################################################################################
    # Signal 모음
    # 1. HudModule 시그널 전송(ATTITUDE + VRF_HUD 데이터)
    # 2. StatusModule  시그널 전송(SYS_STATUS 데이터)
    # 3. Way point Widget  > Map Widget 시그널 전송 (Init,Insert,Delete,Save)
    # 4. Map Widget  > Way point Widget 시그널 전송 (Marker 생성 후 좌표 전달)
    # 5. DroneModule(접속 및 Flight) 시그널 전송 (Heartbeat + TopWidget 시리얼 정보 전달)
    # 6. GpsModule 시그널 전송(GPS_RAW_INT 데이터)
    # 7. 모든 Widget UI 데이터 전달(시리얼 접속 및 접속 해제 처리)
    # 8. LogModule 시그널 전송(STATUSTEXT + COMMAND_ACK 데이터)
    # 9. WaypointModule 시그널 전송(MISSION COUNT(0 or N) OR MISSION 데이터)
    # 10.드론 위치(GPS_RAW_INT) 및 방향 (VFR_HUD) 와 Home 위치 (Mission_item_int(seq=0)를 Map widget으로 시그널 전송
    # #########################################################################################

    send_hud_data = pyqtSignal(dict)
    send_status_data = pyqtSignal(dict)
    send_way_point_to_map = pyqtSignal(str)
    send_map_to_way_point = pyqtSignal(str)
    send_drone_data = pyqtSignal(dict)
    send_gps_data = pyqtSignal(dict)
    send_ui_init = pyqtSignal(str)
    send_log_data = pyqtSignal(str)
    send_mission_data = pyqtSignal(tuple)
    send_map_data = pyqtSignal(dict)

    __instance = None

    @classmethod
    def __get_instance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__get_instance
        return cls.__instance

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self):

        super().__init__()

        # 시리얼 인스턴스 생성
        self.serial = pyserial.Serial()

        # 시리얼 Read 스레드 인스턴스 생성 및 시작
        self.serial_read = SerialReadThread(self.serial)
        self.serial_read.send_received_data.connect(self.get_received_data)
        self.serial_read.start()

        # COMMAND 명령에 수집 큐(FIFO)
        self.write_queue = queue.Queue()

        # 시리얼 Write 쓰레드 인스턴스 생성 및 시작
        self.serial_write = SerialWriteThread(self.serial, self.write_queue)
        self.serial_write.start()

        # mav 인스턴스
        self.mav = MAVLink(self, srcSystem=255, srcComponent=0, use_native=False)

        # Message Pack 모음
        self.mav_msg = SerialMessage(mav=self.mav)
        self.mav_msg = SerialMessage(mav=self.mav)

        # mission count( Way-Point Read 요청시 전체 카운트)
        self.mission_count = 0

        # mission 처리시 설정하는 WayPoint List
        self.mission_way_point = []
    # #########################################################################################
    #    모든 버튼 시그널(예시)
    #    Data >> 1. 시리얼 연결 클릭 시 ('serial',('port 명' , 'baudrate', 'open/close'))
    #            2. 드론 컨트롤 클릭 시 ('control','arm')
    #            3. way-point 클릭 시 ('way_point','read')
    # #########################################################################################
    def btn_clicked(self, data):

        # 데이터 설정
        flag, value = data

        if flag == "serial":

            '''
            # Drone Widget 데이터 패킷 전송 처리
            # Drone Widget 으로 보내지는 데이터 패킷 정보는 두가지로 나뉜다
            # 1. 시리얼 Read(HeartBeat) 후 처리 (Flight Controller, Flight Status, Flight Speed)
            # 2. 시리얼 접속 후 처리(PortName, BaudRate, on/off)
            # 전체 데이터 패킷
            SEND_DRONE_DATA{"controller":"N/A","status":"N/A","speed":"N/A","port":"N/A","baud":"N/A","icon":"N/A"}

            '''
            # 전송 기본 패킷 불러온다.
            drone_data = SerialConfig.get_send_drone_data()

            # 시리얼 접속
            port_name, baud_rate, connect_flag = value

            try:
                # 시리얼 접속 해제 인 경우
                if connect_flag == "close":

                    # 시리얼 접속 해제
                    self.disconnect_serial()

                    # 시리얼 접속 유무 전달(on : 위젯 활성화 , off : 위젯 초기화)
                    self.send_ui_init.emit("off")
                    return

                else:
                    # 시리얼 접속 인 경우
                    if self.connect_serial(port_name, baud_rate):

                        drone_data['port'] = port_name
                        drone_data['baud'] = baud_rate
                        drone_data['icon'] = "ON"

                        # Drone Widget 패킷 전송
                        self.send_drone_data.emit(drone_data)

                        # 시리얼 접속 유무 전달(on : 위젯 활성화 , off : 위젯 초기화)
                        self.send_ui_init.emit("on")

                        # param 0:off, 1:on( 모든 메시지 수신 요청)
                        write_data = self.mav_msg.data_stream_auto_buf(1)
                        self.write_queue.put(write_data)


            except Exception as error:
                print("[error]Serial Connect Error >> {} ".format(str(error)))

        elif flag == "control":

            if value == "take_off":

                self.write_queue.put(self.mav_msg.set_mode_stabilze())
                # Arming 명령어 수집
                self.write_queue.put(self.mav_msg.button_arm_disarm(1))
                time.sleep(1)
                # Guided 명령어 수집
                self.write_queue.put(self.mav_msg.set_mode_guided())
                time.sleep(1)
                # Take Off 명령어 수집
                self.write_queue.put(self.mav_msg.cmd_nav_takeoff())

            elif value == "landing":
                self.write_queue.put(self.mav_msg.set_mode_land())

            elif value == "flight_start":
                self.write_queue.put(self.mav_msg.set_mode_auto())

            elif value == "rtl":
                self.write_queue.put(self.mav_msg.set_mode_rtl())

            elif value == "arming":
                self.write_queue.put(self.mav_msg.button_arm_disarm(1))

            elif value == "dis_arming":
                self.write_queue.put(self.mav_msg.button_arm_disarm(0))

        elif flag == "way_point":

            # WayPoint Read
            if value == "read":
                self.write_queue.put(self.mav_msg.mission_request_list_pack())

            else:

                # WayPoint Mission
                count = value[1]
                waypoints = value[2].split("/")

                print("mission count : "+str(count) + " : waypoints : " + str(waypoints))
                # 설정하려는 WayPoint 를 리스트에 담는다.
                for point in waypoints:
                    if len(point) > 0:
                        self.mission_way_point.append(point)

                print("self.mission_way_point size :: " + str(len(self.mission_way_point)))
                # 초기 미션 카운트를 FC 로 전달한다.
                self.write_queue.put(self.mav_msg.mission_count_pack(count))

        else:
            pass

    # #########################################################################################
    #   SerialReadThread 에서 들어오는 데이터
    # #########################################################################################
    @pyqtSlot(list)
    def get_received_data(self, heartbeat):

        for data in heartbeat:

            read_data = self.mav.decode((bytearray)(data))

            # HEARTBEAT ( #0: type, autopilot, base_mode, custom_mode, system_status, mavlink_version)
            if read_data.name == "HEARTBEAT":

                # HEARTBEAT 기본 패킷 불러온다.
                drone_data = SerialConfig.get_send_drone_data()
                drone_data['controller'] = enums['MAV_AUTOPILOT'][read_data.autopilot].name.replace("MAV_AUTOPILOT_", "")
                drone_data['type'] = enums['MAV_TYPE'][read_data.type].name.replace("MAV_TYPE_", "")
                drone_data['status'] = enums['MAV_STATE'][read_data.system_status].name.replace("MAV_STATE_", "")

                self.send_drone_data.emit(drone_data)

                # STATUS 기본 패킷 구성
                status_data = SerialConfig.get_send_status_data()
                status_data["mode"] = self.mav_msg.get_cust_mode(read_data.custom_mode)
                status_data["arming"] = "ON" if read_data.base_mode & 128 == 1 else "OFF"
                self.send_status_data.emit(status_data)

            # SYS_STATUS(#1)
            # onboard_control_sensors_present, onboard_control_sensors_enabled, onboard_control_sensors_health, load,
            # voltage_battery, current_battery, battery_remaining, drop_rate_comm, errors_comm,
            #  errors_count1, errors_count2, errors_count3, errors_count4

            if read_data.name == "SYS_STATUS":

                status_data = SerialConfig.get_send_status_data()
                status_data["battery_volt"] = read_data.voltage_battery
                status_data["battery_remain"] = read_data.battery_remaining

                self.send_status_data.emit(status_data)

            # GPS_RAW_INT ( #24: time_usec, fix_type, lat, lon, alt, eph, epv, vel, cog, satellites_visible)
            if read_data.name == "GPS_RAW_INT":

                gps_data = SerialConfig.get_send_gps_data()

                gps_data["fix"] = enums['GPS_FIX_TYPE'][read_data.fix_type].name.replace("GPS_FIX_TYPE_", "")
                gps_data["count"] = read_data.satellites_visible
                gps_data["alt"] = read_data.alt
                gps_data["lat"] = read_data.lat
                gps_data["lng"] = read_data.lon
                gps_data["hdop"] = read_data.eph
                gps_data["vdop"] = read_data.epv

                self.send_gps_data.emit(gps_data)

                # drone의 GPS 위치 데이터를 map_widget (google map) 으로 시그널 전송
                map_data = SerialConfig.get_send_map_data()

                map_data["type"] = 'drone'
                map_data["lat"] = read_data.lat / 10000000
                map_data["lon"] = read_data.lon / 10000000

                self.send_map_data.emit(map_data)


            # ATTITUDE ( #30: time_boot_ms, roll, pitch, yaw, rollspeed, pitchspeed, yawspeed)
            if read_data.name == "ATTITUDE":

                hud_data = SerialConfig.get_send_hud_data()
                hud_data["roll"] = 180/3.141593 * read_data.roll
                hud_data["pitch"] = 180/3.141593 * read_data.pitch

                self.send_hud_data.emit(hud_data)

            # MISSION_REQUEST ( #40: target_system, target_component, seq)
            if read_data.name == "MISSION_REQUEST":

                print("MISSION_REQUEST :: " + str(read_data.seq))
                # (myDrone01,0,37.386403, 126.795233,5,0,w)
                way_points = self.mission_way_point[read_data.seq].split(",")

                seq = int(way_points[1])
                lat = float(way_points[2])
                lon = float(way_points[3])
                alt = float(way_points[4])
                hold = float(way_points[5])

                if read_data.seq == 0:
                    # take-off
                    command = MAV_CMD_NAV_TAKEOFF
                else:
                    command = MAV_CMD_NAV_WAYPOINT

                self.write_queue.put(self.mav_msg.mission_item_pack(seq, MAV_FRAME_GLOBAL_RELATIVE_ALT, command,
                                                                    0, 1, hold, 0.0, 0.0, 0.0, lat, lon, alt))

            # MISSION_CURRENT(# 42: seq )
            if read_data.name == "MISSION_CURRENT":

                # STATUS 기본 패킷 구성
                status_data = SerialConfig.get_send_status_data()
                status_data["current_mission"] = read_data.seq
                self.send_status_data.emit(status_data)

            # MISSION_COUNT ( #44: target_system, target_component, count)
            if read_data.name == "MISSION_COUNT":

                self.mission_count = read_data.count

                if self.mission_count < 1:
                    # FC 에 Way-Point 가 존재 하지 않는 경우
                    data = (0,)
                    self.send_mission_data.emit(data)
                else:
                    # 미션 카운트가 존재 하기 때문에 첫번째 way-point 를 요청한다.
                    self.write_queue.put(self.mav_msg.missin_request_int_pack(0))

            # MISSION_ACK ( #47: target_system, target_component, type)
            # MAV_MISSION_RESULT  =  https://mavlink.io/en/messages/common.html#MAV_MISSION_RESULT
            if read_data.name == "MISSION_ACK":

                print("mission_ack : {}".format(str(read_data.type)))

                if read_data.type == MAV_MISSION_ACCEPTED:
                    # 모든 미션이 등록되었다면 리스트 초기화 시킨다.
                    self.mission_way_point.clear()

                    # 미션 완료 이벤트를 WaypointModule 로 전달한다.
                    data = (100,)
                    self.send_mission_data.emit(data)

            # MISSION_ITEM_INT(  # 73 )
            if read_data.name == "MISSION_ITEM_INT":
                if read_data.seq == 0:
                    print(read_data.x)
                    print(read_data.y)
                    print(read_data.z)

                # 웨이포인트 READ시 맵에 홈 위치 전송
                # 보내준 데이터를 기반으로 홈 위치 표시 및 이동
                # seq == 0 의 미션 데이터는 기본적으로 홈으로 설정된다.
                if read_data.seq == 0:
                    # home 위치의 데이터 시그널 구성 및 전송
                    map_data = SerialConfig.get_send_map_data()

                    map_data["type"] = 'home'
                    map_data["lat"] = read_data.x / 10000000
                    map_data["lon"] = read_data.y / 10000000

                    self.send_map_data.emit(map_data)

                if read_data.seq <= self.mission_count - 1:
                    data = (read_data.seq, read_data.x / 10000000, read_data.y / 10000000,
                            int(read_data.z), int(read_data.param1))
                    self.send_mission_data.emit(data)

                    # 마지막 미션을 받았다면 미션 카운트 다시 초기화
                    if read_data.seq == self.mission_count - 1:
                        self.mission_count = 0
                    else:
                        # 다음 MISSION 요청
                        self.write_queue.put(self.mav_msg.missin_request_int_pack(read_data.seq+1))

            # VFR_HUD ( #74: airspeed, groundspeed, heading, throttle, alt, climb)
            if read_data.name == "VFR_HUD":

                # HUD 기초 데이터 수집
                hud_data = SerialConfig.get_send_hud_data()
                hud_data["heading"] = read_data.heading

                self.send_hud_data.emit(hud_data)

                # drone의 heading 데이터를 map_widget (google map) 으로 시그널 전송
                map_data = SerialConfig.get_send_map_data()

                map_data["type"] = 'drone'
                map_data["heading"] = read_data.heading

                self.send_map_data.emit(map_data)


            # COMMAND_ACK(#77: command, result)
            if read_data.name == "COMMAND_ACK":
                self.send_log_data.emit("command >> {} : result >> {}"
                                        .format(str(read_data.command), str(read_data.result)))

            # TIMESYNC ( #111: tc1, ts1)
            if read_data.name == "TIMESYNC":
                pass

            # STATUSTEXT ( #253: severity, text)
            if read_data.name == "STATUSTEXT":
                self.send_log_data.emit(str(read_data.text))

    # #########################################################################################
    #  시리얼 Config 설정 및 연결 처리
    # #########################################################################################
    def connect_serial(self, port_name, baud_rate):

        serial_info = SerialConfig.get_serial_info()

        serial_info["port_name"] = port_name
        serial_info["baud_rate"] = baud_rate
        serial_info["data_bits"] = SerialConfig.DATABITS[3]
        serial_info["parity"] = SerialConfig.PARITY[0]
        serial_info["stop_bits"] = SerialConfig.STOPBITS[0]

        status = self._open(**serial_info)

        if status:
            # 접속 처리 후 Read/Write 쓰레드 기동
            self.serial_read.set_status(status)
            self.serial_write.set_status(status)

        return status

    # #########################################################################################
    #  시러얼 접속 해제 처리
    # #########################################################################################
    def disconnect_serial(self):

        status = False
        # 접속 처리 후 Read/Write 쓰레드 기동
        self.serial_read.set_status(status)
        self.serial_write.set_status(status)

        return self.serial.close()

    # #########################################################################################
    #  시리얼 접속 처리
    # #########################################################################################
    def _open(self, port_name, baud_rate, data_bits, parity, stop_bits, timeout, write_timeout, xonxoff, rtscts, dsrdtr):

        self.serial.port = port_name
        self.serial.baudrate = baud_rate
        self.serial.bytesize = data_bits
        self.serial.parity = parity
        self.serial.stopbits = stop_bits
        self.serial.timeout = timeout
        self.serial.write_timeout = write_timeout
        self.serial.xonxoff = xonxoff
        self.serial.rtscts = rtscts
        self.serial.dsrdtr = dsrdtr

        self.serial.open()

        # isOpen 으로 연결상태 확인
        return self.serial.isOpen()
