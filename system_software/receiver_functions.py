# functions used by GNSS receiver
import serial
import numpy as np

# function to establish da serial connection (used for testing purposes, will not be used for actual system
def cereal_func():
    ser = serial.Serial("/dev/ttyUSB0", 115200)
    return ser

# function to generate NMEA message with checksum
def genChksum(sentence):
    # takes in sentence without checksum and returns checksum
    csum = 0
    for char in sentence:
        csum ^= ord(char)
    checksum_hex = hex(csum)[2:].upper()
    checksum = checksum_hex.zfill(2)
    return checksum

# function to tell receiver to output certain messages at certain rates
def setFreq(ser, desired_freq):
	# takes in desired sampling frequency and name of serial connection
	for n in range(9):
		typ = n
		print('n = ', n)
		if (typ == 0) or (typ == 3): # want GGA and GSV
			freq = desired_freq
			sentence = "PAIR062," + str(typ) + "," + str(freq)
		else:
			freq = 0
			sentence = "PAIR062," + str(typ) + "," + str(freq)
		chksum = genChksum(sentence)
		msg = f"${sentence}*{chksum}\r\n"
		msg = msg.encode('ascii')
		print('msg = ', msg)
		ser.write(msg)
		typ += 1
			
# function to read the nmea data from the receiver and write to .txt file
def read_nmea(ser, dataAmount):
	# input: name of serial connection with devboard/PCB (this will be an environmental variable).
		# dataAmount determines how much data to collect and save to .txt file (currently
		# specified as number of lines but need to change to time or something)
		
	# data will be written to this .txt file
	f = open("nmea.txt", "wb")
	
	line = 0 # potential change: make this dependent on time not number of lines
	freq_change_count = 0 
	while line < dataAmount:
		data = ser.readline()
		f.write(data)
		# messages that the receiver can send back:
		if data == b'$PAIR001,062,0*3F\r\n':
			freq_change_count += 1
			print('freq change count = ', freq_change_count)
			if freq_change_count == 9:
				# output frequency change has been received for all 9 message types (0-8)
				print('Output frequency change has been sent to receiver for all 9 message types ')
		# error messages
		elif data == b'$PAIR001,062,1*3E\r\n':
			print('Frequency change command is being processed. Please wait for the result.')
		elif data == b'$PAIR001,062,2*3D\r\n':
			print('Frequency change command sending failed.')
		elif data == b'$PAIR001,062,3*3C\r\n':
			print('Frequency change command ID is not supported')
		elif data == b'$PAIR001,062,4*3B\r\n':
			print('Frequency change command parameter error. Out of range/Some parameters were lost/Checksum error.')
		elif data == b'$PAIR001,062,5*3A\r\n':
		# potential addition: other error messages ?
			print('MNL service for frequency change command is busy. You can try again soon.')
		else:
			print(data.decode('utf-8').rstrip())
		line += 1
	
