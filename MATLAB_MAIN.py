import CYW_RemoteControl_MATLAB as mtpkg
# import ZED_YOLO_Sensor
# import CYWMainWindow
import sys
import threading
import time
import sys





if __name__=="__main__":


    #init matlab funcs
    mt=mtpkg.MATLABs()
    print(mt.Paras)

    #init db
    db=mtpkg.global_database()
    #init operator
    op=mtpkg.operator(global_db=db,MATLABs_OBJ=mt)
    #init controller
    ct=mtpkg.controller(db,op)

    #start to receive data from iiwa
    op.mode=1
    op.receive_server_start()
    op.send_server_start()





    # #Run windows thread
    # Windows_Thread=threading.Thread(target=CYWMainWindow.MainThread,args=(sys.argv,db,op,ct,))
    # Windows_Thread.start()
    #
    # #Start ZED_YOLO_Sensor Thread
    # #db.cam_ will be updated while running the thread.
    # ZED_YOLO_Sensor_Thread=threading.Thread(target=ZED_YOLO_Sensor.main,args=(sys.argv[1:],db))
    # ZED_YOLO_Sensor_Thread.start()
    #
    # #Holding at a safe place, to keep connection
    # #Thread can be temply interupt by setting db.holding_at_safe_pos_switch=False
    # holding_at_safe_pos_Thread=threading.Thread(target=ct.holding_at_safe_pos,args=())
    # holding_at_safe_pos_Thread.start()

    #Start Show Log Thread
    # Show_Log_Thread=threading.Thread(target=op.show_logs_thread,args=())
    # Show_Log_Thread.start()

    #Do a Mission
    # db.publish_holding_at_safe_pose_switch(0)
    # ct.Mission1_Pick_and_Place(target_name="cube")
    # db.publish_holding_at_safe_pose_switch(1)
    # ct.holding_at_safe_pos()
    while(1):
        time.sleep(1)

