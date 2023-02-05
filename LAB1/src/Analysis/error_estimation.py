from math import radians, cos, sin, asin, sqrt, pi
import bagpy
from bagpy import bagreader
import pandas as pd
import matplotlib.pyplot as plt
import math



b = bagreader('/home/nikhil/LAB1/src/Data/moving.bag')
GPS_MSG = b.message_by_topic('/gps')
gpsdf = pd.read_csv("../Data/moving/gps.csv")


def degreesToRadians(degrees):
  return degrees * pi / 180


def distanceInKmBetweenEarthCoordinates(lat1, lon1, lat2, lon2):
  earthRadiusKm = 6371
  earthRadiusMts = 6.3781 * (10**6) 
  dLat = degreesToRadians(lat2-lat1)
  dLon = degreesToRadians(lon2-lon1)
  lat1 = degreesToRadians(lat1)
  lat2 = degreesToRadians(lat2)
  a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  return earthRadiusMts * c

lat_1, long_1 = 42.339330, -71.086354
lat_2, long_2 = 42.340250, -71.086901

lat_diff = (lat_2 - lat_1) / 42
long_diff = (long_1 - long_2) / 42


distance_error = []
for i in range(gpsdf.shape[0]):
	lat = lat_1 + (i*lat_diff)
	longg = long_1 - (i*long_diff)
	answer = distanceInKmBetweenEarthCoordinates(gpsdf.Latitude[i], gpsdf.Longitude[i], lat, longg)
	distance_error.append(answer)

avg = sum(distance_error) / len(distance_error)
print("Avg ", avg)

print(distance_error)
distance_error.sort()
mid = len(distance_error) // 2
res = (distance_error[mid] + distance_error[~mid]) / 2
print("Medium: ", res)

plt.hist(distance_error)
plt.title("Error Estimation (While moving)", fontsize=25)
plt.ylabel("Number of Seconds", fontsize=15)
plt.xlabel("Error in Meters", fontsize=15)
plt.show()