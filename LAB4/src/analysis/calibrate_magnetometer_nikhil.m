clc;
close all;

%open bag file
bag = rosbag('/MATLAB Drive/data_going_in_circles.bag');

topic = select(bag,'Topic','/imu');
msgStructs = readMessages(topic,'DataFormat','struct');
Mag_x = cellfun(@(m) double(m.MagField.MagneticField_.X),msgStructs);
Mag_y = cellfun(@(m) double(m.MagField.MagneticField_.Y),msgStructs);

[a,b,orientation_radians,offset_x,offset_y] = fit_ellipse(Mag_x,Mag_y);

mag_hard_corrected_x = Mag_x - offset_x;
mag_hard_corrected_y = Mag_y - offset_y;

theta = orientation_radians;
R = [cos(theta) sin(theta);-sin(theta) cos(theta)];
rotated_mag = (R*[mag_hard_corrected_x,mag_hard_corrected_y]')';

scale_factor = b/a;
scale_matrix= [scale_factor 0;0 1];
scaled_mag = (scale_matrix*rotated_mag')';

theta = -theta;
R_back = [cos(theta) sin(theta);-sin(theta) cos(theta)];
corrected_mag= (R_back*scaled_mag')';

figure;
scatter(corrected_mag(:,1),corrected_mag(:,2), "DisplayName","After calibration");
hold on;
scatter(Mag_x, Mag_y, "DisplayName", "Before calibration");
hold on;
xlabel("Magnetic Field X in Gauss");
ylabel("Magnetic Field Y in Gauss");
axis equal;

title('Magnetometer X-Y plot before and after hard - soft iron calibration');
legend;


RotationBackAngle = R_back*scale_matrix*R;


imu_timePoints_sec = cellfun(@(m) double(m.Header.Stamp.Sec),msgStructs);
imu_timePoints_nanosec = cellfun(@(m) double(m.Header.Stamp.Nsec),msgStructs);
imu_timePoints = double(imu_timePoints_sec + ( imu_timePoints_nanosec * 10^(-9)));
imu_time = imu_timePoints - imu_timePoints(1);
 
figure;
plot(imu_time, Mag_x,"DisplayName","Magnotometer X before calibration");
hold on;
plot(imu_time, Mag_y, "DisplayName", "Magnotometer Y before calibration");
hold on;
xlabel("Time (s)");
ylabel("Magnetic Field in Gauss");
title('Time series plot of magnetic field X and Y before correction');
legend;

figure;
plot(imu_time, corrected_mag(:,1), "DisplayName","Magnotometer X after calibration");
hold on;
plot(imu_time, corrected_mag(:,2), "DisplayName", "Magnotometer Y after calibration");
hold on;
xlabel("Time (s)");
ylabel("Magnetic Field in Gauss");
title('Time series plot of magnetic field X and Y after correction');
legend;

%--------------------------------------------------------------------------------------------

function [a,b,orientation_radians,X0,Y0] = fit_ellipse(x,y,axis_handle)
% initialize
orientation_tolerance = 1e-2;

% prepare vectors, must be column vectors
x = x(:);
y = y(:);

% remove bias of the ellipse
mean_x = mean(x);
mean_y = mean(y);
x = x-mean_x;
y = y-mean_y;

% Equation of the ellipse A.x^2 + B.x.y + C.y^2 + D.x + E.y = 0
X = [x.^2, x.*y, y.^2, x, y ];
a = sum(X)/(X'*X);

% extract parameters from the conic equation
[a,b,c,d,e] = deal( a(1),a(2),a(3),a(4),a(5) );

% remove the orientation from the ellipse
if ( min(abs(b/a),abs(b/c)) > orientation_tolerance )
    
    orientation_radians = 1/2 * atan( b/(c-a) );
    cos_phi = cos( orientation_radians);
    sin_phi = sin( orientation_radians);
    [a,b,c,d,e] = deal(a*cos_phi^2 - b*cos_phi*sin_phi + c*sin_phi^2, 0, a*sin_phi^2 + b*cos_phi*sin_phi + c*cos_phi^2, d*cos_phi - e*sin_phi,d*sin_phi + e*cos_phi);
    [mean_x,mean_y] = deal(cos_phi*mean_x - sin_phi*mean_y, sin_phi*mean_x + cos_phi*mean_y );
else
    orientation_radians = 0;
    cos_phi = cos( orientation_radians );
    sin_phi = sin( orientation_radians );
end

if (a*c>0)
    
    % make sure coefficients are positive as required
    if (a<0), [a,c,d,e] = deal( -a,-c,-d,-e ); end
    
    X0          = mean_x - d/2/a;
    Y0          = mean_y - e/2/c;
    F           = 1 + (d^2)/(4*a) + (e^2)/(4*c);
    [a,b]       = deal( sqrt( F/a ),sqrt( F/c ) );    
    
end
end