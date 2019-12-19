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
    def check_xyzabgo_same(list_a, list_b, xyz_single_error, abg_single_error,o_error):
        for i in range(3):
            a = list_a[i]
            b = list_b[i]
            if (abs(a - b) > (xyz_single_error)):
                # print("xyz not ready",list_a,list_b)
                return False
        for i in range(3):
            a = list_a[i + 3]
            b = list_b[i + 3]
            if (abs(a - b) > (abg_single_error)):
                print("abg not ready")
                return False
        oa=list_a[6]
        ob=list_b[6]
        if(abs(oa-ob)>o_error):
            print("gripper not read")
            return False
        return True


    @staticmethod
    def check_xyz_abs_error_ok(error_list,allow_list):
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
    def SendSPtoIIWA(self):
        self.publish()
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
                    # print("no data received")
                    time.sleep(0.1)
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
                self.global_db.r_iiwa_outrange=self.global_db.r_iiwaFltLs[7]
                self.global_db.r_iiwa_FX=self.global_db.r_iiwaFltLs[8]
                self.global_db.r_iiwa_FY=self.global_db.r_iiwaFltLs[9]
                self.global_db.r_iiwa_FZ=self.global_db.r_iiwaFltLs[10]
                self.global_db.r_iiwa_TX=self.global_db.r_iiwaFltLs[11]
                self.global_db.r_iiwa_TY=self.global_db.r_iiwaFltLs[12]
                self.global_db.r_iiwa_TZ=self.global_db.r_iiwaFltLs[13]
                self.global_db.r_iiwa_js=[self.global_db.r_iiwaFltLs[i] for i in range(16,23)]
                # print(self.global_db.__dict__)
                self.global_db.first_update_done=1
                # print("here")
                # tcpCliSock.send('[%s] %s' % (bytes(ctime(), 'utf-8'), data))
        # while (1):
        #     print("receive:xxx")
        #     time.sleep(3)
        # pass
    def launch_ui(self,db):#Deprecated
        #Deprecated
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

    #background thread tasks,for debug use
    def show_logs_thread(self):
        while(1):
            time.sleep(2)
            db=self.global_db
            # print(db.cam_target_place_z)
            # print(db.cam_iiwa_updated)
            print("      LOG:")
            print("      bottle:", db.cam_bottle_updated, db.cam_bottle_x, db.cam_bottle_y, db.cam_bottle_z)
            print("      cube:", db.cam_cube_updated, db.cam_cube_x, db.cam_cube_y, db.cam_cube_z)
            print("      target:", db.cam_target_place_x, db.cam_target_place_y, db.cam_target_place_z)
            print("      iiwa:", db.cam_iiwa_updated,db.cam_iiwa_x, db.cam_iiwa_y, db.cam_iiwa_z)
            print("\n\n")
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
            float_list[i]=round(float(float_list[i]),4)
        return float_list
