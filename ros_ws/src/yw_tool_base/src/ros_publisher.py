#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 该例程将发布/person_info话题，自定义消息类型learning_topic::Person

import rospy
import numpy as np
from learning_topic.msg import Person
from yw_tool_base.msg import db
import random
import multiprocessing
def velocity_publisher():
    # ROS节点初始化
    # rospy.init_node('person_publisher', anonymous=True)
    rospy.init_node('cyw_iiwa_publisher', anonymous=True)

    # 创建一个Publisher，发布名为/person_info的topic，消息类型为learning_topic::Person，队列长度10
    iiwa_info_pub = rospy.Publisher('/yw_iiwa_topic', db, queue_size=10)

    #设置循环的频率
    rate = rospy.Rate(10)

    while (not rospy.is_shutdown()):

        # 初始化learning_topic::Person类型的消息
        # person_msg = Person()
        # person_msg.name = "Tom"
        # person_msg.age  = 15
        # person_msg.sex  = Person.male
        db_msg=db()
        # db_msg.x=int(db_obj.get_target_cam_data_list("hand")[1])
        db_msg.x=random.randint(1,5)
        db_msg.y=random.randint(1,5)
        db_msg.z=random.randint(1,5)

        # 发布消息
        iiwa_info_pub.publish(db_msg)
        rospy.loginfo("Publsh IIWA message[%f, %f, %f]",
                db_msg.x, db_msg.y, db_msg.z)

        # 按照循环频率延时
        rate.sleep()

if __name__ == '__main__':
    try:
        velocity_publisher()
    except rospy.ROSInterruptException:
        pass
