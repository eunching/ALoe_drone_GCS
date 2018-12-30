# -*- coding: utf-8 -*-

import queue
from PyQt5.QtCore import QThread, QWaitCondition, QMutex, pyqtSlot


class SerialWriteThread(QThread):

    # #########################################################################################
    #   initialize
    # #########################################################################################
    def __init__(self, serial, write_queue: queue.Queue):

        QThread.__init__(self)

        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self._status = False
        self.serial = serial
        self.write_queue = write_queue

    def __del__(self):
        self.wait()

    # #########################################################################################
    #   쓰레드 시작
    # #########################################################################################
    def run(self):

        while True:

            self.mutex.lock()

            if not self._status:

                # 하위 실행 안됨
                self.cond.wait(self.mutex)

            if not self.write_queue.empty():
                self.serial.write(self.write_queue.get())

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
