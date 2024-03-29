import rospy
import utm
import sys
import serial
import time
import math
import rosbag
import numpy as np
import matplotlib.pyplot as plt



bag = rosbag.Bag("/home/nikhil/Downloads/LAB_Structure_Checker/Structure_Checker/EECE5554/LAB3/src/Data/stationary_nikhil.bag")



orientation_x = []
orientation_y = []
orientation_z = []
gyro_x = []
gyro_y = []
gyro_z = []
accel_x = []
accel_y = []
accel_z = []



for topic, msg, t in bag.read_messages(topics=['/imu']):

    w = msg.imu.orientation.w
    x = msg.imu.orientation.x
    y = msg.imu.orientation.y
    z = msg.imu.orientation.z
    # Convert quaternion to Euler angles
    roll = math.atan2(2*(w*x + y*z), 1 - 2*(x*x + y*y))
    pitch = math.asin(2*(w*y - x*z))
    yaw = math.atan2(2*(w*z + x*y), 1 - 2*(y*y + z*z))
    gyro_x.append(roll)
    gyro_y.append(pitch)
    gyro_z.append(yaw)

fig, axs = plt.subplots()
axs.plot(gyro_x, label='Roll')
axs.plot(gyro_y, label='Pitch')
axs.plot(gyro_z, label='Yaw')
axs.set_title('Orientation')
axs.set_xlabel('Time in seconds')
axs.set_ylabel('Orientation in Euler angles (radians)')
axs.legend()
plt.show()

for topic, msg, t in bag.read_messages(topics=['/imu']):
    accel_x.append(msg.imu.linear_acceleration.x)
    accel_y.append(msg.imu.linear_acceleration.y)
    accel_z.append(msg.imu.linear_acceleration.z)

fig, axs = plt.subplots()
axs.plot(accel_x, label='x')
axs.plot(accel_y, label='y')
axs.plot(accel_z, label='z')
axs.set_title('Acceleration')
axs.set_xlabel('Time')
axs.set_ylabel('Acceleration (m/s^2)')
axs.legend()
plt.show()

for topic, msg, t in bag.read_messages(topics=['/imu']):

    gyro_x.append(msg.imu.angular_velocity.x)
    gyro_y.append(msg.imu.angular_velocity.y)
    gyro_z.append(msg.imu.angular_velocity.z)

fig, axs = plt.subplots()
axs.plot(gyro_x, label='x')
axs.plot(gyro_y, label='y')
axs.plot(gyro_z, label='z')
axs.set_title('Gyro')
axs.set_xlabel('Time')
axs.set_ylabel('Gyro in rad/sec')
axs.legend()
plt.show()


accel_x = []
for topic, msg, t in bag.read_messages(topics=['/imu']):
    accel_x.append(msg.imu.linear_acceleration.x)

mean = np.mean(accel_x)
median = np.median(accel_x)
std_dev = np.std(accel_x)
print(mean)
print(median)
print(std_dev)
fig, axs = plt.subplots()
axs.hist(accel_x, bins=20)
axs.axvline(mean, color='red', label='Mean')
axs.axvline(median, color='green', label='Median')
axs.axvline(mean+std_dev, color='orange', linestyle='--', label='+1 SD')
axs.axvline(mean-std_dev, color='orange', linestyle='--', label='-1 SD')
axs.set_title('Acceleration X-axis')
axs.set_xlabel('Acceleration (m/s^2)')
axs.set_ylabel('Frequency')
axs.legend()
plt.show()