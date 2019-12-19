#Author: Chen Yiwen
#Date: 2019.9.14
#Functions:
# 1.UDP control for iiwa.
# 2.Dual communication with iiwa.

import socket
import random
import time
import threading

class operator():
    def __init__(self,global_db):
        self.global_db=db
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
        # a = b"abcdefghijklmn"
        while (1):
            iiwa_sp_str=self.global_db.form_sp_Str()
            # a = 1
            rand_msg = bytes(iiwa_sp_str, encoding="utf8")
            self.send_cont(rand_msg)
            time.sleep(0.02)

    def receive_server_start(self):
        main_thread = threading.Thread(target=self.receive_thread, args=())
        main_thread.start()
        print("receive_server start!")
        pass
    def receive_thread(self):
        while True:
            print("waiting for iiwa to send......")
            # tcpCliSock, addr = self.sock.accept()
            # print("...接收到连接：", addr)
            while True:
                # data = self.sock.recv(2000)
                data, client = self.sock.recvfrom(2000)
                # data = tcpSerSock.recv(BUFSIZE)
                if not data:
                    break
                # print("Received len:",len(data))
                b_iiwaStr=data
                self.global_db.r_iiwaStr=b_iiwaStr
                self.global_db.r_iiwaFltLs=self.double_form_iiwaStr(b_iiwaStr)
                print("Received floats",self.global_db.r_iiwaFltLs[0:7])
                self.global_db.r_iiwa_x = self.global_db.r_iiwaFltLs[0]
                self.global_db.r_iiwa_y = self.global_db.r_iiwaFltLs[1]
                self.global_db.r_iiwa_z = self.global_db.r_iiwaFltLs[2]
                self.global_db.r_iiwa_a = self.global_db.r_iiwaFltLs[3]
                self.global_db.r_iiwa_b = self.global_db.r_iiwaFltLs[4]
                self.global_db.r_iiwa_g = self.global_db.r_iiwaFltLs[5]
                self.global_db.r_iiwa_o = self.global_db.r_iiwaFltLs[6]

                # tcpCliSock.send('[%s] %s' % (bytes(ctime(), 'utf-8'), data))
        # while (1):
        #     print("receive:xxx")
        #     time.sleep(3)
        # pass

    @staticmethod
    def double_form_iiwaStr(iiwaStr):
        # biiwaStr
        # b'676.57 9.585 346.26 -0.812 0.056 -1.938 -1.820943008789028 0.951437234630967
        # -1.2420446115938124 -0.49187084033991807 0.3434830777047593 -0.20235079319058677
        # 5 0 -0.3725457495649514 0.5545085277649828 9.734785513046563E-4 -1.712037246399895
        # -1.639705905758684 -1.0333378738451222 -1.127784651313801\x00'

        # print(type(iiwaStr))
        # print(iiwaStr)
        # iiwaStr=str(iiwaStr,encoding="utf8")
        # iiwaStr=iiwaStr.strip("\\x00")

        iiwaStr=iiwaStr.decode('UTF-8', 'ignore').strip().strip(b'\x00'.decode())
        # print(iiwaStr)
        float_list=iiwaStr.split(" ")
        # print(float_list)
        for i in range(len(float_list)):
            float_list[i]=float(float_list[i])
        return float_list

