# import os
# from rockBLOCK_functions import *
from common_functions import *
# import time
from nmea2dino import nmea2dino
from reflector_height import reflector_height
from datetime import datetime
# import serial 


'''
heights = [3, None, 2]

h = ''
for item in heights: 
	h = h + str(item) + ","
			
height_file = "/home/velociraptor/two_hour_lifecycle_test/heights.txt"
f = open(height_file, "r+")
f.write(h + "\n")
f.close()
		
# check system health 
# bat_level, temperature = sys_health(TRX_ser)
bat_level = 50
temperature = 40

# get system time (OR OUTPUT IT FROM ref_height) % should be output from reflector_height
# so that if there are multiple hights, they have induvidual times
now = datetime.now()
end_time = now.strftime("%Y/%j-%H:%M:%S")
		
# send string to ground station 
message = str(end_time) + ";B=" + str(bat_level) + ";T=" + str(temperature) + ";H=" + str(h)
#send_string(message,TRX_ser)
print(message)
'''
'''longitude = "ahh"
latitude = "oop"

data = '$GNGGA, 212030.000, 4000.583620, N, 10514.621424, W, 1, 19, 1.01, 1633.165, M, -20.634, M, , *79'
GGA_line = data.split(",")
print("gga line = ", GGA_line)
latitude = GGA_line[2] + GGA_line[3]
print("latitude = ", latitude)
longitude = GGA_line[4] + GGA_line[5]
print("longitude = ", longitude)
message = "long=" + str(longitude) + ",lat=" + str(latitude) # + ",B=" + bat_level + ",T=" + temperature
# filename = "/home/velociraptor/two_hour_lifecycle_test/long_lat.txt"
# ~ write_file(message,filename)


# ~ long_lat = read_file(filename)
# ~ print(long_lat[0])



# m essage = "long=" + str(longitude) + ",lat=" + str(latitude) # + ",B=" + bat_level + ",T=" + temperature
'''

'''print(message)
filename = "/home/velociraptor/two_hour_lifecycle_test/long_lat.txt"
f = open(filename, "r+")
f.truncate()
f.write(message + "\n")
f.close()
'''
'''
# ''
# # time.sleep(60)
# # message = check_mail() 
# #variable = os.environ.get("TESTVARY")
# #print(variable)

# '''
# #f = open('/home/velociraptor/raptor_test/test_file.txt', "w")
# #f.write(message)
# #f.close() 

# '''
#  write_file(message,'/home/velociraptor/raptor_test/test_file.txt')

dinofile = "current_dino.csv"
nmea2dino("nmea_files/nmea_file_10.txt","current_dino.csv")


print("ahhh")
min_az= 90
max_az = 270
min_el = 5
max_el = 25
t_res = 2
#dinofile = '/home/velociraptor/two_hour_lifecycle_test/current_dino.csv'
reflH = reflector_height(dinofile, min_az, max_az, min_el, max_el, t_res)
print("Average ref height, no dynamic correction = ", reflH)
'''
# '''
# USBs = read_file('/home/velociraptor/two_hour_lifecycle_test/serial_connections.txt')

# # Make serial connections
# GNSS_ser = serial.Serial("/dev/ttyUSB" + USBs[0], 115200)
# TRX_ser = serial.Serial('/dev/ttyUSB' + USBs[1],  19200)
# # message = check_mail(TRX_ser)
# # print(message)

# from receiver_functions import *
# get_lon_lan(GNSS_ser,TRX_ser)

# #time.sleep(20)
# #message2 = check_mail(TRX_ser)
# #print(message2)
# ~ import time
# ~ n = 0

# ~ # from_read_nmea()
# ~ while n < 50:
	# ~ print("hi")
	# ~ time.sleep(3)
	# ~ n = n+1
#mea2dino("nmea_file_11.txt", "testdino.csv")
