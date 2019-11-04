#!/bin/bash

# Update /etc/hosts on master
sudo /usr/sbin/run_ansible

ssh-keygen -R $1
sudo ssh-keygen -R $1

sudo scp -o StrictHostKeyChecking=no -i ~ddietz/cluster.pem -r /root/.ssh/id_rsa ec2-user@$1:~/
sudo scp -o StrictHostKeyChecking=no -i ~ddietz/cluster.pem -r /root/.ssh/id_rsa.pub ec2-user@$1:~/
sudo scp -o StrictHostKeyChecking=no -i ~ddietz/cluster.pem /root/.vaultpass ec2-user@$1:~/
scp -o StrictHostKeyChecking=no -i ~ddietz/cluster.pem /usr/sbin/bootstrap_node.sh ec2-user@$1:~/

ssh -o StrictHostKeyChecking=no -i ~ddietz/cluster.pem ec2-user@$1 "sudo ~ec2-user/bootstrap_node.sh $1"
