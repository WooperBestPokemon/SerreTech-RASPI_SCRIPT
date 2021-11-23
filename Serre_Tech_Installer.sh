#!/bin/bash

#Step 1 : Installing Dependencies...

echo "Checking for updates..."
sudo apt-get update
sudo apt-get upgrade

echo "Installing PIP..."

sudo apt-get install python3-pip -y

echo "Installing MQTT broker..."
sudo apt install mosquitto mosquitto-clients -y

echo "Installing python dependencies..."

pip install paho-mqtt
pip install PyYAML

#Step 2 : Installing the scripts

echo "Installing scripts..."

mv /home/pi/SerreTech-RASPI_SCRIPT /home/pi/scripts

#Step 3 : Creating services / crontab

echo "Creating cronjob for the pump..."

(crontab -u $(whoami) -l; echo "*/30 * * * * python /home/pi/scripts/PUMP.py" ) | crontab -u $(whoami) -

echo "Creating service for the MQTT Broker..."

sudo mv /home/pi/scripts/mqttsub.service /etc/systemd/system
sudo systemctl enable /mqttsub.service

#Step 4 : Cleaning

echo "Cleaning..."

rm /home/pi/scripts/README.md
rm /home/pi/scripts/Serre_Tech_Installer.sh
rm -rf /home/pi/scripts/arduino

#Rebooting the pi

sudo reboot