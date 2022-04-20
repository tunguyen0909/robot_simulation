# CMake generated Testfile for 
# Source directory: /home/ai/ROBI_PROJECT/catkin_ws/src/robot_model
# Build directory: /home/ai/ROBI_PROJECT/catkin_ws/src/robot_model/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_robot_model_roslaunch-check_launch "/home/ai/ROBI_PROJECT/catkin_ws/src/robot_model/build/catkin_generated/env_cached.sh" "/usr/bin/python2" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/home/ai/ROBI_PROJECT/catkin_ws/src/robot_model/build/test_results/robot_model/roslaunch-check_launch.xml" "--return-code" "/usr/bin/cmake -E make_directory /home/ai/ROBI_PROJECT/catkin_ws/src/robot_model/build/test_results/robot_model" "/opt/ros/melodic/share/roslaunch/cmake/../scripts/roslaunch-check -o \"/home/ai/ROBI_PROJECT/catkin_ws/src/robot_model/build/test_results/robot_model/roslaunch-check_launch.xml\" \"/home/ai/ROBI_PROJECT/catkin_ws/src/robot_model/launch\" ")
subdirs("gtest")
