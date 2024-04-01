from receiver_functions import *
import serial
from datetime import datetime
from rockBLOCK_functions import *
from common_functions import *

USBs = read_file('/home/velociraptor/two_hour_lifecycle_test/serial_connections.txt')

# Make serial connections
GNSS_ser = serial.Serial("/dev/ttyUSB" + USBs[0], 115200)
TRX_ser = serial.Serial('/dev/ttyUSB' + USBs[1],  19200)

print(GNSS_ser)
print(TRX_ser)

#send_string("Beginning ops", TRX_ser)

t = datetime.now()

read_nmea(GNSS_ser, t)
