# -*- coding: utf-8 -*-

import time
from PyQt5.QtCore import QThread, QWaitCondition, QMutex, pyqtSignal, pyqtSlot


class SerialReadThread(QThread):

    # 시리얼 매니저로 데이터 전송 시그널 선언
    send_received_data = pyqtSignal(list)

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self, serial):

        QThread.__init__(self)

        self.cond = QWaitCondition()
        self._status = False
        self.mutex = QMutex()
        self.serial = serial

        # Payload 데이터를 제외한 패킷 Default Bytes
        self.packet_def_bytes = 8

        # Serial Read 후 패킷 정보 수집
        self.packet_data = []

        # 패킷 수집 후 나머지 패킷 수집
        self.dummy = []

    def __del__(self):
        self.wait()

    # #########################################################################################
    #   쓰레드 시작
    # #########################################################################################
    def run(self):

        buf_bytes = 1024

        while True:

            self.mutex.lock()

            if not self._status:

                # 하위 실행 안됨
                self.cond.wait(self.mutex)

            # 시리얼 수신 부분 시작
            heartbeat = self.serial.read(buf_bytes)

            if len(heartbeat) > 0:
                self.heartbeat_collection(self.dummy[0]+tuple(heartbeat) if len(self.dummy) > 0 else tuple(heartbeat))

            self.usleep(1)
            self.mutex.unlock()

    # #########################################################################################
    #   쓰레드 활성/비화성
    # #########################################################################################
    @pyqtSlot(bool)
    def set_status(self, status):
        self._status = status

        if self._status:
            self.cond.wakeAll()

    # #########################################################################################
    #   HeartBeat 데이터 패킷별 수집 처리
    #   데이터 패킷 구조
    #       Packet Start 0xFE
    #       Payload      0~255 (254)
    #       Packet Seq   0~255
    #       System ID    1~255 (1)
    #       Component ID 0~255 (1)
    #       Message ID   0~255
    #       Data         0~255 Bytes
    #       Checksum     2 Byte
    # #########################################################################################
    def heartbeat_collection(self, heartbeat):

        # 패킷 리스트 데이터만 삭제 처리
        self.packet_data.clear()

        # dummy 패킷 리스트 데이터만 삭제 처리
        self.dummy.clear()

        start_time = time.time()
        for idx, val in enumerate(heartbeat):

            # Header 비교
            if val == 254:

                # Component Id(header + 4) 인덱스가 전체 길이 보다 작거나 같은 경우를 체크 한다.
                # 마지막 패킷 정보 : 254, 19 , 39 , 1 이런 경우 dummy 로 처리 하기 위함
                # 그냥 체크시 Index Error 발생됨
                if len(heartbeat)-1 >= (idx+4):

                    # Header + System ID + Component ID 까지 비교 처리
                    if heartbeat[idx + 3] == 1 and heartbeat[idx + 4] == 1:

                        # 전체 데이터 길이 추출
                        payload_size = heartbeat[idx+1]

                        # 패킷 header 시작점
                        start_idx = idx

                        # 패킷시작 + 데이터 전체 길이 + 패킷의 기본 구성 사이즈(Payload Data 를 제외한 나머지 구성 패킷 사이즈 : 8)
                        end_idx = start_idx + self.packet_def_bytes + payload_size

                        # 해당 패킷의 전체 사이즈
                        total_size = end_idx - start_idx

                        # 해당 패킷의 사이즈와 파싱을 통해 수집된 데이터 길이가 같은지 확인한다.
                        if total_size == len(heartbeat[start_idx:end_idx]):
                            # message_id check(#0, #1, #24, #30, #42, #43, #44, #47, #73, #74, #77, #111, #253)
                            msg_id = [0, 1, 24, 30, 40, 42, 43, 44, 47, 73, 74, 77, 111, 253]
                            if heartbeat[idx+5] in msg_id:
                                self.packet_data.append(heartbeat[start_idx:end_idx])
                        else:
                            self.dummy.append(heartbeat[start_idx:end_idx])
                else:
                    self.dummy.append(heartbeat[idx:])

        if len(self.packet_data) > 0:
            self.send_received_data.emit(self.packet_data)
