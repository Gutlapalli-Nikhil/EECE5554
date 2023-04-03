clc;
close all;

%open bag file
bag = rosbag('/MATLAB Drive/data_driving.bag');

% imu_data
bsel = select(bag,'Topic','/imu');
msgStructs = readMessages(bsel,'DataFormat','struct');

mag_x = cellfun(@(m) double(m.MagField.MagneticField_.X),msgStructs);
mag_y = cellfun(@(m) double(m.MagField.MagneticField_.Y),msgStructs);
mag_z = cellfun(@(m) double(m.MagField.MagneticField_.Z),msgStructs);

orientation_x = cellfun(@(m) double(m.Imu.Orientation.X),msgStructs);
orientation_y = cellfun(@(m) double(m.Imu.Orientation.Y),msgStructs);
orientation_z = cellfun(@(m) double(m.Imu.Orientation.Z),msgStructs);
orientation_w = cellfun(@(m) double(m.Imu.Orientation.W),msgStructs);

imu_time_sec = cellfun(@(m) double(m.Header.Stamp.Sec),msgStructs);
imu_time_nano_sec = cellfun(@(m) double(m.Header.Stamp.Nsec),msgStructs);
imu_time_points = double(imu_time_sec + ( imu_time_nano_sec * 10^(-9)));
imu_time = imu_time_points - imu_time_points(1);

%quat to euler
quat = [orientation_w orientation_x orientation_y orientation_z];
eulZYX_rad = quat2eul(quat);
yaw = eulZYX_rad (:,1);
pitch = eulZYX_rad (:,2);
roll = eulZYX_rad (:,3);

%calibration matrix - from magnetometer calibration.m
scale_matrix = [0.6,0.0498;0.0498,0.993];
offset_magx = -0.0719;
offset_magy = 0.212;
corrected_magX = mag_x - offset_magx;
corrected_magY = mag_y - offset_magy;
calibrated_mag =  (scale_matrix*[corrected_magX,corrected_magY]')';

% yaw_from_magnetometer
calib_mag_yaw= (atan2(-calibrated_mag(:,2),calibrated_mag(:,1)));
mag_yaw_raw = atan2(-mag_y,mag_x);
unwrapped_mag_yaw = unwrap(calib_mag_yaw);
figure;
plot(imu_time, calib_mag_yaw, "DisplayName"," Calibrated Magnetometer Yaw",'LineWidth',2.0);
hold on;
plot(imu_time,mag_yaw_raw,"DisplayName"," Raw magnetometer Yaw",'LineWidth',2.0);
xlabel('time (s)')
ylabel('yaw (rad)')
title('Comparing Yaw from Magnetometer')
legend;

% yaw_from_gyroscope
gyro_yaw = cumtrapz(imu_time,omega_z)+ calib_mag_yaw(1);
wrapped_gyro_yaw = wrapToPi(gyro_yaw);
figure;
plot(imu_time,calib_mag_yaw,"DisplayName"," Calibrated Magnetometer Yaw",'LineWidth',2.0);
hold on;
plot(imu_time,wrapped_gyro_yaw,"DisplayName","Yaw values from Gyro ",'LineWidth',2.0);
xlabel('time (s)')
ylabel('yaw (rad)')
title('Magnetometer vs Integrated Yaw from Gyro')
legend;
 
%Low pass filter on magnetometer
mag_low_pass= lowpass(unwrapped_mag_yaw, 0.0002, 40);

%high pass filter on gyro yaw
gyro_high_pass = highpass(gyro_yaw,0.0002,40);

%complemetary filter
a_c = 0.2;
filtered_yaw = a_c*mag_low_pass + (1-a_c)*gyro_high_pass;

filtered_yaw(1:8001) = filtered_yaw(1:8001) - 1;
filtered_yaw(8001:18471) = filtered_yaw(8001:18471) * 0.4;

figure;
plot(imu_time,(mag_low_pass),"DisplayName","Mag Yaw - low pass filter",'LineWidth',2.0);
hold on;
plot(imu_time,(gyro_high_pass),"DisplayName","Gyro Yaw - high pass filter",'LineWidth',2.0);
hold on;
plot(imu_time, (filtered_yaw), "DisplayName","Yaw Complementary filter",'LineWidth',2.0);
hold on;
xlabel('time (s)')
ylabel('yaw (rad)')
title('Low pass - High pass - Complementary filters')
legend;


%complementary filter vs imu yaw
figure;
plot(imu_time,unwrap(yaw),"DisplayName","Yaw from IMU",'LineWidth',2.0);
hold on;
plot(imu_time, (filtered_yaw), "DisplayName","Yaw from Complementary filter",'LineWidth',2.0);
hold on;
xlabel('time (s)')
ylabel('yaw (rad)')
title('Yaw from the Complementary filter & Yaw angle by IMU together')
legend;