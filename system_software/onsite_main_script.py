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

#from nmea2dino import nmea2dino
#from ops_functions import calibration_cycle, sys_health, check_mail

###############################################################################
# Functions 

def calibration_cycle(GNSS_ser, TRX_ser, bat_level, temperature, start_t,  file_number, t):
	N = 18 # 18*5 = 90 mins
	# -30 minute to prevent overlap in cron call and allow send_string to complete
	delta = timedelta(minutes=60)

	# get longitude and latitude from NMEA file 
	flag = 0
	while flag == 0: # flag is down
		# read in nmea lines
		data = GNSS_ser.readline()

		if re.search("GGA", data): # line contains long/lat (GLL -- Geographic Position - Longitude/Latitude) GGA
			flag = 1 # flag goes up
			GGA_line = data.split(", ")
			latitude = GGA_line[2] + GGA_line[3]
			longitude = GGA_line[4] + GGA_line[5]

            # send back longitude, latitude, battery health, and sys temp 
			message = "long=" + str(longitude) + ",lat=" + str(latitude) + ",B=" + bat_level + ",T=" + temperature
			send_string(message)

	while datetime.now() <= (start_t + delta):
        # check inbox
		command = check_mail()
		if command == "None":
			time.sleep(5*60) # 5 mins
		else: # execute commands
			freq, min_el, max_el, min_az, max_az, mode, temporal_res = command_interpreter(command)
			if mode == 'normal':
				normal_ops(TRX_ser, min_az, max_az, min_el, max_el, file_number, t)
			else:
				time.sleep(5*60) # 5 mins

def normal_ops(TRX_ser, min_az, max_az, min_el, max_el, file_number):
#	time res idea: read in all available files? divide number of files by 
    # 	number of desired blocks  
	#read_nmea(ser, dataAmount) # occurs via cron 
	path = '/home/velociraptor/raptor_test/'
	dinofile = 'dino.csv'

	nmea2dino(path +'nmea_files/nmea_file_' + str(file_number) + '.txt')
	heights = reflector_height(path + dinofile, min_az, max_az, min_el, max_el)
    
    # check system health 
	bat_level, temperature = sys_health(TRX_ser)
	
	# get system time (OR OUTPUT IT FROM ref_height) % should be output from reflector_height
	# so that if there are multiple hights, they have induvidual times
	now = datetime.now()
	end_time = now.strftime("%Y/%j-%H:%M:%S")
	
    # send string to ground station 
	message = end_time + ";B=" + bat_level + ";T=" + temperature + ";H=" + heights
	send_string(message)

###########################################
# Main function 
def main():
	#t = get_time(GNSS_ser) # need to set time somehow
	t = datetime.now()
	start_t = t.strftime("%Y/%j-%H:%M:%S") 
	minutes_since_midnight = int(t.strftime("%H"))*60 + int(t.strftime("%M")) 
	file_number = np.floor(minutes_since_midnight/90)

	USBs = read_file('setvars.txt')

	# Make serial connections
	GNSS_ser = serial.Serial("/dev/ttyUSB" + USBs[0], 115200)
	TRX_ser = serial.Serial('/dev/ttyUSB' + USBs[1],  19200)

    # Check mailbox 
	command = check_mail() # 0 if no mail
	if command != 0:
		freq, min_el, max_el, min_az, max_az, mode, temporal_res = command_interpreter(command)

	else:
		set_vars = read_file('setvars.txt')
		freq = set_vars[0]
		min_el = set_vars[1]
		max_el = set_vars[2] # [9,17] 
		min_az = set_vars[3] 
		max_az = set_vars[4] # [270, 360]
		mode = set_vars[5]
		temporal_res = set_vars[6]

	# check system health 
	bat_level, temperature = sys_health(TRX_ser)
	
	# if in calibration mode, run every 5 mins until n = N (so it stops in >1.5 hours)
	if mode == 'calibration':
		calibration_cycle(GNSS_ser, TRX_ser, bat_level, temperature, start_t, file_number, t)

	else: #normal ops (need to implement time resolution)
		normal_ops(TRX_ser, min_az, max_az, min_el, max_el, file_number)

if __name__ == "__main__":
    main()
