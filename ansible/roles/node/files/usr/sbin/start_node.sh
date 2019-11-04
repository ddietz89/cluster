#!/usr/bin/bash

sudo /usr/sbin/run_ansible

sudo service munge start
sudo service slurmd restart
sleep 10
sudo service slurmd restart
