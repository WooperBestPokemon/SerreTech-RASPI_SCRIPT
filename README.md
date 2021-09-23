# Serre Tech

This is the code repo for the final project's raspberry pi.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* mqtt broker
  ```sh
  sudo apt install mosquitto mosquitto-clients
  ```
* paho-mqtt
  ```sh
  pip install paho-mqtt
  ```
* requests
  ```sh
  pip install requests
  ```


### Installation

1. Download the file as a zip and extract it in /home/pi/scripts
2. Move the mqttsub.service to the systemd folder
   ```sh
   sudo mv /home/pi/scripts/mqttsub.service /etc/systemd/system
   ```
3. Enable the new service and start it
   ```sh
   sudo systemctl enable /mqttsub.service
   sudo systemctl start /mqttsub.service
   ```
   
![college logo](https://www.cegepjonquiere.ca/media/tinymce/Plus/Logos%20et%20norme%20graphique/Ceg-logo-couleur.gif)
