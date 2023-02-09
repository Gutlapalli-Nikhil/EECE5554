import rospy
from gps_driver.msg import gps_msg as GPS
import utm
import sys
import serial

def transforms_gpgga_to_utm(latitude, longitude):
	
	(utm_easting, utm_northing, zone_number, zone_letter) = utm.from_latlon(latitude, longitude)
	
	return utm_easting, utm_northing, zone_number, zone_letter
		
		
def talker():
	rospy.init_node('driver')
	
	args = rospy.myargv(argv=sys.argv)
	
	serial_port = args[1]
	
	port = serial.Serial(serial_port, 4800)
	
	# rospy.sleep(0.2)
	
	data = port.readline()
	
	output = data.decode('latin-1')

	# while(True):
	# 	data = port.readline()
	
	# 	output = data.decode()
	# 	print(output)
	# 	rospy.sleep(0.2)

	rospy.logdebug("Using GPS sensor on port "+serial_port+" at "+str(4800))
	
	values_pub = rospy.Publisher("gps", GPS, queue_size=5)
	
	gps_msgs = GPS()
	
	rate = rospy.Rate(10)
	
	gps_msgs.Header.frame_id = "GPS1_Frame"


	method = "txty"
	


	try:
		data = port.readline()

		output = data.decode()

		parts = output.split(",")

		if(parts[0] == "$GPGGA"):
			print(parts)
			gps_msgs.Header.stamp.secs = int(parts[1][:6])
			gps_msgs.Header.stamp.nsecs = int(parts[1][7:])
			
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
			values_pub.publish(gps_msgs)  
			rate.sleep()  
			
	except rospy.ROSInterruptException:
		port.close()
	
		
		
if __name__ == '__main__':

	try:
		while(1):
			talker()
	except rospy.ROSInterruptException:
		pass
