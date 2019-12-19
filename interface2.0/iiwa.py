#Chen Yiwen (e0452765@u.nus.edu)
#Connect Me, If there is any issue
#updating log:
#2.0:
#   1.Force ruled control
#   2.Push
#   3.Screw
#   4.get_force

#!/usr/bin/env python

# import rospy
# import urx
# import math3d as m3d
# from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
# import copy
import time
import CYW_RemoteControl
from threading import Thread
#import CYW_RemoteControl

# HOMEJ = [0.7854, -2.0944, -1.0472, -1.5708, 1.5708, -1.5708]
# ACCE = 0.1
# VELO = 0.2
# TOL_TARGET_POSE = 0.002
TOOL_RANGE = [-3.14, 3.14]
TOOL_RANGE = [-3.05, 3.05]
poses_test = [
    [-0.1, -0.49, -0.23, 0, 0, 0],
    [-0.1, -0.49, 0.09, 0, 0, 0],
    [0.2, -0.70, -0.23, 0, 0, 0],
    [0.2, -0.70, -0.2, 0, 0, 0],
]
ACCE = 0.1
VELO = 0.002
TOL_TARGET_POSE = 0.002
class Interface:
    def __init__(self):

        self.db = CYW_RemoteControl.global_database()
        self.op = CYW_RemoteControl.operator(global_db=self.db)
        self.ct = CYW_RemoteControl.controller(self.db, self.op)
        # start to receive data from iiwa . Make sure YW_UDP_Server.java is running on the IIWA
        self.op.receive_server_start()
        # start to send msg to iiwa. This is for build continues connection between IIWA.
        self.op.send_server_start()
        print("IIWA INTERFACE START!")
        self.target_gripper = 1

        # robot init
        # print('Homing robot...')
        # self.gripper.open_gripper()
        self.move_home()
        # self.state_gripper, self.target_gripper = 0, 0
        # self.process_gripper = Thread(target=self._set_gripper)
        # self.target_pose = self.get_tcp_pose()
        self.target_tool = self.get_tool_rot()
        # print('Robot ready!')

        # force monitoring
        self.process_force = Thread(target=self._watch_force)
        self.input_force = False
        self.process_push = Thread(target=self._watch_push)
        self.push_stopped = 0
        # self.timeout_push = None
        # self.offset_force = self.get_force_raw()
    def move_home(self):
        print("move home")
        self.move_tcp_absolute(self.db.get_safe_poses())
    def movj(self,joints,acc,velo):
        velo_list=[velo for i in range(7)]
        print(velo_list)
        # print(velo_list)
        # acc=None
        print("movj joints",joints)
        print("required joints",joints)
        self.ct.joints_control(joints,velo_list)
        print(self.db.form_sp_Str())

    def stopj(self,test_num):
        # print("stop j")
        """
        stop movement
        :param test_num: no use
        :return:
        """
        # joints=self.db.get_read_joints()

        # print("stopj canceled")
        self.ct.stopj()


    def move_tcp_absolute(self, pose):
        '''
        move eff to absolute pose in robot base frame
        :param pose: list [x y z R P Y],
        :param wait: blocking wait (Boolean)
        :return: None
        pose = [x y z R P Y] (x, y, z in m) (R P Y in rad)
        '''

        self.ct.pos_control(sp_x=pose[0]*1000,sp_y=pose[1]*1000,sp_z=pose[2]*1000,sp_a=pose[3],sp_b=pose[4],sp_g=pose[5],sp_o=self.db.r_iiwa_o)
    def set_gripper(self, val):
        '''
        gripper control (Blocking wait)
        :param val: False:RELEASE, True:GRIP
        :return: None

        val = true or false

        '''
        #6 open val=false
        #113 close val=true
        # print("set gripper",val)
        if self.target_gripper != val:
            self.target_gripper = val
        if val:
            # self.gripper.close_gripper()
            # pose_read=self.db.get_read_poses() #this is for keep xyz raw pitch yaw keeps the same.
            self.db.iiwa_o_sp=113
            #self.ct.pos_control(sp_x=pose_read[0],sp_y=pose_read[1],sp_z=pose_read[2],sp_a=pose_read[3],sp_b=pose_read[4],sp_g=pose_read[5],sp_o=113)
        else:
            # pose_read=self.db.get_read_poses()
            self.db.iiwa_o_sp=6
            #self.ct.pos_control(sp_x=pose_read[0],sp_y=pose_read[1],sp_z=pose_read[2],sp_a=pose_read[3],sp_b=pose_read[4],sp_g=pose_read[5],sp_o=6)
            # self.gripper.open_gripper()
        # self.op.SendSPtoIIWA()
    def rot_tool(self, val):
        """
        rotate wrist_3 joint
        :param val: float (0 to 1)
        :return: None
        """
        # print("rot_tool, val=",val)
        # print("rot_tool check:",(self.is_program_running() and
        #     ((val - self.target_tool) ** 2) ** 0.5 > TOL_TARGET_POSE) or \
        #         (not self.is_program_running() and
        #          ((val - self.get_tool_rot()) ** 2) ** 0.5 > TOL_TARGET_POSE))
        # if (self.is_program_running() and
        #     ((val - self.target_tool) ** 2) ** 0.5 > TOL_TARGET_POSE) or \
        #         (not self.is_program_running() and
        #          ((val - self.get_tool_rot()) ** 2) ** 0.5 > TOL_TARGET_POSE):

        self.target_tool = val
        # joints = self.getj()
        #
        # joints[6] = (TOOL_RANGE[1] - TOOL_RANGE[0]) * val + TOOL_RANGE[0]
        self.ct.rot_tool(val,TOOL_RANGE)
        # self.movj(joints, ACCE * 4, 0.002*6)

    def get_tool_rot(self):
        """
        get wrist_3 joint value
        :return: float (0 to 1)
        """
        val = self.getj()[6]
        res=(min(max(val, TOOL_RANGE[0]), TOOL_RANGE[1]) - TOOL_RANGE[0]) / (TOOL_RANGE[1] - TOOL_RANGE[0])
        # print("get_tool_rot",res)
        return res#缩放，-2pi ~ 2pi 等比缩放
    def getj(self):
        return self.db.r_iiwa_js
    def is_program_running(self):
        return True
    def get_tcp_pose(self):
        '''
        get eff pose
        :return: list [x y z R P Y]
        '''
        pose=self.db.get_read_poses()[:6]
        pose[0]=pose[0]/1000
        pose[1]=pose[1]/1000
        pose[2]=pose[2]/1000
        return pose
    def get_gripper(self):
        """
        get gripper status
        :return: Boolean (0 opened / 1 closed)
        """
        #6 open val=false
        #113 close val=true
        res=self.db.get_read_poses()[6] > 90
        # print("gripper:", res)
        # print("gripper:",self.db.get_read_poses()[6])
        return res
    def get_force(self,wait=True):
        """
        :return:force magnitude
        """
        # f=self.get_force_list()[2]
        f=self.get_force_list()
        res=(f[0]**2+f[1]**2+f[2]**2)**(0.5)
        # res-=self.offset_force
        return res
    def get_force_raw(self):
        f = self.get_force_list()[2]
        # f=self.get_force_list()[:3]
        # res=(f[0]**2+f[1]**2+f[2]**2)**(0.5)
        return f
    def get_force_list(self):
        """
        :return:force: list [ForceX ForceY ForceZ TorqueX TorqueY TorqueZ]
        """
        return [self.db.r_iiwa_FX,self.db.r_iiwa_FY,self.db.r_iiwa_FZ,self.db.r_iiwa_TX,self.db.r_iiwa_TY,self.db.r_iiwa_TZ]


    def wait_push_input(self, force):
        """
        wait for push input
        require calling get_push_input to reset before reuse
        :param force: minimum amount of force required (newton)
        :return: None
        """
        if not self.process_force.isAlive() and not self.input_force:
            self.stopj(5)
            time.sleep(1)
            th_force = self.get_force(wait=True) + force
            self.process_force = Thread(target=self._watch_force, args=(th_force,))
            self.process_force.start()
    def get_push_input(self):
        """
        get if a push input has been registered
        :return: boolean (True:Yes, False:No)
        """
        if self.input_force:
            self.input_force = False
            return True
        else:
            return False

    # def waitfor_push(self, force):
    #     """
    #     wait for push input
    #     require calling get_push_input to reset before reuse
    #     :param force: minimum amount of force required (newton)
    #     :return: None
    #     """
    #     if not self.process_force.isAlive() and not self.input_force:
    #         print("waiting!")
    #         # self.rob.stopj(5) # to stop robot
    #         time.sleep(1)
    #         th_force = self.get_force() + force
    #         self.process_force = Thread(target=self._watch_force, args=(th_force,))
    #         self.process_force.start()

    def _get_tcp_state(self):
        return self.get_tcp_pose()[:3] + [self.getj()[6]]

    def _watch_push(self, duration, pose0, max_dist):
        time0 = time.time()
        cnt_stopped = 0
        push_stopped = False
        pose1_ = self._get_tcp_state()
        # print(pose1_)
        pose1_ = [pose1_ for _ in range(10)]
        # print()
        # while time.time() - time0 < duration:
        while 1:
            pose1 = self._get_tcp_state()
            time.sleep(0.001)
            # print("current posel",pose1)
            error_pose=[pose1[i]-pose0[i] for i in range(len(pose0))]
            # print("max dist",max_dist)
            # print("error_pose",error_pose)
            # max displacement check
            for i in range(4):
                # print("pose error",pose1[i] - pose0[i]-max_dist[i])
                if (max_dist[i] > 0 and pose1[i] - pose0[i] > 0.9*max_dist[i]) or \
                   (max_dist[i] < 0 and pose1[i] - pose0[i] < 0.9*max_dist[i]):
                    push_stopped = True
                    break
            if push_stopped:
                # print("push_stoped")
                # print('max_dist')
                # self.rob.send_program('end_force_mode()')
                self.stopj(2)
                self.push_stopped = 1
                # break

            # stationary check
            # old dis check==0.0001
            if self.dist(pose1, pose1_.pop(0)) < 0.01 and \
               self.dist(pose1, pose0) > 0.001:
                cnt_stopped += 1
            else:
                cnt_stopped = 0
            # print("cnt_stopped",cnt_stopped)
            if cnt_stopped > 128:
                print('stationary')
                # self.rob.send_program('end_force_mode()')
                self.stopj(2)
                self.push_stopped = 2
                break
            pose1_.append(pose1)
    def dist(self,pose1,pose2):
        a=pose1[0]-pose2[0]
        b=pose1[1]-pose2[1]
        c=pose1[2]-pose2[2]
        d=pose1[3]-pose2[3]
        dis=(a*a+b*b+c*c)**0.5
        # print("dis:",dis)
        # e=pose1[4]-pose2[4]
        # f=pose1[5]-pose2[5]
        return (a*a+b*b+c*c)**0.5#+(d*d)**0.5
    def _watch_force(self, th_force):
        time0 = time.time()
        while time.time() - time0 < 5:  # 5 seconds input window
            # print("watching force...")
            force = self.get_force()
            if force > th_force:
                self.input_force = True
                print("Force Dected!!")
                break
    def screw(self, cw):
        """
        applying downward force and torque for a duration
        :param cw: boolean (False:clockwise, True:counter-clockwise)
        :param duration: float (second)
        :return: boolean (False:moving, True:done)
        """
        # return self.push([0.0, 0.0, 20.0,  0.0, 0, 2.0 if cw else -2.0], duration)
        # return self.push([0.0, 0.0, 20.0, 2.0 if cw else -2.0, 0.0, 0], duration)
        #[ 0,0,20,2,0,0] iiw
        #[ 0,0,20,0,0,2] ur
        val = self.getj()[6]
        return self.push([0, 0, 20, 2 if cw else -2],
                         [0, 0, 0, (TOOL_RANGE[1] - val) if cw else (TOOL_RANGE[0] - val)])

    def get_push(self):
        """
        get if push has completed
        :return: int (0:No, 1:max distance reached, 2:force acquired)
        """
        if self.push_stopped:
            val = self.push_stopped
            self.push_stopped = 0
            return val
        else:
            return 0
    def get_push_timeout(self):
        if self.timeout_push is None:
            return False
        elif time.time() > self.timeout_push:
            self.timeout_push = None
            return True
        else:
            return False

    # def push(self, force, duration):
    # # def push(self, force):#force: list (x y z R P Y) # max distence to travel, distance limit #
    #     """
    #     apply force and/or torque in 6 dimensions for a duration
    #     require calling get_push to reset before reuse
    #     :param force: list (x y z R P Y) (newton, newton meter)
    #     :param duration: float (second)
    #     :return: boolean (False:moving, True:done)
    #     """
    #     if self.timeout_push is None:
    #         self.timeout_push = time.time() + duration + 2  # 2 seconds are the sleeps in force program
    #         self.offset_force = self.get_force()
    #         self._force_mode_start(force, duration, (0.01, 0.03), (0.02, 0.4), 0)

    def push(self, force, max_dist):
        """
        initiate applying force and/or torque in 4 dimensions
        require calling get_push to reset before reuse
        :param force: list (x y z R) (newton, newton meter)
        :param max_dist: list (x y z R) maximum travel in each dimensions (meter, radian)
        :return: None
        """
        if not self.process_push.isAlive():#and not self.push_stopped:
            print("push start!")
            self.stopj(5)
            time.sleep(1)
            self.process_push = Thread(target=self._watch_push, args=(None, self._get_tcp_state(), max_dist))
            self._force_mode_start(force, max_dist)
            self.process_push.start()

    def _force_mode_start(self, force, maxdist, duration=None, deviation=None, speed=None, damp=None):
        force = force[:3] + [0, 0] + [force[-1]]
        maxdist = maxdist[:3] + [0, 0] + [maxdist[-1]]
        axis = [0 if i == 0 else 1 for i in force]
        pose=self.get_tcp_pose()
        # print("_force_mode_start pose",pose)
        print("original pose",pose)
        print("_force_mode_start maxdist",maxdist)
        goalpose=[0 for i in range(6)]
        for i in range(len(force)):
            goalpose[i]=axis[i]*maxdist[i]+pose[i]
        blending=self.db.get_safe_blending()
        goalpose[0]=goalpose[0]*1000
        goalpose[1]=goalpose[1]*1000
        goalpose[2]=goalpose[2]*1000
        print("goalpose",goalpose)
        self.ct.maxforce_ptpmove(goalpose=goalpose,maxforce=force,blending=blending,Jointspeed=0.05)

    def disconnect(self):
        return True
        # self.rob.send_program(prog)

