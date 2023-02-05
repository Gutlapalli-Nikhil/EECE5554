# import bagpy
# from bagpy import bagreader
# import pandas as pd
# import matplotlib.pyplot as plt

# b = bagreader('/home/nikhil/LAB1/src/Data/moving.bag')
# GPS_MSG = b.message_by_topic('/gps')
# gpsdf = pd.read_csv("../Data/moving/gps.csv")

# fig, ax = plt.subplots()

# ax.scatter(gpsdf['UTM_easting'] - gpsdf['UTM_easting'][0], gpsdf['UTM_northing'] - gpsdf['UTM_northing'][0], c='tab:blue', label='Obtained values from GPS')

# utm_original_start_easting = 328132.07
# utm_original_start_northing = 4689558.80

# utm_original_end_easting = 328085.23
# utm_original_end_northing = 4689668.95

# step_easting = (utm_original_end_easting - utm_original_start_easting) / gpsdf.shape[0]
# step_northing = (utm_original_end_northing - utm_original_start_northing) / gpsdf.shape[0]

# list_easting = []
# list_northing = []

# for i in range(gpsdf.shape[0]):
# 	a = (step_easting*i) + utm_original_start_easting
# 	b = (step_northing*i) - utm_original_start_northing
# 	list_easting.append(a)
# 	list_northing.append(b)

# list_easting = pd.Series(list_easting)
# list_northing = pd.Series(list_northing)

# plt.scatter(list_easting - list_easting[0], list_northing - list_northing[0], c='tab:red', label='Assumed correct values')

# plt.title("UTM_easting vs UTM_northing (calculated while walking)", fontsize=25)
# plt.xlabel("UTM_easting. Values in degrees",fontsize=15)
# plt.ylabel("UTM_northing. Values in degrees", fontsize=15)
# ax.legend()
# plt.show()



import bagpy
from bagpy import bagreader
import pandas as pd
import matplotlib.pyplot as plt

b = bagreader('/home/nikhil/LAB1/src/Data/stationary_beside_buildings.bag')
GPS_MSG = b.message_by_topic('/gps')
gpsdf = pd.read_csv("../Data/stationary_beside_buildings/gps.csv")

fig, ax = plt.subplots()

ax.scatter(gpsdf['UTM_easting'] - gpsdf['UTM_easting'][0], gpsdf['UTM_northing'] - gpsdf['UTM_northing'][0], c='tab:blue', label='Obtained values from GPS')

# utm_original_start_easting = 328132.07
# utm_original_start_northing = 4689558.80

# utm_original_end_easting = 328085.23
# utm_original_end_northing = 4689668.95

# step_easting = (utm_original_end_easting - utm_original_start_easting) / gpsdf.shape[0]
# step_northing = (utm_original_end_northing - utm_original_start_northing) / gpsdf.shape[0]

# list_easting = []
# list_northing = []

# for i in range(gpsdf.shape[0]):
# 	a = (step_easting*i) + utm_original_start_easting
# 	b = (step_northing*i) - utm_original_start_northing
# 	list_easting.append(a)
# 	list_northing.append(b)

# list_easting = pd.Series(list_easting)
# list_northing = pd.Series(list_northing)

plt.scatter(0, 0, c='tab:red', label='Assumed correct values')

plt.title("UTM_easting vs UTM_northing (calculated while standing beside buildings)", fontsize=25)
plt.xlabel("UTM_easting. Values in degrees",fontsize=15)
plt.ylabel("UTM_northing. Values in degrees", fontsize=15)
ax.legend()
plt.show()