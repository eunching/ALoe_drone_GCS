


from PyQt5.QtCore import pyqtSlot, QObject
from GCS.TCP.ClientReadThread import *
from GCS.TCP.ClientWriteThread import *
from GCS.Serial.SerialMessage import *
from GCS.Serial.SerialManager import *
import socket

class ClientManager(QObject):

    # 인스턴스 메소드 생성

    __instance = None

    @classmethod
    def __get_instance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__get_instance
        return cls.__instance



    def __init__(self):
        super().__init__()

        # 시리얼 매니저 인스턴스 가져오기
        self.serial_manager = SerialManager.instance()

        # 소켓 생성
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # 시리얼 Read 스레드 인스턴스 생성 및 시작
        self.client_read = ClientReadThread(self.socket)
        self.client_read.send_received_data.connect(self.get_received_data)
        self.client_read.start()

        # COMMAND 명령에 수집 큐(FIFO)
        self.write_queue = queue.Queue()

        # 시리얼 Write 쓰레드 인스턴스 생성 및 시작
        self.client_write = ClientWriteThread(self.socket, self.write_queue)
        self.client_write.start()


    # #########################################################################################
    #  TCP Client 접속  처리
    # #########################################################################################

    def connectClient(self,ip,port):

        # Python socket은 반환값으로 상태를 확인하는것이 아닌 Exception 을 발생시킨다고 하여
        # try - except 구조로 상태를 확인하도록 수정

        try:
            self.socket.connect((ip, port))

        except socket.error as e:
            print("tcp 연결 실패" + e)

        finally:
            # 정상적으로 접속 된다면 Read/Write 쓰레드 기동
            self.client_read.set_status(True)
            self.client_write.set_status(True)


    # #########################################################################################
    #  TCP Client 접속 해제 처리
    # #########################################################################################


    def disConnectClient(self):

        # 소켓을 닫는것에 앞서 셧다운을 함으로서 기존 데이터 송 수신 차단
        self.socket.shutdown(socket.SHUT_RDWR)

        # 소켓 접속 해제
        self.close()

        # Read/Write 스레드 동작 정지
        self.client_read.set_status(False)
        self.client_write.set_status(False)

    @pyqtSlot(list)
    def get_received_data(self, data):
        print(data)
