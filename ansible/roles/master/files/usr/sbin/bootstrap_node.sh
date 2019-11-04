#!/bin/bash

hostname $i
echo $i > /etc/hostname

yum install git -y
yum amazon-linux-extra install ansible2 -y

mv ~ec2-user/id_rsa* /root/.ssh/
mv ~ec2-user/.vaultpass /root/

cd /root/
git clone git@github.com:ddietz89/cluster.git 
ansible-playbook common.yml node.yml -i \"$1,\" --vault-password-file=/root/.vaultpass

userdel ec2-user
