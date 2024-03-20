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
#import matplotlib.pyplot as plt

#def parse_args():

#    try:
#        print("Hello")
#    except:
#        print("Something went wrong")
#    else:
#        print("Nothing went wrong")

def dec2bin(value, length):
    long_binary = ['0']*length
    binary = [*str(bin(int(value)))]
    long_binary[2+length-len(binary):length] = binary[2:len(binary)]
    bin_string = "".join(long_binary)

    return bin_string

def func(id,value):

    if id.lower() == 'bootgnss':
        # bootgnss
        # send cmd to gnss reciever to boot it?
        bin_id = '0001'

    elif id.lower() == 'bootrpi':
        # bootrpi
        # reboot rpi (but then we need to turn it on again
        bin_id = '0010'

    elif id.lower() == 'setfreq':
        # setfreq
        #bits 5-8 are Hz
        # set sampling frequency of GNSS reciever
        if len(value) > 1:
            print("Error: too many input values for the sampling frequency")
            return
        bin_id = '0011'
        freq = dec2bin(value[0], 4)   #int('0b' + input[6:10],base=2)
        bin_cmd = bin_id + freq

    elif id.lower() == 'setelrng':
        # setelrng
        bin_id = '0100'
        # min elevation (deg.) bits 10-14
        min_el = dec2bin(value[0], 5)       #int('0b' + input[11:16],base=2)

        # max elevation (deg.) bits 5-9
        max_el = dec2bin(value[1], 5)       #int('0b' + input[6:11],base=2)

        bin_cmd = bin_id + min_el + max_el

    elif id.lower() == 'setazrng':
        # setazrng
        bin_id = '0101'

        # min azmuth (deg.) bits 11-16
        min_az = dec2bin(value[0], 6)    #int('0b' + input[12:18],base=2)

        # max azmuth (deg.) bits 5-10
        max_az = dec2bin(value[1], 6)     #int('0b' + input[6:12],base=2)

        bin_cmd = bin_id + min_az + max_az

    elif id.lower() == 'calmode':
        # calmode - calibration
        # set variables/settings/flags such that:
        # - system checks inbox every 5(?) minutes
        # - send back azmuth range once set?
        bin_cmd = '0110'

    elif id.lower() == 'normmode':
        # normmode - normal
        # set variables/settings/flags such that:
        # - system checksvinbox every hour (or is it 2?)
        bin_cmd = '0111'

    elif id.lower() == 8:
        # settimeres
        # # of height calculations per data cycle (int)
        bin_id = '1001'
        # bits 5-10
        time_res = int('0b' + input[6:12],base=2)
        bin_cmd = bin_id + time_res

    else: 
        print('Error: command not defined in database')

    return bin_cmd

def main():
    input = sys.argv

    cmd = input[1:len(input)] # the zeroeth entry is not useful here 

    print('\n')

    bin_cmd = func(cmd[0],cmd[1:len(cmd)])
 
    #os.system("python command_interpreter.py " + bin_cmd)  
    
    print("done")
    
    return 

if __name__ == "__main__":
    main()
    
#input = '0b' + '0101' + '001100' + '110000'
#input = '0b' + '0100' + '00111' + '11111'
#input = '0b' + '0001' + '0011'
#output = ["freq", "max_el", "min_el", "max_az", "min_az","calibration","time_res"]    