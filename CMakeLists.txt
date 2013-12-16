cmake_minimum_required(VERSION 2.8.3)
project(psutil_ros)

find_package(catkin REQUIRED COMPONENTS
  rospy
  roslib 
  std_msgs
  message_generation
)

catkin_python_setup()

add_message_files(
   DIRECTORY msg
   FILES
   Sysinfo.msg
)

generate_messages(DEPENDENCIES std_msgs)

catkin_package(DEPENDS rospy std_msgs roslib message_runtime)


install(PROGRAMS scripts/psutil_ros_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)