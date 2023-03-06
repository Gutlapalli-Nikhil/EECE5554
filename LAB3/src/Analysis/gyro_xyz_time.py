import rospy
import utm
import sys
import serial
import time
import math
import rosbag
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
gyro_x = []
gyro_y = []
gyro_z = []

import bagpy
from bagpy import bagreader
import pandas as pd
import matplotlib.pyplot as plt

import csv

gpsdf = pd.read_csv("/home/nikhil/Downloads/LAB_Structure_Checker/Structure_Checker/EECE5554/LAB3/src/Data/motion_data/imu.csv")

for i in range(1551):
	gyro_x.append(gpsdf["imu.angular_velocity.x"][i])
	gyro_y.append(gpsdf["imu.angular_velocity.y"][i])
	gyro_z.append(gpsdf["imu.angular_velocity.z"][i])

fig, axs = plt.subplots()
axs.plot(gyro_x, label='x')
axs.plot(gyro_y, label='y')
axs.plot(gyro_z, label='z')
axs.set_title('Gyro')
axs.set_xlabel('Time')
axs.set_ylabel('Gyro in rad/sec')
axs.legend()

gyro_x = []
gyro_y = []
gyro_z = []
for i in range(1100, 1500):
	gyro_x.append(gpsdf["imu.linear_acceleration.x"][i])
	gyro_y.append(gpsdf["imu.linear_acceleration.y"][i])
	gyro_z.append(gpsdf["imu.linear_acceleration.z"][i])

fig, axs = plt.subplots()
axs.plot(gyro_x, label='x')
# axs.plot(gyro_y, label='y')
# axs.plot(gyro_z, label='z')
axs.set_title('linear_acceleration')
axs.set_xlabel('Time')
axs.set_ylabel('linear_acceleration in rad/sec^2')
axs.legend()


gyro_x = []
gyro_y = []
gyro_z = []
for i in range(1250, 1500):
	x = gpsdf["imu.orientation.x"][i]
	y = gpsdf["imu.orientation.y"][i]
	z = gpsdf["imu.orientation.z"][i]
	w = gpsdf["imu.orientation.w"][i]
	R = np.array([[1-2*(y**2+z**2), 2*(x*y-z*w), 2*(x*z+y*w)],
                  [2*(x*y+z*w), 1-2*(x**2+z**2), 2*(y*z-x*w)],
                  [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x**2+y**2)]])
	roll = math.atan2(R[2,1], R[2,2])
	pitch = -math.asin(R[2,0])
	yaw = math.atan2(R[1,0], R[0,0])
	gyro_x.append(roll)
	gyro_y.append(pitch)
	gyro_z.append(yaw)

fig, axs = plt.subplots()
# axs.plot(gyro_x, label='Roll')
# axs.plot(gyro_y, label='Pitch')
axs.plot(gyro_z, label='Yaw')
axs.set_title('Yaw')
axs.set_xlabel('Time')
axs.set_ylabel('Yaw in eigan')
axs.legend()
plt.show()