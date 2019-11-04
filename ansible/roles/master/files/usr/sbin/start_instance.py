#!/usr/bin/python

import boto3
import sys
from pprint import pprint
from subprocess import Popen, PIPE
import time

if len(sys.argv) < 2:
    print "Usage: " + sys.argv[0] + " <instance_name>"
    sys.exit(1)

target_instance_string = sys.argv[1]

ec2 = boto3.client('ec2')

instances = ec2.describe_instances()

target_instance = None
for inst in instances['Reservations']:
    if 'Tags' in inst['Instances'][0] and {'Key': 'Name', 'Value': target_instance_string} in inst['Instances'][0]['Tags']:
        if inst['Instances'][0]['State']['Name'] == 'stopped' or inst['Instances'][0]['State']['Name'] == 'running':
            target_instance = inst['Instances'][0]

if target_instance is None:
    print "Couldn't find instance " + target_instance_string 
    sys.exit(1)


if inst['Instances'][0]['State']['Name'] == 'stopped':
    try:
        response = ec2.start_instances(InstanceIds=[target_instance['InstanceId']])
        print response
    except Exception as e:
        print e
        sys.exit(1)

process = Popen("ssh " + target_instance_string + " /usr/sbin/run_ansible", shell=True, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

# Wait for instance to boot
started = False
count = 0
while count < 50 and started == False:
    time.sleep(5)
    process = Popen("ssh " + target_instance_string + " echo hi", shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print "waiting..."
    if stdout.strip() == "hi":
        started = True

if not started:
    print "Error! Startup timed out."
    sys.exit(1)

process = Popen("ssh " + target_instance_string + " /usr/sbin/start_node.sh", shell=True, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

time.sleep(5)

process = Popen("sudo scontrol update NodeName=" + target_instance_string + " State=RESUME", shell=True, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
