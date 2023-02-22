import bagpy
from bagpy import bagreader
import pandas as pd
import matplotlib.pyplot as plt

b = bagreader('/home/nikhil/LAB2/src/data/occluded_walking.bag')
GPS_MSG = b.message_by_topic('/gps')
gpsdf = pd.read_csv("/home/nikhil/LAB2/src/data/occluded_walking/gps.csv")


fig, ax = plt.subplots()

fixed_altitude = []


for i in range(542):
	fixed_altitude.append(21.5)

ax.scatter(gpsdf["Header.seq"], gpsdf['Altitude'], c='tab:blue', label='Values from GPS')
ax.scatter(gpsdf["Header.seq"], fixed_altitude, c='tab:orange', label='Exact Altitude')

plt.title("Altitude vs Time (Occluded Area Walking)", fontsize=25)
plt.ylabel("Altitude in meters",fontsize=15)
plt.xlabel("Time", fontsize=15)

ax.legend()
plt.show()