#!/usr/bin/env python
import rospy
import urx
import math3d as m3d
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
import copy


HOMEJ = [0.7854, -2.0944, -1.0472, -1.5708, 1.5708, -1.5708]
ACCE = 0.1
VELO = 0.2
TOL_TARGET_POSE = 0.002


class Interface:
    def __init__(self):
        rospy.init_node('interface')

        # robot settings
        rospy.loginfo('Connecting robot...')
        self.rob = urx.Robot("192.168.1.5")
        self.rob.set_tcp((0, 0, 0.17, 0, 0, 0))
        self.rob.set_payload(1, (0, 0, 0.1))
        rospy.sleep(rospy.Duration(2))
        self.target_pose = self.get_tcp_pose()

        # robot init
        rospy.loginfo('Homing robot...')
        self.gripper = Robotiq_Two_Finger_Gripper(self.rob)
        self.gripper.open_gripper()
        self.target_gripper = 0

        # robot homing
        self.move_joint(HOMEJ, True)
        rospy.loginfo('Robot ready!')

    def close_connection(self):
        '''
        close robot connection
        :return:
        '''
        self.rob.close()

    def move_home(self, wait):
        '''
        move back to home
        :param wait: blocking wait (Boolean)
        :return:
        '''
        self.move_joint(HOMEJ, wait)

    def move_joint(self, joints, wait):
        '''
        move joints
        :param joints: 6 joints values in radian
        :param wait: blocking wait (Boolean)
        :return:
        '''
        self.rob.movej(joints, ACCE, VELO, wait=wait)

    def move_tcp_relative(self, pose, wait):
        '''
        move eff to relative pose
        :param pose: relative differences in [x y z R P Y] in meter and radian
        :param wait: blocking wait (Boolean)
        :return: None
        '''
        self.rob.add_pose_tool(m3d.Transform(pose), ACCE, VELO, wait=wait)

    def move_tcp_absolute(self, pose, wait):
        '''
        move eff to absolute pose in robot base frame
        :param pose: list [x y z R P Y]
        :param wait: blocking wait (Boolean)
        :return: None

        pose = [x y z R P Y] (x, y, z in m) (R P Y in rad)
        '''
        if (self.is_program_running() and
                self.dist_linear(pose, self.target_pose) > TOL_TARGET_POSE) or \
           (not self.is_program_running() and
                self.dist_linear(pose, self.get_tcp_pose()) > TOL_TARGET_POSE):
            self.target_pose = pose
            self.rob.set_pose(m3d.Transform(pose), ACCE, VELO, wait)

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
                self.gripper.close_gripper()
            else:
                self.gripper.open_gripper()

    def get_tcp_pose(self):
        '''
        get eff pose
        :return: list [x y z R P Y]
        '''
        return copy.deepcopy(self.rob.getl())

    def get_gripper(self):
        """
        get gripper status
        :return: Boolean (0 opened / 1 closed)
        """
        return self.target_gripper

    def get_state(self):
        '''
        get eff and gripper state
        :return: list [x y z R P Y g]
        '''
        return self.get_tcp_pose() + [self.get_gripper()]

    def is_program_running(self):
        '''
        check if a program is already running
        :return: Boolean
        '''
        return self.rob.secmon.is_program_running()

    @staticmethod
    def dist_joint(val1, val2):
        dist = 0
        for i in range(6):
            dist += (val1[i] - val2[i]) ** 2
        return dist ** 0.5

    @staticmethod
    def dist_linear(val1, val2):
        dist = 0
        for i in range(3):
            dist += (val1[i] - val2[i]) ** 2
        for i in range(3, 6):
            dist += ((val1[i] - val2[i]) / 5) ** 2
        return dist ** 0.5


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
