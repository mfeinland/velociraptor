import serial
import numpy as np
# establish da serial connection between RPi and GNSS receiver *sunglasses emoji*
ser = serial.Serial("/dev/ttyUSB0", 115200)

# this would be a user input sampling frequency (defined as outputs per
	# N fixes, with one fix per second)
freq_input = 5

def generateMsg(type, freq):
    # takes in NMEA message type (options 1-8) and number of messages per N fixes (options 1-20)
    # returns complete NMEA message with checksum
    sentence = "PAIR062," + str(type) + "," + str(freq)
    csum = 0
    for char in sentence:
        csum ^= ord(char)
    checksum_hex = hex(csum)[2:].upper()
    checksum = checksum_hex.zfill(2)

    # generate message for receiver
    return f"${sentence}*{checksum}"
	# original devSetup had "$PAIR062,type,freq*checksum\r\n"
	# check sure if \r and \n are necessary

# function to tell receiver to output certain messages at certain rates
def changeFreq(freq):
	# protocol: msg = "$PAIR062,message type,outputs per N fixes*checksum value\r\n"

	# 0 = GGA: want this (one per message)
	msgGGA = generateMsg(0, freq)
	msgGGA = msgGGA.encode('ascii')
	ser.write(msgGGA)
	# 1 = GLL
	msgGLL = generateMsg(1, 0)
	msgGLL = msgGLL.encode('ascii')
	ser.write(msgGLL)
	# 2 = GSA
	msgGSA = generateMsg(2, 0)
	msgGSA = msgGSA.encode('ascii')
	ser.write(msgGSA)
	# 3 = GSV: want this (one per 4 satellites per message)
	msgGSV = generateMsg(3, freq)
	msgGSV = msgGSV.encode('ascii')
	ser.write(msgGSV)
	# 4 = RMC
	msgRMC = generateMsg(4, 0)
	msgRMC = msgRMC.encode('ascii')
	ser.write(msgRMC)
	# 5 = VTG
	msgVTG = generateMsg(5, 0)
	msgVTG = msgVTG.encode('ascii')
	ser.write(msgVTG)
	# 6 = ZDA
	msgZDA = generateMsg(6, 0)
	msgZDA = msgZDA.encode('ascii')
	ser.write(msgZDA)
	# 7 = GRS
	msgGRS = generateMsg(7, 0)
	msgGRS = msgGRS.encode('ascii')
	ser.write(msgGRS)
	# 8 = GST
	msgGST = generateMsg(8, 0)
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
