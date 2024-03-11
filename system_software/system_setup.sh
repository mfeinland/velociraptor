#!/bin/bash

# set up connections and make the serial connection a enviromental variable
usb_connections=$(dmesg | grep "now attached") 
# cp210x (GNSS receiver)
# FTDI (transceiver)

python path/devSetup.py $usb_connections

# get time from GNSS
utc_time=$(python path/get_time.py)

# set system time "12 FEB 2024 00:00:00"
sudo date -s "@$utc_time"

# add leap seconds: TAI = UTC+37 as of Feb 2024
# leap seconds obtained from Bulletin C located at https://www.iers.org/IERS/EN/Publications/Bulletins/bulletins.html
sudo date -s "37 seconds"
