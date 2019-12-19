#Author: Chen Yiwen
#Date: 2019.9.14
#Functions:
# 1.UDP control for iiwa.
# 2.Dual communication with iiwa.

import socket
import random
import time
import threading
class funcs():
    @staticmethod
    def clamp(input,min,max):
        if(input>0):
            if(input>max):
                input=max
            elif(input<min):
                input=min
        if(input<0):
            if(input>-min):
                input=-min
            elif(input<-max):
                input=-max

        return input

    @staticmethod
    def check_xyzabg_same(list_a,list_b,xyz_single_error,abg_single_error):
        for i in range(3):
            a=list_a[i]
            b=list_b[i]
            if(abs(a-b)>(xyz_single_error)):
                # print("xyz not ready",list_a,list_b)
                return False
        for i in range(3):
            a=list_a[i+3]
            b=list_b[i+3]
            if(abs(a-b)>(abg_single_error)):
                print("abg not ready")
                return False
        return True
    @staticmethod
    def check_xyz_error_ok(error_list,allow_list):
        if (abs(error_list[0]) > allow_list[0]):
            # print("x error not ready")
            return False
        if (abs(error_list[1]) > allow_list[1]):
            # print("y error not ready")
            return False
        if (abs(error_list[2]) > allow_list[2]):
            # print("z error not ready")
            return False
        # print("xyz error are ready")
        return True

