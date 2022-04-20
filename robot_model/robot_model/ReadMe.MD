roslaunch display.launch
roslaunch map.launch
roslaunch bringup_robot.launch
roslaunch keyboard_teleop.launch

Chỉnh lại Rviz: 
Phần Global Frame chỉnh về Odom

Test: 
+ Sử dụng bàn phím di chuyển xe xem xe có di chuyển so với odom k
+ Ktra xem có lên Map và lên các điểm Lasersan k 
+ Kiểm tra xem có lên Model xe k 

Chạy câu lệnh: 
rosrun rqt_gui rqt_gui
để kiểm tra xem các topic đã liên kết với nhau chưa
