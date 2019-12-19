from ur import Interface
# from iiwa import Interface

poses = [
    [-0.1, -0.49, -0.23, 0, 0, 0],
    [-0.1, -0.49, 0.09, 0, 0, 0],
    [0.2, -0.70, -0.23, 0, 0, 0],
    [0.2, -0.70, -0.2, 0, 0, 0],
]


# Icarus architecture
def motion(cmd, args, goal, eval, type):
    if not isinstance(args, tuple):
        args = (args, )
    while True:
        cmd(*args)
        if type == 1:
            dist = sum([(v-goal[i])**2 for i, v in enumerate(eval())])**0.5
            if dist < 0.01:
                break
        elif type == 2:
            if eval() == goal:
                break
        elif type == 3:
            if ((eval()-goal)**2)**0.5 < 0.001:
                break
        elif type == 4:
            res = eval()
            val = [res == goal[i] for i in range(len(goal))]
            if sum(val) > 0:
                break


def routine_pickplace():
    # pick
    motion(rob.move_tcp_absolute, poses[0], poses[0], rob.get_tcp_pose, 1)
    motion(rob.move_tcp_absolute, poses[1], poses[1], rob.get_tcp_pose, 1)
    motion(rob.set_gripper, True, True, rob.get_gripper, 2)
    motion(rob.move_tcp_absolute, poses[0], poses[0], rob.get_tcp_pose, 1)

    # place
    motion(rob.move_tcp_absolute, poses[2], poses[2], rob.get_tcp_pose, 1)
    motion(rob.move_tcp_absolute, poses[3], poses[3], rob.get_tcp_pose, 1)
    motion(rob.set_gripper, False, False, rob.get_gripper, 2)
    motion(rob.move_tcp_absolute, poses[2], poses[2], rob.get_tcp_pose, 1)


def routine_screw():
    # pick
    # motion(rob.move_tcp_absolute, poses[0], poses[0], rob.get_tcp_pose, 1)
    # motion(rob.move_tcp_absolute, poses[1], poses[1], rob.get_tcp_pose, 1)
    motion(rob.set_gripper, True, True, rob.get_gripper, 2)
    # motion(rob.move_tcp_absolute, poses[0], poses[0], rob.get_tcp_pose, 1)
    motion(rob.move_tcp_absolute, poses[2], poses[2], rob.get_tcp_pose, 1)

    # insert
    motion(rob.rot_tool, 0, 0, rob.get_tool_rot, 3)
    print('waiting for push input')
    # motion(rob.wait_push_input, 5, True, rob.get_push_input, 2)
    motion(rob.push, ([0, 0, 20, 0], [0, 0, 0.3, 0]), 2, rob.get_push, 2)

    # screw
    for i in range(3):
        motion(rob.set_gripper, True, True, rob.get_gripper, 2)
        motion(rob.screw, 1, (1, 2), rob.get_push, 4)
        motion(rob.set_gripper, False, False, rob.get_gripper, 2)
        motion(rob.rot_tool, 0, 0, rob.get_tool_rot, 3)

    # retreat
    motion(rob.set_gripper, False, False, rob.get_gripper, 2)
    motion(rob.move_tcp_absolute, poses[2], poses[2], rob.get_tcp_pose, 1)


if __name__ == '__main__':
    rob = Interface()

    try:
        # routine_pickplace()
        routine_screw()
    finally:
        rob.disconnect()
