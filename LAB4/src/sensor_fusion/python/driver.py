import rospy
import utm
import sys
import serial
from sensor_fusion.msg import Vectornav as IMU
import time
import math
from sensor_fusion.srv import convert_to_quaternion, convert_to_quaternionRequest



def talker():
	rospy.init_node('driver')
	serial_port = rospy.get_param('imu_port','/dev/pts/')

	port = serial.Serial(serial_port, 115200)
	config_string = '$VNWRG,6,0\r\n'  # This string configures the VectorNav to output data at 40 Hz
	
	port.write(config_string.encode())
	values_pub = rospy.Publisher("imu", IMU, queue_size=5)
	imu_msgs = IMU()
	rate = rospy.Rate(40)
	imu_msgs.Header.frame_id = "imu1_frame"
	seq = 0
	print("Waiting...")
	rospy.wait_for_service('eigan_to_quaternion')
	while not rospy.is_shutdown():

		data = port.readline()
		
		output = data.decode('latin-1')
		
		if "VNYMR" in output:
					print(output)
					parts = output.split(",")
					
					now = time.time()
					secs = int(now)
					nsecs = int((now - secs) * 10**9)

					imu_msgs.Header.seq = seq
					imu_msgs.Header.stamp.secs = secs
					imu_msgs.Header.stamp.nsecs = nsecs

					yaw = float(parts[1])
					pitch = float(parts[2])
					roll = float(parts[3])

					yaw_radians = math.radians(yaw)
					pitch_radians = math.radians(pitch)
					roll_radians = math.radians(roll)

					eigan_to_quaternion = rospy.ServiceProxy('eigan_to_quaternion', convert_to_quaternion)
					req = convert_to_quaternionRequest()
					req.yaw = yaw_radians
					req.pitch = pitch_radians
					req.roll = roll_radians

					req = eigan_to_quaternion(req)
					imu_msgs.imu.orientation.w = req.w
					imu_msgs.imu.orientation.x = req.x
					imu_msgs.imu.orientation.y = req.y
					imu_msgs.imu.orientation.z = req.z

					imu_msgs.imu.angular_velocity.x = float(parts[10])
					imu_msgs.imu.angular_velocity.y = float(parts[11])
					imu_msgs.imu.angular_velocity.z = float(parts[12][:-5])

					imu_msgs.imu.linear_acceleration.x = float(parts[7])
					imu_msgs.imu.linear_acceleration.y = float(parts[8])
					imu_msgs.imu.linear_acceleration.z = float(parts[9])

					imu_msgs.mag_field.magnetic_field.x = float(parts[4])
					imu_msgs.mag_field.magnetic_field.y = float(parts[5])
					imu_msgs.mag_field.magnetic_field.z = float(parts[6])

					imu_msgs.imu_raw_data = str(output)

					seq = seq + 1
					values_pub.publish(imu_msgs)
					rate.sleep() 

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass

