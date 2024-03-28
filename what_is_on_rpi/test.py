import os
from rockBLOCK_functions import *
from common_functions import *
import time
from nmea2dino import nmea2dino
from reflector_height import reflector_height
import serial 

'''
# time.sleep(60)
# message = check_mail() 
#variable = os.environ.get("TESTVARY")
#print(variable)

'''
#f = open('/home/velociraptor/raptor_test/test_file.txt', "w")
#f.write(message)
#f.close() 

'''
# write_file(message,'/home/velociraptor/raptor_test/test_file.txt')
#nmea2dino("nmea_files/nmea_file_9.txt")
dinofile = "dino_copy.csv"
min_az= 90
max_az = 270
min_el = 5
max_el = 25
t_res = 2
heights = reflector_height(dinofile, min_az, max_az, min_el, max_el, t_res)
print("heights = ", heights)

'''
USBs = read_file('/home/velociraptor/two_hour_lifecycle_test/serial_connections.txt')

# Make serial connections
#GNSS_ser = serial.Serial("/dev/ttyUSB" + USBs[0], 115200)
TRX_ser = serial.Serial('/dev/ttyUSB' + USBs[1],  19200)
message = check_mail(TRX_ser)
print(message)

time.sleep(20)
message2 = check_mail(TRX_ser)
print(message2)