class global_database():
    # this database is shared with iiwa through udp
    def __init__(self):
        #iiwaStr
        self.r_iiwaStr=""
        self.r_iiwaFltLs=[]
        #_iiwa_xx == estimation
        self._iiwa_x=706.57;
        self._iiwa_y=4.58;
        self._iiwa_z=376.26;
        self._iiwa_a=-0.812;
        self._iiwa_b=0.056;
        self._iiwa_g=-1.938;
        self._iiwa_o=255;

        #iiwa_xx_sp == setpoint
        self.iiwa_x_sp=706.57;
        self.iiwa_y_sp=4.58;
        self.iiwa_z_sp=376.26;
        self.iiwa_a_sp=-0.812;
        self.iiwa_b_sp=0.056;
        self.iiwa_g_sp=-1.938;
        self.iiwa_o_sp=255;

        #v_iiwa_xx == from camera

        #r_iiwa_xx == read from iiwa
        self.r_iiwa_x=706.57;
        self.r_iiwa_y=4.58;
        self.r_iiwa_z=376.26;
        self.r_iiwa_a=-0.812;
        self.r_iiwa_b=0.056;
        self.r_iiwa_g=-1.938;
        self.r_iiwa_o=255;

        ##safe_iiwa_xx == safe position
        self.safe_iiwa_x=706.57;
        self.safe_iiwa_y=4.58;
        self.safe_iiwa_z=376.26;
        self.safe_iiwa_a=-0.812;
        self.safe_iiwa_b=0.056;
        self.safe_iiwa_g=-1.938;
        self.safe_iiwa_o=100;
    def form_sp_Str(self):
        sendStr=str(self.iiwa_x_sp)+" "+str(self.iiwa_y_sp)+" "+str(self.iiwa_z_sp)+" "+str(self.iiwa_a_sp)+" "+str(self.iiwa_b_sp)+" "+str(self.iiwa_g_sp)+" "+str(self.iiwa_o_sp)

        return sendStr
class controller():
    def __init__(self):
        pass
    def u_x(self):
        # u_x=random.randint(-50,50)
        # u_x=100
        return u_x
    def u_y(self):
        u_y = random.randint(-50, 50)
        # u_x=100
        return u_y
    def u_z(self):
        u_z=random.randint(-50,50)
        # u_x=100
        return u_z
    def u_o(self):
        u_o=random.randint(-50,50)
        # u_x=100
        return u_o

    def line_path_planer(self,read_value,safe_value,u):

        if(read_value<(safe_value+80) and read_value>(safe_value-80)):
            pass
        elif(read_value>(safe_value+80)):

            u =-3
        elif(read_value<(safe_value-80)):
            u = 3
        else:
            pass
        print("direction:",u)
        # sp_value=read_value+x_direction
        return u


if __name__=="__main__":
    db = global_database()
    operator = operator(db)
    operator.send_server_start()
    operator.receive_server_start()
    ct=controller()
    print(db.form_sp_Str())

    x_direction=3
    y_direction=3
    z_direction=3
    direction=3
    u=3
    while(1):
        #
        # if(db.r_iiwa_x<(db.safe_iiwa_x+80) and db.r_iiwa_x>(db.safe_iiwa_x-80)):
        #     pass
        # elif(db.r_iiwa_x>(db.safe_iiwa_x+80)):
        #     x_direction =-3
        # elif(db.r_iiwa_x<(db.safe_iiwa_x-80)):
        #     x_direction = 3
        # else:
        #     pass
        # print("x direction:",x_direction)
        # db.iiwa_x_sp = db.r_iiwa_x + x_direction
        # u=ct.line_path_planer(db.r_iiwa_y,db.safe_iiwa_y,u=u)
        # db.iiwa_y_sp = db.r_iiwa_y+u
        u=ct.line_path_planer(db.r_iiwa_z,db.safe_iiwa_z,u=u)
        db.iiwa_z_sp = db.r_iiwa_z+u

        # if(db.r_iiwa_x<(db.safe_iiwa_y+80) and db.r_iiwa_x>(db.safe_iiwa_y-80)):
        #     pass
        # elif(db.r_iiwa_x>(db.safe_iiwa_x+80)):
        #     x_direction =-3
        # elif(db.r_iiwa_x<(db.safe_iiwa_x-80)):
        #     x_direction = 3
        # else:
        #     pass
        # print("x direction:",x_direction)
        # db.iiwa_x_sp = db.r_iiwa_x + x_direction


        # db.iiwa_y_sp = ct.u_y() + db.safe_iiwa_y
        # db.iiwa_z_sp=ct.u_z()+db.safe_iiwa_z
        # db.iiwa_o_sp=ct.u_o()+db.safe_iiwa_o
        # print(db.r_iiwaFltLs)
        time.sleep(0.02)
        # print(db.__dict__)

