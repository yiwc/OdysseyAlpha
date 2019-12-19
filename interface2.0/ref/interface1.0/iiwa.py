#Chen Yiwen (e0452765@u.nus.edu)
#Connect Me, If there is any issue

#!/usr/bin/env python

# import rospy
# import urx
# import math3d as m3d
# from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
# import copy

from . import CYW_RemoteControl
#import CYW_RemoteControl

HOMEJ = [0.7854, -2.0944, -1.0472, -1.5708, 1.5708, -1.5708]
ACCE = 0.1
VELO = 0.2
TOL_TARGET_POSE = 0.002


class Interface:
    def __init__(self):
        # init temp db
        print("Point 0")
        self.db = CYW_RemoteControl.global_database()
        print("Point 1")
        # init operator
        self.op = CYW_RemoteControl.operator(global_db=self.db)
        print("Point 2")
        # init controller
        self.ct = CYW_RemoteControl.controller(self.db, self.op)
        print("Point 3")
        
        # return
        # start to receive data from iiwa . Make sure YW_UDP_Server.java is running on the IIWA
        self.op.receive_server_start()
        print("Point 4")
        #return
        # start to send msg to iiwa. This is for build continues connection between IIWA.
        self.op.send_server_start()
        pass
        print("IIWA INTERFACE START!")

    #     rospy.init_node('interface')
    #
    #     # robot settings
    #     rospy.loginfo('Connecting robot...')
    #     self.rob = urx.Robot("192.168.1.5")
    #     self.rob.set_tcp((0, 0, 0.17, 0, 0, 0))
    #     self.rob.set_payload(1, (0, 0, 0.1))
    #     rospy.sleep(rospy.Duration(2))
    #     self.target_pose = self.get_tcp_pose()
    #
    #     # robot init
    #     rospy.loginfo('Homing robot...')
    #     self.gripper = Robotiq_Two_Finger_Gripper(self.rob)
    #     self.gripper.open_gripper()
        self.target_gripper = 0
    #
    #     # robot homing
    #     self.move_joint(HOMEJ, True)
    #     rospy.loginfo('Robot ready!')
    #(def py_class (py/import-module "src.rospy.interface"))
    #
    # def close_connection(self):
    #     '''
    #     close robot connection
    #     :return:
    #     '''
    #     self.rob.close()
    # def move_home(self, wait):
    #     '''
    #     move back to home
    #     :param wait: blocking wait (Boolean)
    #     :return:
    #     '''
    #     self.move_joint(HOMEJ, wait)
    # def move_joint(self, joints, wait):
    #     '''
    #     move joints
    #     :param joints: 6 joints values in radian
    #     :param wait: blocking wait (Boolean)
    #     :return:
    #     '''
    #     self.rob.movej(joints, ACCE, VELO, wait=wait)
    # def move_tcp_relative(self, pose, wait):
    #     '''
    #     move eff to relative pose
    #     :param pose: relative differences in [x y z R P Y] in meter and radian
    #     :param wait: blocking wait (Boolean)
    #     :return: None
    #     '''
    #     self.rob.add_pose_tool(m3d.Transform(pose), ACCE, VELO, wait=wait)

    def move_tcp_absolute(self, pose):
        '''
        move eff to absolute pose in robot base frame
        :param pose: list [x y z R P Y],
        :param wait: blocking wait (Boolean)
        :return: None

        pose = [x y z R P Y] (x, y, z in m) (R P Y in rad)
        '''
        #
        # if (self.is_program_running() and
        #         self.dist_linear(pose, self.target_pose) > TOL_TARGET_POSE) or \
        #    (not self.is_program_running() and
        #         self.dist_linear(pose, self.get_tcp_pose()) > TOL_TARGET_POSE):
        #     self.target_pose = pose
        #     self.rob.set_pose(m3d.Transform(pose), ACCE, VELO, wait)
        # print(pose)

        self.ct.pos_control(sp_x=pose[0]*1000,sp_y=pose[1]*1000,sp_z=pose[2]*1000,sp_a=pose[3],sp_b=pose[4],sp_g=pose[5],sp_o=self.db.r_iiwa_o)
        # self.op.SendSPtoIIWA()



    def set_gripper(self, val):
        '''
        gripper control (Blocking wait)
        :param val: False:RELEASE, True:GRIP
        :return: None

        val = true or false

        '''
        if self.target_gripper != val:
            self.target_gripper = val
            if val:
                # self.gripper.close_gripper()
                pose_read=self.db.get_read_poses() #this is for keep xyz raw pitch yaw keeps the same.
                self.db.iiwa_o_sp=113
                #self.ct.pos_control(sp_x=pose_read[0],sp_y=pose_read[1],sp_z=pose_read[2],sp_a=pose_read[3],sp_b=pose_read[4],sp_g=pose_read[5],sp_o=113)
            else:
                pose_read=self.db.get_read_poses()
                self.db.iiwa_o_sp=6
                #self.ct.pos_control(sp_x=pose_read[0],sp_y=pose_read[1],sp_z=pose_read[2],sp_a=pose_read[3],sp_b=pose_read[4],sp_g=pose_read[5],sp_o=6)
                # self.gripper.open_gripper()
            # self.op.SendSPtoIIWA()

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
        return self.db.get_read_poses()[6]>90


    #
    # def get_state(self):
    #     '''
    #     get eff and gripper state
    #     :return: list [x y z R P Y g]
    #     '''
    #     return self.get_tcp_pose() + [self.get_gripper()]
    #
    # def is_program_running(self):
    #     '''
    #     check if a program is already running
    #     :return: Boolean
    #     '''
    #     return self.rob.secmon.is_program_running()
    #
    # @staticmethod
    # def dist_joint(val1, val2):
    #     dist = 0
    #     for i in range(6):
    #         dist += (val1[i] - val2[i]) ** 2
    #     return dist ** 0.5
    #
    # @staticmethod
    # def dist_linear(val1, val2):
    #     dist = 0
    #     for i in range(3):
    #         dist += (val1[i] - val2[i]) ** 2
    #     for i in range(3, 6):
    #         dist += ((val1[i] - val2[i]) / 5) ** 2
    #     return dist ** 0.5

if __name__=="__main__":
    interface=Interface()
    print("\n\nREAD ME:",
          "\n1. Upload 'YW_UDP_Server.java' and 'YW_UDPThread.java' into IIWA applications",
          "\n2. PC change IP to 172.31.1.40 or corresponding UDP IP. Customised IP config see Interface.op.__init__.",
          "\n3. IIWA: Run 'YW_UDP_Server.java'",
          "\n4. PC: Run 'interface_iiwa_ChenYiwen.py'",
          "\n5. Any issues, connect to author for help: e0452765@u.nus.edu (Chen Yiwen)")
    while(1):
        command=input("\n---------\nThis is a test for interface\nInput test number:\n10. GO to Safe Pose \n11. Go to Safe Pose 2 \n20. Gripper Release \n21. Gripper Grip \n3.  Get Pose \n4.  Get Gripper:\n---------\n")
        if(command=='10'):
            pose=interface.db.get_safe_poses()
            interface.move_tcp_absolute(pose=pose)
            #interface.move_tcp_absolute(pose=pose,wait=None)
        if(command=='11'):
            pose=interface.db.get_safe_poses()
            pose[0]=pose[0]+50
            pose[1]=pose[1]+50
            pose[2]=pose[2]+30
            pose[3]=pose[3]+0.1
            pose[4]=pose[4]+0.1
            pose[5]=pose[5]+0.1
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
