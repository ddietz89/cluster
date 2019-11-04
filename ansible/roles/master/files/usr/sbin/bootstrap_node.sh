#!/bin/bash

hostname $1
echo $1 > /etc/hostname

yum install git -y
amazon-linux-extras install ansible2 -y

mv ~ec2-user/id_rsa* /root/.ssh/
mv ~ec2-user/.vaultpass /root/

cd /root/
export GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
git clone git@github.com:ddietz89/cluster.git 

cd cluster/ansible/

cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook common.yml node.yml -i "$1," --vault-password-file=/root/.vaultpass

