#!/bin/bash
# Example SuspendProgram
echo "`date` Suspend invoked $0 $*" >>/var/log/power_save.log
hosts=`scontrol show hostnames $1`
for host in $hosts
do
   /usr/sbin/stop_instance.py $host
done