class operator():
    def __init__(self,global_db):
        self.global_db=global_db
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
        # print("send message:", MESSAGE)

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
    def publish(self):
        iiwa_sp_str = self.global_db.form_sp_Str()
        pub_msg = bytes(iiwa_sp_str, encoding="utf8")
        # print("publish:",pub_msg)
        self.send_cont(pub_msg)
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
                # print("Received floats",self.global_db.r_iiwaFltLs[0:7])
                self.global_db.r_iiwa_x = self.global_db.r_iiwaFltLs[0]
                self.global_db.r_iiwa_y = self.global_db.r_iiwaFltLs[1]
                self.global_db.r_iiwa_z = self.global_db.r_iiwaFltLs[2]
                self.global_db.r_iiwa_a = self.global_db.r_iiwaFltLs[3]
                self.global_db.r_iiwa_b = self.global_db.r_iiwaFltLs[4]
                self.global_db.r_iiwa_g = self.global_db.r_iiwaFltLs[5]
                self.global_db.r_iiwa_o = self.global_db.r_iiwaFltLs[6]
                # print(self.global_db.__dict__)
                self.global_db.first_update_done=1
                # print("here")
                # tcpCliSock.send('[%s] %s' % (bytes(ctime(), 'utf-8'), data))
        # while (1):
        #     print("receive:xxx")
        #     time.sleep(3)
        # pass
    def launch_ui(self,db):
        while(1):
            # print("db.target_detected_list",db.target_detected_list)
            # time.sleep(0.1)
            db.pose_pid_control_able=0 # it will stop pid control
            db.finished_pick_and_place=0
            db.finished_only_place = 0
            db.finished_only_pick = 0
            print("I have those things:",db.target_detected_list)
            target_name=input("What do you want me to grasp?")
            while(not target_name in db.target_detected_list):
                print("I don't have that, please input again")
                print("I have those things:{", db.target_detected_list,'}')
                target_name = input()

            #target_name set success
            db.target_name_sp=target_name
            db.pose_pid_control_able=1 # start to pick up
            while(db.finished_pick_and_place==0 and db.finished_only_place==0):

                print("I'm now doing it!......")
                time.sleep(3)
            print("I finished pick up and place the ",target_name)


        # return target_name


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
        #functional
        self.first_update_done=0
        self.blocked=0 # if some function need to occupy iiwa fully, should set it be 1
        # self.ui_blocked=0 # if ui is running, ui will block the control part.
        self.pose_pid_control_able=1 # if 1, pid control able.
        #iiwaStr
        self.r_iiwaStr=""
        self.r_iiwaFltLs=[]


        # ##safe_iiwa_xx == safe position

        # table position
        # self.x_max = 620
        # self.x_min = 200
        # self.y_max = 830
        # self.y_min = 680
        # self.z_max = 1000
        # self.z_min = 380
        # self.safe_iiwa_x = 300  # 180~700
        # self.safe_iiwa_y = 680  # 680~900
        # self.safe_iiwa_z = 500  # 220~1000
        # self.safe_iiwa_a = 0  # pitch
        # self.safe_iiwa_b = 0.5  # yaw
        # self.safe_iiwa_g = -2  # roll
        # self.safe_iiwa_o = 100
            #oringinal position
        #   #Received floats [706.577703254111, 9.489756422152325, 376.2598473404427, -0.8127086912743297, 0.05697711457431897, -1.9384994457679934, 255.0]
        self.x_max = 930
        self.x_min = 566
        self.y_max = 389
        self.y_min = -250
        self.z_max = 936
        self.z_min = 73
        self.safe_iiwa_x=706#180~700
        self.safe_iiwa_y=9.4#680~900
        self.safe_iiwa_z=376#220~1000
        self.safe_iiwa_a=-0.8#pitch
        self.safe_iiwa_b=0.056#yaw
        self.safe_iiwa_g=-1.93 #roll
        self.safe_iiwa_o=100


        #_iiwa_xx == estimation
        # self._iiwa_x=706.57
        # self._iiwa_y=4.58
        # self._iiwa_z=376.26
        # self._iiwa_a=-0.812
        # self._iiwa_b=0.056
        # self._iiwa_g=-1.938
        # self._iiwa_o=255

        #iiwa_xx_sp == setpoint
        self.iiwa_x_sp=self.safe_iiwa_x
        self.iiwa_y_sp=self.safe_iiwa_y
        self.iiwa_z_sp=self.safe_iiwa_z
        self.iiwa_a_sp=self.safe_iiwa_a
        self.iiwa_b_sp=self.safe_iiwa_b
        self.iiwa_g_sp=self.safe_iiwa_g
        self.iiwa_o_sp=self.safe_iiwa_o

        #v_iiwa_xx == from camera

        #r_iiwa_xx == read from iiwa
        self.r_iiwa_x=706.57
        self.r_iiwa_y=4.58
        self.r_iiwa_z=376.26
        self.r_iiwa_a=-0.812
        self.r_iiwa_b=0.056
        self.r_iiwa_g=-1.938
        self.r_iiwa_o=255

        ##safe_iiwa_xx == safe position
        # self.safe_iiwa_x=706.57
        # self.safe_iiwa_y=4.58
        # self.safe_iiwa_z=376.26
        # self.safe_iiwa_a=-0.812
        # self.safe_iiwa_b=0.056
        # self.safe_iiwa_g=-1.938
        # self.safe_iiwa_o=100

        #opencv
        self.click_cv_x=620
        self.click_cv_y=475

        #camera
        self.cam_iiwa_x=1
        self.cam_iiwa_y=1
        self.cam_iiwa_z=1
        self.cam_iiwa_updated=0
        self.cam_cube_x=1
        self.cam_cube_y=1
        self.cam_cube_z=1
        self.cam_cube_updated=0

        self.cam_target_place_x=0.03
        self.cam_target_place_y=0.27
        self.cam_target_place_z=0.98


        self.target_detected_list=[]
        self.target_name_sp=""
        self.finished_pick_and_place=0 # if once pick and place operation finished, it should be 1.else be 0
        self.finished_only_pick=0
        self.finished_only_place=0
    def form_sp_Str(self):
        sendStr=str(self.iiwa_x_sp)+" "+str(self.iiwa_y_sp)+" "+str(self.iiwa_z_sp)+" "+str(self.iiwa_a_sp)+" "+str(self.iiwa_b_sp)+" "+str(self.iiwa_g_sp)+" "+str(self.iiwa_o_sp)
        return sendStr

    def coordinate_cam_2_iiwaBase(self,pos_xyz):
        cx=pos_xyz[0]
        cy=pos_xyz[1]
        cz=pos_xyz[2]
        ix=-cz
        iy=cx
        iz=-cy
        pos_xyz_iiwaBase=[ix,iy,iz]
        return pos_xyz_iiwaBase

    @staticmethod
    def value_clamp(input,min,max):
        # return input
        if(input>max):
            input=max
        elif(input<min):
            input=min
        return input

    def set_x_sp(self,input):
        self.iiwa_x_sp=self.value_clamp(input,min=self.x_min,max=self.x_max)
    def set_y_sp(self,input):
        self.iiwa_y_sp=self.value_clamp(input,min=self.y_min,max=self.y_max)
    def set_z_sp(self,input):
        self.iiwa_z_sp=self.value_clamp(input,min=self.z_min,max=self.z_max)


