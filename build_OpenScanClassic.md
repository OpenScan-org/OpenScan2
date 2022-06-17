# OpenScan Classic

## Overview
The OpenScan Classic is a compact desktop 3D scanner capable of scanning objects up to ~16 cm with an accuracy of up to 0.02 mm. The frame can be fully 3d printed, and all other components are off-the-shelf parts. You should be able to source all parts locally, or chose to support the OpenScan project by ordering (some) parts through [Openscan.eu/shop](https://www.openscan.eu/shop). Currently, the following cameras can be used without any additional modifications: Arducam IMX519 16mp & autofocus, Pi Camera v2 8mp and Pi Camera v1.3 5mp, where the Arducam IMX519 has to be considered the gold standard (for now :). Alternatively, you can even use many DSLR cameras, which can be connected and controlled through the Raspberry Pis USB interface...

## Bill of material (BOM)
TODO

## 3D Printing
Get the printable .stl (and design) files
TODO

## Assembly

TODO

### Preparing the Ringlight Module

** IMPORTANT: Make sure to follow the right setup for your camera module (either Arducam IMX519 or PiCamera V1.3/V2):

#### Arducam IMX519 16mp with Autofocus
* 1x Ringlight PCB
* 1x Arducam IMX519 16mp camera module 
* 2x M2x6 screws
* 2x M2x6 standoffs
* 2x M2 nuts

See the sequence of the parts: 

![image](https://user-images.githubusercontent.com/57842400/174085376-bd4337ea-9719-4759-b4ed-e29f14d615cb.png)

**Make sure that the lens is properly centered (looking at the ringlight from the front as shown in the right image):**

![arducam](https://user-images.githubusercontent.com/57842400/174086556-5910f154-6780-4acd-94b1-73ce9ca5a6db.jpg)

#### Pi Camera v2.1 or v1.3

* 1x Ringlight PCB
* Pi Camera v2.1 or v1.3 module 
* 2x M2x12 screws
* 2x spacer
* 2x M2 nuts

See the sequence of the parts: 

![image](https://user-images.githubusercontent.com/57842400/174087838-dd806e6d-5823-4748-9241-7bf04aed1ba9.png)

![picamera](https://user-images.githubusercontent.com/57842400/174087769-922aa8e4-7e88-4b05-b342-0912f542a6b9.jpg)

### Mounting and connecting the Ringlight and the Pi Shield

Control Module:
![cm1](https://user-images.githubusercontent.com/57842400/174266033-a81330d0-3ee6-4003-9ea8-c61052450e82.jpg)

Use 8x M3x8 screws to mount the ringlight module and the Pi Shield:
![cm2](https://user-images.githubusercontent.com/57842400/174266045-947d8560-28cf-4865-a757-6b2b86a89879.jpg)

Connect the ringlight module and the pi shield with the 50cm ringlight cable, connect the motor cables:
![cm3](https://user-images.githubusercontent.com/57842400/174266161-1997a631-11e5-42b6-9b2c-18bf01383317.jpg)

Use the 15cm camera ribbon cable to connect the Raspberry Pi and the camera. Make sure that the ribbon cables side with the metal pins is facing away from the USB ports of the Raspberry Pi.:
![cm3a](https://user-images.githubusercontent.com/57842400/174270185-d77f9e4e-0d06-4ced-bae6-abc95f301ba8.jpg)

Make sure to properly align the Raspberry Pi with the Pin headers on the Pi Shield. **Misalignment might destroy both the Raspberry Pi and the Pi Shield!**:
![cm5](https://user-images.githubusercontent.com/57842400/174270550-4c2011cf-f341-496f-865f-2ff76aa30541.jpg)

Your control module is ready to use and should look something like:
![cm6](https://user-images.githubusercontent.com/57842400/174271651-d889a7b1-677b-444f-bfb7-48d45ed78e58.jpg)

