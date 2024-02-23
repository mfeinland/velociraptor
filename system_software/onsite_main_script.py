# onsite_main_script.py
# Date: 2/10/24
# Author: Rebecca Blum
# 
# Revisions: 
#   [name]       [date]       [notes]
#   R. Blum      2/10/24      initial script creation 
#
# Summary: 
#     
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
import re
import sys, os # maybe not os if we turn cmd interpreter into function
from common_functions import read_file, write_file
import time
from receiver_functions import read_nmea, cereal_func
#from ops_functions import calibration_cycle, sys_health, check_mail

###############################################################################
# Functions 

def calibration_cycle(ser, bat_level, temperature):
	N = 18 # 18*5 = 90 mins
	for n in range(0,N):
		if n == 0: # send back longitude, latitude, battery health, and sys temp
			# get longitude and latitude from NMEA file 
			flag = 0
			while flag == 0: # flag is down
				# read in nmea lines
				data = ser.readline()
				# if line contains long/lat (GLL -- Geographic Position - Longitude/Latitude) GGA
				check = re.search("GGA", data)
				if check:
					flag = 1 # flag goes up
					GGA_line = data.split(", ")
					latitude = GGA_line[2] + GGA_line[3]
					longitude = GGA_line[4] + GGA_line[5]

            		# send message 
					message = "long=" + str(longitude) + ",lat=" + str(latitude) + ",B=" + bat_level + ",T=" + temperature
            		# send_string
					send_string(message)
													
		else:
            	# check inbox
			command = check_mail()
			if command == "no_message": # execute commands
				time.sleep(5)
			else:
				os.system("python command_interpreter.py " + command)
				time.sleep(5)

#def send_string(message):
#	print(message)

#def check_mail():
	# check inbox
#	bla = 1
	
def sys_health():
	message = []
	   # get battery level [units]
	bat_level = 30
   	# get system temperature [deg. C]
	temperature = 20

	# check battery level 
	if bat_level <= 10: # no idea what value or units this should be
		message.append("Battery level too low. Pausing ops for 2 hrs")
	
	# check system temperature 
	if temperature < -30: # degrees Celcius
		message.append("System temperature too hot. Pausing ops for 2 hrs")
	elif temperature > 55: # degrees Celsius 
		message.append("System temperature too cold. Pausing ops for 2 hrs")
		
	# send messages back if needed 
	if len(message[0]) > 1:
		for item in message:
			send_string(item)
			sys.exit() # if there are any issues (might change this for cold temp)
	
	return bat_level, temperature

###########################################
# Main function 
def main():
	filename = "dino.csv"
	dataAmount = 20000
	#ser = os.environ.get("SERIAL")
	#if ser == "None":
	ser = cereal_func() #os.system(cereal()) #cereal.py 
	ser = "None"
	send_string("Serial connections have been made")

	set_vars = read_file('setvars.txt')
	freq = set_vars[0]
	el_mask = [9,17] #[set_vars[1], set_vars[2]]
	az_mask = [270, 360] #[set_vars[3], set_vars[4]]
	mode = "Normal" #set_vars[5]
	temporal_res = set_vars[6]

    # Check mailbox 
	#command = check_mail() # 0 if no mail
    # if command != 0:
	#os.system("python command_interpreter.py " + command)
    # or make this a function: command_interpreter(command)

	# check system health 
	#bat_level, temperature = sys_health()
	
	bat_level = 20
	temperature = 100
	
	# if in calibration mode, run every 5 mins until n = N (so it stops in >1.5 hours)
	if mode == "calibration":
		calibration_cycle(ser, bat_level, temperature)

	else: #normal ops (need to implement time resolution)
    #	time res idea: read in all available files? divide number of files by 
    # 	number of desired blocks  
		read_nmea(ser, dataAmount)

		nmea2dino("nmea.txt")
		heights = reflector_height(filename, az_mask[0], az_mask[1], el_mask[0], el_mask[1])
    
        # check system health 
		#bat_level, temperature = sys_health()
    
        # send string to ground station 
		#message = "B=" + bat_level + ",T=" + temperature + "H=" + heights[0]
		message = "H=" + heights[0]
		send_string(message)

if __name__ == "__main__":
    main()
