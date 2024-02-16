#!/bin/bash

# set up env variables
# either run 'export VAR="variable"' (probably not cause its only valid for the current shell and its child processes)
# or have them all in a text file 

# set up connections and make the serial connection a enviromental variable
export SERIAL=$(python3 devSetup.py)

# get time from GNSS
utc_time=$(python path/get_time.py)

# set system time

sudo date -s "@$utc_time"
# "12 FEB 2024 00:00:00"

# add leap seconds: TAI = UTC+37 as of Feb 2024
# leap seconds obtained from Bulletin C located at https://www.iers.org/IERS/EN/Publications/Bulletins/bulletins.html

sudo date -s "37 seconds"