class global_database():
    # this database is shared with iiwa through udp
    def __init__(self):
        #functional
        self.first_update_done=0
        self.blocked=0 # if some function need to occupy iiwa fully, should set it be 1
        # self.ui_blocked=0 # if ui is running, ui will block the control part.
        self.pose_pid_control_able=1 # if 1, pid control able.
        self.holding_at_safe_pos_switch=True
        self.inMission=0 #if inMission=1, it means IIWA is doing a mission, better not to interupt
        #iiwaStr
        self.r_iiwaStr=""
        self.r_iiwaFltLs=[]

        self.EmergencySTOP_Sig=0 #if ==1, movement STOP!

        self.ControlMode=0 #0,SmartServo, 1,DirectServo, 2 Force impedance Control

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
        self.safe_iiwa_js=[0,0,0,0,0,0,0]
        self.safe_iiwa_speed=0.1
        self.safe_iiwa_F=[0,0,0,0,0,0]#Fx Fy Fz Tx Ty Tz
        self.safe_iiwa_stiff=[300,300,300,0,0,0] #xyzabg
        self.safe_iiwa_jspeed_default=0.01
        self.safe_iiwa_jspeed=[self.safe_iiwa_jspeed_default for i in range(7)]
        self.safe_iiwa_maxforce=[15,15,15,3,3,3]
        self.safe_iiwa_blending=0.5
        self.safe_iiwa_tcp_xyzabg=[0,0,0,0,0,0]
        self.safe_iiwa_addForce=[0,0,0,0,0,0]#xyzabg
        #iiwa_xx_sp == setpoint
        self.iiwa_x_sp=self.safe_iiwa_x
        self.iiwa_y_sp=self.safe_iiwa_y
        self.iiwa_z_sp=self.safe_iiwa_z
        self.iiwa_a_sp=self.safe_iiwa_a
        self.iiwa_b_sp=self.safe_iiwa_b
        self.iiwa_g_sp=self.safe_iiwa_g
        self.iiwa_o_sp=self.safe_iiwa_o
        self.iiwa_js_sp=self.safe_iiwa_js
        self.iiwa_jspeed_sp=self.safe_iiwa_jspeed# [j1,j2,j3..j7]
        self.iiwa_F_sp=self.safe_iiwa_F
        self.iiwa_speed_sp=self.safe_iiwa_speed# double x
        self.iiwa_stiff_sp=self.safe_iiwa_stiff #xyzabg
        self.iiwa_maxforce_sp=self.safe_iiwa_maxforce #xyzabc
        self.iiwa_blending_sp=self.safe_iiwa_blending
        self.iiwa_tcp_xyzabg_sp=self.safe_iiwa_tcp_xyzabg
        self.iiwa_addForce_sp=self.safe_iiwa_addForce
        #v_iiwa_xx == from camera

        #r_iiwa_xx == read from iiwa
        #r means read from iiwa
        self.r_iiwa_x=706.57
        self.r_iiwa_y=4.58
        self.r_iiwa_z=376.26
        self.r_iiwa_a=-0.812
        self.r_iiwa_b=0.056
        self.r_iiwa_g=-1.938
        self.r_iiwa_o=255
        self.r_iiwa_outrange=0
        self.r_iiwa_FX = 0
        self.r_iiwa_FY = 0
        self.r_iiwa_FZ = 0
        self.r_iiwa_TX = 0
        self.r_iiwa_TY = 0
        self.r_iiwa_TZ = 0
        self.r_iiwa_js=[0,0,0,0,0,0,0]
        # self.r_tcp_xyzabg_sp=[0,0,0,0,0,0]

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
        self.cam_iiwa_x=-1
        self.cam_iiwa_y=-1
        self.cam_iiwa_z=-1
        self.cam_iiwa_updated=0
        self.cam_cube_x=-1
        self.cam_cube_y=-1
        self.cam_cube_z=-1
        self.cam_cube_updated=0
        self.cam_bottle_x=-1
        self.cam_bottle_y=-1
        self.cam_bottle_z=-1
        self.cam_bottle_updated=0
        self.cam_hand_x=-1
        self.cam_hand_y=-1
        self.cam_hand_z=-1
        self.cam_isfeast=0
        self.cam_hand_updated=0

        # self.cam_too_close_error=1

        self.cam_image=None
        self.cam_f=0
        self.cam_target_place_x=0.03
        self.cam_target_place_y=0.27
        self.cam_target_place_z=0.98


        self.target_detected_list=[]
        self.target_name_sp=""
        self.finished_pick_and_place=0 # if once pick and place operation finished, it should be 1.else be 0
        self.finished_only_pick=0
        self.finished_only_place=0
    def form_sp_Str(self):
        sendStr=str(self.ControlMode)
        #sp xyzabg
        sendStr+=" "+str(self.iiwa_x_sp)+" "+str(self.iiwa_y_sp)+" "+str(self.iiwa_z_sp)+" "+str(self.iiwa_a_sp)+" "+str(self.iiwa_b_sp)+" "+str(self.iiwa_g_sp)+" "+str(self.iiwa_o_sp)
        #sp joints
        sendStr+=" "+str(self.iiwa_js_sp[0])+" "+str(self.iiwa_js_sp[1])+" "+str(self.iiwa_js_sp[2])+" "+str(self.iiwa_js_sp[3])+" "+str(self.iiwa_js_sp[4])+" "+str(self.iiwa_js_sp[5])+" "+str(self.iiwa_js_sp[6])
        #sp force FxFyFz TxTyTz
        for f in self.iiwa_F_sp:
            sendStr+=" "+str(f)
        #speed
        sendStr+=" "+str(self.iiwa_speed_sp)
        # sp stiffness xyzabg
        for f in self.iiwa_stiff_sp:
            sendStr += " " + str(f)
        # sp joitspeed 1234567
        for f in self.iiwa_jspeed_sp:
            sendStr += " " + str(f)
        # sp blending
        sendStr+=" "+str(self.iiwa_blending_sp)

        # sp maxforce
        for f in self.iiwa_maxforce_sp:
            sendStr += " " + str(f)

        for f in self.iiwa_tcp_xyzabg_sp:
            sendStr += " " + str(f)
        for f in self.safe_iiwa_addForce:
            sendStr += " " + str(f)

        # print("Sending Cont:",sendStr)
        return sendStr

    def get_safe_blending(self):
        return self.safe_iiwa_blending
    def get_safe_poses(self):
        return [self.safe_iiwa_x,self.safe_iiwa_y,self.safe_iiwa_z,self.safe_iiwa_a,self.safe_iiwa_b,self.safe_iiwa_g,self.safe_iiwa_o]
    def get_safe_poses_in_meters(self):
        return [self.safe_iiwa_x/1000,self.safe_iiwa_y/1000,self.safe_iiwa_z/1000,self.safe_iiwa_a,self.safe_iiwa_b,self.safe_iiwa_g,self.safe_iiwa_o]
    def get_read_poses(self):
        return [self.r_iiwa_x,self.r_iiwa_y,self.r_iiwa_z,self.r_iiwa_a,self.r_iiwa_b,self.r_iiwa_g,self.r_iiwa_o]
    def get_sp_poses(self):
        return [self.iiwa_x_sp,self.iiwa_y_sp,self.iiwa_z_sp,self.iiwa_a_sp,self.iiwa_b_sp,self.iiwa_g_sp,self.iiwa_o_sp]
    def get_read_joints(self):
        return self.r_iiwa_js
    # def check_updated(self):
    def get_target_cam_data_list(self,name):
        if(name=="cube"):
            list=[self.cam_cube_updated,self.cam_cube_x,self.cam_cube_y,self.cam_cube_z]
        elif(name=="iiwa"):
            list=[self.cam_iiwa_updated,self.cam_iiwa_x,self.cam_iiwa_y,self.cam_iiwa_z]
        elif(name=="hand"):
            list=[self.cam_hand_updated,self.cam_hand_x,self.cam_hand_y,self.cam_hand_z]
        elif(name=="bottle"):
            list=[self.cam_bottle_updated,self.cam_bottle_x,self.cam_bottle_y,self.cam_bottle_z]
        else:
            return [False,False,False,False]
        return list
        # elif(name=="cube"):
        #     list=[self.cam_cube_updated,self.cam_cube_x,self.cam_cube_y,self.cam_cube_z]

    #funcs
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

    #set xyz sp; In case out of range.
    def set_x_sp(self,input):
        self.iiwa_x_sp=self.value_clamp(input,min=self.x_min,max=self.x_max)
    def set_y_sp(self,input):
        self.iiwa_y_sp=self.value_clamp(input,min=self.y_min,max=self.y_max)
    def set_z_sp(self,input):
        self.iiwa_z_sp=self.value_clamp(input,min=self.z_min,max=self.z_max)
    def set_o_sp(self,input):
        self.iiwa_o_sp=self.value_clamp(input,min=6,max=113)

    def publish_cam_image(self,image):
        self.cam_image=image
    def get_cam_image(self):
        return self.cam_image

    def publish_cam_data(self,data_list):
        name=data_list[0]
        updated=data_list[1]
        x=data_list[2]
        y=data_list[3]
        z=data_list[4]
        if(name=="iiwa_gripper"):
            self.cam_iiwa_updated=updated
            self.cam_iiwa_x=x
            self.cam_iiwa_y=y
            self.cam_iiwa_z=z
        elif(name=="cube"):
            self.cam_cube_updated=updated
            self.cam_cube_x=x
            self.cam_cube_y=y
            self.cam_cube_z=z
        elif(name=="bottle"):
            self.cam_bottle_updated=updated
            self.cam_bottle_x=x
            self.cam_bottle_y=y
            self.cam_bottle_z=z
        elif (name == "hand"):
            isfeast=data_list[5]
            self.cam_hand_updated = updated
            self.cam_hand_x = x
            self.cam_hand_y = y
            self.cam_hand_z = z
            self.cam_isfeast= isfeast
    def publish_cam_data_quick(self,data_list):
        store_thread=threading.Thread(target=self.publish_cam_data,args=(data_list,))
        store_thread.start()
    def get_target_detected_list(self):
        return self.target_detected_list

    def publish_holding_at_safe_pose_switch(self,switch):
        self.holding_at_safe_pos_switch=switch
        return True
    def publish_inMission(self,inmission):
        self.inMission=inmission
        return True
    def get_inMission(self):
        return self.inMission
