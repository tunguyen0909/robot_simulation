cmake_minimum_required(VERSION 3.0.2)
project(robot_model)

find_package(catkin REQUIRED COMPONENTS
  gazebo_msgs
  gazebo_plugins
  gazebo_ros
  gazebo_ros_control
  geometry_msgs
  move_base_msgs
  nav_msgs
  roscpp
  std_msgs
  tf
  actionlib
  actionlib_msgs
  message_generation
)

find_package(Boost REQUIRED COMPONENTS system)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES robot_model 
  CATKIN_DEPENDS roscpp rospy std_msgs actionlib actionlib_msgs message_runtime 
)

if(CATKIN_ENABLE_TESTING)
  find_package(roslaunch REQUIRED)
  roslaunch_add_file_check(launch)
endif()

install(DIRECTORY images meshes launch rviz urdf msg
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})


include_directories(
  include
  ${Boost_INCLUDE_DIR} 
  ${catkin_INCLUDE_DIRS}
)

add_library(ceSerial src/ceSerial.cpp include/ceSerial.h)

add_executable(send_imu src/send_imu_data.cpp)

add_executable(diff_tf src/diff_tf.cpp)
add_executable(diff_tf_old src/diff_tf_old.cpp)

add_executable(imu_trans src/imu_trans.cpp)

add_executable(send_goal src/send_goal.cpp)

add_executable(sub_button_msg src/sub_button_status.cpp)

target_link_libraries(diff_tf 
  ${catkin_LIBRARIES}
)

target_link_libraries(diff_tf_old
  ${catkin_LIBRARIES}
)

target_link_libraries(imu_trans 
  ${catkin_LIBRARIES}
)

target_link_libraries(send_goal
  ${catkin_LIBRARIES}
)

target_link_libraries(sub_button_msg
  ${catkin_LIBRARIES}
)
target_link_libraries(send_imu
  ${catkin_LIBRARIES} ceSerial
)
#add_dependencies(ceSerial)

