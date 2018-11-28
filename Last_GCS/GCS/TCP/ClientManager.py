


from PyQt5.QtCore import pyqtSlot, QObject
from GCS.TCP.ClientReadThread import *
from GCS.TCP.ClientWriteThread import *
from GCS.Serial.SerialMessage import *
from GCS.Serial.SerialManager import *
import socket

class ClientManager(QObject):

    def __init__(self, ip, port):
        super().__init__()

        self.ip = ip
        self.port = port

        # 소켓 생성
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.connect((self.ip, self.port))

        except socket.error as e:
            print("tcp 연결 실패" + e)


    def send_tcp_data(self):
        #print("send_tcp_data >> {}".format(data))
        try:
            self.socket.send(b'0')
            print("send data ")
        except socket.error as e:
            print("client manager send error ::::: " + e)
    # #########################################################################################
    #  TCP Client 접속 해제 처리
    # #########################################################################################


    def disConnectClient(self):

        # 소켓을 닫는것에 앞서 셧다운을 함으로서 기존 데이터 송 수신 차단
        self.socket.shutdown(socket.SHUT_RDWR)

        # 소켓 접속 해제
        self.close()
