# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindows.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1246, 965)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 40, 691, 171))
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 701, 121))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.Cam_iiwa_label_title = QtWidgets.QLabel(self.formLayoutWidget)
        self.Cam_iiwa_label_title.setObjectName("Cam_iiwa_label_title")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Cam_iiwa_label_title)
        self.Cam_iiwa_label_content_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Cam_iiwa_label_content_label.setObjectName("Cam_iiwa_label_content_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Cam_iiwa_label_content_label)
        self.Cam_bottle_label_title = QtWidgets.QLabel(self.formLayoutWidget)
        self.Cam_bottle_label_title.setObjectName("Cam_bottle_label_title")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Cam_bottle_label_title)
        self.Cam_bottle_label_content_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Cam_bottle_label_content_label.setObjectName("Cam_bottle_label_content_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Cam_bottle_label_content_label)
        self.Cam_cube_label_title = QtWidgets.QLabel(self.formLayoutWidget)
        self.Cam_cube_label_title.setObjectName("Cam_cube_label_title")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.Cam_cube_label_title)
        self.Cam_cube_label_content_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Cam_cube_label_content_label.setObjectName("Cam_cube_label_content_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.Cam_cube_label_content_label)
        self.Cam_f_title = QtWidgets.QLabel(self.formLayoutWidget)
        self.Cam_f_title.setObjectName("Cam_f_title")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Cam_f_title)
        self.Cam_f_cont = QtWidgets.QLabel(self.formLayoutWidget)
        self.Cam_f_cont.setObjectName("Cam_f_cont")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Cam_f_cont)
        self.Cam_hand_label_title = QtWidgets.QLabel(self.formLayoutWidget)
        self.Cam_hand_label_title.setObjectName("Cam_hand_label_title")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.Cam_hand_label_title)
        self.Cam_hand_label_content_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Cam_hand_label_content_label.setObjectName("Cam_hand_label_content_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.Cam_hand_label_content_label)
        self.CamImgGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.CamImgGroup.setGeometry(QtCore.QRect(40, 430, 681, 431))
        self.CamImgGroup.setObjectName("CamImgGroup")
        self.CamCVImageLabel = QtWidgets.QLabel(self.CamImgGroup)
        self.CamCVImageLabel.setGeometry(QtCore.QRect(0, 30, 671, 361))
        self.CamCVImageLabel.setObjectName("CamCVImageLabel")
        self.DetectedItemsLabel = QtWidgets.QLabel(self.centralwidget)
        self.DetectedItemsLabel.setGeometry(QtCore.QRect(800, 80, 241, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.DetectedItemsLabel.setFont(font)
        self.DetectedItemsLabel.setObjectName("DetectedItemsLabel")
        self.DetectedListView = QtWidgets.QListView(self.centralwidget)
        self.DetectedListView.setGeometry(QtCore.QRect(800, 100, 241, 351))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.DetectedListView.setFont(font)
        self.DetectedListView.setObjectName("DetectedListView")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(800, 10, 111, 27))
        self.pushButton.setObjectName("pushButton")
        self.Mission2Button = QtWidgets.QPushButton(self.centralwidget)
        self.Mission2Button.setGeometry(QtCore.QRect(800, 530, 241, 27))
        self.Mission2Button.setObjectName("Mission2Button")
        self.M1TitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.M1TitleLabel.setGeometry(QtCore.QRect(800, 460, 251, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.M1TitleLabel.setFont(font)
        self.M1TitleLabel.setObjectName("M1TitleLabel")
        self.M2TitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.M2TitleLabel.setGeometry(QtCore.QRect(800, 510, 251, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.M2TitleLabel.setFont(font)
        self.M2TitleLabel.setObjectName("M2TitleLabel")
        self.Mission1Button = QtWidgets.QPushButton(self.centralwidget)
        self.Mission1Button.setGeometry(QtCore.QRect(800, 480, 241, 27))
        self.Mission1Button.setObjectName("Mission1Button")
        self.MissionAbsortButton = QtWidgets.QPushButton(self.centralwidget)
        self.MissionAbsortButton.setGeometry(QtCore.QRect(1080, 580, 141, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.MissionAbsortButton.setFont(font)
        self.MissionAbsortButton.setStyleSheet("background-color: rgb(255,120,0);")
        self.MissionAbsortButton.setObjectName("MissionAbsortButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(800, 550, 241, 51))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.ControlRecoverButton = QtWidgets.QPushButton(self.centralwidget)
        self.ControlRecoverButton.setGeometry(QtCore.QRect(1080, 670, 141, 27))
        self.ControlRecoverButton.setStyleSheet("")
        self.ControlRecoverButton.setObjectName("ControlRecoverButton")
        self.M3TitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.M3TitleLabel.setGeometry(QtCore.QRect(800, 600, 251, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.M3TitleLabel.setFont(font)
        self.M3TitleLabel.setObjectName("M3TitleLabel")
        self.Mission3Button = QtWidgets.QPushButton(self.centralwidget)
        self.Mission3Button.setGeometry(QtCore.QRect(800, 620, 241, 27))
        self.Mission3Button.setObjectName("Mission3Button")
        self.Mission2KeepcheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.Mission2KeepcheckBox.setGeometry(QtCore.QRect(880, 560, 151, 22))
        self.Mission2KeepcheckBox.setObjectName("Mission2KeepcheckBox")
        self.Mission4Button = QtWidgets.QPushButton(self.centralwidget)
        self.Mission4Button.setGeometry(QtCore.QRect(800, 670, 241, 27))
        self.Mission4Button.setObjectName("Mission4Button")
        self.M4TitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.M4TitleLabel.setGeometry(QtCore.QRect(800, 650, 251, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.M4TitleLabel.setFont(font)
        self.M4TitleLabel.setObjectName("M4TitleLabel")
        self.content_plot = QtWidgets.QWidget(self.centralwidget)
        self.content_plot.setGeometry(QtCore.QRect(420, 230, 301, 191))
        self.content_plot.setObjectName("content_plot")
        self.VoiceTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.VoiceTextBrowser.setGeometry(QtCore.QRect(1050, 100, 181, 171))
        self.VoiceTextBrowser.setObjectName("VoiceTextBrowser")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1060, 80, 101, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.VoiceControlCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.VoiceControlCheckBox.setGeometry(QtCore.QRect(1080, 300, 131, 22))
        self.VoiceControlCheckBox.setObjectName("VoiceControlCheckBox")
        self.VoiceListenCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.VoiceListenCheckBox.setGeometry(QtCore.QRect(1080, 280, 121, 22))
        self.VoiceListenCheckBox.setObjectName("VoiceListenCheckBox")
        self.SpeakingLabel = QtWidgets.QLabel(self.centralwidget)
        self.SpeakingLabel.setGeometry(QtCore.QRect(1140, 80, 81, 17))
        self.SpeakingLabel.setObjectName("SpeakingLabel")
        self.ROScheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.ROScheckBox.setGeometry(QtCore.QRect(800, 40, 211, 22))
        self.ROScheckBox.setObjectName("ROScheckBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(1050, 330, 181, 231))
        self.groupBox_2.setObjectName("groupBox_2")
        self.ros_console_button = QtWidgets.QPushButton(self.groupBox_2)
        self.ros_console_button.setGeometry(QtCore.QRect(10, 20, 71, 27))
        self.ros_console_button.setObjectName("ros_console_button")
        self.ros_graph_button = QtWidgets.QPushButton(self.groupBox_2)
        self.ros_graph_button.setGeometry(QtCore.QRect(10, 50, 71, 27))
        self.ros_graph_button.setObjectName("ros_graph_button")
        self.ros_plot_button = QtWidgets.QPushButton(self.groupBox_2)
        self.ros_plot_button.setGeometry(QtCore.QRect(10, 80, 71, 27))
        self.ros_plot_button.setObjectName("ros_plot_button")
        self.ros_image_button = QtWidgets.QPushButton(self.groupBox_2)
        self.ros_image_button.setGeometry(QtCore.QRect(10, 110, 71, 27))
        self.ros_image_button.setObjectName("ros_image_button")
        self.ros_rqt_button = QtWidgets.QPushButton(self.groupBox_2)
        self.ros_rqt_button.setGeometry(QtCore.QRect(10, 140, 71, 27))
        self.ros_rqt_button.setObjectName("ros_rqt_button")
        self.ros_rviz_button = QtWidgets.QPushButton(self.groupBox_2)
        self.ros_rviz_button.setGeometry(QtCore.QRect(100, 20, 71, 27))
        self.ros_rviz_button.setObjectName("ros_rviz_button")
        self.ros_gazebo_button = QtWidgets.QPushButton(self.groupBox_2)
        self.ros_gazebo_button.setGeometry(QtCore.QRect(100, 50, 71, 27))
        self.ros_gazebo_button.setObjectName("ros_gazebo_button")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(40, 230, 181, 101))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 210, 673, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(230, 230, 181, 101))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_4)
        self.label_8 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_8.setObjectName("label_8")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_5)
        self.label_9 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_9.setObjectName("label_9")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_6)
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_7.setObjectName("label_7")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.checkBox_6DAble = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_6DAble.setGeometry(QtCore.QRect(40, 370, 291, 21))
        self.checkBox_6DAble.setObjectName("checkBox_6DAble")
        self.checkBox_DFsensor_able = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_DFsensor_able.setGeometry(QtCore.QRect(40, 340, 171, 21))
        self.checkBox_DFsensor_able.setObjectName("checkBox_DFsensor_able")
        self.content_plot.raise_()
        self.CamImgGroup.raise_()
        self.groupBox.raise_()
        self.DetectedItemsLabel.raise_()
        self.DetectedListView.raise_()
        self.pushButton.raise_()
        self.Mission2Button.raise_()
        self.M1TitleLabel.raise_()
        self.M2TitleLabel.raise_()
        self.Mission1Button.raise_()
        self.MissionAbsortButton.raise_()
        self.label.raise_()
        self.ControlRecoverButton.raise_()
        self.M3TitleLabel.raise_()
        self.Mission3Button.raise_()
        self.Mission2KeepcheckBox.raise_()
        self.Mission4Button.raise_()
        self.M4TitleLabel.raise_()
        self.VoiceTextBrowser.raise_()
        self.label_2.raise_()
        self.VoiceControlCheckBox.raise_()
        self.VoiceListenCheckBox.raise_()
        self.SpeakingLabel.raise_()
        self.ROScheckBox.raise_()
        self.groupBox_2.raise_()
        self.formLayoutWidget_2.raise_()
        self.label_3.raise_()
        self.formLayoutWidget_3.raise_()
        self.checkBox_6DAble.raise_()
        self.checkBox_DFsensor_able.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1246, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "A.R.C Intelligent Grasping Robotics System (Author: Chen Yiwen cywgoog@gmail.com)"))
        self.groupBox.setTitle(_translate("MainWindow", "Camera Reading Data"))
        self.Cam_iiwa_label_title.setText(_translate("MainWindow", "IIwa"))
        self.Cam_iiwa_label_content_label.setText(_translate("MainWindow", "Wating for Data"))
        self.Cam_bottle_label_title.setText(_translate("MainWindow", "Bottle"))
        self.Cam_bottle_label_content_label.setText(_translate("MainWindow", "Wating for Data"))
        self.Cam_cube_label_title.setText(_translate("MainWindow", "Cube"))
        self.Cam_cube_label_content_label.setText(_translate("MainWindow", "Wating for Data"))
        self.Cam_f_title.setText(_translate("MainWindow", "F/hz"))
        self.Cam_f_cont.setText(_translate("MainWindow", "0"))
        self.Cam_hand_label_title.setText(_translate("MainWindow", "Hand"))
        self.Cam_hand_label_content_label.setText(_translate("MainWindow", "Wating for Data"))
        self.CamImgGroup.setTitle(_translate("MainWindow", "Camera Image"))
        self.CamCVImageLabel.setText(_translate("MainWindow", "CV"))
        self.DetectedItemsLabel.setText(_translate("MainWindow", "Detected Items "))
        self.pushButton.setText(_translate("MainWindow", "Connect IIWA"))
        self.Mission2Button.setText(_translate("MainWindow", "Do Mission2"))
        self.M1TitleLabel.setText(_translate("MainWindow", "Mission 1 Obj Grasp&Place "))
        self.M2TitleLabel.setText(_translate("MainWindow", "Mission 2 Hand Tracking"))
        self.Mission1Button.setText(_translate("MainWindow", "Do Mission1"))
        self.MissionAbsortButton.setText(_translate("MainWindow", "STOP"))
        self.label.setText(_translate("MainWindow", "Attention: \n"
"Be Sure Only one hand  in camera"))
        self.ControlRecoverButton.setText(_translate("MainWindow", "Recover"))
        self.M3TitleLabel.setText(_translate("MainWindow", "Mission 3 Fetch Obj for Me"))
        self.Mission3Button.setText(_translate("MainWindow", "Do Mission3"))
        self.Mission2KeepcheckBox.setText(_translate("MainWindow", "Keeping Tracking"))
        self.Mission4Button.setText(_translate("MainWindow", "Do Mission4"))
        self.M4TitleLabel.setText(_translate("MainWindow", "Mission 4 Hand Remote Control"))
        self.content_plot.setProperty("text", _translate("MainWindow", "content_plot"))
        self.label_2.setText(_translate("MainWindow", "Voice"))
        self.VoiceControlCheckBox.setText(_translate("MainWindow", "Voice Control"))
        self.VoiceListenCheckBox.setText(_translate("MainWindow", "Voice Listen"))
        self.SpeakingLabel.setText(_translate("MainWindow", "Speaking"))
        self.ROScheckBox.setText(_translate("MainWindow", "Publish to ROS"))
        self.groupBox_2.setTitle(_translate("MainWindow", "ROS TOOLS"))
        self.ros_console_button.setText(_translate("MainWindow", "console"))
        self.ros_graph_button.setText(_translate("MainWindow", "graph"))
        self.ros_plot_button.setText(_translate("MainWindow", "plot"))
        self.ros_image_button.setText(_translate("MainWindow", "image"))
        self.ros_rqt_button.setText(_translate("MainWindow", "rqt"))
        self.ros_rviz_button.setText(_translate("MainWindow", "Rviz"))
        self.ros_gazebo_button.setText(_translate("MainWindow", "Gazebo"))
        self.label_4.setText(_translate("MainWindow", "Joint Speed"))
        self.lineEdit.setText(_translate("MainWindow", "0.1"))
        self.label_5.setText(_translate("MainWindow", "Max Force"))
        self.lineEdit_2.setText(_translate("MainWindow", "15"))
        self.label_6.setText(_translate("MainWindow", "Robot Name"))
        self.lineEdit_3.setText(_translate("MainWindow", "IIWA"))
        self.label_3.setText(_translate("MainWindow", "Parameters (Testing)"))
        self.lineEdit_4.setText(_translate("MainWindow", "2.55"))
        self.label_8.setText(_translate("MainWindow", "para2"))
        self.lineEdit_5.setText(_translate("MainWindow", "3.48"))
        self.label_9.setText(_translate("MainWindow", "para3"))
        self.lineEdit_6.setText(_translate("MainWindow", "552.1"))
        self.label_7.setText(_translate("MainWindow", "para1"))
        self.checkBox_6DAble.setText(_translate("MainWindow", " Show 6D Estimation"))
        self.checkBox_DFsensor_able.setText(_translate("MainWindow", "6D Estimation"))

