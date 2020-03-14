from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QSizePolicy, QLabel, QPushButton, QMessageBox, QWidget, \
    QTableWidgetItem, QTableWidget
from MainWindows import Ui_MainWindow
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QStringListModel, QSize, QTimer, QCoreApplication, QThread
from PyQt5.QtGui import *
import sys
import time
# from PyQt5 import QtCore
import CYW_RemoteControl
import ZED_YOLO_Sensor
import CYWMainWindow
import cv2
import AudioOperator as AO
import multiprocessing
import os
from PyQt5 import QtCore, QtWidgets, uic

import matplotlib
matplotlib.use('QT5Agg')

from matplotlib.figure import Figure
# import matplotlib.pylab as plt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from mpl_toolkits import mplot3d

class MyMainWindow(QMainWindow, Ui_MainWindow):
    DetectedListClickedSig = pyqtSignal(int)

    def __init__(self, parent=None, db=None, op=None, ct=None,ao=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.db = db
        self.op = op
        self.ct = ct
        print("ct",ct)
        self.ao = ao

        self.detected_list = []
        self.target_DetectedItem_selected = ""

        self.VoiceSpeakingCountDown=3.0
        self.VoiceCheckTime=0.1#s
        # Threads
        self.updateInfoThread = updateInfoThread()
        self.updateInfoThread.updateInfoSig.connect(self.updateInfo)
        self.updateInfoThread.start()

        self.updatePlotThread = updatePlotThread()
        self.updatePlotThread.updatePlotSig.connect(self.updatePlot)
        self.updatePlotThread.start()

        self.updateCVImgThread = updateCVImgThread()
        self.updateCVImgThread.updateCVImgSig.connect(self.updateCvImg)
        self.updateCVImgThread.start()

        self.updateDetectedListThread = updateDetectedListThread()
        self.updateDetectedListThread.updateDetectedListSig.connect(self.updateDetectedList)
        self.updateDetectedListThread.start()

        self.CheckVoiceCheckingThread = CheckVoiceCheckingThread()
        self.CheckVoiceCheckingThread.CheckVoiceCheckingSig.connect(self.CheckVoiceChecking)
        self.CheckVoiceCheckingThread.start()

        self.CheckROSChekcingThread = CheckROSChekcingThread()
        self.CheckROSChekcingThread.CheckROSCheckingSig.connect(self.CheckROSChecking)
        self.CheckROSChekcingThread.start()

        # self.Cam_bottle_label_title.setText("test")

        self.main_widget = QWidget(self)
        self.myplot = MyMplCanvas(self.main_widget)

        # self.fig = plt.figure()
        # self.ax = plt.axes(projection='3d')
        # self.ax.plot([0,0],[0,0],[0,5],"r")
        # self.ax.plot([0,5],[0,0],[0,0],"r")
        # self.ax.plot([0,0],[0,5],[0,0],"r")
        # self.plotWidget = FigureCanvas(self.fig)

        lay = QtWidgets.QVBoxLayout(self.content_plot)
        lay.setContentsMargins(0, 0, 0, 0)
        # lay.addWidget(self.plotWidget)
        lay.addWidget(self.myplot)
        # add toolbar
        # self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.plotWidget, self))

        # self.myplot = MyMplCanvas(self.main_widget)

    def updatePlot(self):
        if(self.checkBox_DFsensor_able.isChecked()):
            # self.db.DF_sensor_able=1
            if(self.db.DF_pred_matrix.size==0):
                # print("DF_pred_matrix size =0")
                # m = np.ones([4,4])/3
                # self.draw_vectors(xs=m[1, :], ys=m[2, :], zs=m[3, :])
                pass
            else:
                m=self.db.DF_pred_matrix
                # m=np.linalg.inv(self.db.DF_pred_matrix)
                self.draw_vectors(xs=m[1,:3],ys=m[2,:3],zs=m[3,:3])
        # else:
        #     self.db.DF_sensor_able=0
    def draw_vectors(self,xs,ys,zs):

        self.myplot.ax.cla()
        # self.myplot.ax.plot([0,0],[0,0],[0,0.5],"r")
        # self.myplot.ax.plot([0,0.5],[0,0],[0,0],"r")
        # self.myplot.ax.plot([0,0],[0,0.5],[0,0],"r")
        for i in range(len(xs)-1):
            x=xs[i]
            y=ys[i]
            z=zs[i]
            self.myplot.ax.plot([0,x],[0,y],[0,z],"r")
        self.myplot.ax.plot([0,xs[-1]],[0,ys[-1]],[0,zs[-1]],"b")
        self.myplot.draw()
        # self.plotWidget.updateGeometry()
        # self.plotWidget = FigureCanvas(self.fig)
        # self.ax.plot([0,xs[0]])
    def initUI(self):

        self.DetectedListClickedSig.connect(self.DetectedListViewClicked)
        self.DetectedListView.clicked.connect(self.emitDetectedListClickedSig)
        self.Mission1Button.clicked.connect(self.DoMission1)
        self.Mission2Button.clicked.connect(self.DoMission2)
        self.Mission3Button.clicked.connect(self.DoMission3)
        self.Mission4Button.clicked.connect(self.DoMission4)
        self.ros_console_button.clicked.connect(self.ros_console)
        self.ros_graph_button.clicked.connect(self.ros_graph)
        self.ros_plot_button.clicked.connect(self.ros_plot)
        self.ros_image_button.clicked.connect(self.ros_image)
        self.ros_rqt_button.clicked.connect(self.ros_rqt)
        self.ros_rviz_button.clicked.connect(self.ros_rviz)
        self.ros_gazebo_button.clicked.connect(self.ros_gazebo)
        self.MissionAbsortButton.clicked.connect(self.AbsortMission)
        self.ControlRecoverButton.clicked.connect(self.RecoverControl)
        pass

    def ros_gazebo(self):
        def run():
            os.system("gazebo")
        q=multiprocessing.Process(target=run,args=())
        q.start()
    def ros_rviz(self):
        def run():
            os.system("rviz")
        q=multiprocessing.Process(target=run,args=())
        q.start()
    def ros_console(self):
        def run():
            os.system("rqt_console")
        q=multiprocessing.Process(target=run,args=())
        q.start()
    def ros_graph(self):
        def run():
            os.system("rqt_graph")
        q=multiprocessing.Process(target=run,args=())
        q.start()
    def ros_plot(self):
        def run():
            os.system("rqt_plot")
        q=multiprocessing.Process(target=run,args=())
        q.start()
    def ros_image(self):
        def run():
            os.system("rqt_image")
        q=multiprocessing.Process(target=run,args=())
        q.start()
    def ros_rqt(self):
        def run():
            os.system("rqt")
        q=multiprocessing.Process(target=run,args=())
        q.start()
    def CheckROSChecking(self):


        ros_checkbox_checked=self.ROScheckBox.isChecked()
        if(self.op.get_ros_publisher_running()):
            # print("ROS is running!")
            self.ROScheckBox.setChecked(1)
        else:
            if(ros_checkbox_checked):
                print("start ros publisher!")
                self.op.start_ros_publisher()

    def CheckVoiceChecking(self):


        if(self.VoiceControlCheckBox.isChecked()):
            self.VoiceListenCheckBox.setChecked(1)

        Voice_control_able=self.VoiceControlCheckBox.isChecked()
        Voice_listen_able=self.VoiceListenCheckBox.isChecked()
        ts = []
        text=''
        t1=''
        t2=''
        if(Voice_control_able):
            t1="Voice_control_able"
            pass
        else:
            t1="Voice_control close"
            pass

        if(Voice_listen_able):
            t2="Voice_listen_able"
            self.ao.SetRuningAble(1)
            # self.VoiceTextBrowser.setText("Voice_listen_able")
            pass
        else:#close
            self.ao.SetRuningAble(0)
            t2="Voice_listen close"
            pass

        is_listening=self.ao.isListening
        if(is_listening):
            pass
            self.VoiceSpeakingCountDown-=0.1
            self.SpeakingLabel.setText("Speaking "+str(round(self.VoiceSpeakingCountDown+0.2)))
            self.SpeakingLabel.setStyleSheet('background-color: green;color:white;')
        elif(is_listening==0 and Voice_listen_able==1):
            self.SpeakingLabel.setText("Analysing")
            self.SpeakingLabel.setStyleSheet('background-color: red')
        else:
            self.SpeakingLabel.setText("Ready")
            self.SpeakingLabel.setStyleSheet('background-color: white')

        is_Recognizing=self.ao.isRecognizing
        if(is_Recognizing):
            self.VoiceSpeakingCountDown=3.0

        ts=[]
        # ts.append(t1)
        # ts.append(t2)
        # ts.append("run_main_able"+str(self.ao.run_main_able))
        # ts.append("isListening"+str(self.ao.isListening))
        # ts.append("isAnalysing"+str(self.ao.isRecognizing))
        # ts.append("ListenMode"+str(self.ao.ListenMode))
        # ts.append("Result:"+str(self.ao.res))
        ts.append("Target:"+str(self.ao.res_target))
        # text=t1+"\n"+t2
        for t in ts:
            text+=(str(t)+"\n")
        self.VoiceTextBrowser.setText(text)

        if(self.ao.res_target=="cube" or self.ao.res_target=="bottle"):
            self.target_DetectedItem_selected=self.ao.res_target
            self.DoMission3()
            self.ao.res_target=""

    def VoiceListen(self):
        pass
    def VoiceControl(self):
        pass
    def RecoverControl(self):
        self.ct.EmergencySTOP_recover()

    def AbsortMission(self):
        self.ct.EmergencySTOP()

    def emitDetectedListClickedSig(self, qModelIndex):
        self.DetectedListClickedSig.emit(qModelIndex.row())

    def DoMission1(self):
        target_name = self.target_DetectedItem_selected
        print(target_name)
        if (target_name == ""):
            print("Please select a item first!")
            return False
        if (self.db.get_inMission()):
            print("IIWA has been occupied")
        else:
            print("Start a Mission1")
            # self.db.publish_holding_at_safe_pose_switch(0)
            # self.ct.Mission1_Pick_and_Place(target_name)
            # self.db.publish_holding_at_safe_pose_switch(1)
            self.ct.Start_Mission1(target_name)

    def DoMission2(self):

        target_name = "hand"
        print(target_name)
        # if(target_name==""):
        #     print("Please select a item first!")
        #     return False
        if (not ("hand" in self.detected_list)):
            print("Hand Not Detected, Retry")
        if (self.db.get_inMission()):
            print("IIWA has been occupied")
        else:
            print("Start a Mission2")
            # self.db.publish_holding_at_safe_pose_switch(0)
            # self.ct.Mission1_Pick_and_Place(target_name)
            # self.db.publish_holding_at_safe_pose_switch(1)
            self.ct.Start_Mission2(target_name, self.Mission2KeepcheckBox.isChecked() == 1)

    def DoMission4(self):

        # target_name="hand"
        # print(target_name)
        # if(target_name==""):
        #     print("Please select a item first!")
        #     return False
        if (not ("hand" in self.detected_list)):
            print("Hand Not Detected, Retry")
        if (self.db.get_inMission()):
            print("IIWA has been occupied")
        else:
            print("Start a Mission4")
            # self.db.publish_holding_at_safe_pose_switch(0)
            # self.ct.Mission1_Pick_and_Place(target_name)
            # self.db.publish_holding_at_safe_pose_switch(1)
            self.ct.Start_Mission4()

    def DoMission3(self):
        target_name = self.target_DetectedItem_selected
        print(target_name)
        if (target_name == ""):
            print("Please select a item first!")
            return False
        if (not ("hand" in self.detected_list)):
            print("Hand Not Detected, Retry")
        if (self.db.get_inMission()):
            print("IIWA has been occupied")
        else:
            print("Start a Mission3")
            self.ct.Start_Mission3(target_name)

    def DetectedListViewClicked(self, row):
        target_name = self.detected_list[row]
        self.target_DetectedItem_selected = target_name

    def updateInfo(self):
        # print("accept")
        # self.Cam_bottle_label_title.setText("22")
        # self.Cam_bottle_label_title.s
        self.Cam_f_cont.setText(str(self.db.cam_f))
        self.Cam_bottle_label_content_label.setText(str(self.db.get_target_cam_data_list("bottle")))
        self.Cam_cube_label_content_label.setText(str(self.db.get_target_cam_data_list("cube")))
        self.Cam_iiwa_label_content_label.setText(str(self.db.get_target_cam_data_list("iiwa")))
        self.Cam_hand_label_content_label.setText(str(self.db.get_target_cam_data_list("hand")))
        if(self.checkBox_DFsensor_able.isChecked()):
            self.db.DF_sensor_able=1
        else:
            self.db.DF_sensor_able=0
    def updateCvImg(self):
        # if()
        if(self.checkBox_6DAble.isChecked()):
            image = self.db.get_cam_image_with_mask()
        else:
            image = self.db.get_cam_image()

        try:
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w, ch = image.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB32)
            p = convertToQtFormat.scaled(960, 720, Qt.KeepAspectRatio)
            # self.changePixmap.emit(p)
            self.CamCVImageLabel.setPixmap(QPixmap.fromImage(p))
            # self.CamImgGroup.setScaledContents(True)
            self.CamCVImageLabel.setScaledContents(True)
        except Exception as err:
            self.CamCVImageLabel.setText("Cam Not Ready\n" + str(err))

        # if(image==None):
        #     self.CamCVImageLabel.setText("Cam Not Ready")
        # else:

    def updateDetectedList(self):
        slm = QStringListModel()
        new_list = self.db.get_target_detected_list()
        old_list = self.detected_list
        # print("new:",new_list)
        # print("old:",old_list)
        # if(len(set(new_list)|set(old_list))==len(set(old_list))):
        if (set(new_list) == set(old_list)):
            pass
            # print("same")
        else:
            self.detected_list = self.db.get_target_detected_list()
            slm.setStringList(self.detected_list)
            self.DetectedListView.setModel(slm)

        # = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
        pass

    def keyPressEvent(self, QKeyEvent):
        print("here")
        print(QKeyEvent.key())
        if QKeyEvent.key() == 49:
            print("m1 clicked")
            self.Mission1Button.click()
        if QKeyEvent.key() == 50:
            print("m2 clicked")
            self.Mission2Button.click()
        if QKeyEvent.key() == 51:
            print("m3 clicked")
            self.Mission3Button.click()


