import serial
# establish da serial connection *sunglasses emoji*
ser = serial.Serial("/dev/ttyUSB0", 115200)

# this would be a user input sampling frequency (defined as outputs per
	# N fixes, with one fix per second)
freq_input = 5

# function to tell receiver to output certain messages at certain rates
def changeFreq(freq):
	# protocol: msg = "$PAIR062,message type, outputs per N fixes*checksum value\r\n"

	# 0 = GGA: want this (one per message)
	msgGGA = "$PAIR062,0,freq*3B\r\n" # what is the \r doing here ?
	msgGGA = msgGGA.encode('ascii')
	ser.write(msgGGA)
	# 1 = GLL
	msgGLL = "$PAIR062,1,0*3F\r\n"
	msgGLL = msgGLL.encode('ascii')
	ser.write(msgGLL)
	# 2 = GSA
	msgGSA = "$PAIR062,2,0*3C\r\n"
	msgGSA = msgGSA.encode('ascii')
	ser.write(msgGSA)
	# 3 = GSV: want this (one per 4 satellites per message)
	msgGSV = "$PAIR062,3,freq*38\r\n"
	msgGSV = msgGSV.encode('ascii')
	ser.write(msgGSV)
	# 4 = RMC
	msgRMC = "$PAIR062,4,0*3A\r\n"
	msgRMC = msgRMC.encode('ascii')
	ser.write(msgRMC)
	# 5 = VTG
	msgVTG = "$PAIR062,5,0*3B\r\n"
	msgVTG = msgVTG.encode('ascii')
	ser.write(msgVTG)
	# 6 = ZDA
	msgZDA = "$PAIR062,6,0*38\r\n"
	msgZDA = msgZDA.encode('ascii')
	ser.write(msgZDA)
	# 7 = GRS
	msgGRS = "$PAIR062,7,0*39\r\n"
	msgGRS = msgGRS.encode('ascii')
	ser.write(msgGRS)
	# 8 = GST
	msgGST = "$PAIR062,8,0*36\r\n"
	msgGST = msgGST.encode('ascii')
	ser.write(msgGST)

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
