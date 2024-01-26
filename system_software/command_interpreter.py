# command_interpreter.py
# Date: 1/11/24
# Author: Rebecca Blum
# 
# Revisions: 
#     [name]     [date]     [notes]
#     R. Blum    1/11/24    initial script creation 
#
# Summary:
#     
#
# Inputs:
#
# Outputs:
#
#------------------------------------------------------------------------------
# import packages and library 
import argparse
import sys
# 
def func(input,output):

    if int(input[0:6],base=2) == 1:
        # bootgnss
        # send cmd to gnss reciever to boot it?
        print(2)

    elif int(input[0:6],base=2) == 2:
        # bootrpi
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

def main():
    #input = '0b' + '0101' + '001100' + '110000'
    #input = '0b' + '0100' + '00111' + '11111'

    input = sys.argv
    #input = '0b' + '0001' + '0011'
    cmd = '0b' + input[1]
    
    #print('0b'+cmd)
    #[None]*7
    #output = ["freq", "max_el", "min_el", "max_az", "min_az","calibration","time_res"]
    
    output = [None]*7

    f = open("setvars.txt", "r")
    with open("setvars.txt") as fh:
        i = 0
        for line in fh:
            output[i] = line.strip("\n")
            i = i + 1

    bla = func(cmd,output)

    f = open("setvars.txt", "r+")
    for item in bla:
        f.write(str(item) + "\n")
    f.close()

if __name__ == "__main__":
    main()
