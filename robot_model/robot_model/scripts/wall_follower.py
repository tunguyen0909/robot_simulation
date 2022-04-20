#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations

import math 

state_ = 0

"""
RObot in simulator is rotate 0 degree 

"""

right_range = 270
left_range = 90
font_range = 0
back_range = 180

def change_state(state):
    global state_
    state_ = state
    

def take_action(regions):
	print("==========================================================")
	for dir in regions:
		print("{}: {}".format(dir, regions[dir]))

	"""
    if regions["front"] <= 0.4:
        print("Turning right")
        change_state(2) # Turn right

    else:
        if regions["left"] <= 0.4:
            print("follow wall")
            change_state(0) # forward
        else:
            print("turn left")
            change_state(1) # turn left

        if regions["fleft"] <= 0.3:
            change_state(2) # turn 

	"""

	print("==========================================================")

def laser_callback(msg):
    print(len(msg.ranges[:]))

    # front_range = msg.ranges[0:46] + msg.ranges[675:719]
    # front_range = msg.ranges[135:225]

    regions = {
        "front": msg.ranges[1],
        "left": msg.ranges[90],
        "right": msg.ranges[270],
        "fleft": msg.ranges[180],
        #"fright": min(msg.ranges[225:315])

    }

    take_action(regions)


def forward():
    msg = Twist()
    msg.linear.x = 0.3
    msg.angular.z = 0
    return msg

def turn_left():
    msg = Twist()
    msg.linear.x = 0.1
    msg.angular.z = 0.4
    return msg

def turn_right():
    msg = Twist()
    msg.linear.x = 0.1
    msg.angular.z = -0.4
    return msg


def main():
    rospy.init_node("reading_laser")

    sub = rospy.Subscriber("base_scan", LaserScan, laser_callback)

    pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)

    rate = rospy.Rate(20)

    while not rospy.is_shutdown():

        msg = Twist()

        if state_ == 0:
            msg = forward()
        
        elif state_ == 1:
            msg = turn_left()
        
        elif state_ == 2:
            msg = turn_right()

        pub.publish(msg)
        rate.sleep()

if __name__ == "__main__":
    main()
