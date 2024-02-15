# functions used by GNSS receiver
import serial
import numpy as np

# genrate NMEA message wth checksum
def generateMsg(typ, freq):
    # takes in NMEA message type (options 1-8) and number of messages per N fixes (options 1-20)
    # returns complete NMEA message with checksum
    sentence = "PAIR062," + str(typ) + "," + str(freq)
    csum = 0
    for char in sentence:
        csum ^= ord(char)
    checksum_hex = hex(csum)[2:].upper()
    checksum = checksum_hex.zfill(2)

    # generate message for receiver
    return f"${sentence}*{checksum}\r\n"

# function to tell receiver to output certain messages at certain rates
def changeFreq(freq, ser):
	# takes in desired sampling frequency and name of serial connection
	
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