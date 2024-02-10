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
import sys, os # maybe not os
#import write, read and close file?

###########################################
# Functions 

def calibration_cycle():
# for n in range(0,N)
# 	if n = 0 send back longitude and latitude 
#		get longitude and latitude from NMEA file 
# 	else: send back battery health, temp and check inbox
#		get battery health 
# 		get temperature 
# 		check inbox
#		if message, execute commands
#			call command interpreter 
#       else:
# 			continue
# 	 sleep(5) #maybe less cause it would take a few seconds to run code

###########################################
# Main function 

# check system health 
	bat_level, temp = sys_health()

# Check mailbox 
	command = check_mail() # 0 if no mail
# if command != 0:
	command_interpreter(command)
# else: 
# 	continue

# if battery level is too low 
	return # need to find out how long it takes battery to charge 

# if in calibration mode, run every 5 mins until n = N (so it stops in >1.5 hours)
	calibration_cycle()

# else: normal ops (need to implement time resolution)
#	time res idea: read in all available files? divide number of files by 
# 	number of desired blocks  
	read_nmea()
    
# check system health 
	bat_level, temp = sys_health()
    
# send string to ground station 
	send_string()
