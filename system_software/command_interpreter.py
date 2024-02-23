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
import sys
from common_functions import *

# Function to read in contents of specified file
#def read_file(filename):

    #file = open(filename, 'r')
    #lines = file.readlines()
    #i = 0
    #for line in lines:
        #lines[i] = line.strip("\n")
        #i = i+1
    #file.close()
    #return lines

# Function to write to file
#def write_file(content,filename):
    #f = open(filename, "r+")
    #for item in content:
        #f.write(str(item) + "\n")
    #f.close()
    #return

# Interpret and execute command 
def func(input,output):

    if int(input[0:6],base=2) == 1:
        # rebootgnss
        # send cmd to gnss reciever to boot it?
        # return completely from this script (no updates to setvars file)
        print(2)

    elif int(input[0:6],base=2) == 2:
        # rebootrpi
        # reboot rpi (but then we need to turn it on again)
        print(3)  

    elif int(input[0:6],base=2) == 3:
        # setfreq - set sampling frequency of GNSS reciever

        # - bits 5-8: sampling freq (Hz)
        # - or have lookup table for common frequencies 
        freq = int('0b' + input[6:10],base=2)

        output[0] = freq

    elif int(input[0:6],base=2) == 4:
        # setelrng - set elevation range for height computation 

        # limits:           el from NMEA exists in [0,90] (deg.) 
        # usable limits:    5 - 25 (deg.) because...
        # representation:   5 bits where max is 11111 = 32

        # (Possible change if needed: 111111 = 63 -> go to 50 where el exits in [0:0.5:25])

        # - bits 5-9: max elevation (deg.) 
        max_el = int('0b' + input[6:11],base=2)

        # - bits 10-14: min elevation (deg.)
        min_el = int('0b' + input[11:16],base=2)

        output[1] = max_el
        output[2] = min_el

    elif int(input[0:6],base=2) == 5:
        # setazrng - set azmuth range for usable reflections

        # max azmuth (deg.) bits 5-10
        max_az = int('0b' + input[6:12],base=2)

        # min azmuth (deg.) bits 11-16
        min_az = int('0b' + input[12:18],base=2)

        output[3] = max_az
        output[4] = min_az   

    elif int(input[0:6],base=2) == 6:
        # calmode
        # set variables/settings/flags such that:
        # - system checks inbox every 5(?) minutes
        # - send back azmuth range once set?
        output[5] = 'calibration'

    elif int(input[0:6],base=2) == 7:
        # normmode
        # set variables/settings/flags such that:
        # - system checksvinbox every hour (or is it 2?)
        output[5] = 'normal'

    elif int(input[0:6],base=2) == 8:
        # settimeres
        # # of height calculations per data cycle (int)
        # bits 5-10
        time_res = int('0b' + input[6:12],base=2)
        output[6] = time_res
        print(8)

    else:
        print("Error: command not defined in database")
    return output

# Main function
def main():
    # grab input to script
    input = sys.argv

    # convert string to Python representation of binary digit
    cmd = '0b' + input[1] 

    # read in setvars file with current configuration 
    set_vars = read_file('setvars.txt')

    # Interpret command and update settings if it applies 
    updated_vars = func(cmd,set_vars)

    # update setvars file with new configuration 
    write_file(updated_vars, "setvars.txt")

if __name__ == "__main__":
    main()

#input = '0b' + '0101' + '001100' + '110000'
#input = '0b' + '0100' + '00111' + '11111'
#input = '0b' + '0001' + '0011'
#output = ["freq", "max_el", "min_el", "max_az", "min_az","calibration","time_res"]    
