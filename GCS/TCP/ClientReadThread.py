# -*- coding: utf-8 -*-

import time
from PyQt5.QtCore import QThread, QWaitCondition, QMutex, pyqtSignal, pyqtSlot
import socket

class ClientReadThread(QThread):

    # 시리얼 매니저로 데이터 전송 시그널 선언
    send_received_data = pyqtSignal(list)

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self, socket):

        QThread.__init__(self)

        self.cond = QWaitCondition()
        self._status = False
        self.mutex = QMutex()
        self.socket = socket

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
                data = self.socket.recv(buf_bytes)

            if len(data) > 0:
                print(data)

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
