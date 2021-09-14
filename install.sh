#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
sudo cp ./cloudtodo.service /etc/systemd/system/cloudtodo.service
sudo systemctl daemon-reload
sudo systemctl enable cloudtodo.service
sudo mkdir /cloudtodo
sudo chmod 777 /cloudtodo
cp -r ./cloudtodo /cloudtodo
sudo chmod +x /cloudtodo/cloudtodo.sh
pip3 install --upgrade pip
pip3 install discord
sudo systemctl start cloudtodo.service