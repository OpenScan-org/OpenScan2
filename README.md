# OpenScan2
## Overview:
The Raspberry Pi + OpenScan Pi Shield can be used to control two independent stepper motors and a variety of different cameras (Pi Camera, DSLR - via GPhoto and external Cameras like Smartphone and others). The mechanism can be used in various forms (see for example [OpenScan Classic](https://www.thingiverse.com/thing:3050437) or [OpenScan Mini](https://www.thingiverse.com/thing:4562060) and it could be easily adapted to be used as a camera slider or in other mechanisms.
After sticking to my [original code](https://github.com/OpenScanEu/OpenScan) for way to long, I have spent a lot of time rewriting and re-organizing the whole code/structure/documentation and started this new repository. This should make it much easier to collaborate, implement future updates and continue exploring the wonderful world of 3d scanning :)

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
    * beta.json
    * main.json
    * beta/
    * main/
    
## Setup

### Prerequisites
It is necessary to use a **Raspberry Pi with at least 1GB of RAM** to run the firmware. This includes the Raspberry Pi model 2B, 3B, 3B+ and all 4B variants.
The firmware and following installation guide is optimized for **Raspbian Bullseye with Desktop** environment, but can also be used headless (Note, that the desktop version comes with some libraries that you will otherwise need to install manually). 



```
#todo 
```
