# LAB 2 Assignment


## Steps to run

1) Git clone the package

2) cd EECE5554/LAB2

3) catkin_make

4) source devel/setup.bash

## For collecting GPS data into /gps topic

5) roslaunch gnss_driver driver.launch port:="/dev/ttyACM0". Note: Please specify the correct port.

6) To create a ROS bag file, run - rosbag record /gps

## Obtained Results.

### Altitude vs Time Graph

![alt_vs_time_buliding_area_standing](https://user-images.githubusercontent.com/122410344/220502598-f66030ed-7715-4a23-8464-46a225198a3a.png)

![alt_vs_time_occluded_area_walking](https://user-images.githubusercontent.com/122410344/220502620-580a96c0-2bf7-4699-9420-918225f826bc.png)

![alt_vs_time_open_area_standing](https://user-images.githubusercontent.com/122410344/220502640-dca7a62f-a475-45dd-bd30-606894961334.png)

![alt_vs_time_open_area_walking](https://user-images.githubusercontent.com/122410344/220502671-d59f3c53-0545-4a3f-be88-6bdfbd35d0ee.png)

### Easting vs Northing data

![east_vs_north_occluded_area_standing](https://user-images.githubusercontent.com/122410344/220502758-ca76bb9f-56a6-4594-8840-694be62805d0.png)

![east_vs_north_occluded_area_walking](https://user-images.githubusercontent.com/122410344/220502774-d68ed82f-d043-4742-abe2-40902a70894a.png)

![east_vs_north_open_area_standing](https://user-images.githubusercontent.com/122410344/220502783-4599bbd7-9bd1-4bbc-9b8c-6443d90b41b3.png)

![east_vs_north_open_area_walking](https://user-images.githubusercontent.com/122410344/220502803-f4d15f28-e375-420f-8446-ca13801682bb.png)

### Error Estimation

![error_est_occluded_area_standing](https://user-images.githubusercontent.com/122410344/220502853-1d4a9439-f2ad-4858-81e9-2b6dfe6c6b5d.png)

![error_est_open_area_standing](https://user-images.githubusercontent.com/122410344/220502890-32f4749c-7382-4b87-96ce-f4ae18e152a4.png)
