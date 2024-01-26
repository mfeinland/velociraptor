import serial
# establish da serial connection *sunglasses emoji*
ser = serial.Serial("/dev/ttyUSB0", 115200)

# idk what this does
ser.write(bytearray('S', 'ascii'))

f = open("sample_nmea.txt", "w")

samplevariable = 0
while samplevariable < 10:
	data = ser.readline()
	f.write(str(data))
	samplevariable = samplevariable + 1
f.close()
