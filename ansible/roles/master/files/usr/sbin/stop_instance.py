#!/usr/bin/python

import boto3
import sys
from pprint import pprint

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


try:
    response = ec2.stop_instances(InstanceIds=[target_instance['InstanceId']])
    print response
except ClientError as e:
    print e
    sys.exit(1)
