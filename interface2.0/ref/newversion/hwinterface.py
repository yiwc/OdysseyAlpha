from abc import ABC, abstractmethod


class HWInterface(ABC):
    @abstractmethod
    def disconnect(self):
        """
        terminate connection with robot
        :return: None
        """
        pass

    @abstractmethod
    def move_home(self):
        """
        move back to home (Blocking)
        :return: None
        """
        pass

    @abstractmethod
    def move_tcp_absolute(self, pose):
        """
        move eff to absolute pose in robot base frame
        :param pose: list [x y z R P Y] (meter, radian)
        :return: None
        """
        pass

    @abstractmethod
    def get_tcp_pose(self):
        """
        get eff pose
        :return: list [x y z R P Y] (meter, radian)
        """
        pass

    @abstractmethod
    def set_gripper(self, val):
        """
        gripper position control
        :param val: boolean (False:released, True:gripped)
        :return: None
        """
        pass

    @abstractmethod
    def get_gripper(self):
        """
        get gripper position
        :return: boolean (False:released, True:gripped)
        """
        pass

    @abstractmethod
    def rot_tool(self, val):
        """
        rotate wrist_3 joint
        :param val: float (0 to 1)
        :return: None
        """
        pass

    @abstractmethod
    def get_tool_rot(self):
        """
        get wrist_3 joint value
        :return: float (0 to 1)
        """
        pass

    @abstractmethod
    def wait_push_input(self, force):
        """
        initiate waiting for push input
        require calling get_push_input to reset before reuse
        :param force: minimum amount of force required (newton)
        :return: None
        """
        pass

    @abstractmethod
    def get_push_input(self):
        """
        get if a push input has been registered, reset flag if yes
        :return: boolean (True:Yes, False:No)
        """
        pass

    @abstractmethod
    def push(self, force, max_dist):
        """
        initiate applying force and/or torque in 4 dimensions
        require calling get_push to reset before reuse
        :param force: list (x y z R) (newton, newton meter)
        :param max_dist: list (x y z R) maximum travel in each dimensions (meter, radian)
        :return: None
        """
        pass

    @abstractmethod
    def screw(self, cw):
        """
        initiate applying downward force and torque for a duration
        :param cw: boolean (False:clockwise, True:counter-clockwise)
        :return: None
        """
        pass

    @abstractmethod
    def get_push(self):
        """
        get if push has completed
        :return: int (0:No, 1:max distance reached, 2:force acquired)
        """
        pass

    @abstractmethod
    def is_program_running(self):
        """
        check if a program is already running
        :return: boolean (False:stopped, True:Moving)
        """
        pass

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
            dist += ((val1[i] - val2[i]) * 0.9) ** 2
        return dist ** 0.5

    @staticmethod
    def dist(val1, val2):
        dist = 0
        for i in range(len(val1)):
            dist += (val1[i] - val2[i]) ** 2
        return dist ** 0.5

    @staticmethod
    def pose_m2mm(pose):
        return [i * 1000. for i in pose[:3]] + pose[-3:]

    @staticmethod
    def pose_mm2m(pose):
        return [i / 1000. for i in pose[:3]] + pose[-3:]


### init
# (require '[libpython-clj.python :as py])
# (py/initialize!)
# (def py_class (py/import-module "src.hwinterface.ur"))
# (def obj_instance (py/call-attr py_class "Interface"))

### read eff pose
# (py/call-attr obj_instance "get_tcp_pose")

### gripper open & close
# (py/call-attr obj_instance "set_gripper" 0)
# (py/call-attr obj_instance "set_gripper" 1)

### move eff to absolute pose
# (py/call-attr obj_instance "move_tcp_absolute" [0.21 0.54 0.05 -2.9 -1.2 0])

### ending
# (py/call-attr obj_instance "move_home")
# (py/call-attr obj_instance "disconnect")
