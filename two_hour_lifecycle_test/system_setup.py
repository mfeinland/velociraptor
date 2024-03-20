## Imports and libraries 
from common_functions import *
import sys 
import re
import serial
from receiver_functions import *

#-------------------------------------------------------------
## Functions

#-------------------------------------------------------------
## Main function 
def main(): 
    # Grab system input to script
    sys_args = sys.argv 

    arg =' '.join(sys_args[1:])
    usb_connections = arg.split("[") #print(stuff) #usb_connections = stuff[1:] #print(usb_connections)

    path = '/home/velociraptor/two_hour_lifecycle_test/'
    USBs = ['None','None']

    # set mode to calibration
    #s et_vars = read_file(path + 'setvars.txt')
    # set_vars[5] = 'calibration'
    #write_file(set_vars,path + 'setvars.txt')

    for item in usb_connections:
        if re.search("ttyUSB", item):
            thing = item.split('ttyUSB')

            if re.search("cp210x",thing[0]): # cp210x (GNSS receiver)
                print("cp210x is connected to ttyUSB" + thing[1])
                USBs[0] = thing[1].strip() # GNSS_usb
                GNSS_ser = serial.Serial("/dev/ttyUSB" + USBs[0], 115200)

            if re.search("FTDI",thing[0]): # FTDI (transceiver)
                print("FTDI is connected to ttyUSB" + thing[1])
                USBs[1] = thing[1].strip() # TRX_usb
                TRX_ser = serial.Serial('/dev/ttyUSB' + USBs[1],  19200)
                
    # get time from GNSS
    t = 1 # get_time(GNSS_ser) 

    write_file(USBs, path + 'serial_connections.txt')
    # send_string("Connection between RPI and TRX is successful")

    sys.exit(t)

if __name__ == "__main__":
    main()
