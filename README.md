# OpenScan2

## Overview:
Here you can find everything you need to know in order to build your own 3D Scanner. The OpenScan concept is very modular, so that you can take individual parts and adjust it to your needs (i.e. firmware, 3d printed design, PCB, photogrammetry cloud processing ...). The center piece is a Raspberry Pi driven camera/motor controller, which can be used to drive various photogrammetry rigs. Currently, there are two major hardware designs available - the OpenScan Classic and Mini. Everything is controlled by the OpenScan Firmware, which is based on the Node-Red browser interface.

Note, that I am currently centralizing all the information and manuals, that were created since 2018, into this repository. If you are looking for anything in particular, feel free to join the [discussions](https://github.com/OpenScanEu/OpenScan2/discussions) or open an [issue](https://github.com/OpenScanEu/OpenScan2/issues).

## Documentation
* [TODO Build Instructions - Pi Shield & Ringlight](.md)
* [TODO Build Instructions - OpenScan Mini](.md)
* [TODO Build Instructions - OpenScan Classic](.md)
* [Firmware - Setup](firmware_setup.md)
* [Firmware - Usage](HowToUse.md)
* [Photogrammetry - Basics](photogrammetry_basics.md)
* [TODO Photogrammetry - Software](photogrammetry_software.md.md)

The Raspberry Pi + OpenScan Pi Shield can be used to control two independent stepper motors and a variety of different cameras (Pi Camera, various Arducams, DSLR - via GPhoto and external Cameras like Smartphone and others). The mechanism can be used in various forms (see for example [OpenScan Classic](https://www.thingiverse.com/thing:3050437) or [OpenScan Mini](https://www.thingiverse.com/thing:4562060) and it could be easily adapted to be used as a camera slider or in other mechanisms.

### I have pre-compiled a working Raspbian Image (2022-04-20), that can be downloaded from [Google Drive (1.5GB)](https://drive.google.com/file/d/1wppbey1Fpqb-MpgHfnHXEZbjoDHfc8P4/view?usp=sharing) (working flawlessly on Raspberry Pi 3b+ and 4)


## Changelog
### 2022-05-11 beta
* added: changelog and version (finally ;)
* added: create an update using the node-red-backend inject node ("create beta" and "prepare image creation" in "update" tab)
* fixed: Error handling in flask (when no preview is taken)
* fixed: Error when upload failed + node red restarted (multiple instances of curl)
* fixed: When closing the browser session/missing the popup after the routine, the data set got lost (if this happens, just restart the device and it will be moved to the right location)
### 2022-04-26 beta 
* added: donation button ;)
* fixed: the wonderful camera position algorithm was faulty and a bit inefficient
* fixed: downscaling the preview image caused the preview to disappear (when crop value was to high)
* fixed: delay_before and delay_after are now properly applied, so that you can set a delay before/after taking a photo
* fixed: updates might crash the selected camera --> it is now necessary to re-select the camera after certain updates
### 2022-04-21 beta
* added: timer (ETA) until a routine is done
* added: showing progress, while files are being split (before uploading to OpenScanCloud)
* added: infotexts (FINALLY :)
* added: several stats/device information
* fixed: combining two sets did not delete the smaller set
### 2022-04-20 beta & main
* !fixed: pi cameras (v1.3, v2.1 and HQ) finally work and can be simply selected in the settings menu
* !fixed: Raspberry Pi 3B+ and 4 work! (the main limiting factor now is the RAM, where at least 1GB RAM is needed)
* fixed: live preview sometimes did not work. This has been a network speed issue and has been solved by downscaling the image (resolution can be set)
* fixed: it is now possible to delete individual sets.
* fixed: it is now possible to use all LEDs.
* added: Turntable mode (disable the second axis)
* added: Pause scan. You can pause and un-pause the scan by simply pressing the button
* added: second scan pass. When one scan is done, you can immediately run a second pass. This is especially useful, if you want to re-orient the object
* added: auto-timeout. Turn off the ringlight (todo: and motors) after 300 seconds (value can be set)
* added: diskspace warning. When free diskspace drops below a given threshold (4GB by default), a warning message will appear
* changed: new background image, minor design changes
* changed: log file can be easily generated and downloaded by clicking a button (update&info tab)## Main Features:

## Structure of this repository

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
