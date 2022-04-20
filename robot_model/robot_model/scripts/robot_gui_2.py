#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import time
from PyQt5 import QtCore, QtGui, QtWidgets


moveBindings = {
                "forward": (1,0,0,0),
                "backward": (-1,0,0,0),
                "left": (0,0,0,1), # Goc nguoc chieu kim dong ho la goc duong
                "right": (0,0,0,-1),
                "stop": (0,0,0,0)
            }


class Ui_WINDOW(object):
    def __init__(self):
        rospy.init_node("listener", anonymous=True)
        self.nodeName = rospy.get_name()
        rospy.loginfo("Started %s" %self.nodeName)

        rospy.Subscriber("raw_vel", Twist, self.callback)
        self.pub_vel = rospy.Publisher("cmd_vel", Twist, queue_size=1)

        self.init_variable()
   
    def init_variable(self):
        self.data = ""
        self.dir = ""
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0

        self.speed = 0.35
        self.turn = 0.50

        self.twist = Twist()


    def setupUi(self, WINDOW):
        WINDOW.setObjectName("WINDOW")
        WINDOW.resize(930, 587)
        # AUTO MODE CHECKBOX
        self.auto_mode_checkbox = QtWidgets.QCheckBox(WINDOW)
        self.auto_mode_checkbox.setEnabled(True)
        self.auto_mode_checkbox.setGeometry(QtCore.QRect(20, 20, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.auto_mode_checkbox.setFont(font)
        self.auto_mode_checkbox.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.auto_mode_checkbox.setAutoFillBackground(False)
        self.auto_mode_checkbox.setObjectName("auto_mode_checkbox")

        #mANUAL MODE CHECKBOX
        self.manual_mode_checkbox = QtWidgets.QCheckBox(WINDOW)
        self.manual_mode_checkbox.setGeometry(QtCore.QRect(20, 60, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.manual_mode_checkbox.setFont(font)
        self.manual_mode_checkbox.setObjectName("manual_mode_checkbox")

        # VEL X LABEL
        self.vel_x_label = QtWidgets.QLabel(WINDOW)
        self.vel_x_label.setGeometry(QtCore.QRect(20, 110, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.vel_x_label.setFont(font)
        self.vel_x_label.setFrameShape(QtWidgets.QFrame.Box)
        self.vel_x_label.setObjectName("vel_x_label")

        # ANG Z LABEL
        self.ang_z_label = QtWidgets.QLabel(WINDOW)
        self.ang_z_label.setGeometry(QtCore.QRect(20, 170, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.ang_z_label.setFont(font)
        self.ang_z_label.setFrameShape(QtWidgets.QFrame.Box)
        self.ang_z_label.setObjectName("ang_z_label")

        # DIRECTION LABEL
        self.direction_label = QtWidgets.QLabel(WINDOW)
        self.direction_label.setGeometry(QtCore.QRect(520, 20, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.direction_label.setFont(font)
        self.direction_label.setFrameShape(QtWidgets.QFrame.Box)
        self.direction_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.direction_label.setObjectName("direction_label")

        # GROUP BOX 
        self.gridGroupBox = QtWidgets.QGroupBox(WINDOW)
        self.gridGroupBox.setGeometry(QtCore.QRect(370, 70, 541, 301))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridGroupBox.sizePolicy().hasHeightForWidth())
        self.gridGroupBox.setSizePolicy(sizePolicy)
        self.gridGroupBox.setObjectName("gridGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.gridGroupBox)
        self.gridLayout.setObjectName("gridLayout")

        #BACKWARD BUTTON
        self.backward_button = QtWidgets.QPushButton(self.gridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backward_button.sizePolicy().hasHeightForWidth())
        self.backward_button.setSizePolicy(sizePolicy)
        self.backward_button.setObjectName("backward_button")
        self.gridLayout.addWidget(self.backward_button, 2, 1, 1, 1)

        # STOP BUTTON
        self.stop_button = QtWidgets.QPushButton(self.gridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
        self.stop_button.setSizePolicy(sizePolicy)
        self.stop_button.setObjectName("stop_button")
        self.gridLayout.addWidget(self.stop_button, 1, 1, 1, 1)

        #FORWARD BUTTON
        self.forward_button = QtWidgets.QPushButton(self.gridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.forward_button.sizePolicy().hasHeightForWidth())
        self.forward_button.setSizePolicy(sizePolicy)
        self.forward_button.setObjectName("forward_button")
        self.gridLayout.addWidget(self.forward_button, 0, 1, 1, 1)

        #TURN LEFT BUTTON
        self.turn_left_button = QtWidgets.QPushButton(self.gridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.turn_left_button.sizePolicy().hasHeightForWidth())
        self.turn_left_button.setSizePolicy(sizePolicy)
        self.turn_left_button.setObjectName("turn_left_button")
        self.gridLayout.addWidget(self.turn_left_button, 1, 0, 1, 1)

        #TURN RIGHT BUTTON
        self.turn_right_button = QtWidgets.QPushButton(self.gridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.turn_right_button.sizePolicy().hasHeightForWidth())
        self.turn_right_button.setSizePolicy(sizePolicy)
        self.turn_right_button.setObjectName("turn_right_button")
        self.gridLayout.addWidget(self.turn_right_button, 1, 2, 1, 1)

        #SPEED SLIDER
        self.speed_slider = QtWidgets.QSlider(self.gridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speed_slider.sizePolicy().hasHeightForWidth())
        self.speed_slider.setSizePolicy(sizePolicy)
        self.speed_slider.setOrientation(QtCore.Qt.Vertical)
        self.speed_slider.setObjectName("speed_slider")
        self.gridLayout.addWidget(self.speed_slider, 0, 3, 3, 1)

        #TURN SLIDER
        self.turn_slider = QtWidgets.QSlider(self.gridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.turn_slider.sizePolicy().hasHeightForWidth())
        self.turn_slider.setSizePolicy(sizePolicy)
        self.turn_slider.setOrientation(QtCore.Qt.Vertical)
        self.turn_slider.setObjectName("turn_slider")
        self.gridLayout.addWidget(self.turn_slider, 0, 4, 3, 1)

        # SPEED SLIDER LABEL
        self.speed_slider_label = QtWidgets.QLabel(self.gridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speed_slider_label.sizePolicy().hasHeightForWidth())
        self.speed_slider_label.setSizePolicy(sizePolicy)
        self.speed_slider_label.setObjectName("speed_slider_label")
        self.gridLayout.addWidget(self.speed_slider_label, 3, 3, 1, 1)

        # TURN SLIDER LABEL
        self.turn_slider_label = QtWidgets.QLabel(self.gridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.turn_slider_label.sizePolicy().hasHeightForWidth())
        self.turn_slider_label.setSizePolicy(sizePolicy)
        self.turn_slider_label.setObjectName("turn_slider_label")
        self.gridLayout.addWidget(self.turn_slider_label, 3, 4, 1, 1)

        # SPEED LABEL
        # self.speed_label = QtWidgets.QLabel(WINDOW)
        # self.speed_label.setGeometry(QtCore.QRect(360, 420, 181, 41))
        # font = QtGui.QFont()
        # font.setPointSize(20)
        # font.setBold(True)
        # font.setWeight(75)
        # self.speed_label.setFont(font)
        # self.speed_label.setFrameShape(QtWidgets.QFrame.Box)
        # self.speed_label.setObjectName("speed_label")
        
        # TURN LABEL
        # self.turn_label = QtWidgets.QLabel(WINDOW)
        # self.turn_label.setGeometry(QtCore.QRect(690, 420, 181, 41))
        # font = QtGui.QFont()
        # font.setPointSize(20)
        # font.setBold(True)
        # font.setWeight(75)
        # self.turn_label.setFont(font)
        # self.turn_label.setFrameShape(QtWidgets.QFrame.Box)
        # self.turn_label.setObjectName("turn_label")


        self.update_value()

        

        self.turn_right_button.clicked.connect(self.TURN_RIGHT)
        self.forward_button.clicked.connect(self.FORWARD)
        self.turn_left_button.clicked.connect(self.TURN_LEFT)
        self.backward_button.clicked.connect(self.BACKWARD)
        self.stop_button.clicked.connect(self.STOP)
        self.auto_mode_checkbox.stateChanged['int'].connect(self.CHECK)
        self.manual_mode_checkbox.stateChanged['int'].connect(self.CHECK)

        self.speed_slider.setValue(int(self.speed * 100 / 2))
        self.speed_slider.setTickPosition(QtWidgets.QSlider.TicksLeft)
        self.speed_slider.setTickInterval(20)
        self.speed_slider.valueChanged.connect(self.SPEED_SLIDER)
        
        self.turn_slider.setValue(int(self.turn * 100 / 2))
        self.turn_slider.setTickPosition(QtWidgets.QSlider.TicksLeft)
        self.turn_slider.setTickInterval(20)
        self.turn_slider.valueChanged.connect(self.TURN_SLIDER)


        self.retranslateUi(WINDOW)

        QtCore.QMetaObject.connectSlotsByName(WINDOW)

    def retranslateUi(self, WINDOW):
        _translate = QtCore.QCoreApplication.translate
        WINDOW.setWindowTitle(_translate("WINDOW", "Form"))
        self.auto_mode_checkbox.setText(_translate("WINDOW", "Auto Mode"))
        self.manual_mode_checkbox.setText(_translate("WINDOW", "Manual Mode"))
        self.vel_x_label.setText(_translate("WINDOW", "Vel x:"))
        self.ang_z_label.setText(_translate("WINDOW", "Ang z:"))
        self.direction_label.setText(_translate("WINDOW", "Direction: "))
        self.forward_button.setText(_translate("WINDOW", "Forward"))
        self.turn_left_button.setText(_translate("WINDOW", "Left"))
        self.stop_button.setText(_translate("WINDOW", "Stop"))
        self.turn_right_button.setText(_translate("WINDOW", "Right"))
        self.speed_slider_label.setText(_translate("WINDOW", "Speed range: {}".format(float(self.speed_slider.value())*2/100)))
        self.turn_slider_label.setText(_translate("WINDOW", "Turning range:{}".format(float(self.turn_slider.value())*2/100)))
        self.backward_button.setText(_translate("WINDOW", "Backward"))
        # self.speed_label.setText(_translate("WINDOW", "Speed: "))
        # self.turn_label.setText(_translate("WINDOW", "Turning "))

    def TURN_LEFT(self):
        self.x = moveBindings["left"][0]
        self.y = moveBindings["left"][1]
        self.z = moveBindings["left"][2]
        self.th = moveBindings["left"][3]
    
    def TURN_RIGHT(self):
        self.x = moveBindings["right"][0]
        self.y = moveBindings["right"][1]
        self.z = moveBindings["right"][2]
        self.th = moveBindings["right"][3]
    
    def FORWARD(self):
        self.x = moveBindings["forward"][0]
        self.y = moveBindings["forward"][1]
        self.z = moveBindings["forward"][2]
        self.th = moveBindings["forward"][3]
         
    def BACKWARD(self):
        self.x = moveBindings["backward"][0]
        self.y = moveBindings["backward"][1]
        self.z = moveBindings["backward"][2]
        self.th = moveBindings["backward"][3]

    def STOP(self):
        self.x = moveBindings["stop"][0]
        self.y = moveBindings["stop"][1]
        self.z = moveBindings["stop"][2]
        self.th = moveBindings["stop"][3]
       
    def CHECK(self):
        if self.auto_mode_checkbox.isChecked() == True:
            print("auto mode is ON")
        else:
            print("auto mode is OFF")
        
        if self.manual_mode_checkbox.isChecked() == True:
            print("manual mode is ON")
        else:
            print("manual mode is OFF")

    def SPEED_SLIDER(self, value):
        value = float(value * 2) / 100
        text = "Speed range: {}".format(value)
        self.speed_slider_label.setText(str(text))
        self.speed = value
        # self.speed_label.setText(str(value))

    def TURN_SLIDER(self, value):
        value = float(value * 2) / 100
        text = "speed range: {}".format(value)
        self.turn_slider_label.setText(str(text))
        self.turn = value
        

    def add(self, count):

        self.twist.linear.x = self.x * self.speed
        self.twist.linear.y = self.y * self.speed
        self.twist.linear.z = self.z * self.speed


        self.twist.angular.x = 0
        self.twist.angular.y = 0
        self.twist.angular.z = self.th * self.turn

        self.update_direction()
        
        self.pub_vel.publish(self.twist)
        
    def update_direction(self):
        if self.x == 1 and self.th == 0:
            self.dir = "fb"
        elif self.x == -1 and self.th == 0:
            self.dir = "bd"
        elif self.x == 0 and self.th == 1:
            self.dir = "left"
        elif self.x == 0 and self.th == -1:
            self.dir = "right"
        elif self.x == 0 and self.th == 0:
            self.dir = "stop"
        text = "Dir: {}".format(self.dir)
        self.direction_label.setText(text)

    def update_value(self):
        self.thread = WorkThread()
        self.thread.start()
        self.thread.signal.connect(self.add)

    def callback(self, data):
        linear_x = data.linear.x
        angular_z = data.angular.z
        rospy.loginfo("I heard %d and %d", linear_x, angular_z)
        vel_x_text = "Vel_x: {}".format(linear_x)
        ang_z_text = "Ang_z: {}".format(angular_z)
        self.vel_x_label.setText(vel_x_text)
        self.ang_z_label.setText(ang_z_text)


        


class WorkThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    def __init__(self):
        QtCore.QThread.__init__(self)
    
    def __del__(self):
        self.wait()
    
    def run(self):
        count = 0
        while not rospy.is_shutdown():

            time.sleep(0.3)

            self.signal.emit(" ")
            r = rospy.Rate(50)
            r.sleep()
        return



if __name__ == "__main__":



    import sys

   
    app = QtWidgets.QApplication(sys.argv)
    WINDOW = QtWidgets.QWidget()
    ui = Ui_WINDOW()
    ui.setupUi(WINDOW)
    WINDOW.show()
    sys.exit(app.exec_())
