# functions used by GNSS receiver
import serial
import numpy as np
from datetime import datetime, timedelta

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
def setFreq(GNSS_ser, desired_freq, nmea_types):
    '''
    Takes in desired sampling frequency and name of serial connection.
    Last modified: 3/17/24 by Max
    The sampling frequency is given as inverse Hz. So, a freq of 5 means 0.2 Hz.
    The nmea_types are as follows:
    0 = GGA
    1 = GLL
    2 = GSA
    3 = GSV
    4 = RMC
    5 = NVTG
    6 = ZDA
    7 = GRS
    8 = GST
    '''
    all_freqs = np.arange(0, 9)
    for n in all_freqs:
        print('n = ', n)
        if n in nmea_types:
            freq = desired_freq
        else:
            freq = 0
        sentence = "PAIR062," + str(n) + "," + str(freq)
        chksum = genChksum(sentence)
        msg = f"${sentence}*{chksum}\r\n"
        msg = msg.encode('ascii')
        print('msg = ', msg)
        GNSS_ser.write(msg)
			
# function to read the nmea data from the receiver and write to .txt file
def read_nmea(GNSS_ser, date_time):
	# input: name of serial connection with devboard/PCB (this will be an environmental variable).
	#        dataAmount determines how much data to collect and save to .txt file (currently
	#        specified as number of lines but need to change to time or something)
	path = '/home/velociraptor/raptor_test/nmea_files' 

	# Determine file name (out of 16 daily files which cover 90 minutes each)
	minutes_since_midnight = int(date_time.strftime("%H"))*60 + int(date_time.strftime("%M")) 
	start_t = date_time.strftime("%Y/%j-%H:%M:%S")
	file_number = np.ceil(minutes_since_midnight/90)
	delta = timedelta(minutes=89) # -1 minute to prevent overlap in cron call
	
	# data will be written to this .txt file
	f = open(path + "nmea_file_" + str(file_number) + ".txt", "wb")
	
	#line = 0 # potential change: make this dependent on time not number of lines. Change made!
	freq_change_count = 0 

	while datetime.now() <= (date_time + delta):
		data = GNSS_ser.readline()
		f.write(data)
		# messages that the receiver can send back:
		if data == b'$PAIR001,062,0*3F\r\n':
			freq_change_count += 1
			print('freq change count = ', freq_change_count)
			#if freq_change_count == 9:
				# output frequency change has been received for all 9 message types (0-8)
			#	print('Output frequency change has been sent to receiver for all 9 message types ')
		# frequency change error messages
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
		# line += 1
	
def get_time(GNSS_ser):
    # tell GNSS reciever to output ZDA nmea messages
	freq = 1
	setFreq(GNSS_ser, freq, [2]) # this is not a 2!!!
	flag = 0
	while flag == 0: # flag is down
        # read in nmea lines until we come across a ZDA
		line = GNSS_ser.readline()# if line contains time nmea (ZDA - SiRF Timing Message) 
		#line = '$GPZDA,181813,14,10,2003,00,00*4F'
		if re.search("ZDA", line):
			flag = 1 # flag goes up
			zda = line.split(",")
			t = datetime( int(zda[4]), int(zda[3]), int(zda[2]), int(zda[1][0:2]), int(zda[1][2:4]), int(zda[1][4:]))
			t = t.strftime("%d %b %Y %H:%M:%S") # "12 FEB 2024 00:00:00" 
			setFreq(GNSS_ser, 0, [2])
	return t    