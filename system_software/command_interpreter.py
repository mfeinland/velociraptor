# command_interpreter.py
# Date: 1/11/24
# Author: Rebecca Blum
# 
# Revisions: 
#   [name]       [date]       [notes]
#   R. Blum      1/11/24      initial script creation 
#
# Summary: 
#     
#
# Inputs:
#   [command] - a string of binary digits 
#
# Outputs: 
#   [setvars.txt] - updated with commanded values 
#
# Limitations: 
#   The script currently only can handle one input command at a time. 
#
# Future edits: 
#   [issue]                               [status]                    [name]
#   Allow multiple input args             incomplete
#
#------------------------------------------------------------------------------
# import packages and library 
# import argparse

from receiver_functions import setFreq
import sys, os
from common_functions import *
#from receiver_functions import setFreq
import re

# Interpret and execute command 
def interpret_cmd(message,output):

    cmd_list = message.split(";")
    for item in cmd_list:
        cmd = re.split('=|,', item)

        if cmd[0] == 'rbrx':
            # rebootgnss
            # send cmd to gnss reciever to boot it?
            print(2)

        elif cmd[0] == 'rbpi':
            # rebootrpi: reboot rpi (but then we need to turn it on again)
            print(3)  

        elif cmd[0] == 'sf':
            # setfreq - set sampling frequency of GNSS reciever

            freq = cmd[1]
            
            #ser = os.environ.get("SERIAL")
            #setFreq(ser, freq) # have to get ser

            output[0] = freq # does it still need to output this?

        elif cmd[0] == 'el':
            # setelrng - set elevation range for height computation 

            # limits:           el from NMEA exists in [0,90] (deg.) 
            # usable limits:    5 - 25 (deg.) because...
            # representation:   5 bits where max is 11111 = 32

            # (Possible change if needed: 111111 = 63 -> go to 50 where el exits in [0:0.5:25])

            min_el = cmd[1]
            max_el = cmd[2]

            output[1] = min_el
            output[2] = max_el

        elif cmd[0] == 'az':
            # setazrng - set azmuth range for usable reflections

            min_az = cmd[1]
            max_az = cmd[2]

            output[3] = min_az
            output[4] = max_az   

        elif cmd[0] == 'mode':
            # calmode
            # set variables/settings/flags such that:
            # - system checks inbox every 5(?) minutes
            # - send back azmuth range once set?
            # normmode
            # set variables/settings/flags such that:
            # - system checksvinbox every hour (or is it 2?)

            if cmd[1] == '0':
                output[5] = 'calibration'
            elif cmd[1] == '1':
                output[5] = 'normal'

        elif cmd[0] == 'tres':
            # settimeres
            # # of height calculations per data cycle (int)

            time_res = cmd[1]

            output[6] = time_res

        else:
            print("Error: command not defined in database")

    return output

# Main function
def main():
    # grab input to script
    input = sys.argv

    # convert string to Python representation of binary digit
    message = input[1]

    # read in setvars file with current configuration 
    set_vars = read_file('setvars.txt')
    print(set_vars)

    # Interpret command and update settings if it applies 
    updated_vars = interpret_cmd(message,set_vars)

    # update setvars file with new configuration 
    write_file(updated_vars, "setvars.txt")
    print(updated_vars)
    return updated_vars

if __name__ == "__main__":
    main()
