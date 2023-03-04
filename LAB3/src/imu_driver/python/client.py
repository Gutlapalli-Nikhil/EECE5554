#!/usr/bin/env python3

import rospy
from imu_driver.srv import AddTwoInts, AddTwoIntsRequest

def add_two_ints_client(x, y):
    rospy.wait_for_service('add_two_ints')
    try:
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
        req = AddTwoIntsRequest()
        req.a = x
        req.b = y
        response = add_two_ints(req)
        return response.sum
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

if __name__ == '__main__':
    x = 45
    y = 2
    print("Requesting %s + %s"%(x, y))
    result = add_two_ints_client(x, y)
    print("Result: %s"%result)
