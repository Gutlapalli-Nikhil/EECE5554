#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(data):
	msg = data.data
	
	## Replacing the characters in a string
	new_msg = msg.replace("H","#")
	new_msg = new_msg.replace("a","@")
	
	## Lowercase to Uppercase
	new_msg = new_msg.upper()		
		
	rospy.loginfo("I heard %s", new_msg)

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("chatter", String, callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
