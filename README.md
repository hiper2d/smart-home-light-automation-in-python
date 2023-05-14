# Smart light control system in home WiFi network

### Goals
* Design devices (hardware and firmware) that can be controlled over a web application in a home WiFi network
* Each device based on ESP8266 WiFi module
* Raspberry Pi 4 server to control devices and to host a web client
* So far, devices are RGB lights but I plan to add more types in the future. The next type is a sensor

### Project structure
* [Frontend](frontend/README.md) and [Backend](raspberrypi): Website in Angular 15 server by Python/Flask webserver hosted on Raspberry Pi server to control devices
* [Mosquitto](mosquitto/README.md): Mosquitto messaging queue for MQTT communication between
* [ESP8266](esp8266) firmware in MicroPython for devices
* SMD5050 RGB LED Strip Lights as controlled devices
* Electrical circuits and diagrams of devices
* Guidance of how to setup this all

This is how the web interface looks like for now:
![interface](./images/interface.png)

# Build Images

To build docker images, install Docker, Docker Compose and run the following:
```bash
docker-compose build
```

You can update the image name for `backend` and `frontend` services with your DockerHub repository and push the images into your repo:
```bash
docker-compose push
```

# Installation to Raspberry Pi

### Raspberry Pi

Just install clone the repository into some folder on Raspberry Pi and start it using `docker-compose`:
```bash
docker-compose up
```

It's required to install Docker and Docker Compose to Raspberry Pi and enable the MQTT server port:
```bash
# Google how to install Docker and Docker Compose
# Open Mosquitto port:
sudo ufw allow 1883/tcp
sudo ufw allow 1883/udp
```

# Prepare Development Environment

To work with this project as a programmer, you need to have Python 3, Node.js installed. You also need Docker and Docker compose

You can run it from Docker images. Use `--build` to rebuild igamges from the source code before ruggin:
```bash
docker-compose --build up
```
In this case the main UI is available at the port 8080

Or run only the Mosquitto server form a container. `frontend`, `backend` server can be started in a terminal or from IDE:
```bash
# from the project root directory
docker-compose up mosquitto
# from the frontend directory
ng serve --host 0.0.0.0 --port 80
# from the backend directory
python3 backend/website.py
```
In this case the main UI is available at the port 80

### ESP8266

1. Use the [official guide](https://docs.micropython.org/en/v1.14/esp8266/tutorial/intro.html) of installing MicroPython to a ESP8266. Finding a serial port may be tricky. Before connecting the ESP8266 to Raspberry Pi run the following:

   ```bash
   ls -l /dev/ttyUSB*
   ```
   
2. Edit MicroPython scripts in the `esp8266` project's directory:
   - *boot.py*: update `ssid` and `password` with your local home WiFi network name and password
   - *main.py* update `mqtt_server` with your Raspberry Pi IP address in the home network
   
3. Copy all 4 files from the `esp8266` project's directory

# Circuit diagram

![circuit diagram](./images/circuit_diagram.jpg)

### List of components

1. 1 x ESP8266 NodeMCU development board
2. 1 x SMD 5050 RGB LED strip - 1
3. 3 x TIP120 NPN transistor
4. 3 x 180-240 Ohm resistor
5. 1 x Mini-360 DC-DC buck converter
6. 1 x 1N914 switching diode
7. 1 x 12V 3A power supply

# How this all Works

Diagram with no text explanation for now about the device register process:

![smart light ping](./images/smart_light_ping.png)
