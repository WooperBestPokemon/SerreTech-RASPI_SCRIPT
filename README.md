# Serre Tech

This is the code repo for the final project's raspberry pi and Arduido.

# Raspberry Pi 0

#Automatic Installation
_____________________

### Prerequisites

* git
  ```sh
  sudo apt install git
  ```

### Installation

1. Clone this repository in your home folder

  ```sh
  cd /home/pi
  git clone https://github.com/WooperBestPokemon/SerreTech-RASPI_SCRIPT
  ```
2. Execute the installer with super user privilege
  ```sh
  sudo chmod +x ./Serre_Tech_Installer.sh
  sudo ./Serre_Tech_Installer.sh
  ```
#Manual Installation
_____________________

### Prerequisites

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
* yaml
  ```sh
  pip install PyYAML
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
4. Create a cronjob for the pump script
   ```sh
   crontab -e
   ```
   Add this line at the end of the file (it will execute the script every 30s)
   ```sh
   */30 * * * * python /home/pi/scripts/PUMP.py
   ```
   
#Configuration
_____________________

1. First, you need to get the token of your account via a POST request (http://testenv.pcst.xyz/api/login) and place it in the config.yaml on 'token : your_token'
2. Next, you need to place your zone id into 'zone_id : your_zone'
3. And lastly, you need to place your captors id into the correct captor_sensor

### Debug
_____________________

Everything will be logged under scripts/logs.

The prototype is using a leds system to alert if there is a problem with the scripts.

Green Light : The light will turn Green as soon as the MQTT_SUB.py starts.
Red Light : If the light turns red and turns green right after, that mean there is a problem with the POST REQUEST (check the logs). If it stays red, that mean the script had an error and is not working anymore.
Blue Light : Will blink when the MQTT broker is sending a POST request. If it doesn't blink every 30s, that mean the captors aren't sending any data to the MQTT Broker.

![college logo](https://www.cegepjonquiere.ca/media/tinymce/Plus/Logos%20et%20norme%20graphique/Ceg-logo-couleur.gif)
