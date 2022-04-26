
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

### Accessing the user-interface

Insert the Micro-SD card into the Raspberry Pi and power up the device. The first boot will take 2-3 minutes. The LED ring light will blink several times after successfully starting the scanner.

You will be able to access the scanner's interface from any device in the same network. Open any browser and follow this link: **[http://openscan/](http://openscan/)**, which will open the following start screen: 

![image](https://user-images.githubusercontent.com/57842400/165322638-bb3b2524-70f1-4a66-9d7f-aeb60535760f.png)

Note: It is highly recommended (but not necessary) to allow internet access in order to get the latest updates and/or use the free OpenScanCloud processing pipeline. Alternatively, you can deactivate internet access in your router's settings and use the scanner locally. 

The scanner will automatically check, if new updates are available. Before continuing, make sure to **install updates** by clicking the button. The device will reboot.

### Select camera and scanner model

Select the scanner's model from the dropdown menu:

- [OpenScan Classic](https://en.openscan.eu/openscan-classic)

- [OpenScan Mini](https://en.openscan.eu/openscan-mini)

Select the camera from the dropdown menu:

- Pi Camera v1, v2, HQ, Arducam IMX519, IMX290, IMX378, OV9281 are connected through the ribbon cable. If you encounter any issues, please check the cable's orientation!

- DSLR (gphoto) - can be used with a wide range of cameras, which can be connected and controlled via USB. Check [GPhoto](http://www.gphoto.org/proj/libgphoto2/support.php) if your camera is supported.

- External Camera - Can be used to connect your camera trigger to the GPIO pins on the front of the pi shield. This can be used with any (modified) remote shutter release, and thus it is possible to use Smartphones, DSLR and compact cameras

After selecting camera and model, you should restart the device one final time ;)


![image](https://user-images.githubusercontent.com/57842400/165325652-c8b6da72-5322-4a2b-a5d2-dcd8beaac39e.png)

Now, the shown start screen will appear in its full glory showing all available sub-menus. You can navigate the menu by expanding the navigation bar on the top left:

You are ready to start scanning :)

But before you do so, please open the settings menu in order to customize the device to your needs and use its full potential!

## Settings Menu

![image](https://user-images.githubusercontent.com/57842400/165332037-27323913-a45e-40cc-9d10-f277fd25489c.png)

Note that there are small **Info** buttons in every column, which will open a pop-up window with additional information

### SSH
**If you do not intend to access the device by terminal, please deactivate ssh.**
If you want to use ssh, please use the following credentials to login and change the password immediately! (default user: pi, password: raspberry)

### Samba
Samba is a local filesharing server, which allows accessing the files on the device directly from your computer. This can be used to manage the image sets in your file browser. Additionally, you can upload zip files containing image sets from your computer to the Raspberry Pi in order to use the OpenScanCloud processing pipeline. **If you do not intend to use this feature, please deactivate samba.**

Please change the default password by running the following command (default user: pi, password: raspberry): 

```sudo smbpasswd -a pi```

Copy the following address to your file browser in order to access the local files: ```\\openscan\PiShare\OpenScan\scans```

### OpenScanCloud
In order to use the free/donation-based OpenScanCloud, you first have to read & agree to the Terms of use. The only requirement is an individual token, which is a 32-digit individual key, which you can easily get through the user interface. In order to get such a token you need to hit **register** and enter your e-mail address, first and family name. The token will be sent to the given mail within one or two days. Please check your spam folder!

As soon as you enter a token, it will be verified and you can see your individual "limits"

![image](https://user-images.githubusercontent.com/57842400/165333684-83cccd65-15a2-4e87-85e0-a314714d97d8.png)

Each token comes with a given amount of 'credit' which is another measure against spam. The given number in Gigabyte indicates the amount of data, that you can process on the servers. IMPORTANT: The credit can be increased at any time by sending a mail to cloud@openscan.eu

### Network - Hostname
If you use multiple OpenScan devices in the same network, it is quite useful to give every scanner its individual name ;)

### Advanced settings
There are a ton of additional settings, which you can modify. Note, that for the OpenScan Classic & Mini, you do not need to touch any of those settings.

## SCAN

![image](https://user-images.githubusercontent.com/57842400/165336866-0aac79ff-6b4f-41d8-87fd-ed793c3f9f02.png)

Finally! Time to start scanning :)

- set the projectname
- Place the **prepared** object on the turntable (**please follow *how to get good scanning results*, to properly prepare your object  and setup and avoid disappointing results :)**)
- Turn on the ring light
- when using the OpenScan Classic: move the camera close to the object
- adjust the shutter speed, so that there are no over- or underexposed areas
- crop the image, so that the amount of visible background is minimal
- 70 - 100 photos are more than enough for almost all objects. If the result is bad, 200 photos won't improve it significantly ;)
- Start the routine
- Pause, unpause or stop the routine if you need to
- After the scan is done, you can choose, whether you want to do a second pass, with a different object orientation or finish the scan. Once finished, the image set can be accessed in the **Files&Cloud** menu.

## HOW TO GET GOOD SCANNING RESULTS

Whether a scanning result will be good or bad is fully determined before even starting the scan. Especially metal and plastic parts will need some kind of preparation (i.e. chalk or scanning spray). Please read the following guide and understand the basic principles depicted here [Openscan.eu/photogrammetry](https://en.openscan.eu/photogrammetrie)

![DecisionTree](https://user-images.githubusercontent.com/57842400/165338465-a8296dba-f05b-4db1-908f-e1f7d921e373.png)

## Troubleshooting

### What is the starting position for the rotor
Please understand the coordinate-system used here. The following image shows the 0°-position

![image](https://user-images.githubusercontent.com/57842400/165343581-94caf3bb-97cd-4892-a441-9cd95ee834e7.png)

and you can set the starting position of the rotor in the settings menu/motor tab (advanced settings)
### The motor moves to fast
- lower the acceleration in the settings menu/motor tab (advanced settings)
- increase the motor delay (advanced settings)
### The images are out of focus
- in case of Arducam: use manual focus mode
- in case of Pi Camera: re-focus the camera using the focus adjustment tool
### The scanner does not cover the whole object
- change the min/max angle in the motor rotor settings (advanced settings)
### when pressing up, the rotor is moving down
- invert the motor by either flipping the motor cable's connector 180° (after powering off the device!!) or change the motor's direction in the motor settings menu (advanced settings)
### I do not want the fancy scan routine and instead use the turntable only
- activate the turntable mode in the motor settings (advanced settings), which will deactivate the rotor


## FILES & CLOUD

![image](https://user-images.githubusercontent.com/57842400/165345009-1bf5bb61-5df6-4521-8723-8d120ad18df0.png)

## UPDATE & INFO

![image](https://user-images.githubusercontent.com/57842400/165345299-9269ae69-4bdd-43bd-a57d-b1624d37c534.png)


### Backend (node-red)
You can access the backend/programming interface Node-red through the following link [http://openscan/editor](http://openscan/editor)

![image](https://user-images.githubusercontent.com/57842400/165345589-58a6f50c-ee0b-4812-b96f-74448c83f21e.png)

