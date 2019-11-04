#!/bin/bash

# Update /etc/hosts on master
sudo /usr/sbin/run_ansible

ssh-keygen -R $i
sudo ssh-keygen -R $i

sudo scp -i ~ddietz/cluster.pem -r /root/.ssh/id_rsa* ec2-user@$1:~/
sudo scp -i ~ddietz/cluster.pem /root/.vaultpass ec2-user@$1:~/
scp -i /usr/sbin/bootstrap_node.sh  /root/.vaultpass ec2-user@$1:~/

ssh -i ~ddietz/cluster.pem ec2-user@$1: "sudo ~ec2-user/bootstrap_node.sh"
