# onsite_main_script.py
# Date: 2/10/24
# Author: Rebecca Blum
# 
# Revisions: 
#   [name]       [date]       [notes]
#   R. Blum      2/10/24      initial script creation 
#
# Summary: 
#     @reboot /path/to/the/script arguments
#
# Inputs:
#   [] 
#
# Outputs: 
#   []
#
# Limitations: 
#   
#
# Future edits: 
#   [issue]                               [status]                    [name]
#   
#
#------------------------------------------------------------------------------
#
# Import Packages and Libraries 
from datetime import datetime, timedelta
import re
import sys, os # maybe not os if we turn cmd interpreter into function
from common_functions import *
import time
from receiver_functions import *
from reflector_height import reflector_height
from rockBLOCK_functions import *
from nmea2dino import nmea2dino
import serial
import threading
# from get_nmea import get_nmea
# from test import test
from onsite_main_script import *


#from nmea2dino import nmea2dino
#from ops_functions import calibration_cycle, sys_health, check_mail

###############################################################################
# Functions 

def onsite_main():
	

	def calibration_cycle(GNSS_ser, TRX_ser, bat_level, temperature, start_t,  file_number, t, t_res):
		#N = 18 # 18*5 = 90 mins
		# -30 minute to prevent overlap in cron call and allow send_string to complete
		delta = timedelta(minutes=60)

		while datetime.now() <= (start_t + delta):
			# check inbox
			command = check_mail(TRX_ser)
			if command == "None":
				time.sleep(5*60) # 5 mins
			else: # execute commands
				freq, min_el, max_el, min_az, max_az, mode, temporal_res = command_interpreter(command, TRX_ser, GNSS_ser)
				if mode == 'normal':
					normal_ops(TRX_ser, min_az, max_az, min_el, max_el, file_number, t_res)
				else:
					time.sleep(5*60) # 5 mins

	def normal_ops(TRX_ser, min_az, max_az, min_el, max_el, file_number,t_res):
	#	time res idea: read in all available files? divide number of files by 
		# 	number of desired blocks  
		#read_nmea(ser, dataAmount) # occurs via cron 
		path = '/home/velociraptor/two_hour_lifecycle_test/'
		dinofile = 'current_dino.csv'
		
		date_time = datetime.now()
		year_doy = date_time.strftime("%Y_%j_")
		
		print("running nmea2dino")
		nmea2dino(path +'nmea_files/nmea_file_' + year_doy + str(file_number) + '.txt', path + dinofile)

		#nmea2dino(path +'nmea_files/nmea_file_' + str(file_number) + '.txt', path + dinofile)
		#nmea2dino(path +'nmea_files/test.txt')
		print("calculating reflector height")
		#send_string("Calculating reflector height rn", TRX_ser)
		
		try:
			heights = reflector_height(path + dinofile, min_az, max_az, min_el, max_el, t_res)
		except:
			heights = ["couldn't resolve height"]

		h = ""
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
		print(end_time)


		time.sleep(60)
		send_string("hellooooo", TRX_ser)


		time.sleep(60)
        #print("wooooooooorkk")
		# send string to ground station 
		message = str(end_time) + ";B=" + str(bat_level) + ";T=" + str(temperature) + ";H=" + str(h)
		send_string(message,TRX_ser)
        #print("ahhhhhhhggggg")

	###########################################
	# Main function 

	#t = get_time(GNSS_ser) # need to set time somehow
	t = datetime.now()
	start_t = t.strftime("%Y/%j-%H:%M:%S") 
	print(start_t)
	minutes_since_midnight = int(t.strftime("%H"))*60 + int(t.strftime("%M")) 
	file_number = int(np.floor(minutes_since_midnight/90))

	if file_number == 0:
		file_number = int(16)

	USBs = read_file('/home/velociraptor/two_hour_lifecycle_test/serial_connections.txt')
	path = '/home/velociraptor/two_hour_lifecycle_test/'

	print("line 127, making serial connections")
	# Make serial connections
	GNSS_ser = serial.Serial("/dev/ttyUSB" + USBs[0], 115200)
	TRX_ser = serial.Serial('/dev/ttyUSB' + USBs[1],  19200)
	
	long_lat_file = "/home/velociraptor/two_hour_lifecycle_test/long_lat.txt"
	
	print("Sleeping while longitude and latitude are retrieved")
	time.sleep(2*60)
	
	print("not sending back longitude and latitude")
	#long_lat = read_file(long_lat_file)
	#send_string(long_lat[0], TRX_ser)
	
	#time.sleep(60)
	
	#print("setfreq")
	#setFreq(GNSS_ser, 5, [0,3])

	# Check mailbox 
	command = check_mail(TRX_ser) # 0 if no mail
	print("check mail")
	if command != "None":
		print("doing command interpreter")
		freq, min_el, max_el, min_az, max_az, mode, t_res = command_interpreter(command, TRX_ser, GNSS_ser)

	else:
		print("doing set_vars")
		set_vars = read_file(path + 'setvars.txt')
		freq = set_vars[0]
		min_el = int(set_vars[1])
		max_el = int(set_vars[2]) # [9,17] 
		min_az = int(set_vars[3]) 
		max_az = int(set_vars[4]) # [270, 360]
		mode = set_vars[5]
		t_res = int(set_vars[6])

	# check system health 
	# bat_level, temperature = sys_health(TRX_ser)
	bat_level = 50
	temperature = 40
	cur_str = "Commencing normal ops; az1 = " + str(min_az) + ", az2 = " + str(max_az)
	print(cur_str)
	# send_string(cur_str, TRX_ser)
	
	# if in calibration mode, run every 5 mins until n = N (so it stops in >1.5 hours)
	if mode == 'calibration':
		print("doing calibration")
		calibration_cycle(GNSS_ser, TRX_ser, bat_level, temperature, start_t, file_number, t, t_res)

	else: #normal ops (need to implement time resolution)
		print("doing normal ops")
		normal_ops(TRX_ser, min_az, max_az, min_el, max_el, file_number, t_res)
		
def get_nmea():
	USBs = read_file('/home/velociraptor/two_hour_lifecycle_test/serial_connections.txt')

	# Make serial connections
	GNSS_ser = serial.Serial("/dev/ttyUSB" + USBs[0], 115200)
	TRX_ser = serial.Serial('/dev/ttyUSB' + USBs[1],  19200)

	print(GNSS_ser)
	print(TRX_ser)
	
	t = datetime.now()
	
	get_lon_lan(GNSS_ser,TRX_ser)

	# send_string("Beginning ops", TRX_ser)

	read_nmea(GNSS_ser, t)
		

if __name__ == "__main__":
	t1 = threading.Thread(target=get_nmea)
	t2 = threading.Thread(target=onsite_main)
	
	t1.start()
	t2.start()
	
	t1.join()
	t2.join()
