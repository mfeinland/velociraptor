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

	nmea2dino(path +'nmea_files/nmea_file_' + str(file_number) + '.txt', path + dinofile)
	#nmea2dino(path +'nmea_files/test.txt')
	
	heights = reflector_height(path + dinofile, min_az, max_az, min_el, max_el, t_res)
	
	for item in heights: 
		h = h + str(item) + ","
	
    # check system health 
	#bat_level, temperature = sys_health(TRX_ser)
	bat_level = "20"
	temperature = "30"
	
	# get system time (OR OUTPUT IT FROM ref_height) % should be output from reflector_height
	# so that if there are multiple hights, they have induvidual times
	now = datetime.now()
	end_time = now.strftime("%Y/%j-%H:%M:%S")
	
    # send string to ground station 
	message = str(end_time) + ";B=" + str(bat_level) + ";T=" + str(temperature) + ";H=" + str(h)
	send_string(message,TRX_ser)

###########################################
# Main function 
def main():
	#t = get_time(GNSS_ser) # need to set time somehow
	t = datetime.now()
	start_t = t.strftime("%Y/%j-%H:%M:%S") 
	minutes_since_midnight = int(t.strftime("%H"))*60 + int(t.strftime("%M")) 
	file_number = int(np.floor(minutes_since_midnight/90))
	if file_number == 0:
		file_number = int(16)

	USBs = read_file('/home/velociraptor/two_hour_lifecycle_test/serial_connections.txt')
	path = '/home/velociraptor/two_hour_lifecycle_test/'

	# Make serial connections
	GNSS_ser = serial.Serial("/dev/ttyUSB" + USBs[0], 115200)
	TRX_ser = serial.Serial('/dev/ttyUSB' + USBs[1],  19200)
	
	setFreq(GNSS_ser, 5, [0,3])

    # Check mailbox 
	command = "None" #check_mail(TRX_ser) # 0 if no mail
	if command != "None":
		freq, min_el, max_el, min_az, max_az, mode, t_res = command_interpreter(command, TRX_ser, GNSS_ser)

	else:
		set_vars = read_file(path + 'setvars.txt')
		freq = set_vars[0]
		min_el = int(set_vars[1])
		max_el = int(set_vars[2]) # [9,17] 
		min_az = int(set_vars[3]) 
		max_az = int(set_vars[4]) # [270, 360]
		mode = 'Normal' #set_vars[5]
		t_res = int(set_vars[6])

	# check system health 
	#bat_level, temperature = sys_health(TRX_ser)
	bat_level = 20
	temperature = 40
	
	# if in calibration mode, run every 5 mins until n = N (so it stops in >1.5 hours)
	if mode == 'calibration':
		calibration_cycle(GNSS_ser, TRX_ser, bat_level, temperature, start_t, file_number, t, t_res)

	else: #normal ops (need to implement time resolution)
		normal_ops(TRX_ser, min_az, max_az, min_el, max_el, file_number, t_res)

if __name__ == "__main__":
    main()
