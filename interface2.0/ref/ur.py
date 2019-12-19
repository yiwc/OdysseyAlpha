"""
modifications in urx:
    1. commented in line 216-217 urrobot.py
        # if not self.is_running():
        #     raise RobotException("Robot stopped")

    2. added script compatibility program in line 36-42 ursecmon.py
        self.condition = Condition()
        self.script = 'def '.encode() in prog or 'sec '.encode() in prog

        def __str__(self):
            if self.script:
                return "{}".format(self.program)
            else:
                return "Program({})".format(self.program)
"""
from .hwinterface import HWInterface
import rospy
import time
from threading import Thread
import math3d as m3d
import urx
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper


HOMEJ = [0.7854, -1.5708, -1.5708, -1.5708, 1.5708, 0]
ACCE = 0.1
VELO = 0.2
TOL_TARGET_POSE = 0.002
TOOL_RANGE = [-3.1416, 3.1416]


class Interface(HWInterface):
    def __init__(self):
        rospy.init_node('ur_interface')

        # robot setup
        print('Connecting robot...')
        self.rob = urx.Robot("192.168.1.5", True)
        self.rob.set_tcp((0, 0, 0.17, 0, 0, 0))
        self.rob.set_payload(1, (0, 0, 0.1))
        self.rob.set_gravity((0, 0, 9.82))
        self.rob.set_csys(m3d.Transform([0, 0, 0, -2.9, 1.2, 0]))
        time.sleep(0.2)
        self.gripper = Robotiq_Two_Finger_Gripper(self.rob)

        # robot init
        print('Homing robot...')
        self.gripper.open_gripper()
        self.move_home()
        self.state_gripper, self.target_gripper = 0, 0
        self.process_gripper = Thread(target=self._set_gripper)
        self.target_pose = self.get_tcp_pose()
        self.target_tool = self.get_tool_rot()
        print('Robot ready!')

        # force monitoring
        self.process_force = Thread(target=self._watch_force)
        self.input_force = False
        self.timeout_push = None
        self.offset_force = 0

    def disconnect(self):
        """
        terminate connection with robot
        :return:
        """
        self.rob.close()

    def move_home(self):
        """
        move back to home (Blocking)
        :return:
        """
        self.rob.movej(HOMEJ, ACCE*2, VELO*3, wait=True)

    def move_tcp_relative(self, pose):
        """
        move eff to relative pose
        :param pose: relative differences in [x y z R P Y] (meter, radian)
        :return: None
        """
        self.rob.add_pose_tool(m3d.Transform(pose), ACCE, VELO, wait=False)

    def move_tcp_absolute(self, pose):
        """
        move eff to absolute pose in robot base frame
        :param pose: list [x y z R P Y] (meter, radian)
        :return: None
        """
        if (self.is_program_running() and
             self.dist_linear(pose, self.target_pose) > TOL_TARGET_POSE) or \
           (not self.is_program_running() and
             self.dist_linear(pose, self.get_tcp_pose()) > TOL_TARGET_POSE):
            self.target_pose = pose
            self.rob.set_pose(m3d.Transform(pose), ACCE, VELO, False)

    def get_tcp_pose(self):
        """
        get eff pose
        :return: list [x y z R P Y] (meter, radian)
        """
        return self.rob.getl()

    def set_gripper(self, val):
        """
        gripper position control
        :param val: Boolean (False:released, True:gripped)
        :return: None
        """
        if self.target_gripper != val:
            self.target_gripper = val
            if not self.process_gripper.is_alive():
                self.process_gripper = Thread(target=self._set_gripper)
                self.process_gripper.start()

    def get_gripper(self):
        """
        get gripper position
        :return: Boolean (False:released, True:gripped)
        """
        return self.state_gripper

    def rot_tool(self, val):
        """
        rotate wrist_3 joint
        :param val: float (0 to 1)
        :return: None
        """
        if (self.is_program_running() and
            ((val-self.target_tool)**2)**0.5 > TOL_TARGET_POSE) or \
           (not self.is_program_running() and
            ((val-self.get_tool_rot())**2)**0.5 > TOL_TARGET_POSE):
            self.target_tool = val
            joints = self.rob.getj()
            joints[5] = (TOOL_RANGE[1] - TOOL_RANGE[0]) * val + TOOL_RANGE[0]
            self.rob.movej(joints, ACCE*4, VELO*6, wait=False)

    def get_tool_rot(self):
        """
        get wrist_3 joint value
        :return: float (0 to 1)
        """
        val = self.rob.getj()[5]
        return (min(max(val, TOOL_RANGE[0]), TOOL_RANGE[1]) - TOOL_RANGE[0]) / (TOOL_RANGE[1] - TOOL_RANGE[0]) #缩放，-2pi ~ 2pi 等比缩放

    def waitfor_push(self, force):
        """
        wait for push input
        require calling get_push_input to reset before reuse
        :param force: minimum amount of force required (newton)
        :return: None
        """
        if not self.process_force.isAlive() and not self.input_force:
            self.rob.stopj(5)
            time.sleep(1)
            th_force = self.rob.get_force(wait=True) + force
            self.process_force = Thread(target=self._watch_force, args=(th_force,))
            self.process_force.start()

    def get_push_input(self):
        """
        get if a push input has been registered
        :return: Boolean (True:Yes, False:No)
        """
        if self.input_force:
            self.input_force = False
            return True
        else:
            return False

    def push(self, force, duration):
        """
        apply force and/or torque in 6 dimensions for a duration
        require calling get_push to reset before reuse
        :param force: list (x y z R P Y) (newton, newton meter)
        :param duration: float (second)
        :return: boolean (False:moving, True:done)
        """
        if self.timeout_push is None:
            self.timeout_push = time.time() + duration + 2  # 2 seconds are the sleeps in force program
            self.offset_force = self.rob.get_force(wait=True)
            self._force_mode_start(force, duration, (0.01, 0.03), (0.02, 0.4), 0)

    def get_push_timeout(self):
        if self.timeout_push is None:
            return False
        elif time.time() > self.timeout_push:
            self.timeout_push = None
            return True
        else:
            return False

    def get_force(self):
        """
        get tcp force after offset
        :return:  int #!=force [x y z Tx Ty Tz] or
        """
        return self.rob.get_force(wait=True) - self.offset_force

    def screw(self, cw, duration):
        """
        applying downward force and torque for a duration
        :param cw: boolean (False:clockwise, True:counter-clockwise)
        :param duration: float (second)
        :return: boolean (False:moving, True:done)
        """
        return self.push([0.0, 0.0, 20.0, 0.0, 0.0, 2.0 if cw else -2.0], duration)

    def is_program_running(self):
        """
        check if a program is already running
        :return: Boolean (False:stopped, True:Moving)
        """
        return self.rob.secmon.is_program_running()

    def _set_gripper(self):
        while self.state_gripper != self.target_gripper:
            if self.target_gripper:
                self.gripper.close_gripper()
                self.state_gripper = 1
            else:
                self.gripper.open_gripper()
                self.state_gripper = 0

    def _watch_force(self, th_force):
        time0 = time.time()
        while time.time() - time0 < 5:  # 5 seconds input window
            force = self.rob.get_force(wait=True)
            if force > th_force:
                self.input_force = True
                break

    def _force_mode_start(self, force, duration, deviation, speed, damp):
        # force, duration, (0.01, 0.03), (0.02, 0.4), 0
        #[0.0, 0.0, 20.0, 0.0, 0.0, 0.0], 4, (0.01, 0.03), (0.02, 0.4), 0
        axis = [0 if i == 0 else 1 for i in force]  #[0,0,1,0,0,0]
        limit = [speed[0] if i else deviation[0] for i in axis[:3]] + \
                [speed[1] if i else deviation[1] for i in axis[3:]]
        prog = 'def force_run():\n' + \
               ' stopl(5)\n' + \
               ' sleep(1)\n' + \
               ' force_mode_set_damping({})\n'.format(str(damp)) + \
               ' force_mode(tool_pose(), {}, {}, 2, {})\n'.format(str(axis), str(force), str(limit)) + \
               ' sleep({})\n'.format(str(duration)) + \
               ' end_force_mode()\n' + \
               ' stopl(5)\n' + \
               ' sleep(1)\n' + \
               'end'
        self.rob.send_program(prog)
