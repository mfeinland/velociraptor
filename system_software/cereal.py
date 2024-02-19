# establishes da serial connection
# ser needs to be saved as environmental variable
import serial 
ser = serial.Serial("/dev/ttyUSB0", 115200)
