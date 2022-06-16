# OpenScan Mini with Polarizer Module

## Overview
The OpenScan Mini is a compact desktop 3D scanner capable of scanning objects up to ~8-10 cm with an accuracy of up to 0.02 mm. The frame can be fully 3d printed, and all other components are off-the-shelf parts. You should be able to source all parts locally, or chose to support the OpenScan project by ordering (some) parts through [Openscan.eu/shop](https://www.openscan.eu/shop). Currently, the following cameras can be used without any additional modifications: Arducam IMX519 16mp & autofocus, Pi Camera v2 8mp and Pi Camera v1.3 5mp, where the Arducam IMX519 has to be considered the gold standard (for now :)

## Bill of material (BOM)

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

* 1x Frontplate
* 1x Pi Shield
* 4x M3x8

![01 Front Plate](https://user-images.githubusercontent.com/57842400/174010152-9fbd78e1-ace7-4039-8b84-0317904dfff7.jpg)

Mount the Pi Shield to the front plate using four M3x8mm screws

![image](https://user-images.githubusercontent.com/57842400/174010869-10b5b811-ec70-494f-9561-13c06db15225.png)

### Base + Rotor

![image](https://user-images.githubusercontent.com/57842400/174011199-4c490f54-23da-428f-b591-879528749ccf.png)

Insert the rotor into the base and make sure, that the rotor can slide freely! (It might require some sanding and/or lubrication)

![image](https://user-images.githubusercontent.com/57842400/174011429-829c49ff-1984-482a-a365-f43797455679.png)

### Mounting the Turntable Motor

* 1x Base + Rotor
* 1x Nema17 small
* 4x M3x8

Make sure to mount the small stepper motor (Turntable) first. The motor connector should face to the left.

![image](https://user-images.githubusercontent.com/57842400/174012562-1a7dbb75-fd7f-461c-b66c-2d5fc197203c.png)

### Mounting the Rotor Motor

* 1x small gear
* 1x Nema17 large
* 4x M3x8

Press the small gear onto the shaft of the larger stepper motor.

![image](https://user-images.githubusercontent.com/57842400/174012814-5df28109-02cf-4510-999c-205db8ce5b93.png)

Mount the stepper motor with four M3x8 screws like shown below. Move the large ring a couple of times to make sure, that the gears fit. Again, the motor connector should face to the left.

![image](https://user-images.githubusercontent.com/57842400/174013038-1652bd7d-440b-44f8-a39a-a31aad0bb571.png)

### Mounting the Raspberry Pi

* 1x Raspberry Pi
* 1x Micro SD Card with OpenScan Image. See [Firmware - Setup - Prepare/compile the SD Card](firmware_setup.md). (Alternatively you can use a recent Raspbian version, if you intend to build the firmware yourself.)
* 4x M3x8

Insert the Micro SD card into the slot of the Raspberry Pi.

Mount the Raspberry Pi with four M3x8 screws. Make sure not to overtighten the screws, which might bend and damage the board. Note, that the Raspberry Pis screw holes are quite tight.

![image](https://user-images.githubusercontent.com/57842400/174013798-e6b72852-53f9-493a-96d3-4bc26c1b1188.png)








### Preparing the Ringlight Module

* 1x Base+Ring
* 1x Nema17 small
* 4x M3x8

**Arducam IMX519**

**Pi Camera v2**

**Pi Camera v1.3**

### Preparing the camera cable

### Mounting and connecting the Ringlight Module 

### Connecting the Pi Shield

### Mounting the Frontplate

### Mounting the Backplate

### Mounting the Diffuser/Polarizer


