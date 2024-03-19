# command_encoder.py
# Date: 1/2/24
# Author: Rebecca Blum
# 
# Revisions:
#   [name]     [date]     [notes]
#   R. Blum    1/11/24    initial script creation 
#
# Summary:
#   This script translates input "human readable" commands into binary. It then
#   sends off the binary sequences to the onsite system via Iridium. 
#
# Inputs:
#   [command type]
#   [command argument 1] - optional
#   [command argument 2] - optional
#
# Outputs:
#   None/message sent to Iridium
#
#------------------------------------------------------------------------------
# import packages and library 
import os
import sys
import argparse
import numpy

def func(id,value):
    # id determined by which button is pushed

    if id.lower() == 'sf':
        # set sampling frequency of GNSS reciever
        if len(value) > 1:
            print("Error: too many input values for the sampling frequency")
            return
        cmd = 'sf='+value[0]

    elif id.lower() == 'el':
        # set elevation angle range
        if len(value) > 2:
            print("Error: too many input values for the elevation angle range")
            return
        cmd = 'el='+value[0]+','+value[1]

    elif id.lower() == 'az':
        # set azimuth angle range
        if len(value) > 2:
            print("Error: too many input values for the azimuth angle range")
            return
        cmd = 'az='+value[0]+','+value[1]

    elif id.lower() == 'mode':
        # set system to calibration or normal mode
        if len(value) > 1:
            print("Error: too many input values for the mode")
            return
        cmd = 'mode='+value[0]

    elif id.lower() == 'tres':
        # set time resolution of water level measurements
        if len(value) > 1:
            print("Error: too many input values for the time resolution")
            return
        cmd = 'tres='+value[0]

    else: 
        print('Error: command not defined in database')
    # need to concert command to hex
    cmd_hex = 0
    return cmd_hex

def main():
    # this main script was just a test (not applicable anymore)
    input = sys.argv

    cmd = input[1:len(input)] # the zeroeth entry is not useful here 

    print('\n')
 
    #os.system("python command_interpreter.py " + cmd)  
    
    print("done")
    
    return 

if __name__ == "__main__":
    main()
