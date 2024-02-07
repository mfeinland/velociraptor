import serial
# establish da serial connection *sunglasses emoji*
ser = serial.Serial("/dev/ttyUSB0", 115200)

# tell receiver to output certain messages at certain rates
msg = "$PAIR062,5,1*3A\r\n"
msg = msg.encode('ascii')
# print(msg)
ser.write(msg)
var = 0
while var < 100:
	line = ser.readline().decode('utf-8').rstrip()
	print(line)
	# print('\n')
	var += 1