class controller():
    def __init__(self,db,operator):
        self.db=db
        self.op=operator
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

    def line_path_planer(self,read_value,safe_value,u,distance=80,u_step=20):
        # print("safe_value",safe_value)
        max_pos=safe_value+distance
        min_pos=safe_value-distance
        # print("max_pos",max_pos,"min_pos",min_pos)
        if(read_value<max_pos and read_value>min_pos):
            pass
        elif(read_value>max_pos):
            u =-u_step
        elif(read_value<min_pos):
            u = u_step
        else:
            pass
        # print("direction:",u)
        # sp_value=read_value+x_direction
        return u

    def pos_control(self,sp_x,sp_y,sp_z,sp_o,sp_a,sp_b,sp_g):
        self.db.iiwa_x_sp=sp_x
        self.db.iiwa_y_sp=sp_y
        self.db.iiwa_z_sp=sp_z
        self.db.iiwa_a_sp = sp_a
        self.db.iiwa_b_sp = sp_b
        self.db.iiwa_g_sp = sp_g
        self.db.iiwa_o_sp=sp_o

    def pos_pid_control(self,dx=0,dy=0,dz=0,P_gain=10,I_gain=0,D_gain=0):
        P_max_error=30
        Min_u=1
        Max_u=50
        Px=funcs.clamp(dx*P_gain,Min_u,Max_u)
        Py=funcs.clamp(dy*P_gain,Min_u,Max_u)
        Pz=funcs.clamp(dz*P_gain,0,Max_u)

        self.db.set_x_sp(self.db.r_iiwa_x + Px)
        self.db.set_y_sp(self.db.r_iiwa_y + Py)
        self.db.set_z_sp(self.db.r_iiwa_z + Pz)
        # print('dz',dz)
    def do_pos_sequence(self,target_pos_ls):
        self.db.blocked = 1
        db=self.db
        gripper_last=target_pos_ls[0][6]
        for i in range(len(target_pos_ls)):
            target_pos = target_pos_ls[i]
            current_pos = [db.r_iiwa_x, db.r_iiwa_y, db.r_iiwa_z, db.r_iiwa_a, db.r_iiwa_b, db.r_iiwa_g]
            print("Go to #", i, "Point", target_pos)
            while (funcs.check_xyzabg_same(target_pos, current_pos, xyz_single_error=15,
                                           abg_single_error=0.15) == False):

                self.pos_control(sp_x=target_pos[0], sp_y=target_pos[1], sp_z=target_pos[2],
                               sp_a=target_pos[3], sp_b=target_pos[4], sp_g=target_pos[5], sp_o=target_pos[6])
                self.op.publish()
                # if((target_pos[6]-gripper_last)>50):#gripping detected
                #     time.sleep(5)

                gripper_last=target_pos[6]
                # if(abs(target_pos[6]-db.r_iiwa_o)>30):
                #     time.sleep(1)
                current_pos = [db.r_iiwa_x, db.r_iiwa_y, db.r_iiwa_z, db.r_iiwa_a, db.r_iiwa_b, db.r_iiwa_g]
                time.sleep(0.1)
        self.db.blocked=0

    def do_go_to_xy_then_pick(self, x, y):
        # self.db.finished_pick_and_place = 0
        target_pos_ls = []
        # x=655 #y=229
        target_pos_ls.append([x, y, 216, -0.8, 0.056, -1.93, 10])  # 1
        target_pos_ls.append([x, y, 216, -0.8, 0.056, -1.93, 10])  # 2#6
        target_pos_ls.append([x, y, 83, -0.74, 0.08, -1.93, 10])  # 3 #height 76
        target_pos_ls.append([x, y, 83, -0.74, 0.08, -1.93, 150])  # 4
        target_pos_ls.append([x, y, 376, -0.74, 0.08, -1.93, 150])  # 5
        target_pos_ls.append([691, -116, 312, -0.76, 0.058, -1.9, 150])  # 6
        target_pos_ls.append([691, -116, 83, -0.76, 0.058, -1.9, 150])  # 7
        target_pos_ls.append([691, -116, 83, -0.76, 0.058, -1.9, 10])  # 8
        target_pos_ls.append([691, -116, 330, -0.76, 0.08, -1.9, 10])  # 9
        self.do_pos_sequence(target_pos_ls) #block pid
        print("finish go_to_xy_then_pick", "x=", x, "y=", y)
        self.db.finished_pick_and_place = 1
        self.db.pose_pid_control_able = 0

    def do_go_to_xy_only_pick(self, x, y):
        # self.db.finished_pick_and_place = 0
        print("im doing only pick")
        target_pos_ls = []
        # x=655 #y=229
        target_pos_ls.append([x, y, 216, -0.8, 0.056, -1.93, 10])  # 1
        target_pos_ls.append([x, y, 216, -0.8, 0.056, -1.93, 10])  # 2#6
        target_pos_ls.append([x, y, 93, -0.74, 0.08, -1.93, 10])  # 3
        target_pos_ls.append([x, y, 93, -0.74, 0.08, -1.93, 150])  # 4
        target_pos_ls.append([x, y, 376, -0.74, 0.08, -1.93, 150])  # 5
        # target_pos_ls.append([691, -116, 312, -0.76, 0.058, -1.9, 150])  # 6
        # target_pos_ls.append([691, -116, 73, -0.76, 0.058, -1.9, 150])  # 7
        # target_pos_ls.append([691, -116, 73, -0.76, 0.058, -1.9, 10])  # 8
        # target_pos_ls.append([691, -116, 274, -0.76, 0.08, -1.9, 10])  # 9
        self.do_pos_sequence(target_pos_ls)
        print("finish go_to_xy_then_pick", "x=", x, "y=", y)
        self.db.finished_only_pick = 1
        # self.db.pose_pid_control_able = 1
    def do_go_to_xy_only_place(self, x, y):
        # self.db.finished_pick_and_place = 0

        print("im doing only place")
        target_pos_ls = []
        # x=655 #y=229
        # target_pos_ls.append([x, y, 216, -0.8, 0.056, -1.93, 10])  # 1
        # target_pos_ls.append([x, y, 216, -0.8, 0.056, -1.93, 10])  # 2#6
        # target_pos_ls.append([x, y, 76, -0.74, 0.08, -1.93, 10])  # 3
        # target_pos_ls.append([x, y, 76, -0.74, 0.08, -1.93, 150])  # 4
        # target_pos_ls.append([x, y, 376, -0.74, 0.08, -1.93, 150])  # 5
        target_pos_ls.append([x, y, 312, -0.76, 0.058, -1.9, 150])  # 6
        target_pos_ls.append([x, y, 93, -0.76, 0.058, -1.9, 150])  # 7
        target_pos_ls.append([x, y, 93, -0.76, 0.058, -1.9, 10])  # 8
        target_pos_ls.append([x, y, 274, -0.76, 0.08, -1.9, 10])  # 9
        self.do_pos_sequence(target_pos_ls)
        print("finish go_to_xy_then_pick", "x=", x, "y=", y)
        self.db.finished_only_place = 1
        self.db.finished_only_pick = 1
        self.db.pose_pid_control_able = 0 #this is to block pid, wait for ui to restart


