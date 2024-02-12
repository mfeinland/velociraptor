import serial
import numpy as np
from receiver_functions import generateMsg, changeFreq

# establish da serial connection *sunglasses emoji*
ser = serial.Serial("/dev/ttyUSB0", 115200)

# this would be a user input sampling frequency (defined as outputs per
	# N fixes, with one fix per second)
freq_input = 5
changeFreq(freq_input)

# opens text file
f = open("sample_nmea.txt", "wb")

# reads lines of nmea data, writes to file, prints lines
samplevariable = 0
while samplevariable < 20:
	data = ser.readline()
	f.write(data)
	line = ser.readline().decode('utf-8').rstrip()
	print(line)
	samplevariable = samplevariable + 1
f.close()
