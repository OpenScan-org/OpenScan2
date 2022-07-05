# OpenScan Mini with Polarizer Module

![OS_mini](https://user-images.githubusercontent.com/57842400/174252972-7d1f8ca2-e316-400d-b8b6-607e3f5f5140.jpg)


## Overview
The OpenScan Mini is a compact desktop 3D scanner capable of scanning objects up to ~8-10 cm with an accuracy of up to 0.02 mm. The frame can be fully 3d printed, and all other components are off-the-shelf parts. You should be able to source all parts locally, or chose to support the OpenScan project by ordering (some) parts through [Openscan.eu/shop](https://www.openscan.eu/shop). Currently, the following cameras can be used without any additional modifications: Arducam IMX519 16mp & autofocus, Pi Camera v2 8mp and Pi Camera v1.3 5mp, where the Arducam IMX519 has to be considered the gold standard (for now :)

## Bill of material (BOM)
* 24x M3x8 screws
* 1x M3x12 screw
* 1x [Pi Shield](https://en.openscan.eu/product-page/raspberry-pi-shield)
* 1x Nema 17 (>40Ncm)
* 1x Nema 17 (>13Ncm)
* 1x Raspberry Pi 3B+ or 4 (any)
* 1x Micro SD Card (>16GB)
* 1x Camera Ribbon Cable 50cm
* 1x [Ringlight](https://en.openscan.eu/product-page/pi-camera-ringlicht)
* 1x Camera Module IMX519 (alternatively Pi Camera V2 or V1.3)
* 2x M2x6 Nylon Screw
* 2x M2x6 Nylon Standoff
* 2x M2 Nuts
* (2x M2x12 Nylon Screw if you use the Pi Camera module)
* 1x Polarizer module

3d printed parts:
* Frontplate
* Base
* Rotor
* small gear
* backplate
* object holders (4 sizes)

## 3D Printing
Get the printable .stl (and design) files [here](https://github.com/OpenScanEu/OpenScan-Design/tree/main/OpenScanMini).

**PRINTER**
- you will need a print-bed of at least 200x200mm
- depending on your printer's capabilities (and your risk aversion), all parts can be fitted onto one build plate of min. 220x210mm
- printing all parts can be done in under 17h (tested on Prusa MK3S+ using default Draft profile)

**PRINT SETTINGS**
- support: no (* except for 07_polarizer_b
- layer-height: 0.2-0.3 mm
- print speed: depends on your printer's calibration

**MATERIAL**
- COLOR - main Frame: Please use a material without visible particles or structure. Avoid transparent materials
- COLOR - 07_polarizer_a: translucent/natural
- COLOR - 07_polarizer_b: any non-translucent material (like PETG black, Prusament Galaxy Black) 
- PLA is totally fine, since there is not a lot of mechanical strength needed
- PETG, ABS, ASA can be used for increased temperature resistance in warm environments

## Assembly

### Frontplate + Pi-Shield

* 1x Frontplate (3d print)
* 1x Pi Shield
* 4x M3x8

![01 Front Plate](https://user-images.githubusercontent.com/57842400/174010152-9fbd78e1-ace7-4039-8b84-0317904dfff7.jpg)

Mount the Pi Shield to the front plate using four M3x8mm screws

![image](https://user-images.githubusercontent.com/57842400/174010869-10b5b811-ec70-494f-9561-13c06db15225.png)

### Base + Rotor
* 1x Base (3d print)
* 1x Rotor (3d print)
* lubricant and/or sandpaper (optional)

![image](https://user-images.githubusercontent.com/57842400/174011199-4c490f54-23da-428f-b591-879528749ccf.png)

Insert the rotor into the base and make sure, that the rotor can slide freely! (It might require some sanding and/or lubrication)

![image](https://user-images.githubusercontent.com/57842400/174011429-829c49ff-1984-482a-a365-f43797455679.png)

### Mounting the Turntable Motor

* 1x Base + Rotor
* 1x Nema17 small
* 4x M3x8 screws

Make sure to mount the small stepper motor (Turntable) first. The motor connector should face to the left.

![image](https://user-images.githubusercontent.com/57842400/174012562-1a7dbb75-fd7f-461c-b66c-2d5fc197203c.png)

### Mounting the Rotor Motor

* 1x small gear (3d print)
* 1x Nema17 large
* 4x M3x8 screw

Press the small gear onto the shaft of the larger stepper motor.

![image](https://user-images.githubusercontent.com/57842400/174012814-5df28109-02cf-4510-999c-205db8ce5b93.png)

Mount the stepper motor with four M3x8 screws like shown below. Move the large ring a couple of times to make sure, that the gears fit. Again, the motor connector should face to the left.

![image](https://user-images.githubusercontent.com/57842400/174013038-1652bd7d-440b-44f8-a39a-a31aad0bb571.png)

### Mounting the Raspberry Pi

* 1x Raspberry Pi
* 1x Micro SD Card with OpenScan Image. See [Firmware - Setup - Prepare/compile the SD Card](../firmware/setup.md). (Alternatively you can use a recent Raspbian version, if you intend to build the firmware yourself.)
* 4x M3x8 screws

Insert the Micro SD card into the slot of the Raspberry Pi.

Mount the Raspberry Pi with four M3x8 screws. Make sure not to overtighten the screws, which might bend and damage the board. Note, that the Raspberry Pis screw holes are a tight fit for those M3 screws.

![image](https://user-images.githubusercontent.com/57842400/174013798-e6b72852-53f9-493a-96d3-4bc26c1b1188.png)

### Preparing the camera cable

* 1x camera ribbon cable (50cm)

Insert the camera ribbon cable through the two slots (red arrows). Make sure that the metal plating of the cable is facing the stepper motor (yellow circle).
**Take care not to create sharp bends as this might damage the cable.:**

![image](https://user-images.githubusercontent.com/57842400/174072692-455368ca-7a0b-497c-8972-670d874e2e8e.png)

Continue through the next slot (again the metal plating should be facing away from you):

![image](https://user-images.githubusercontent.com/57842400/174072990-5dd92e10-4e8b-439f-b5c1-4b65b0573030.png)

Insert the camera ribbon cable into the socket. The metal plating should be facing away from the USB/Ethernet ports (yellow circle). Gently close the sockets bracke by pushing it down (dark part that likes to break).

![image](https://user-images.githubusercontent.com/57842400/174073304-8fe99998-6cd1-4678-bc74-b34034983e60.png)

### Preparing the Ringlight Module

** IMPORTANT: Make sure to follow the right setup for your camera module:

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

### Mounting and connecting the Ringlight Module 
* 1x Ringlight Module
* 1x 50cm ringlight power cable (3P JST XH)
* 4x M3x8 screws

Mount the ringlight module using 4 M3x8mm bolts as indicated by the red arrows:
![image](https://user-images.githubusercontent.com/57842400/174088696-c2679271-221a-4d9e-8668-62ab5f7b548f.png)

Connect the camera ribbon cable with the camera. The Metal plating is facing down. (yellow circle)
Connect the 50cm ringlight cable with 3P JST connectors to the Ringlight (red arrow):

![image](https://user-images.githubusercontent.com/57842400/174090062-214e2906-c021-4d3a-a00e-800714ea3225.png)

Guide the ringlight cable as indicated by the yellow circles:

![image](https://user-images.githubusercontent.com/57842400/174090027-2d1beaf6-c534-471c-bbe4-a1a458adef7a.png)

### Connecting the Pi Shield
* 1x Frontplate with Pi Shield
* 2x stepper motor cable

Connect the stepper motor cables to the Pi Shield and the corresponding stepper motors (see labels bellow):

![image](https://user-images.githubusercontent.com/57842400/174090377-aad5fdb1-fe46-4c98-8993-eb941254509e.png)

* (1) Turntable (small Nema 17)
* (2) Rotor (large Nema 17)
* (3) ST XH 3P (from ringlight module, see previous step)

### Mounting the Frontplate
* 1x M3x12 screw
* 1x frontplate with Pi Shield
* 1x base/rotor

Mount the frontplate to the base. **Make sure that the pin headers of the Raspberry Pi and the Pi shield are properly aligned. (Yellow circle):**

![image](https://user-images.githubusercontent.com/57842400/174091581-3bbc2ec2-97e7-4629-83f1-7ec37a521db4.png)

Use the M3 screw to connect the frontplate to the base_

![image](https://user-images.githubusercontent.com/57842400/174091474-c69e5b4e-965c-44b3-a53d-5347741ceaaa.png)

### Mounting the Backplate
* 4x M3x8 screws
* base/rotor
* backplate (3d print)

Make sure, that the ringlight cable is sitting in the guide slot. (yellow circle)
Use the 4 M3x8 screws to mount the backplate (red arrows):

![image](https://user-images.githubusercontent.com/57842400/174092053-64635fb3-bd46-4a16-9aa4-e80b42860089.png)

### Mounting the Diffuser/Polarizer
* OpenScan Mini
* Polarizer Module

The Polarizer module can be easily mounted by clicking it onto the rotor:
![image](https://user-images.githubusercontent.com/57842400/174101063-19a57087-fed6-4942-9bfe-185390ca3e7c.png)

The polarizer module consists of two printed parts. It is very important that the smaller printed part (yellow circle) is not translucent in order to block all light. 
There are two pieces of linear polarizer foil. The smaller piece (15x11mm) was inserted into the slot (red arrow). The larger piece (75x66mm) is covering the whole front area except for the middle (red arrow). It is absolutely crucial that those two pieces are oriented perpendicularly against each other. The polarizer will greatly improve the results by filtering allmost all direct reflections.
![image](https://user-images.githubusercontent.com/57842400/174097472-3fcbf9ff-4506-4d25-a7c9-11e51c692b21.png)

### Starting the device for the first time

Plug in a 12V (min. 2A power supply) and start the device. 

Continue with [this guide, which shows the initial setup of the firmware and some general tips & tricks](../firmware/usage.md)
