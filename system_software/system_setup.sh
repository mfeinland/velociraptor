#!/bin/bash

# Determine the USB connections
usb_connections=$(dmesg | grep "now attached") 
# cp210x (GNSS receiver)
# FTDI (transceiver)

# get time from GNSS
utc_time=$(python path/system.py $usb_connections)

# set system time "12 FEB 2024 00:00:00"
sudo date -s "@$utc_time"

# add leap seconds: TAI = UTC+37 as of Feb 2024
# leap seconds obtained from Bulletin C located at 
# https://www.iers.org/IERS/EN/Publications/Bulletins/bulletins.html
sudo date -s "37 seconds"
