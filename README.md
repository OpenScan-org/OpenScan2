# OpenScan2
## Overview:
The Raspberry Pi + OpenScan Pi Shield can be used to control two independent stepper motors and a variety of different cameras (Pi Camera, DSLR - via GPhoto and external Cameras like Smartphone and others). The mechanism can be used in various forms (see for example [OpenScan Classic](https://www.thingiverse.com/thing:3050437) or [OpenScan Mini](https://www.thingiverse.com/thing:4562060) and it could be easily adapted to be used as a camera slider or in other mechanisms.
After sticking to my [original code](https://github.com/OpenScanEu/OpenScan) for way to long, I have spent a lot of time rewriting and re-organizing the whole code/structure/documentation and started this new repository. This should make it much easier to collaborate, implement future updates and continue exploring the wonderful world of 3d scanning :)

I have pre-compiled a working Raspbian Image, that can be downloaded from [Google Drive (1.5GB)](https://drive.google.com/file/d/128VQ4KB6vNhLotbOsOKdBW8b1EHVzUw6/view?usp=sharing) (working flawlessly on Raspberry Pi 3b+. Need to re-install the camera drivers on Raspberry Pi 4!)

# IMPORTANT: The following setup works for the adjustable focus camera Arducam IMX519, supported DSLR cameras and external cameras (via Gpio triggering). IT SOMEHOW DOES NOT WORK WITH THE STANDARD PI CAMERAS V1.3 V2.1 and HQ! There might be some issues when using the Raspberry Pi 4 and the provided pre-compiled Raspbian image. But I am doing my best to fixing those issues soon!

## Main Features:
* use your Raspberry Pi to take very consistent image sets for photogrammetry (other use cases should be possible to ;)
* use the included cloud processing function to automatically create highly detailed 3d models (see [OpenScanCloud](https://github.com/OpenScanEu/OpenScanCloud))
* various supported camera modules:
    * standard Raspberry Pi Cameras (v1.3, v2.1 and HQ)
    * Arducam IMX 519 (with 16mp and autofocus)
    * and many other cameras through the libcamera framework
* DSLRs:
    * many different models supported
    * preview and data acquisition via USB cable
    * see [gphoto](http://www.gphoto.org/doc/remote/)
    * and [gphoto](http://www.gphoto.org/proj/libgphoto2/support.php)
    * for lists of the various models
* triggering any camera through an isolated GPIO signal using a modified remote control

## Pre-compiled Raspbian image
You can download a pre-compiled Raspbian image from [Openscan.eu](http://www.openscan.eu/pi-shield)

## Structure of this repository

Many free image datasets with additional information and discussion
* datasets/
    * readme.md #todo

Several manuals on how to build/use/adjust the OpenScan devices, firmware and electronics
* manual/
    * readme.md #todo 
    * firmware-browserinterface.md #todo
    * firmware-backend.md #todo
    * object-preparation.md #todo

Providing the update files for the firmware, where the two .json files give a short summary of what changed
* update/
    * update.json
    * beta/
    * main/
    
## Setup

### Prerequisites
It is necessary to use a **Raspberry Pi with at least 1GB of RAM** to run the firmware. This includes the Raspberry Pi model 2B, 3B, 3B+ and all 4B variants.
The firmware and following installation guide is optimized for **Raspbian Bullseye with Desktop** environment, but can also be used headless (Note, that the desktop version comes with some libraries that you will otherwise need to install manually). 

### Raspi-config
```sudo raspi-config```

```--> performance options --> GPU --> change to 256```
Increase GPU memory, which helps processing the captured photos

```--> localization settings --> wlan country --> your country```
Change the WLAN settings, so that device works in your area

Save and reboot now (or later ;)

### Folder structure

Create directories

``` mkdir /home/pi/OpenScan/ /home/pi/OpenScan/scans /home/pi/OpenScan/files /home/pi/OpenScan/settings /home/pi/OpenScan/tmp /home/pi/OpenScan/updates ```

### WLAN settings

Open the settings file

```sudo nano /etc/network/interfaces```

And add to the end:

```
auto wlan0
iface wlan0 inet manual
wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```

### Samba (optional but highly recommended)
Create a shared network drive, so that you can easily access the Raspberry Pi's filesystem. It enables you to upload custom datasets to the OpenScanCloud through the browser interface. Simply copy a zip file containing your photos to the *../OpenScan/scans* directory.

Install the package

```sudo apt-get install samba samba-common-bin```

Open the configuration file

```sudo nano /etc/samba/smb.conf```

And change the following lines:

```
read only = no
create mask = 0775
directory mask = 0775
```

Add the following line, if you are using Windows:

```wins support = yes```

And add to the end of the file:

```
[PiShare]
comment=Raspberry Pi Share
path=/home/pi/
browseable=Yes
writeable=Yes
only guest=no
create mask=0777
directory mask=0777
public=yes
```

Set a password for user pi (by default I use password *raspberry*)

```sudo smbpasswd -a pi```

And add rights:

```sudo chmod -R 777 /home/pi/OpenScan```

### Gphoto

Necessary to controll DSLR cameras connected by USB cable.

```
sudo apt install libgphoto2-dev gphoto2
sudo pip3 install -v gphoto2
```

### NodeRed

Download and install:

```
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
```

--> confirm with yes and yes :)

Open node-red daemon file:

```sudo nano /lib/systemd/system/nodered.service```

add to the section [Unit]

```
Wants=network.target flask.service
After=flask.service
```

and change the following lines under [Service] to run nodered as root:

```
User = root
#Group = pi
```

Initialize node-red:

```sudo node-red admin init```

* settings file: ```/root/.node-red/settings.js```
* Security: ```No``` 
* Project: ```No``` 
* Flows File Settings: ```Enter``` 
* Passphrase: ```Enter``` 
* Theme: ```default``` 
* Text editor: ```default``` 
* External Modules: ```Yes```

Open node-red settings file:

```sudo nano /root/.node-red/settings.js```

And find, uncomment and change the following parameters:

```
userDir: '/home/pi/OpenScan/settings/.node-red/',

uiPort: process.env.PORT || 80,

httpAdminRoot: '/editor',

httpStatic: '/home/pi/OpenScan/',

ui: { path: "" },

functionGlobalContext: { // enables and pre-populates the context.global variable
    os:require('os'),
    path:require('path'),
    fs:require('fs')
    },
```

Enable nodered daemon and restart the device:

```
sudo systemctl enable nodered.service
sudo reboot -h
```

Open the node-red settings directory:

```cd /home/pi/OpenScan/settings/.node-red/```

And run the following command to install some additional palettes to node-red

```sudo npm i node-red-dashboard && sudo npm i node-red-contrib-python3-function && sudo npm i node-red-node-ui-table```

```node-red-restart```

### Libcamera - to run Arducam IMX519 (and other non-Raspberry-Pi camera moduls)
See [Arducam.com](https://www.arducam.com/docs/cameras-for-raspberry-pi/raspberry-pi-libcamera-guide/#how-to-install-libcamera-d9f38d46-8576-43e2-9375-e225c272095f) for more details

Download all necessary files

```wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh && chmod +x install_pivariety_pkgs.sh```

```sudo apt update ```

```./install_pivariety_pkgs.sh -p libcamera_dev```

```./install_pivariety_pkgs.sh -p libcamera_apps```

```./install_pivariety_pkgs.sh -p imx519_kernel_driver```

### Download OpenScan Firmware

Custom node red flows (browser interface):

```sudo wget https://raw.githubusercontent.com/OpenScanEu/OpenScan2/main/update/main/flows.json -O /home/pi/OpenScan/settings/.node-red/flows.json```

Some Python functions used by the firmware:

```sudo wget https://raw.githubusercontent.com/OpenScanEu/OpenScan2/main/update/main/OpenScan.py -O /usr/lib/python3/dist-packages/OpenScan.py```

A local server providing several functions (flask):

```sudo wget https://raw.githubusercontent.com/OpenScanEu/OpenScan2/main/update/main/fla.py -O /home/pi/OpenScan/files/fla.py```

Custom config.txt file, which is needed to use different camera moduls (especially IMX519):

```sudo wget https://raw.githubusercontent.com/OpenScanEu/OpenScan2/main/update/main/config.txt -O /boot/config.txt```

Arducam's camera focus script for the IMX519 sensor:

```sudo wget https://raw.githubusercontent.com/OpenScanEu/OpenScan2/main/update/main/Arducam.py -O /usr/lib/python3/dist-packages/Arducam.py```

And the OpenScan Logo to have a nice background:

```sudo wget https://raw.githubusercontent.com/OpenScanEu/OpenScan2/main/update/files/logo.jpg -O /home/pi/OpenScan/files/logo.jpg```

### Enable Flask local server:

create and open the service file:
```sudo nano /lib/systemd/system/flask.service```

with the following content:
```
[Unit]
Description=photo service
After=multi-user.target
[Service]
#ExecStartPre=/bin/sleep 5
ExecStart=/usr/bin/python3 /home/pi/OpenScan/files/fla.py
StandardOutput=inherit
StandardError=inherit
Restart=always
RestartSec=5
User=root
[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```sudo systemctl daemon-reload && sudo systemctl enable flask.service && sudo systemctl start flask.service```

### others

add to /boot/config.txt to disable display which causes some issues --> WHY???

```hdmi_blanking=2```
