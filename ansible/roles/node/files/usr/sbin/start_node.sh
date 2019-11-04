#!/usr/bin/bash

sudo service munge start
sudo service slurmd restart
sleep 10
sudo service slurmd restart
