#!/bin/sh
sudo ifconfig wlan1 down
sudo create_ap wlan1 wlan0 MyAP abc12345
