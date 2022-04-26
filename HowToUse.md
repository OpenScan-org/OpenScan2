
# How to use the OpenScan Firmware

## TLDR
* Add your wifi credentials to wpa_supplicant.conf in the /boot/ directory of the SD card **OR** connect the device to your router with an Ethernet cable
* connect the device to a 12V power source and start booting
* after 1-2 mins, access **[http://openscan/](http://openscan/)** on a device, which is connected to the same network (alternatively, you can connect to http:// + **IP** with the local IP of the device)
* enter the model and camera type 
* optional: open settings menu and request & insert the OpenScanCloud token
* open **Scan** menu, turn on the ringlight, adjust the brightness, crop unneeded background and make a first dataset of 50-100 photos
* download the photos to your PC in the **Files&Cloud** menu (alternatively, upload the dataset to OpenScanCloud for processing)

## Connecting to the device for the first time

### By ethernet
It is highly recommended to use an Ethernet cable for the first start and add Wi-Fi credentials in settings menu later (see ...). 

To do so, connect the Raspberry Pi to your router using an Ethernet cable. Skip the next step.

### By wifi
Insert the Micro-SD card into your computer and open the **boot**-directory. Find and open the file **wpa_supplicant.conf**
![image](https://user-images.githubusercontent.com/57842400/165316356-04fd9f0d-7526-4ac7-a9b0-6879b29f7310.png)

Change the country code according to your location (see [Wikipedia - ISO3166-1 alpha-2 country codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)) and change your Network name (SSID) and Wifi-Password (psk):

![image](https://user-images.githubusercontent.com/57842400/165317238-07f2b4b3-e786-4285-8d69-65e918a44793.png)

Double-check your SSID and psk! 
Seriously! ;)

Save the file and unmount the Micro-SD card from your computer.

### Accessing the device

Insert the Micro-SD card into the Raspberry Pi and power up the device. The first boot will take 2-3 minutes. The LED ring light will blink several times after successfully starting the scanner.

You will be able to access the scanner's interface from any device in the same network. Open any browser and follow this link: **[http://openscan/](http://openscan/)**, which will open the following start screen: 

![image](https://user-images.githubusercontent.com/57842400/165322638-bb3b2524-70f1-4a66-9d7f-aeb60535760f.png)

Note: It is highly recommended (but not necessary) to allow internet access in order to get the latest updates and/or use the free OpenScanCloud processing pipeline. Alternatively, you can deactivate internet access in your router's settings and use the scanner locally. 

The scanner will automatically check, if new updates are available. Before continuing, make sure to **install updates** by clicking the button. The device will reboot.

Add the scanner's model from the dropdown menu:

- [OpenScan Classic](https://en.openscan.eu/openscan-classic)

- [OpenScan Mini](https://en.openscan.eu/openscan-mini)

Select the camera from the dropdown menu:

- Pi Camera v1, v2, HQ, Arducam IMX519, IMX290, IMX378, OV9281 are connected through the ribbon cable. If you encounter any issues, please check the cable's orientation!

- DSLR (gphoto) - can be used with a wide range of cameras, which can be connected and controlled via USB. Check [GPhoto](http://www.gphoto.org/proj/libgphoto2/support.php) if your camera is supported.

- External Camera - Can be used to connect your camera trigger to the GPIO pins on the front of the pi shield. This can be used with any (modified) remote shutter release, and thus it is possible to use Smartphones, DSLR and compact cameras

### Initial Software Setup

(model, camera, cloud)
disable ssh, samba, change password


## Quickstart
a summarized version, how to get your first scan

## Detailed description - Frontend
### SCAN
### FILES & CLOUD
### SETTINGS
### UPDATE & INFO

### Detailed description - Backend (node-red)
