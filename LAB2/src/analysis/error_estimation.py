from math import radians, cos, sin, asin, sqrt, pi
import bagpy
from bagpy import bagreader
import pandas as pd
import matplotlib.pyplot as plt
import math

def distanceInKmBetweenEarthCoordinates(a1 , b1, a2, b2):
  return math.sqrt((a1-a2)**2 + (b1-b2)**2)

b = bagreader('/home/nikhil/LAB1/src/Data/moving.bag')
GPS_MSG = b.message_by_topic('/gps')
gpsdf = pd.read_csv("/home/nikhil/LAB2/src/data/open_stationary/gps.csv")

northing_original = 4686126.5
easting_original = 326315.78125

# easting_original = 326434.0625

# northing_original = 4686142


distance_error = []

for i in range(gpsdf.shape[0]):

  answer = distanceInKmBetweenEarthCoordinates(gpsdf.UTM_easting[i], gpsdf.UTM_northing[i], easting_original, northing_original)

  distance_error.append(answer)

import statistics

mean = statistics.mean(distance_error)

stdev = statistics.stdev(distance_error)

print("Mean:", mean)
print("Standard deviation:", stdev)

plt.hist(distance_error)
plt.title("Error Estimation (Occluded Area Standing)", fontsize=25)
plt.ylabel("Frequency", fontsize=15)
plt.xlabel("Error in Meters", fontsize=15)
plt.show()