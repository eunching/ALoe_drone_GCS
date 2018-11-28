# -*- coding: utf-8 -*-

from pymavlink.dialects.v10.ardupilotmega import *


class SerialMessage:

    # mav-link 객체 선언
    def __init__(self, systemid=1, compid=1, mav=None):
        self.mav = mav
        self.systemId = systemid
        self.compId = compid

    # dataStreamAuto 메시지로 현재 보낼수 있는 메시지를 다 보내달라고 요청
    # start 1 은 On , 0 은 off
    # Fc에 전원이 계속 들어가고 있는 이상 계속 유지된다.
    def data_stream_auto_buf(self, start):
        data = self.mav.request_data_stream_encode(self.systemId, self.compId, MAV_DATA_STREAM_ALL, 1, 1)
        return data.pack(self.mav)


    # send Heartbeat 현재 GCS의 하트비트 메시지 전송
    # Type = MAV_TYPE_GCS 로 기본설정

    def heartbeat_buf(self, autopilot, base_mode, custom_mode, sys_status, type = MAV_TYPE_GCS):
        data = self.mav.heartbeat_encode(type, autopilot, base_mode, custom_mode, sys_status)
        return data.pack(self.mav)

    def cmd_long_buf(self, cmd, param1=0, param2=0, param3=0, param4=0, param5=0, param6=0, param7=0):
        data = self.mav.command_long_encode(1, 1, cmd, 0, param1, param2, param3, param4, param5, param6, param7)
        return data.pack(self.mav)

    # 미션 메시지 (READ)
    def mission_request_list_pack(self):
        data = self.mav.mission_request_list_encode(self.systemId, self.compId)
        return data.pack(self.mav)


    def missin_request_int_pack(self, seq):
        data = self.mav.mission_request_int_encode(self.systemId, self.compId, seq)
        return data.pack(self.mav)

    # 마지막 최종 seq의 Mission까지 다 받았다면 보내주는 메시지
    # 단 꼭 보낼 필요는 없다. 굳이 보내지 않아도 큰 영향은 없다.
    def mission_ack_pack(self, result):
        data = self.mav.mission_ack_encode(self.systemId, self.compId, result)
        return data.pack(self.mav)

    # 미션 메시지 (WRITE)
    def mission_count_pack(self, count):
        data = self.mav.mission_count_encode(self.systemId, self.compId, count)
        return data.pack(self.mav)

    #def button_ip_address(self, ):

    def mission_item_int_pack(self, seq, frame, command, current, autocontinue, param1, param2, param3, param4,
                              x, y, z):
        data = self.mav.mission_item_int_encode(self.systemId, self.compId, seq, frame, command, current, autocontinue,
                                            param1, param2, param3, param4, x, y, z)
        return data.pack(self.mav)

    def mission_item_pack(self, seq, frame, command, current, autocontinue, param1, param2, param3, param4,
                              x, y, z):
        data = self.mav.mission_item_encode(self.systemId, self.compId, seq, frame, command, current, autocontinue,
                                            param1, param2, param3, param4, x, y, z)
        return data.pack(self.mav)

    # 현재 진행중인 미션의 순서 수정
    def mission_set_current_pack(self, seq):
        data = self.mav.mission_set_current_encode(self.systemId, self.compId, seq)
        return data.pack(self.mav)

    ''' 
      base_mode는 1로 맞춘후 custom_mode를 조정해서 모드변경이 가능하다
      https://github.com/ArduPilot/ardupilot/blob/master/ArduCopter/defines.h#L34 참고

       STABILIZE =     0,  // manual airframe angle with manual throttle
       ACRO =          1,  // manual body-frame angular rate with manual throttle
       ALT_HOLD =      2,  // manual airframe angle with automatic throttle
       AUTO =          3,  // fully automatic waypoint control using mission commands
       GUIDED =        4,  // fully automatic fly to coordinate or fly at velocity/direction using GCS immediate commands
       LOITER =        5,  // automatic horizontal acceleration with automatic throttle
       RTL =           6,  // automatic return to launching point
       CIRCLE =        7,  // automatic circular flight with automatic throttle
       LAND =          9,  // automatic landing with horizontal position control
       DRIFT =        11,  // semi-automous posidion, yaw and throttle control
       SPORT =        13,  // manual earth-frame angular rate control with manual throttle
       FLIP =         14,  // automatically flip the vehicle on the roll axis
       AUTOTUNE =     15,  // automatically tune the vehicle's roll and pitch gains
       POSHOLD =      16,  // automatic position hold with manual override, with automatic throttle
       BRAKE =        17,  // full-brake using inertial/GPS system, no pilot input
       THROW =        18,  // throw to launch mode using inertial/GPS system, no pilot input
       AVOID_ADSB =   19,  // automatic avoidance of obstacles in the macro scale - e.g. full-sized aircraft
       GUIDED_NOGPS = 20,  // guided mode but only accepts attitude and altitude
       SMART_RTL =    21,  // SMART_RTL returns to home by retracing its steps
       FLOWHOLD  =    22,  // FLOWHOLD holds position with optical flow without rangefinder
       FOLLOW    =    23,  // follow attempts to follow another vehicle or ground station
       ZIGZAG    =    24,  // ZIGZAG mode is able to fly in a zigzag manner with predefined point A and point B
       '''

    # FC의 모드는 Base_mode 로 상태를 확인한후
    #  custom_mode의 값으로 전환이 이루어진다.
    ## 위의 값은 Apm firmware 기반의 모드 전환에 관련된 값들을 정리해둔것이다.

    def set_mode_buf(self, custom_mode):
        data = self.mav.set_mode_encode(1, 1, custom_mode)
        return data.pack(self.mav)

    ########################################################################################
    #  SET_MODE 명령어
    ########################################################################################

    def set_mode_stabilze(self):
        data = self.set_mode_buf(0)
        return data

    def set_mode_guided(self):
        data = self.set_mode_buf(2)
        return data

    def set_mode_auto(self):
        data = self.set_mode_buf(3)
        return data

    def set_mode_rtl(self):
        data = self.set_mode_buf(6)
        return data


    def set_mode_land(self):
        data = self.set_mode_buf(9)
        return data
    ########################################################################################
    #  COMMAND_LONG 분기
    ########################################################################################
    # Nav Take off (cmd : 22)
    def cmd_nav_takeoff(self, height=10):
        data = self.cmd_long_buf(22, param7=height)
        return data

    # GET_HOME_POSITION (CMD : 410) (APM 계열 펌웨어에서는 미지원  요청시 result 4 (Unsupported 확인)
    def cmd_get_home_position(self):
        data = self.cmd_long_buf(410)
        return data

    ########################################################################################
    # BUTTON COMMAND
    ########################################################################################
    # power(param1) 1일시 ON / 0 일시 off
    def button_arm_disarm(self, power):
        data = self.cmd_long_buf(cmd=MAV_CMD_COMPONENT_ARM_DISARM, param1=power)
        return data

    ########################################################################################
    # BUTTON COMMAND
    ########################################################################################
    def get_cust_mode(self, idx):

        modes = ("STABILIZE", "ACRO", "ALT_HOLD", "AUTO", "GUIDED", "LOITER", "RTL", "CIRCLE","","LAND", "N/A",
                 "DRIFT", "", "SPORT", "FLIP", "AUTOTUNE", "POSHOLD", "BRAKE", "THROW", "AVOID_ADSB", "GUIDED_NOGPS",
                 "SMART_RTL", "FLOWHOLD", "FOLLOW", "ZIGZAG")

        return modes[idx]
