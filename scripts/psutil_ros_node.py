#!/usr/bin/env python
import psutil
import rospy

from psutil_ros.msg import Sysinfo
from std_msgs.msg import Time



def pusblisher():
    pub = rospy.Publisher('psutil_ros', Sysinfo)
    rospy.init_node('psutil_ros')
    while not rospy.is_shutdown():
        #str = "hello world %s" % rospy.get_time()
        sys_info = Sysinfo()
        
        sys_info.stamp = rospy.Time.now()
        
        loads = psutil.cpu_percent(interval=0,percpu=True)
        
        meminfo=psutil.virtual_memory()
        
        sys_info.cpu_load=loads
        
        rospy.loginfo(sys_info)
        pub.publish(sys_info)
        rospy.sleep(1.0)


if __name__ == '__main__':
    try:
        pusblisher()
    except rospy.ROSInterruptException:
        pass