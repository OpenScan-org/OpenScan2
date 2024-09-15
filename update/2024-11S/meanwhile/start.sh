#!/bin/bash

flow_dir="/home/pi/OpenScan/settings/.node-red"
flows_json_file=$flow_dir/flows.json
hostname=`hostname`
echo $hostname
session_token=`echo $RANDOM | md5sum | head -c 20`
echo $session_token > /home/pi/OpenScan/settings/session_token

cat $flow_dir/flows.json.tmpl|sed "s|{{ hostname }}|$hostname.local|g" > $flows_json_file
sed -i "s|{{ session_token }}|$session_token|g" $flows_json_file