if __name__=="__main__":
    interface=Interface()
    print("\n\nREAD ME:",
          "\n1. Upload 'YW_UDP_Server.java' and 'YW_UDPThread.java' into IIWA applications",
          "\n2. PC change IP to 172.31.1.40 or corresponding UDP IP. Customised IP config see Interface.op.__init__.",
          "\n3. IIWA: Run 'YW_UDP_Server.java'",
          "\n4. PC: Run 'interface_iiwa_ChenYiwen.py'",
          "\n5. Any issues, connect to author for help: e0452765@u.nus.edu (Chen Yiwen)")
    while(1):
        cmd_str="\n---------\nThis is a test for interface\nInput test number:" \
                "\nGO to Safe Pose:10/11    " \
                "\nGripper Release/Grip: 20/21. " \
                "\nGet Pose:3 / Get Gripper:4" \
                "\nGet_force_list:50,  get_force Z:51"
        cmd_str+="\nmovj:60/61"
        cmd_str+="\nptp force control:70 71"
        cmd_str+="\nget_tool_rot 80 , getj 81 , rot_tool 82~84 ,stopj 85 "
        cmd_str+="\n100 screw test"
        cmd_str+="\n---------"
        command=input(cmd_str)
        if(command=='10'):
            pose=interface.db.get_safe_poses()
            pose[:3]=[pose[0]/1000,pose[1]/1000,pose[2]/1000]

            print(pose)
            interface.move_tcp_absolute(pose=pose)
            #interface.move_tcp_absolute(pose=pose,wait=None)
        if(command=='11'):
            pose=interface.db.get_safe_poses()

            print(pose)
            pose[:3] = [pose[0] / 1000, pose[1] / 1000, pose[2] / 1000]
            pose[0]=pose[0]+50/1000
            pose[1]=pose[1]+50/1000
            pose[2]=pose[2]+30/1000
            pose[3]=pose[3]+0.1
            pose[4]=pose[4]+0.1
            pose[5]=pose[5]+0.1
            print(pose)
            interface.move_tcp_absolute(pose=pose)
            #interface.move_tcp_absolute(pose=pose,wait=None)
        elif(command=='20'):
            interface.set_gripper(False)
        elif(command=='21'):
            interface.set_gripper(True)
        elif(command=='3'):
            print("tcp pose get:",interface.get_tcp_pose())
        elif(command=="4"):
            print("gripper get:",interface.get_gripper())
        elif(command=="50"):
            print("get_force_list",interface.get_force_list())
        elif(command=="51"):
            print("get_force",interface.get_force())
        elif(command=="60"):
            print("movj",interface.movj([0,0,0,0,0,0,0],acc=None,velo=VELO))
        elif(command=="61"):
            print("movj",interface.movj([0.3,0,0,0,0,0,0],acc=None,velo=VELO))
        elif(command=="70"):
            pose=interface.db.get_safe_poses()
            # pose[:3] = [pose[0] / 1000, pose[1] / 1000, pose[2] / 1000]
            stifs=[300,300,300,200,200,200]
            addforce=[0,0,0,0,0,0]
            speed=0.01
            interface.ct.ptp_force_control(pose=pose,stifs=stifs,addforce=addforce,speed=speed)
        elif(command=="71"):
            pose=interface.db.get_safe_poses()
            # pose[:3] = [pose[0] / 1000+0.1, pose[1] / 1000+0.1, pose[2] / 1000]
            # pose[0]-=130
            stifs=[1000,1000,1000,300,300,30]
            addforce=[0,0,0,0,0,3]
            speed=0.01
            interface.ct.ptp_force_control(pose=pose,stifs=stifs,addforce=addforce,speed=speed)
        elif(command=="80"):
            print("get_tool_rot",interface.get_tool_rot())
        elif (command == "81"):
            print("getj", interface.getj())
        elif (command == "82"):
            print("rot_tool", interface.rot_tool(0))
        elif (command == "83"):
            print("rot_tool", interface.rot_tool(0.5))
        elif (command == "84"):
            print("rot_tool", interface.rot_tool(1))
        elif(command=="85"):
            print("stop j",interface.stopj(5))
        elif(command=="101"):
            while(interface.get_push_timeout()==False):
                print("doing screw")
                interface.screw(1,3)
            print("screw finished")
        elif(command=="100"):
            interface.waitfor_push(5)
        elif(command=="102"):
            pass
### init
# (require '[libpython-clj.python :as py])
# (py/initialize!)
# (def py_class (py/import-module "src.rospy.interface"))
# (def obj_instance (py/call-attr py_class "Interface"))

### read eff pose
# (py/call-attr obj_instance "get_tcp_pose")

### gripper open & close
# (py/call-attr obj_instance "set_gripper" 0)
# (py/call-attr obj_instance "set_gripper" 1)

### move eff to absolute pose (blocking/non-blocking)
# (py/call-attr obj_instance "move_tcp_absolute" [0.21 0.54 0.05 -2.9 -1.2 0] 0)
# (py/call-attr obj_instance "move_tcp_absolute" [0.21 0.54 0.05 -2.9 -1.2 0] 1)

### ending
# (py/call-attr obj_instance "move_home" 1)
# (py/call-attr obj_instance "close_connection")

### point A, B, C, D
# [0.21 0.54 0.05 -2.9 -1.2 0]
# [0.21 0.54 0.18 -2.9 -1.2 0]
# [0.64 0.24 0.18 -2.9 -1.2 0]
# [0.64 0.24 0.12 -2.9 -1.2 0]
