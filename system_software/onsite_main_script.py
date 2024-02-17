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
import sys, os # maybe not os if we turn cmd interpreter into function
from common_functions import read_file, write_file
# request that generateMsg and changeFreq become functions in common_functions 
# or we could call it receiver_functions
# so we can use them in the command interpreter


###########################################
# Functions 

def calibration_cycle():
	for n in range(0,N)
		if n = 0: # send back longitude, latitude, battery health, and sys temp
			# get longitude and latitude from NMEA file 

			# bat and temp could be passed in

			# send_string
			
		else: # check inbox

			# check inbox
			if message != no_message: # execute commands
				# command interpreter
			else:
#       else:
# 			continue
# 	 sleep(5) #maybe less cause it would take a few seconds to run code

def check_mail():
	# check inbox
	
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
		message.append("System temp. is too hot. Pausing ops for 2 hrs")
	elif temperature > 55: # degrees Celsius 
		message.append("System temp. is too cold. Pausing ops for 2 hrs")
		
	# send messages back if needed 
	if len(message[0]) > 1:
		for item in message 
			send_string(item)
  sys.exit() # if there are any issues (might change this for cold temp)
	
	return bat_level, temperature

###########################################
# Main function 
def main():
	
	set_vars = read_file('setvars.txt')
	freq = set_vars[0]
	el_mask = [set_vars[1], set_vars[2]]
	az_mask = [set_vars[3], set_vars[4]]
	mode = set_vars[5]
	timeres = set_vars[6]

# Check mailbox 
	command = check_mail() # 0 if no mail
# if command != 0:
	os.system("python command_interpreter.py " + command)
	# or make this a function: command_interpreter(command)
# else: 
# 	continue

# check system health 
	bat_level, temperature = sys_health()

# if in calibration mode, run every 5 mins until n = N (so it stops in >1.5 hours)
	if mode == "calibration":
		calibration_cycle()

	else: #normal ops (need to implement time resolution)
#	time res idea: read in all available files? divide number of files by 
# 	number of desired blocks  
		read_nmea()
		nmea2dino()
		reflector_height()
    
# check system health 
	bat_level, temperature = sys_health()
    
# send string to ground station 
	send_string()

if __name__ == "__main__":
    main()
