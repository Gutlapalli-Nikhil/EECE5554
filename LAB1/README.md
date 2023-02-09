# LAB 1 Assignment


## Steps to run

1) Git clone the package

2) cd EECE5554/LAB1

3) catkin_make

4) source devel/setup.bash

## For collecting GPS data into /gps topic

5) roslaunch gps_driver driver.launch port:="/dev/ttyUSB0". Note: Please specify the correct port.

6) To create a ROS bag file, run - rosbag record /gps

## Obtained Results.

### While standing in open env

![Altitude_vs_Time_standing_in_open_env](https://user-images.githubusercontent.com/122410344/216852362-15d51e92-bcd3-4318-ae17-ffaf59e0ca29.png)

![easting_northing_cal_while_stationary](https://user-images.githubusercontent.com/122410344/217718236-ee516ad4-cc41-432e-a6bd-28071ff217aa.png)

![error_estimation_in_open_ground](https://user-images.githubusercontent.com/122410344/216852379-92086604-f398-47fc-84b5-6e7a1817c5a9.png)

### While standing beside buildings

![Altitude_vs_Time_standing_beside_building](https://user-images.githubusercontent.com/122410344/216852416-576b05fa-9120-4333-9e8f-f023276f89e6.png)

![easting_northing_stationary_beside_buildings](https://user-images.githubusercontent.com/122410344/217718279-f8342dcc-3df4-46ac-9597-d5fda071c2bd.png)

![error_estimation_beside_buildings](https://user-images.githubusercontent.com/122410344/216852431-44cd63cf-fe90-46ca-ba4c-eebcbf6a0fea.png)

### While moving

![Altitude_vs_Time_calculated_while_moving](https://user-images.githubusercontent.com/122410344/216852442-278ff59b-555a-4879-b7b0-866ee0066f7f.png)

![easting_vs_northing_while_moving](https://user-images.githubusercontent.com/122410344/217718305-43ab4887-78a8-4bee-a1e9-7d19ecd9b451.png)

![error_estimation_while_moving](https://user-images.githubusercontent.com/122410344/216852464-710f012d-0143-4eae-93ee-9068ac9aea19.png)
