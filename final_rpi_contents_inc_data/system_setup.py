## Imports and libraries 
from common_functions import *
import sys 
import re
import serial
from receiver_functions import *
from datetime import datetime

#-------------------------------------------------------------
## Important! DONT HAVE ANYTHING PRINTED OUT EXCEPT FOR t
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
    # set_vars = read_file(path + 'setvars.txt')
    # set_vars[5] = 'calibration'
    # write_file(set_vars,path + 'setvars.txt')

    for item in usb_connections:
        if re.search("ttyUSB", item):
            thing = item.split('ttyUSB')

            if re.search("cp210x",thing[0]): # cp210x (GNSS receiver)
                USBs[0] = thing[1].strip() # GNSS_usb
                GNSS_ser = serial.Serial("/dev/ttyUSB" + USBs[0], 115200)

            if re.search("FTDI",thing[0]): # FTDI (transceiver)
                USBs[1] = thing[1].strip() # TRX_usb
                TRX_ser = serial.Serial('/dev/ttyUSB' + USBs[1],  19200)

    write_file(USBs, path + 'serial_connections.txt')
    
    #send_string("getting time", TRX_ser)
    
    # Get time from GNSS
    #if USBs[0] != 'None':
    #    t = get_time(GNSS_ser)
    #    print(t)
    #else:
    #    t = datetime.now()
    #    print(t)
    #send_string("time is: " + str(t), TRX_ser)
    
    # Signal that operations have started 
#    if USBs[1] != 'None':
#        send_string("Beginning ops", TRX_ser)

        #message = check_mail(TRX_ser)

        #time.sleep(20)
        #message2 = check_mail(TRX_ser)

#    if USBs[0] != 'None':
#        get_lon_lan(GNSS_ser,TRX_ser)

    t = "1 Apr 2024 00:01:00"

    sys.exit(t)
    
if __name__ == "__main__":
    main()
