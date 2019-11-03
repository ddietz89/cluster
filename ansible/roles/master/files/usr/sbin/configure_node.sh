#!/bin/bash

# Update /etc/hosts on master
sudo /usr/sbin/run_ansible

ssh -i ~/cluster.pem ec2-user@$1 "sudo yum install git -y"
ssh -i ~/cluster.pem ec2-user@$1 "sudo amazon-linux-extras install ansible2 -y"

sudo scp -i ~ddietz/cluster.pem -r /root/.ssh/ ec2-user@$1:~/
ssh -i ~/cluster.pem ec2-user@$1 "sudo mv ~ec2-user/.ssh/ /root/"
sudo scp -i ~ddietz/cluster.pem -r /root/.vaultpass ec2-user@$1:~/
ssh -i ~/cluster.pem ec2-user@$1 "sudo mv ~ec2-user/.vaultpass /root/"
ssh -i ~/cluster.pem ec2-user@$1 "sudo git clone git@github.com:ddietz89/cluster.git /root/cluster/"
ssh -i ~/cluster.pem ec2-user@$1 "sudo ansible-playbook common.yml node.yml -i \"$1,\" --vault-password-file=/root/.vaultpass" 
