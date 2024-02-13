import serial
import numpy as np
from receiver_functions import generateMsg, changeFreq

# establish da serial connection *sunglasses emoji*
ser_name = serial.Serial("/dev/ttyUSB0", 115200)

# user input sampling frequency
freq_input = 4
changeFreq(freq_input, ser_name)

f = open("devSetup_nmea.txt", "wb")

var = 0
while var < 20:
	data = ser_name.readline()
	f.write(data)
	print_line = data.decode('utf-8').rstrip()
	print(print_line)
	var += 1
