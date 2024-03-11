## Imports and libraries 
from common_functions import *
import sys
#import serial 
import re

#-------------------------------------------------------------
## Functions 


#-------------------------------------------------------------
## Main function 
def main(): 
 	# Grab system input to script
    #sys_args = sys.argv
    input = "cp210x now attached to ttyUSB0\nFTDI now attached to ttyUSB1" # sys_args[1] 

    # set mode to calibration
    '''set_vars = read_file('setvars.txt')
    set_vars[5] = 'calibration'
    write_file(set_vars, "setvars.txt")'''

    usb_connections = input.split("\n")
    print(usb_connections)
    
    # cp210x (GNSS receiver)
    # FTDI (transceiver)
    #txt = "cp210x now attached to ttyUSB0"
    for item in usb_connections:
        thing = item.split('ttyUSB')

        x = re.search("cp210x",thing[0])
        if x:
            print("cp210x is connected to ttyUSB" + str(thing[1]))
            GNSS_usb = str(thing[1])

        x = re.search("FTDI",thing[0])
        if x:
            print("FTDI is connected to ttyUSB" + str(thing[1]))
            TRX_usb = str(thing[1])

    #GNSS_ser = serial.Serial("/dev/ttyUSB" + GNSS_usb, 115200)
    #TRX_ser = serial.Serial("/dev/ttyUSB" + TRX_usb,  19200)
            
    # get time from GNSS 

if __name__ == "__main__":
    main()