class updateCVImgThread(QThread):
    updateCVImgSig = pyqtSignal(bool)

    def __init__(self):
        super(updateCVImgThread, self).__init__()

    def run(self):
        while (1):
            self.updateCVImgSig.emit(True)
            time.sleep(0.1)


class updateDetectedListThread(QThread):
    updateDetectedListSig = pyqtSignal(bool)

    def __init__(self):
        super(updateDetectedListThread, self).__init__()

    def run(self):
        while (1):
            self.updateDetectedListSig.emit(True)
            time.sleep(0.1)


class updateInfoThread(QThread):
    updateInfoSig = pyqtSignal(bool)

    def __init__(self):
        super(updateInfoThread, self).__init__()

    def run(self):
        while 1:
            self.updateInfoSig.emit(True)
            # print("thread running +1")
            time.sleep(0.1)


class updatePlotThread(QThread):
    updatePlotSig = pyqtSignal(bool)

    def __init__(self):
        super(updatePlotThread, self).__init__()

    def run(self):
        while 1:
            self.updatePlotSig.emit(True)
            # print("thread running +1")
            time.sleep(0.5)


class CheckVoiceCheckingThread(QThread):

    CheckVoiceCheckingSig=pyqtSignal(bool)

    def __init__(self):
        super(CheckVoiceCheckingThread, self).__init__()

    def run(self):
        while 1:
            self.CheckVoiceCheckingSig.emit(True)
            # print("thread running +1")
            time.sleep(0.1)

