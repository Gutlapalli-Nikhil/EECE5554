import rospy
import utm
import sys
import serial
from gnss_driver.msg import gnss_msgs as GPS

def transforms_gpgga_to_utm(latitude, longitude):
	
	(utm_easting, utm_northing, zone_number, zone_letter) = utm.from_latlon(latitude, longitude)
	
	return utm_easting, utm_northing, zone_number, zone_letter

def talker():
	rospy.init_node('driver')
	serial_port = rospy.get_param('/port', '/dev/ttyACM0')
	port = serial.Serial(serial_port, 57600)
	values_pub = rospy.Publisher("gps", GPS, queue_size=5)
	gps_msgs = GPS()
	rate = rospy.Rate(10)
	gps_msgs.Header.frame_id = "GPS1_Frame"
	seq = 0
	
	while not rospy.is_shutdown():

		data = port.readline()
		
		output = data.decode('latin-1')

		if "GNGGA" in output:

					parts = output.split(",")
					print(parts)
					
					time_str = parts[1]
					time_float = float(time_str)

					seconds = int(time_float)
					nanoseconds = int((time_float - seconds) * 1e9)

					gps_msgs.Header.seq = seq
					gps_msgs.Header.stamp.secs = seconds
					gps_msgs.Header.stamp.nsecs = nanoseconds
					
					lat_str = parts[2]
					lon_str = parts[4]
					
					lat_deg = float(lat_str[:2])
					lat_min = float(lat_str[2:])
					latitude = lat_deg + (lat_min/60)
					
					lon_deg = float(lon_str[:3])
					lon_min = float(lon_str[3:])
					longitude = lon_deg + (lon_min/60)
					
					if(parts[3] == 'S'):
						latitude = -latitude

					if(parts[5] == 'W'):
						longitude = -longitude
					
					altitude = parts[9]
					hdop = parts[8]
					utm_easting, utm_northing, zone_number, zone_letter = transforms_gpgga_to_utm(latitude, longitude)
					
					utc = parts[1]
					gps_msgs.Quality = float(parts[6])
					gps_msgs.Latitude = float(latitude)
					gps_msgs.Longitude = float(longitude)
					gps_msgs.Altitude = float(altitude)
					gps_msgs.HDOP = float(hdop)
					gps_msgs.UTM_easting = float(utm_easting)
					gps_msgs.UTM_northing = float(utm_northing)
					gps_msgs.UTC = float(utc)
					gps_msgs.Zone = float(zone_number)
					gps_msgs.Letter = str(zone_letter)
					print(gps_msgs)
					seq = seq + 1
					values_pub.publish(gps_msgs)
					rate.sleep() 

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
