#!/bin/bash
# Example ResumeProgram
echo "`date` Resume invoked $0 $*" >>/var/log/power_save.log
hosts=`scontrol show hostnames $1`
for host in $hosts
do
   timeout 10m /usr/sbin/start_instance.py $host &
done
wait