la=[100,100,100,1.5,1,1]
lb=[90,100,100,1,1,1]
print(funcs.check_xyzabg_same(la,lb,xyz_single_error=11,abg_single_error=0.5))

if __name__=="__main__":
    db = global_database()
    operator = operator(db)
    # operator.send_server_start() #no auto send. use manual publish
    operator.receive_server_start()
    ct=controller(db,operator)

    u=3
    # operator.publish()
    CONTROL_MODE=1 #0 default; 1 manual; 2 hardcode pick and place
    # MANUAL_CONTROL=1

    if(CONTROL_MODE==1):
        operator.send_server_start()
        sp_x=db.safe_iiwa_x
        sp_z=db.safe_iiwa_z
        sp_y=db.safe_iiwa_y
        sp_b=db.safe_iiwa_b
        sp_o=60
        s=20
        while(1):
            manual_x=input("manual control")
            # self.safe_iiwa_x=300#180~700
            # self.safe_iiwa_y=680#680~950
            # self.safe_iiwa_z=500#400~1000


            if(manual_x=="r"):
                print(db.r_iiwaFltLs[0:7])
            if(manual_x=='4'):
                sp_x=sp_x+s
            if(manual_x=='6'):
                sp_x=sp_x-s
            if(manual_x=='-'):
                sp_y=sp_y-s
            if(manual_x=='+'):
                sp_y=sp_y+s
            if(manual_x=='8'):
                sp_z=sp_z+s
            if (manual_x == '2'):
                sp_z = sp_z - s
            if (manual_x == '1'):
                sp_b = sp_b - 0.1
            if (manual_x == '3'):
                sp_b = sp_b + 0.1
            if (manual_x == '0'):
                if(sp_o<240):
                    sp_o = sp_o + 10
            if (manual_x == '.'):
                if(sp_o>10):
                    sp_o = sp_o - 10

            ct.pos_control(sp_x=sp_x,sp_y=sp_y,sp_z=sp_z,sp_a=db.safe_iiwa_a,sp_b=sp_b,sp_g=db.safe_iiwa_g,sp_o=sp_o)

            operator.publish()
            # u=ct.line_path_planer(read_value=db.r_iiwa_y,safe_value=db.safe_iiwa_y,u=u,distance=100,u_step=20)
            # db.iiwa_y_sp =db.r_iiwa_y+u
            # operator.publish()
            # db.iiwa_y_sp = db.r_iiwa_y-20
            # operator.publish()
            # u=ct.line_path_planer(read_value=db.r_iiwa_y,safe_value=db.safe_iiwa_y,u=u,distance=100,u_step=20)
            # db.iiwa_y_sp =350
            # print("z sp",db.iiwa_z_sp)
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

            # u=ct.line_path_planer(db.r_iiwa_y,db.safe_iiwa_y,u=u,distance=30)

            # print(db.__dict__)
            # u=ct.line_path_planer(read_value=db.r_iiwa_y,safe_value=db.safe_iiwa_y,u=u,distance=100)
            # db.iiwa_y_sp =350
            # print("sp:"+str(db.iiwa_y_sp))
            # print("db:",db.__dict__)
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
    elif(CONTROL_MODE==2):
        # pos1=655 229.4 216 -0.8 0.056 -1.93 60 #hover
        # pos2=655 229.4 216 -0.8 0.056 -1.93 10 #hover+open
        # pos3=655 225 76 -0.74 0.08 -1.92 10 #go down
        # pos4=655 225 76 -0.74 0.08 -1.92 70 #grasp
        # pos5=646 225 376 -0.74 0.08 -1.92 70 #go up
        # pos6=692 -116 312 -0.76 0.058 -1.90 70#hover another
        # pos7=691 -116 73 -0.76 0.058 -1.89 70# go down

        # pos8=691 -116 73 -0.76 0.058 -1.89 10# let it go

        # pos9=691 -116 274 -0.76 0.058 -1.89 10 # go up

        target_pos_ls=[]
        target_pos_ls.append([655,229.4,216,-0.8,0.056,-1.93,10])#1
        target_pos_ls.append([655,229.4,216,-0.8,0.056,-1.93,10])#2#6
        target_pos_ls.append([655,225,76,-0.74,0.08,-1.93,10])#3
        target_pos_ls.append([655,225,76,-0.74,0.08,-1.93,70])#4
        target_pos_ls.append([646,225,376,-0.74,0.08,-1.93,70])#5
        target_pos_ls.append([691,-116,312,-0.76,0.058,-1.9,70])#6
        target_pos_ls.append([691,-116,73,-0.76,0.058,-1.9,70])#7
        target_pos_ls.append([691,-116,73,-0.76,0.058,-1.9,10])#8
        target_pos_ls.append([691,-116,274,-0.76,0.08,-1.9,10])#9

        dance_pos_ls=[]
        # dance_pos_ls.append([670,150,300,-0.8,0.2,-1.93,10])#1
        dance_pos_ls.append([670,150,300,-0.5,-0.2,-1.43,10])#1
        # dance_pos_ls.append([670,150,300,-0.8,0.2,-1.93,10])#1
        dance_pos_ls.append([670,150,300,-0.2,0.2,-2.23,10])#1
        # dance_pos_ls.append([670,150,300,-0.8,0.2,-1.93,10])#1


        print(target_pos_ls)
        while(1):
            # for i in range(len(target_pos_ls)):
            #     target_pos=target_pos_ls[i]
            #     current_pos=[db.r_iiwa_x,db.r_iiwa_y,db.r_iiwa_z,db.r_iiwa_a,db.r_iiwa_b,db.r_iiwa_g]
            #     print("Go to #",i,"Point",target_pos)
            #     while(funcs.check_xyzabg_same(target_pos,current_pos,xyz_single_error=15,abg_single_error=0.1)==False):
            #         ct.pos_control(sp_x=target_pos[0], sp_y=target_pos[1], sp_z=target_pos[2],
            #                        sp_a=target_pos[3], sp_b=target_pos[4], sp_g=target_pos[5], sp_o=target_pos[6])
            #         operator.publish()
            #         current_pos = [db.r_iiwa_x, db.r_iiwa_y, db.r_iiwa_z, db.r_iiwa_a, db.r_iiwa_b, db.r_iiwa_g]
            #         time.sleep(0.1)
            ct.do_pos_sequence(target_pos_ls)
            target_pos_ls_inv=target_pos_ls[:]
            for i in range(len(target_pos_ls)):
                target_pos_ls_inv[i]=target_pos_ls[8-i]
            target_pos_ls=target_pos_ls_inv[:]
            print("target:",target_pos_ls)
            print("target_inv",target_pos_ls_inv)
            ct.do_pos_sequence(dance_pos_ls)
        pass
    else:
        while (1):

            ct.pos_control(sp_x=340, sp_y=850, sp_z=500, sp_a=db.safe_iiwa_a, sp_b=db.safe_iiwa_b,
                           sp_g=db.safe_iiwa_g, sp_o=60)

            operator.publish()
            time.sleep(0.02)
