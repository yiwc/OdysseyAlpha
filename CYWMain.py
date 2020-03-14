import CYW_RemoteControl2_3 as CYW_RemoteControl
import ZED_YOLO_Sensor
import ZED_DF_Sensor
import CYWMainWindow
import sys
import threading
import time
import sys
import AudioOperator as AO
import multiprocessing

if __name__=="__main__":

    #init db
    db=CYW_RemoteControl.global_database()
    #init operator
    op=CYW_RemoteControl.operator(global_db=db)
    #init controller
    ct=CYW_RemoteControl.controller(db,op)
    #init voice control
    ao=AO.Audio_Operator(db)
    #start voice server
    ao.SetRuningAble(0)#no run. To run, it needs checked in the window
    ao.start_run_main_thread()

    #start to receive data from iiwa
    op.receive_server_start()

    #Run windows thread
    Windows_Thread=threading.Thread(target=CYWMainWindow.MainThread,args=(sys.argv,db,op,ct,ao,))
    Windows_Thread.start()

    #Start ZED_YOLO_Sensor Thread
    #db.cam_ will be updated while running the thread.
    ZED_YOLO_Sensor_Thread=threading.Thread(target=ZED_YOLO_Sensor.main,args=(sys.argv[1:],db))
    ZED_YOLO_Sensor_Thread.start()

    #Start ZED_DF_Sensor Thread
    #db.cam_ will be updated while running the thread.
    ZED_DF_Sensor_Thread=threading.Thread(target=ZED_DF_Sensor.main,args=(db,))
    ZED_DF_Sensor_Thread.start()
    print("ZED_DF_Sensor.py START!")

    #Holding at a safe place, to keep connection
    #Thread can be temply interupt by setting db.holding_at_safe_pos_switch=False
    holding_at_safe_pos_Thread=threading.Thread(target=ct.holding_at_safe_pos,args=())
    holding_at_safe_pos_Thread.start()

    #Start Show Log Thread
    # Show_Log_Thread=threading.Thread(target=op.show_logs_thread,args=())
    # Show_Log_Thread.start()

    #Do a Mission
    # db.publish_holding_at_safe_pose_switch(0)
    # ct.Mission1_Pick_and_Place(target_name="cube")
    # db.publish_holding_at_safe_pose_switch(1)
    # ct.holding_at_safe_pos()

    #Start ROS CORE
    # def roscore():
    #     os.system("roscore")
    # roscore_p=multiprocessing.Process(target=roscore,args=())
    # roscore_p.start()
    # print("roscore start")

    while(1):
        time.sleep(1)
    



# ZED_YOLO_Sensor.main(argv=sys.argv[1:])