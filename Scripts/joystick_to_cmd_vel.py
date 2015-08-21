#!/usr/bin/env python

__author__ = 'Han Wopereis'
__contact__ = 'hanwopereis@gmail.com'

"""
This executable converts joystick values to cmd_vel commands (TwistStamped):
"""

# Ros imports
import rospy
import geometry_msgs.msg
import sensor_msgs.msg

# Initialize global data
publishLocation = '/aeroquad/cmd_vel_joy'
cmd_vel_msg = geometry_msgs.msg.TwistStamped()

gain_x = 1
gain_y = 1
gain_z = 1
gain_yaw = 1

def joystickConverter():

    # Init ROS
    rospy.init_node('joystick_to_cmd_vel')
    rate = rospy.Rate(100)
    
    gain_x      = rospy.get_param('joy_gain_x',10)
    gain_y      = rospy.get_param('joy_gain_y',-10)
    gain_z      = rospy.get_param('joy_gain_z',1)
    gain_yaw    = rospy.get_param('joy_gain_yaw',1)
    
    
    # Init ROS publisher
    pub_cmd_vel = rospy.Publisher(publishLocation, geometry_msgs.msg.TwistStamped, queue_size=1)
    sub_joy = rospy.Subscriber('/joy',sensor_msgs.msg.Joy,getJoystickValues)
  
    print "===== Initializing joystick_to_cmd_vel converter ====="
    print ""
    print "Converter_node started."
    print "Publisher started: ", pub_cmd_vel
    print "Subscriber started: ", sub_joy
    print ""
    print "Publishes on:" + publishLocation
    print ""    
    print "-----------------------------"
    print ""
   
    # Main loop
    while not rospy.is_shutdown():
        
        pub_cmd_vel.publish(cmd_vel_msg)
        rate.sleep()
    
def getJoystickValues(msg):
        
    roll = msg.axes[0]
    pitch = msg.axes[1]
    yaw = msg.axes[2]
    thrust = msg.axes[3]
    
    cmd_vel_msg.header = msg.header
    cmd_vel_msg.twist.linear.x = gain_x*roll
    cmd_vel_msg.twist.linear.y = gain_y*pitch
    cmd_vel_msg.twist.linear.z = gain_z*thrust
    cmd_vel_msg.twist.angular.x = 0
    cmd_vel_msg.twist.angular.y = 0    
    cmd_vel_msg.twist.angular.z = gain_yaw*yaw
    

if __name__ == '__main__':
    # Enable verbose to get textual feedback.
    VERBOSE = 0
    SIMPLE_VERBOSE = 1
    # Run node --> Node will loop in its initialization function. 
    joystickConverter()







