#!/bin/bash
# Example SuspendProgram
echo "`date` Suspend invoked $0 $*" >>/var/log/power_save.log
hosts=`scontrol show hostnames $1`
for host in $hosts
do
   timeout 10m /usr/sbin/stop_instance.py $host 2>&1 >> /var/log/power_save.log &
done
wait
