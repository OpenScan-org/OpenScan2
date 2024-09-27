#!/bin/bash

settings_folder="/home/pi/OpenScan/settings"

# Generate an unique UUID that identifies that OpenScan

if [ ! -f $settings_folder/openscan_uuid ]; then
	echo $(cat /proc/sys/kernel/random/uuid) > $settings_folder/openscan_uuid
fi
echo `cat /proc/cpuinfo|grep Model|cut -d: -f2|awk '{$1=$1};1'` > $settings_folder/architecture
echo `libcamera-still  --list-cameras|head -3|tail -1|cut -d: -f2|cut -d[ -f1|awk '{$1=$1};1'` > $settings_folder/camera
