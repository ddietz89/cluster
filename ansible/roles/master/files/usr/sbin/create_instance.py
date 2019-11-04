#!/usr/bin/python

import boto3
import sys
from pprint import pprint
from subprocess import Popen,PIPE
import time

if len(sys.argv) < 2:
    print "Usage: " + sys.argv[0] + " <instance_name>"
    sys.exit(1)

target_instance_string = sys.argv[1]

ec2 = boto3.client('ec2')
ec2r = boto3.resource('ec2')

try:
    instances = ec2.run_instances(
         ImageId='ami-00bf61217e296b409',
         MinCount=1,
         MaxCount=1,
         InstanceType='t2.nano',
         KeyName='cluster',
         SecurityGroupIds=[
        'sg-018fbf329acd16069',
    ],
     )
except ClientError as e:
    print e
    sys.exit(1)

private_ip = instances['Instances'][0]['PrivateIpAddress']
instance = ec2r.Instance(instances['Instances'][0]['InstanceId'])


instance.wait_until_running()
ec2.create_tags(Resources=[instance.id], Tags=[{'Key': 'Name', 'Value': target_instance_string}])


# Replace IP address in hosts
process = Popen("sed -ie '/" + target_instance_string + "/c\\" + private_ip + " " + target_instance_string + "' ~/cluster/ansible/roles/common/files/etc/hosts", shell=True, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

process = Popen("git -C ~/cluster/ commit ~/cluster/ansible/roles/common/files/etc/hosts -m 'Creating new host' && git -C ~/cluster/ push", shell=True, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

process = Popen("/usr/sbin/configure_node.sh " + target_instance_string, shell=True, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
print stdout
print stderr

process = Popen("/usr/sbin/stop_instance.py " + target_instance_string, shell=True, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

time.sleep(30)

process = Popen("/usr/sbin/start_instance.py " + target_instance_string, shell=True, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
