import bagpy
from bagpy import bagreader
import pandas as pd
import matplotlib.pyplot as plt

b = bagreader('/home/nikhil/LAB1/src/Data/moving.bag')
GPS_MSG = b.message_by_topic('/gps')
gpsdf = pd.read_csv("../Data/moving/gps.csv")


fig, ax = plt.subplots()

fixed_altitude = []

start = 13.1
end = 9.8


for i in range(42):
	a = start + (0.07857142857*i)
	fixed_altitude.append(a)

ax.scatter(gpsdf["header.seq"], gpsdf['Altitude'], c='tab:blue', label='Values from GPS')
ax.scatter(gpsdf["header.seq"], fixed_altitude, c='tab:orange', label='Exact Altitude')

plt.title("Altitude vs Time (Calculated while moving)", fontsize=25)
plt.ylabel("Altitude in meters",fontsize=15)
plt.xlabel("Time", fontsize=15)

ax.legend()
plt.show()