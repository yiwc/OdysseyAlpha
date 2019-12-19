# References
# ----------
# https://wiki.python.org/moin/UdpCommunication

import socket
import random
import time
import threading

class operator():
    def __init__(self):
        self.iiwa_ip="172.31.1.147"
        self.iiwa_port=30009
        self.sock=socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        self.my_address=("172.31.1.40",12358)
        # self.sock.bind(self.my_address)
        pass
    def send_cont(self,MESSAGE=b'123456789'):
        UDP_IP = self.iiwa_ip
        UDP_PORT = self.iiwa_port
        # MESSAGE = b'Hello, World!'
        # MESSAGE = b'123456789'

        #print("UDP target IP:", UDP_IP)
        #print("UDP target port:", UDP_PORT)
        print("send message:", MESSAGE)

        # sock = socket.socket(socket.AF_INET, # Internet
        #                      socket.SOCK_DGRAM) # UDP
        self.sock.sendto(MESSAGE, (self.iiwa_ip, self.iiwa_port))

    def send_server_start(self):
        main_thread=threading.Thread(target=self.send_thread, args=())
        main_thread.start()
        print("send_server start!")
    def send_thread(self):
        a = b"abcdefghijklmn"
        while (1):
            # a = 1
            rand_msg = bytes(str(a), encoding="utf8")
            self.send_cont(rand_msg)
            time.sleep(3)

    def receive_server_start(self):
        main_thread = threading.Thread(target=self.receive_thread, args=())
        main_thread.start()
        print("receive_server start!")
        pass
    def receive_thread(self):
        while True:
            print("等待连接......")
            # tcpCliSock, addr = self.sock.accept()
            # print("...接收到连接：", addr)
            while True:
                # data = self.sock.recv(2000)
                data, client = self.sock.recvfrom(2000)

                # data = tcpSerSock.recv(BUFSIZE)
                if not data:
                    break
                print("Received:",data)
                # tcpCliSock.send('[%s] %s' % (bytes(ctime(), 'utf-8'), data))
        # while (1):
        #     print("receive:xxx")
        #     time.sleep(3)

        # pass


if __name__=="__main__":
    operator = operator()
    operator.send_server_start()
    operator.receive_server_start()

    # a = b"abcdefghijklmn"
    # while(1):
    # # a = 1
    #     rand_msg=bytes(str(a), encoding="utf8")
    #     operator.send_cont(rand_msg)
    #     time.sleep(3)

        # a=a+1
        # if(a>100):
        #     a=4