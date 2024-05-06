#!/bin/bash

# Determine the USB connections
usb_connections=$(dmesg | grep "now attached") 
# cp210x (GNSS receiver)
# FTDI (transceiver)

# get time from GNSS
utc_time=$(python /home/velociraptor/two_hour_lifecycle_test/system_setup.py $usb_connections)
echo "$utc_time" 

#sudo date -s "$utc_time"

# add leap seconds: TAI = UTC+37 as of Feb 2024
# leap seconds obtained from Bulletin C located at 
# https://www.iers.org/IERS/EN/Publications/Bulletins/bulletins.html
#sudo date -s "37 seconds"
