#!/usr/bin/env python
import psutil
import rospy

from psutil_ros.msg import *
from std_msgs.msg import Time



def publisher():
    
    cpu_load_pub = rospy.Publisher('cpu_load', Cpuload)
    meminfo_pub = rospy.Publisher('meminfo', Meminfo)
    network_pub = rospy.Publisher('network', Network)
   
    rospy.init_node('psutil_ros')
    publish_rate = rospy.get_param("~publish_rate",1);   
    r = rospy.Rate(publish_rate)
    
    while not rospy.is_shutdown():
        #str = "hello world %s" % rospy.get_time()
        time = rospy.Time.now()
        
        cpuloadmsg = Cpuload()
        cpuloadmsg.stamp = time
	total = psutil.cpu_percent(interval=0)
        loads = psutil.cpu_percent(interval=0,percpu=True)
        cpuloadmsg.cpu_load=[total]+loads
        
        meminfomsg = Meminfo()
        meminfomsg.stamp = time
        meminfo=psutil.virtual_memory()
        meminfomsg.memtotal = meminfo.total
        meminfomsg.memavailable = meminfo.available
        meminfomsg.mempercent = meminfo.percent
        meminfomsg.memused = meminfo.used
        meminfomsg.memfree = meminfo.free
        meminfomsg.memactive = meminfo.active
        meminfomsg.meminactive = meminfo.inactive
        meminfomsg.membuffers = meminfo.buffers
        
        networkmsg = Network()
        networkmsg.stamp=time
        
        interfaces = psutil.net_io_counters(pernic=True)
        
        for interface in interfaces:
            interfacemsg=Interface()
            interfacemsg.name=interface
            interfacemsg.bytes_sent=interfaces[interface].bytes_sent
            interfacemsg.bytes_recv=interfaces[interface].bytes_recv
            interfacemsg.packets_sent=interfaces[interface].packets_sent
            interfacemsg.packets_recv=interfaces[interface].packets_recv
            interfacemsg.errin=interfaces[interface].errin
            interfacemsg.errout=interfaces[interface].errout
            interfacemsg.dropin=interfaces[interface].dropin
            interfacemsg.dropout=interfaces[interface].dropout
            networkmsg.interfaces.append(interfacemsg)
        
        
        #rospy.loginfo(sys_info)
        cpu_load_pub.publish(cpuloadmsg)
        meminfo_pub.publish(meminfomsg)
        network_pub.publish(networkmsg)
        r.sleep()


if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
