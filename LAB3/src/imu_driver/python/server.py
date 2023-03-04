#!/usr/bin/env python

import rospy
import math
from imu_driver.srv import convert_to_quaternion, convert_to_quaternionResponse

def handle_convert_to_quaternion(req):
    resp = convert_to_quaternionResponse()
    resp.w = math.cos(req.roll/2) * math.cos(req.pitch/2) * math.cos(req.yaw/2) + math.sin(req.roll/2) * math.sin(req.pitch/2) * math.sin(req.yaw/2)
    resp.x = math.sin(req.roll/2) * math.cos(req.pitch/2) * math.cos(req.yaw/2) - math.cos(req.roll/2) * math.sin(req.pitch/2) * math.sin(req.yaw/2)
    resp.y = math.cos(req.roll/2) * math.sin(req.pitch/2) * math.cos(req.yaw/2) + math.sin(req.roll/2) * math.cos(req.pitch/2) * math.sin(req.yaw/2)
    resp.z = math.cos(req.roll/2) * math.cos(req.pitch/2) * math.sin(req.yaw/2) - math.sin(req.roll/2) * math.sin(req.pitch/2) * math.cos(req.yaw/2)
    return resp
	
def eigan_to_quaternion_server():
    rospy.init_node('eigan_to_quaternion_server')
    s = rospy.Service('eigan_to_quaternion', convert_to_quaternion, handle_convert_to_quaternion)
    print("Ready to convert eigan to quaternion.")
    rospy.spin()

if __name__ == "__main__":
    eigan_to_quaternion_server()
