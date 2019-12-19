from .hwinterface import HWInterface
from threading import Thread
import rospy
import time
import socket


HOMEJ = [0, 0, 0, 0, 0, 0, 0]  ## TODO: Find iiwa home_joint_positoin
VELO = 0.3
TOL_TARGET_POSE = 0.002
GRIPPER_FORCE = 5
GRIPPER_SPEED = 255
GRIPPER_MODE = 11
TOOL_RANGE = [-4.88, 0.0]


class Interface(HWInterface):
    def __init__(self):
        rospy.init_node('iiwa_interface')

        # robot setup
        print('Connecting robot...')
        self.rob = LBR_ROS("172.31.1.147", 30009)

        # robot init
        print('Homing robot...')
        self.set_gripper(0)
        self.move_home()
        self.target_gripper = self.get_gripper()
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
        self.rob.disconnect()

    def move_home(self):
        """
        move back to home (Blocking)
        :return:
        """
        self.rob.move_joint(HOMEJ, VELO)
        while True:
            if self.is_program_running():
                time.sleep(0.1)
            else:
                break

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
            self.rob.move_tcp(self.pose_m2mm(pose), VELO)

    def get_tcp_pose(self):
        """
        get eff pose
        :return: list [x y z R P Y] (meter, radian)
        """
        return self.pose_mm2m(self.rob.get_tcp_frame())

    def set_gripper(self, val):
        """
        gripper position control
        :param val: Boolean (False:released, True:gripped)
        :return: None
        """
        if self.target_gripper != val:
            self.target_gripper = val
            self.rob.move_gripper(val*255, GRIPPER_FORCE, GRIPPER_SPEED, GRIPPER_MODE)

    def get_gripper(self):
        """
        get gripper position
        :return: Boolean (False:released, True:gripped)
        """
        return self.rob.get_gripper_position_force()[0] > 90

    def rot_tool(self, val):
        """
        rotate wrist_3 joint
        :param val: float (0 to 1)
        :return: None
        """
        if (self.is_program_running() and
            ((val - self.target_tool) ** 2) ** 0.5 > TOL_TARGET_POSE) or \
           (not self.is_program_running() and
            ((val - self.get_tool_rot()) ** 2) ** 0.5 > TOL_TARGET_POSE):
            self.target_tool = val
            joints = self.rob.get_joint_position()
            joints[6] = (TOOL_RANGE[1] - TOOL_RANGE[0]) * val + TOOL_RANGE[0]
            self.rob.move_joint(joints, VELO)

    def get_tool_rot(self):
        """
        get wrist_3 joint value
        :return: float (0 to 1)
        """
        val = self.rob.get_joint_position()[5]
        return (min(max(val, TOOL_RANGE[0]), TOOL_RANGE[1]) - TOOL_RANGE[0]) / (TOOL_RANGE[1] - TOOL_RANGE[0])

    def waitfor_push(self, force):
        """
        initiate waiting for push input
        require calling get_push_input to reset before reuse
        :param force: minimum amount of force required (newton)
        :return: None
        """
        if not self.process_force.isAlive() and not self.input_force:
            while self.is_program_running():
                time.sleep(0.1)
            th_force = self._get_force() + force
            self.process_force = Thread(target=self._watch_force, args=(th_force,))
            self.process_force.start()

    def get_push_input(self):
        """
        get if a push input has been registered, reset flag if yes
        :return: Boolean (True:Yes, False:No)
        """
        if self.input_force:
            self.input_force = False
            return True
        else:
            return False

    def push(self, force, duration):
        """
        initiate applying force and/or torque in 6 dimensions for a duration
        require calling get_push to reset before reuse
        :param force: list (x y z R P Y) (newton, newton meter)
        :param duration: float (second)
        :return: boolean (False:moving, True:done)
        """
        if self.timeout_push is None:
            self.timeout_push = time.time() + duration
            self.offset_force = self._get_force()
            self.rob.move_tcp_stiff(self.rob.get_tcp_frame(), force, VELO, 1000)

    def get_push_timeout(self):
        """
        get if push has timeout
        :return: boolean (False: No)
        """
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
        :return:
        """
        return self._get_force() - self.offset_force

    def screw(self, cw, duration):
        """
        initiate applying downward force and torque for a duration
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
        return self.rob.get_status() == 'moving'

    def _watch_force(self, th_force):
        time0 = time.time()
        while time.time() - time0 < 5:  # 5 seconds input window
            force = self._get_force()
            if force > th_force:
                self.input_force = True
                break

    def _get_force(self):
        return sum([i**2 for i in self.rob.get_tcp_force_torque()])**0.5


class LBR_ROS:
    def __init__(self, ip, port):
        self.robot_addr = (ip, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        while True:
            try:
                self.socket.connect(self.robot_addr)
                break
            except:
                time.sleep(1)

    def disconnect(self):
        self._talk('bye')

    def ping_robot(self):
        return self._talk('hello') == 'hello'

    def get_status(self):
        return self._talk('get status')  # 'moving' or 'stopped'

    def get_joint_position(self):
        reply = self._talk('get joint position')
        return [float(i) for i in reply.split()]

    def get_joint_torque(self):
        reply = self._talk('get joint torque')
        return [float(i) for i in reply.split()]

    def get_tcp_frame(self):
        reply = self._talk('get tool frame')
        return [float(i) for i in reply.split()]

    def get_tcp_force_torque(self):
        reply = self._talk('get cartesian force')
        return [float(i) for i in reply.split()]

    def get_gripper_position_force(self):
        reply = self._talk('get gripper position force')
        return [int(i) for i in reply.split()]

    def move_gripper(self, position, force, speed, mode):
        self._talk('gripper move',
                   '{} {} {} {}'.format(position, force, speed, mode))

    def move_joint(self, position, speed):
        self._talk('smart joint move',
                   ' '.join(str(i) for i in position) + ' ' + ' '.join(str(speed) for _ in range(len(position))))

    def move_tcp(self, pose, speed):
        self._talk('smart cartesian move',
                   ' '.join(str(i) for i in pose) + ' {}'.format(speed))

    def move_tcp_collide_stop(self, pose, force_th, speed, blending):
        self._talk('linforce move',
                   ' '.join(str(i) for i in pose) + ' {} {} '.format(speed, blending) + ' '.join(str(i) for i in force_th))

    def move_tcp_stiff(self, pose, forcetorque, speed, stiffness):
        self._talk('linstiff move',
                   ' '.join(str(i) for i in pose) + ' {} {} '.format(speed, stiffness) + ' '.join(str(i) for i in forcetorque))

    def _talk(self, cmd, arg=''):
        while True:
            try:
                msg = cmd + " : " + arg + "\n"
                self.socket.send(msg)
                reply = self.socket.recv(1024)
                break
            except:
                self.connect()
        if reply == 'error' or reply == 'unknown command':
            print('"{}" returned from robot when calling "{}"!'.format(reply, cmd))
        return reply