class CheckROSChekcingThread(QThread):

    CheckROSCheckingSig=pyqtSignal(bool)

    def __init__(self):
        super(CheckROSChekcingThread, self).__init__()

    def run(self):
        while 1:
            self.CheckROSCheckingSig.emit(True)
            # print("thread running +1")
            time.sleep(0.1)


def MainThread(sys_argv, db=None, op=None, ct=None,ao=None):
    # print("main thread running")
    app = QApplication(sys_argv)
    win = MyMainWindow(db=db, op=op, ct=ct,ao=ao)
    win.show()
    # print("here")
    sys.exit(app.exec_())

class MyMplCanvas(FigureCanvas):

    def __init__(self, parent=None):
        # self.fig = Figure()
        # self.axes = self.fig.add_subplot(111)
        # plot empty line
        # self.line, = self.axes.plot([],[], color="orange")

        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')
        self.ax.plot([0,0],[0,0],[0,0.5],"r")
        self.ax.plot([0,0.5],[0,0],[0,0],"r")
        self.ax.plot([0,0],[0,0.5],[0,0],"r")
        # self.plotWidget = FigureCanvas(self.fig)



        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

if __name__ == "__main__":
    # #init db
    # db=CYW_RemoteControl.global_database()
    # #init operator
    # op=CYW_RemoteControl.operator(global_db=db)
    # #init controller
    # ct=CYW_RemoteControl.controller(db,op)

    MainThread(sys.argv)
    # app = QApplication(sys.argv)
    # win = MyMainWindow()
    # win.show()
    # sys.exit(app.exec_())
