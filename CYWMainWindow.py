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

        self.updateCVImgThread = updateCVImgThread()
        self.updateCVImgThread.updateCVImgSig.connect(self.updateCvImg)
        self.updateCVImgThread.start()

        self.updateDetectedListThread = updateDetectedListThread()
        self.updateDetectedListThread.updateDetectedListSig.connect(self.updateDetectedList)
        self.updateDetectedListThread.start()

        self.CheckVoiceCheckingThread = CheckVoiceCheckingThread()
        self.CheckVoiceCheckingThread.CheckVoiceCheckingSig.connect(self.CheckVoiceChecking)
        self.CheckVoiceCheckingThread.start()
        # self.Cam_bottle_label_title.setText("test")


    def initUI(self):

        self.DetectedListClickedSig.connect(self.DetectedListViewClicked)
        self.DetectedListView.clicked.connect(self.emitDetectedListClickedSig)
        self.Mission1Button.clicked.connect(self.DoMission1)
        self.Mission2Button.clicked.connect(self.DoMission2)
        self.Mission3Button.clicked.connect(self.DoMission3)
        self.Mission4Button.clicked.connect(self.DoMission4)
        self.MissionAbsortButton.clicked.connect(self.AbsortMission)
        self.ControlRecoverButton.clicked.connect(self.RecoverControl)
        pass

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

    def updateCvImg(self):
        # if()
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


class CheckVoiceCheckingThread(QThread):

    CheckVoiceCheckingSig=pyqtSignal(bool)

    def __init__(self):
        super(CheckVoiceCheckingThread, self).__init__()

    def run(self):
        while 1:
            self.CheckVoiceCheckingSig.emit(True)
            # print("thread running +1")
            time.sleep(0.1)


def MainThread(sys_argv, db=None, op=None, ct=None,ao=None):
    # print("main thread running")
    app = QApplication(sys_argv)
    win = MyMainWindow(db=db, op=op, ct=ct,ao=ao)
    win.show()
    # print("here")
    sys.exit(app.exec_())


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