class controller():
    def __init__(self,db,operator):
        self.db=db
        self.op=operator

        self.pid_MaxUDefault=40
        self.pid_MinUDefault=1
        self.pid_MaxU=self.pid_MaxUDefault
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
    def set_gripper(self, GRIP=1):
        '''
        gripper control (Blocking wait)
        :param val: False:RELEASE, True:GRIP
        :return: None

        val = true or false

        '''
        # if self.target_gripper != val:
        #     self.target_gripper = val
        val=GRIP
        if val:
            pose_read=self.db.get_read_poses() #this is for keep xyz raw pitch yaw keeps the same.
            self.db.set_o_sp(113)
            # self.pos_control(sp_x=pose_read[0],sp_y=pose_read[1],sp_z=pose_read[2],sp_a=pose_read[3],sp_b=pose_read[4],sp_g=pose_read[5],sp_o=113)
        else:
            self.db.set_o_sp(6)
            pose_read=self.db.get_read_poses()
            # self.pos_control(sp_x=pose_read[0],sp_y=pose_read[1],sp_z=pose_read[2],sp_a=pose_read[3],sp_b=pose_read[4],sp_g=pose_read[5],sp_o=6)
    def set_gripper_value(self,value):
        #value==113 grip
        #value==6 open
        pose_read = self.db.get_read_poses()  # this is for keep xyz raw pitch yaw keeps the same.
        self.pos_control(sp_x=pose_read[0], sp_y=pose_read[1], sp_z=pose_read[2], sp_a=pose_read[3],
                            sp_b=pose_read[4], sp_g=pose_read[5], sp_o=value)
    def set_goal_pose(self,pose):
        self.db.iiwa_x_sp=pose[0]
        self.db.iiwa_y_sp=pose[1]
        self.db.iiwa_z_sp=pose[2]
        self.db.iiwa_a_sp=pose[3]
        self.db.iiwa_b_sp=pose[4]
        self.db.iiwa_g_sp=pose[5]
    def get_gripper_value(self):
        return self.db.get_read_poses()[6]

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
        self.db.ControlMode=0#0,smartservo
        self.db.iiwa_x_sp=sp_x
        self.db.iiwa_y_sp=sp_y
        self.db.iiwa_z_sp=sp_z
        self.db.iiwa_a_sp = sp_a
        self.db.iiwa_b_sp = sp_b
        self.db.iiwa_g_sp = sp_g
        self.db.iiwa_o_sp=sp_o
    def joints_control(self,sp_joints,sp_joints_speeds):
        self.db.ControlMode = 1  # 1,smartservo joints contorl
        self.db.iiwa_js_sp=sp_joints
        self.db.iiwa_jspeed_sp=sp_joints_speeds
    def stopj(self):
        self.db.ControlMode = 9  # 1,smartservo joints contorl
    def ptp_force_control(self,pose,stifs,addforce,speed):
        self.db.ControlMode = 2
        self.set_goal_pose(pose)
        self.db.iiwa_stiff_sp=stifs
        self.db.iiwa_F_sp=addforce
        self.db.iiwa_speed_sp=speed
    def pos_pid_control(self,dx=0,dy=0,dz=0,P_gain=10,I_gain=0,D_gain=0):

        has_outrange=self.db.r_iiwa_outrange
        P_max_error=30
        # Min_u=self.pid_MaxUDefault
        if(has_outrange):
            if(self.pid_MaxU>self.pid_MinUDefault+20):
                self.pid_MaxU-=2
        else:
            if(self.pid_MaxU<self.pid_MaxUDefault):
                self.pid_MaxU+=1
            # self.pid_MaxU=self.pid_MaxUDefault

        Max_u=self.pid_MaxU
        Min_u=self.pid_MinUDefault
        # print("Maxu",Max_u)
        Px=funcs.clamp(dx*P_gain,Min_u,Max_u)
        Py=funcs.clamp(dy*P_gain,Min_u,Max_u)
        Pz=funcs.clamp(dz*P_gain,Min_u,Max_u)
        # print("PxPyPz",Px,Py,Pz)
        self.db.set_x_sp(self.db.r_iiwa_x + Px)
        self.db.set_y_sp(self.db.r_iiwa_y + Py)
        self.db.set_z_sp(self.db.r_iiwa_z + Pz)
        # print('dz',dz)
    def maxforce_ptpmove(self,goalpose,maxforce,blending,Jointspeed):
        self.db.ControlMode=3
        self.set_goal_pose(goalpose)
        self.db.iiwa_blending_sp=blending
        self.db.iiwa_speed_sp=Jointspeed
        for i in range(len(maxforce)):
            if(maxforce[i]==0):
                maxforce[i]=self.db.safe_iiwa_maxforce[i]
        # maxforce=[20 if f==0 else f for f in force]
        self.db.iiwa_maxforce_sp=maxforce
    #Basic Motion Squence (Blocking running)
    def do_gripper_fully(self,grip_value,last_time=1):
        start_time=time.time()
        while(time.time()-start_time<last_time):
            # print("grip time")
            self.set_gripper_value(grip_value)
            time.sleep(0.05)
            if(self.get_gripper_value()==grip_value):
                break

    def do_pos_sequence(self,target_pos_ls):

        self.db.blocked = 1
        db=self.db
        gripper_last=target_pos_ls[0][6]
        for i in range(len(target_pos_ls)):
            if(self.db.EmergencySTOP_Sig):
                break
            target_pos = target_pos_ls[i]
            current_pos = [db.r_iiwa_x, db.r_iiwa_y, db.r_iiwa_z, db.r_iiwa_a, db.r_iiwa_b, db.r_iiwa_g,db.r_iiwa_o]
            print("Go to #", i, "Point", target_pos)
            while (funcs.check_xyzabgo_same(target_pos, current_pos, xyz_single_error=15,
                                           abg_single_error=0.15,o_error=70) == False):
                if (self.db.EmergencySTOP_Sig):
                    break
                self.pos_control(sp_x=target_pos[0], sp_y=target_pos[1], sp_z=target_pos[2],
                               sp_a=target_pos[3], sp_b=target_pos[4], sp_g=target_pos[5], sp_o=target_pos[6])
                self.op.publish()
                # if((target_pos[6]-gripper_last)>50):#gripping detected
                #     time.sleep(5)

                gripper_last=target_pos[6]
                # if(abs(target_pos[6]-db.r_iiwa_o)>30):
                #     time.sleep(1)
                current_pos = [db.r_iiwa_x, db.r_iiwa_y, db.r_iiwa_z, db.r_iiwa_a, db.r_iiwa_b, db.r_iiwa_g,db.r_iiwa_o]
                time.sleep(0.1)
        self.db.blocked=0
    def do_go_to_xy_then_pick(self, x, y):

        print("I'm now doing do_go_to_xy_then_pick")
        # self.db.finished_pick_and_place = 0
        target_pos_ls = []
        # x=655 #y=229
        target_pos_ls.append([x, y, 216, -0.8, 0.056, -1.93, 10])  # 1
        target_pos_ls.append([x, y, 216, -0.8, 0.056, -1.93, 10])  # 2#6
        target_pos_ls.append([x, y, 83, -0.74, 0.08, -1.93, 10])  # 3 #height 76
        target_pos_ls.append([x, y, 83, -0.74, 0.08, -1.93, 113])  # 4
        target_pos_ls.append([x, y, 376, -0.74, 0.08, -1.93, 113])  # 5
        target_pos_ls.append([691, -0, 312, -0.76, 0.058, -1.9, 113])  # 6
        target_pos_ls.append([691, -0, 83, -0.76, 0.058, -1.9, 113])  # 7
        target_pos_ls.append([691, -0, 83, -0.76, 0.058, -1.9, 10])  # 8
        target_pos_ls.append([691, -0, 330, -0.76, 0.08, -1.9, 10])  # 9
        self.do_pos_sequence(target_pos_ls) #block pid


        print("finish go_to_xy_then_pick", "x=", x, "y=", y)
        self.db.finished_pick_and_place = 1
        self.db.pose_pid_control_able = 0
        return True
    def do_go_to_xy_only_pick(self, x, y):
        # self.db.finished_pick_and_place = 0
        print("im doing only pick")
        target_pos_ls = []
        # x=655 #y=229
        # target_pos_ls.append([x, y, 216, -0.8, 0.056, -1.93, 10])  # 1
        # target_pos_ls.append([x, y, 216, -0.8, 0.056, -1.93, 10])  # 2#6
        target_pos_ls.append([x, y, 87, -0.74, 0.08, -1.93, 10])  # 3
        target_pos_ls.append([x, y, 87, -0.74, 0.08, -1.93, 113])  # 4
        target_pos_ls.append([x, y, 376, -0.74, 0.08, -1.93, 113])  # 5
        # target_pos_ls.append([691, -116, 312, -0.76, 0.058, -1.9, 150])  # 6
        # target_pos_ls.append([691, -116, 73, -0.76, 0.058, -1.9, 150])  # 7
        # target_pos_ls.append([691, -116, 73, -0.76, 0.058, -1.9, 10])  # 8
        # target_pos_ls.append([691, -116, 274, -0.76, 0.08, -1.9, 10])  # 9
        self.do_pos_sequence(target_pos_ls)
        print("finish go_to_xy_then_pick", "x=", x, "y=", y)
        self.db.finished_only_pick = 1
        return True
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
        target_pos_ls.append([x, y, 312, -0.76, 0.058, -1.9, 113])  # 6
        target_pos_ls.append([x, y, 93, -0.76, 0.058, -1.9, 113])  # 7
        target_pos_ls.append([x, y, 93, -0.76, 0.058, -1.9, 10])  # 8
        target_pos_ls.append([x, y, 274, -0.76, 0.08, -1.9, 10])  # 9
        self.do_pos_sequence(target_pos_ls)
        print("finish go_to_xy_then_pick", "x=", x, "y=", y)
        self.db.finished_only_place = 1
        self.db.finished_only_pick = 1
        self.db.pose_pid_control_able = 0 #this is to block pid, wait for ui to restart
        return True



    def do_go_to_target_obj(self,target_name,error_allow_list_in_iiwabase,bias_list_in_iiwaBase=[0,0,0]):
        mission_finished = 0
        db = self.db
        while (1):
            if (self.db.EmergencySTOP_Sig):
                break
            # print(db.get_target_cam_data_list(target_name))
            cam_target_updated = db.get_target_cam_data_list(target_name)[0]
            cam_target_x = db.get_target_cam_data_list(target_name)[1]
            cam_target_y = db.get_target_cam_data_list(target_name)[2]
            cam_target_z = db.get_target_cam_data_list(target_name)[3]
            if (db.cam_iiwa_updated and cam_target_updated):
                pass
            else:
                if (db.cam_iiwa_updated == 0):
                    pass
                    print("Wait for cam iiwa data updating")
                if (cam_target_updated == 0):
                    pass
                    print("Wait for cam " + target_name + " data updating")
                time.sleep(0.1)
                continue
            # print("in mission loop ")
            target_x_iiwaBse_add=bias_list_in_iiwaBase[0]
            target_y_iiwaBse_add=bias_list_in_iiwaBase[1]
            target_z_iiwaBse_add = bias_list_in_iiwaBase[2]
            pos_error_cam = [-(db.cam_iiwa_x - cam_target_x-target_y_iiwaBse_add), -(db.cam_iiwa_y - cam_target_y + target_z_iiwaBse_add),
                             -(db.cam_iiwa_z - cam_target_z+target_x_iiwaBse_add)]
            pos_error_iiwaBase = db.coordinate_cam_2_iiwaBase(pos_error_cam)
            error_allow_list = error_allow_list_in_iiwabase  # m
            # print("pos_error_cam",pos_error_cam)
            # print("pos_error_iiwaBase",pos_error_iiwaBase)

            # #if xy in acceptable error, do grasp behavior
            if (funcs.check_xyz_abs_error_ok(error_list=pos_error_iiwaBase,
                                         allow_list=error_allow_list)):  # at the correct place, ready to pick up
                if (self.db.EmergencySTOP_Sig):
                    break
                print("Error_Check_Passed!")
                mission_finished = 1
                # grasp_and_place_finished=self.do_go_to_xy_then_pick(db.r_iiwa_x, db.r_iiwa_y)
                # main_thread = threading.Thread(target=ct.do_go_to_xy_then_pick, args=(db.r_iiwa_x, db.r_iiwa_y))
                # main_thread.start()
                pass
            #
            if (mission_finished):
                # print("Finished!")
                break
            self.pos_pid_control(dx=pos_error_iiwaBase[0], dy=pos_error_iiwaBase[1], dz=pos_error_iiwaBase[2]*0.3, P_gain=160, I_gain=0, D_gain=0)


            self.op.SendSPtoIIWA()
        return mission_finished

    def do_go_to_target_obj_Mission4_with_feast_detection(self, target_name, error_allow_list_in_iiwabase, bias_list_in_iiwaBase=[0, 0, 0]):
        mission_finished = 0
        db = self.db
        while (1):
            if (self.db.EmergencySTOP_Sig):
                break
            # print(db.get_target_cam_data_list(target_name))
            cam_target_updated = db.get_target_cam_data_list(target_name)[0]
            cam_target_x = db.get_target_cam_data_list(target_name)[1]
            cam_target_y = db.get_target_cam_data_list(target_name)[2]
            cam_target_z = db.get_target_cam_data_list(target_name)[3]
            if (db.cam_iiwa_updated and cam_target_updated):
                pass
            else:
                if (db.cam_iiwa_updated == 0):
                    pass
                    print("Wait for cam iiwa data updating")
                if (cam_target_updated == 0):
                    pass
                    print("Wait for cam " + target_name + " data updating")
                time.sleep(0.1)
                continue
            # print("in mission loop ")
            target_x_iiwaBse_add = bias_list_in_iiwaBase[0]
            target_y_iiwaBse_add = bias_list_in_iiwaBase[1]
            target_z_iiwaBse_add = bias_list_in_iiwaBase[2]
            pos_error_cam = [-(db.cam_iiwa_x - cam_target_x - target_y_iiwaBse_add),
                             -(db.cam_iiwa_y - cam_target_y + target_z_iiwaBse_add),
                             -(db.cam_iiwa_z - cam_target_z + target_x_iiwaBse_add)]
            pos_error_iiwaBase = db.coordinate_cam_2_iiwaBase(pos_error_cam)
            error_allow_list = error_allow_list_in_iiwabase  # m
            # print("pos_error_cam",pos_error_cam)
            # print("pos_error_iiwaBase",pos_error_iiwaBase)

            # #if xy in acceptable error, do grasp behavior
            if (funcs.check_xyz_abs_error_ok(error_list=pos_error_iiwaBase,
                                             allow_list=error_allow_list)):  # at the correct place, ready to pick up
                if (self.db.EmergencySTOP_Sig):
                    break
                print("Error_Check_Passed!")
                mission_finished = 1
                # grasp_and_place_finished=self.do_go_to_xy_then_pick(db.r_iiwa_x, db.r_iiwa_y)
                # main_thread = threading.Thread(target=ct.do_go_to_xy_then_pick, args=(db.r_iiwa_x, db.r_iiwa_y))
                # main_thread.start()
                pass
            #
            if (mission_finished):
                print("Finished!")
                break
            self.pos_pid_control(dx=pos_error_iiwaBase[0], dy=pos_error_iiwaBase[1], dz=pos_error_iiwaBase[2] * 0.3,
                                 P_gain=160, I_gain=0, D_gain=0)
            #feat detection
            if(self.db.cam_isfeast):
                self.set_gripper(GRIP=1)
                # self.set_gripper()
            else:
                self.set_gripper(GRIP=0)
            self.op.SendSPtoIIWA()
        return mission_finished

    def do_fetch_target_item(self,target_name):
        grasp_and_place_finished=0
        db=self.db
        while(1):
            if(self.db.EmergencySTOP_Sig):
                break
            # print(db.get_target_cam_data_list(target_name))
            cam_target_updated=db.get_target_cam_data_list(target_name)[0]
            cam_target_x=db.get_target_cam_data_list(target_name)[1]
            cam_target_y=db.get_target_cam_data_list(target_name)[2]
            cam_target_z=db.get_target_cam_data_list(target_name)[3]
            if(db.cam_iiwa_updated and cam_target_updated):
                pass
            else:
                if(db.cam_iiwa_updated==0):
                    pass
                    print("Wait for cam iiwa data updating")
                if(cam_target_updated==0):
                    pass
                    print("Wait for cam "+target_name+" data updating")
                time.sleep(0.1)
                continue
            # print("in mission loop ")
            target_z_iiwaBse_add = 0.3
            pos_error_cam = [-(db.cam_iiwa_x - cam_target_x), -(db.cam_iiwa_y - cam_target_y - target_z_iiwaBse_add),
                             -(db.cam_iiwa_z - cam_target_z)]
            pos_error_iiwaBase = db.coordinate_cam_2_iiwaBase(pos_error_cam)
            error_allow_list = [0.02, 0.02, 0.8]  # m
            # print("pos_error_cam",pos_error_cam)
            # print("pos_error_iiwaBase",pos_error_iiwaBase)

            #if xy in acceptable error, do grasp behavior
            if  (funcs.check_xyz_abs_error_ok(error_list=pos_error_iiwaBase,
                                         allow_list=error_allow_list)):  # at the correct place, ready to pick up
                # print("Error_Check_Passed!")

                grasp_and_place_finished=self.do_go_to_xy_only_pick(db.r_iiwa_x, db.r_iiwa_y)
                # main_thread = threading.Thread(target=ct.do_go_to_xy_then_pick, args=(db.r_iiwa_x, db.r_iiwa_y))
                # main_thread.start()
                pass
            if(grasp_and_place_finished):
                print("MISSION 1 Finished!")
                break
            self.pos_pid_control(dx=pos_error_iiwaBase[0], dy=pos_error_iiwaBase[1], dz=0, P_gain=160, I_gain=0, D_gain=0)
            self.op.SendSPtoIIWA()

    #missions, only one mission runs in a main loop.
    def holding_at_safe_pos(self):
        while(1):
            if(self.db.EmergencySTOP_Sig):
                continue
            if(self.db.holding_at_safe_pos_switch==True):
                pass
            else:
                time.sleep(0.5)

            safe_pos=self.db.get_safe_poses()
            spx=safe_pos[0]
            spy=safe_pos[1]
            spz=safe_pos[2]
            spa=safe_pos[3]
            spb=safe_pos[4]
            spg=safe_pos[5]
            spo=safe_pos[6]
            self.pos_control(sp_x=spx,sp_y=spy,sp_z=spz,sp_a=spa,sp_b=spb,sp_g=spg,sp_o=spo)
            time.sleep(0.5)
            self.op.SendSPtoIIWA()

    def Mission1_Pick_and_Place(self,target_name):
        self.db.publish_holding_at_safe_pose_switch(0)
        self.db.publish_inMission(1)
        # self.db.finished_pick_and_place = 0
        grasp_and_place_finished=0
        db=self.db
        while(1):
            if(self.db.EmergencySTOP_Sig):
                break
            # print(db.get_target_cam_data_list(target_name))
            cam_target_updated=db.get_target_cam_data_list(target_name)[0]
            cam_target_x=db.get_target_cam_data_list(target_name)[1]
            cam_target_y=db.get_target_cam_data_list(target_name)[2]
            cam_target_z=db.get_target_cam_data_list(target_name)[3]
            if(db.cam_iiwa_updated and cam_target_updated):
                pass
            else:
                if(db.cam_iiwa_updated==0):
                    pass
                    print("Wait for cam iiwa data updating")
                if(cam_target_updated==0):
                    pass
                    print("Wait for cam "+target_name+" data updating")
                time.sleep(0.1)
                continue
            # print("in mission loop ")
            target_z_iiwaBse_add = 0.3
            pos_error_cam = [-(db.cam_iiwa_x - cam_target_x), -(db.cam_iiwa_y - cam_target_y - target_z_iiwaBse_add),
                             -(db.cam_iiwa_z - cam_target_z)]
            pos_error_iiwaBase = db.coordinate_cam_2_iiwaBase(pos_error_cam)
            error_allow_list = [0.02, 0.02, 0.8]  # m
            # print("pos_error_cam",pos_error_cam)
            # print("pos_error_iiwaBase",pos_error_iiwaBase)

            #if xy in acceptable error, do grasp behavior
            if  (funcs.check_xyz_abs_error_ok(error_list=pos_error_iiwaBase,
                                         allow_list=error_allow_list)):  # at the correct place, ready to pick up
                print("Error_Check_Passed!")

                grasp_and_place_finished=self.do_go_to_xy_then_pick(db.r_iiwa_x, db.r_iiwa_y)
                # main_thread = threading.Thread(target=ct.do_go_to_xy_then_pick, args=(db.r_iiwa_x, db.r_iiwa_y))
                # main_thread.start()
                pass
            if(grasp_and_place_finished):
                print("MISSION 1 Finished!")
                break
            self.pos_pid_control(dx=pos_error_iiwaBase[0], dy=pos_error_iiwaBase[1], dz=0, P_gain=160, I_gain=0, D_gain=0)
            self.op.SendSPtoIIWA()
        self.db.publish_inMission(0)
        self.db.publish_holding_at_safe_pose_switch(1)
    def Start_Mission1(self,target_name):
        # if(MissionNum==1):
        doMission1_thread=threading.Thread(target=self.Mission1_Pick_and_Place,args=(target_name,))
        doMission1_thread.start()
        # self.db.publish_holding_at_safe_pose_switch(0)
        # self.ct.Mission1_Pick_and_Place(target_name)
        # self.db.publish_holding_at_safe_pose_switch(1)

    def Mission2_Obj_Tracking(self,target_name,keep_doing):
        self.db.publish_holding_at_safe_pose_switch(0)
        self.db.publish_inMission(1)
        # mission_finished=0
        while(keep_doing):
            if(self.db.EmergencySTOP_Sig):
                break
            self.do_go_to_target_obj(target_name=target_name,bias_list_in_iiwaBase=[0,0.05,0.05],error_allow_list_in_iiwabase=[0.1,0.1,0.15])
        self.db.publish_inMission(0)
        self.db.publish_holding_at_safe_pose_switch(1)
    def Start_Mission2(self,target_name,keep_doing):
        # if(MissionNum==1):
        doMission2_thread=threading.Thread(target=self.Mission2_Obj_Tracking,args=(target_name,keep_doing,))
        doMission2_thread.start()

    def Mission3_HandMeSth(self,target_name):
        self.db.publish_holding_at_safe_pose_switch(0)
        self.db.publish_inMission(1)
        mission_finished=0

        #go grasp

        self.do_fetch_target_item(target_name)
        #put on hand
        # self.do_go_to_target_obj(target_name=target_name, bias_list_in_iiwaBase=[0, 0.05, 0.12],
        #                          error_allow_list_in_iiwabase=[0.15, 0.15, 0.15])
        self.do_go_to_target_obj(target_name="hand", bias_list_in_iiwaBase=[0.06, 0, 0.1],
                                 error_allow_list_in_iiwabase=[0.08, 0.08, 0.15])

        #release
        # self.set_gripper(0)
        self.do_gripper_fully(last_time=1.5,grip_value=0)

        self.db.publish_inMission(0)
        self.db.publish_holding_at_safe_pose_switch(1)
    def Start_Mission3(self,target_name):
        # if(MissionNum==1):
        doMission3_thread=threading.Thread(target=self.Mission3_HandMeSth,args=(target_name,))
        doMission3_thread.start()


    def Mission4_HandRemoteControl(self):
        self.db.publish_holding_at_safe_pose_switch(0)
        self.db.publish_inMission(1)
        # mission_finished=0
        target_name="hand"
        while (1):
            if (self.db.EmergencySTOP_Sig):
                break
            self.do_go_to_target_obj_Mission4_with_feast_detection(target_name=target_name, bias_list_in_iiwaBase=[0, -0.40,-0.15],
                                     error_allow_list_in_iiwabase=[0.05, 0.05, 0.05])
        self.db.publish_inMission(0)
        self.db.publish_holding_at_safe_pose_switch(1)

    def Start_Mission4(self):
        # if(MissionNum==1):
        doMission4_thread = threading.Thread(target=self.Mission4_HandRemoteControl, args=())
        doMission4_thread.start()

    def EmergencySTOP(self):
        self.db.EmergencySTOP_Sig=1
    def EmergencySTOP_recover(self):
        self.db.EmergencySTOP_Sig=0

# la=[100,100,100,1.5,1,1]
# lb=[90,100,100,1,1,1]
# print(funcs.check_xyzabg_same(la,lb,xyz_single_error=11,abg_single_error=0.5))


# Main has no use, if you dont need it.
if __name__=="__main__":
    db = global_database()
    operator = operator(db)
    # operator.send_server_start() #no auto send. use manual
    operator.receive_server_start()
    ct=controller(db,operator)

    u=3
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
